from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest

from app.models import Event, DeadLetterEvent, ForwardLog
from app.settings import settings
from tests.test_webhooks import client, TestingSessionLocal, Base, engine


@pytest.fixture(autouse=True)
def cleanup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        db.query(DeadLetterEvent).delete()
        db.query(ForwardLog).delete()
        db.query(Event).delete()
        db.commit()
    finally:
        db.close()
    original_cooldown = settings.REPLAY_COOLDOWN_SECONDS
    original_ttl = settings.REPLAY_SUCCESS_TTL_SECONDS
    settings.REPLAY_COOLDOWN_SECONDS = 0
    settings.REPLAY_SUCCESS_TTL_SECONDS = 0
    yield
    db = TestingSessionLocal()
    try:
        db.query(DeadLetterEvent).delete()
        db.query(ForwardLog).delete()
        db.query(Event).delete()
        db.commit()
    finally:
        db.close()
    settings.REPLAY_COOLDOWN_SECONDS = original_cooldown
    settings.REPLAY_SUCCESS_TTL_SECONDS = original_ttl


def _create_event(source: str, event_type: str, signature_valid: bool = True, created_at: datetime | None = None) -> int:
    db = TestingSessionLocal()
    try:
        event = Event(
            source=source,
            event_type=event_type,
            payload='{"id": "evt-test"}',
            headers='{}',
            signature_valid=signature_valid,
            created_at=created_at or datetime.utcnow(),
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event.id
    finally:
        db.close()


def _insert_forward_log(event_id: int, *, target_url: str, success: bool, created_at: datetime | None = None, status_code: int | None = None):
    db = TestingSessionLocal()
    try:
        log = ForwardLog(
            event_id=event_id,
            target_url=target_url,
            success=success,
            status_code=status_code if status_code is not None else (200 if success else 500),
            created_at=created_at or datetime.utcnow(),
        )
        db.add(log)
        db.commit()
    finally:
        db.close()


def _create_dead_letter(event_id: int, retry_count: int = 0) -> int:
    db = TestingSessionLocal()
    try:
        item = DeadLetterEvent(
            event_id=event_id,
            target_url="https://example.com/webhook",
            reason="timeout",
            last_error="Request timeout",
            retry_count=retry_count,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item.id
    finally:
        db.close()


def test_search_events_supports_filters_and_pagination():
    # 准备数据：不同来源/类型/签名状态
    now = datetime.utcnow()
    _create_event("stripe", "invoice.paid", True, now - timedelta(hours=1))
    _create_event("github", "push", False, now - timedelta(days=1))
    _create_event("stripe", "subscription.created", True, now)

    response = client.get(
        "/api/events/search",
        params={
            "source": "stripe",
            "signature_valid": "true",
            "page": "1",
            "page_size": "1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["source"] == "stripe"


def test_batch_replay_events_returns_success_and_failed(monkeypatch):
    event_ok = _create_event("stripe", "invoice.paid")
    event_fail = _create_event("github", "push")

    async_mock = AsyncMock(side_effect=[True, False])
    monkeypatch.setattr("app.main.EventForwarder.replay_event", async_mock)

    response = client.post(
        "/api/events/replay/batch",
        json={
            "ids": [event_ok, event_fail, 9999],
            "target_url": "https://example.com/webhook",
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert event_ok in result["success_ids"]
    assert str(event_fail) in result["failed"]
    assert result["failed"][str(event_fail)] == "Replay failed"
    assert result["failed"]["9999"] == "Event not found"


def test_batch_replay_events_handles_duplicates(monkeypatch):
    event_id = _create_event("stripe", "invoice.paid")
    async_mock = AsyncMock(return_value=True)
    monkeypatch.setattr("app.main.EventForwarder.replay_event", async_mock)

    response = client.post(
        "/api/events/replay/batch",
        json={"ids": [event_id, event_id], "target_url": "https://example.com/webhook"},
    )

    assert response.status_code == 200
    data = response.json()
    assert event_id in data["success_ids"]
    assert str(event_id) in data["failed"]
    assert data["failed"][str(event_id)] == "Duplicate id ignored"


def test_replay_event_skips_recent_success(monkeypatch):
    event_id = _create_event("stripe", "invoice.paid")
    target = "https://example.com/webhook"
    _insert_forward_log(event_id, target_url=target, success=True)

    async_mock = AsyncMock(return_value=True)
    monkeypatch.setattr("app.forwarder.EventForwarder.forward_event", async_mock)

    original_cooldown = settings.REPLAY_COOLDOWN_SECONDS
    original_ttl = settings.REPLAY_SUCCESS_TTL_SECONDS
    settings.REPLAY_COOLDOWN_SECONDS = 0
    settings.REPLAY_SUCCESS_TTL_SECONDS = 120

    try:
        response = client.post(f"/api/events/{event_id}/replay", params={"target_url": target})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "跳过" in data["message"]
        assert data.get("notes")
        assert async_mock.await_count == 0
    finally:
        settings.REPLAY_COOLDOWN_SECONDS = original_cooldown
        settings.REPLAY_SUCCESS_TTL_SECONDS = original_ttl


def test_replay_event_enforces_cooldown(monkeypatch):
    event_id = _create_event("stripe", "invoice.paid")
    target = "https://example.com/webhook"
    _insert_forward_log(event_id, target_url=target, success=False)

    async_mock = AsyncMock(return_value=True)
    monkeypatch.setattr("app.forwarder.EventForwarder.forward_event", async_mock)

    original_cooldown = settings.REPLAY_COOLDOWN_SECONDS
    original_ttl = settings.REPLAY_SUCCESS_TTL_SECONDS
    settings.REPLAY_COOLDOWN_SECONDS = 60
    settings.REPLAY_SUCCESS_TTL_SECONDS = 0

    try:
        response = client.post(f"/api/events/{event_id}/replay", params={"target_url": target})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data.get("retry_after") is not None
        assert "冷却" in data["message"]
        assert async_mock.await_count == 0
    finally:
        settings.REPLAY_COOLDOWN_SECONDS = original_cooldown
        settings.REPLAY_SUCCESS_TTL_SECONDS = original_ttl


def test_batch_replay_skips_recent_success(monkeypatch):
    event_id = _create_event("stripe", "invoice.paid")
    target = "https://example.com/webhook"
    _insert_forward_log(event_id, target_url=target, success=True)

    async_mock = AsyncMock(return_value=True)
    monkeypatch.setattr("app.forwarder.EventForwarder.forward_event", async_mock)

    original_cooldown = settings.REPLAY_COOLDOWN_SECONDS
    original_ttl = settings.REPLAY_SUCCESS_TTL_SECONDS
    settings.REPLAY_COOLDOWN_SECONDS = 0
    settings.REPLAY_SUCCESS_TTL_SECONDS = 120

    try:
        response = client.post(
            "/api/events/replay/batch",
            json={"ids": [event_id], "target_url": target},
        )
        assert response.status_code == 200
        data = response.json()
        assert event_id in data["success_ids"]
        assert str(event_id) not in data["failed"]
        assert str(event_id) in data["notes"]
        assert async_mock.await_count == 0
    finally:
        settings.REPLAY_COOLDOWN_SECONDS = original_cooldown
        settings.REPLAY_SUCCESS_TTL_SECONDS = original_ttl


def test_dlq_batch_replay_and_clear(monkeypatch):
    event_id = _create_event("stripe", "invoice.paid")
    dlq_id_1 = _create_dead_letter(event_id)
    dlq_id_2 = _create_dead_letter(event_id)

    async_mock = AsyncMock(side_effect=[True, False])
    monkeypatch.setattr("app.main.EventForwarder.replay_event", async_mock)

    # 批量重试
    resp = client.post(
        "/api/dlq/replay/batch",
        json={"ids": [dlq_id_1, dlq_id_2]},
    )
    assert resp.status_code == 200
    result = resp.json()
    assert dlq_id_1 in result["success_ids"]
    assert str(dlq_id_2) in result["failed"]

    # 清空剩余死信
    resp = client.post("/api/dlq/clear")
    assert resp.status_code == 200
    assert resp.json()["success"] is True


def test_stats_endpoint_returns_extended_fields():
    db = TestingSessionLocal()
    try:
        e1 = Event(
            source="stripe",
            event_type="invoice.paid",
            payload="{}",
            headers="{}",
            signature_valid=True,
        )
        db.add(e1)
        db.flush()
        db.add(
            ForwardLog(
                event_id=e1.id,
                target_url="https://example.com",
                status_code=200,
                success=True,
            )
        )
        db.add(
            ForwardLog(
                event_id=e1.id,
                target_url="https://example.com",
                status_code=500,
                success=False,
            )
        )
        db.add(
            DeadLetterEvent(
                event_id=e1.id,
                target_url="https://example.com",
                reason="timeout",
                last_error="timeout",
                retry_count=1,
            )
        )
        db.commit()
    finally:
        db.close()

    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "forward_success" in data and data["forward_success"] >= 1
    assert "forward_failed" in data and data["forward_failed"] >= 1
    assert "dead_letters" in data and data["dead_letters"] >= 1
