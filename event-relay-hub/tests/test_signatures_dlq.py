import os
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.models import SignatureTemplate, DeadLetterEvent, Event
from app.settings import settings
import app.forwarder as forwarder_module
from tests.test_webhooks import client, TestingSessionLocal, Base, engine  # reuse overrides

forwarder_module.SessionLocal = TestingSessionLocal


@pytest.fixture(autouse=True)
def cleanup_db():
    forwarder_module.SessionLocal = TestingSessionLocal
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        db.query(DeadLetterEvent).delete()
        db.query(SignatureTemplate).delete()
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
        db.query(SignatureTemplate).delete()
        db.query(Event).delete()
        db.commit()
    finally:
        db.close()
    settings.REPLAY_COOLDOWN_SECONDS = original_cooldown
    settings.REPLAY_SUCCESS_TTL_SECONDS = original_ttl


def test_signature_template_crud():
    resp = client.get("/api/signatures")
    assert resp.status_code == 200
    templates = resp.json()
    sources = {tpl["source"] for tpl in templates}
    assert {"github", "stripe", "custom"}.issubset(sources)

    update_payload = {
        "enabled": True,
        "secret": "secret-token",
        "signature_header": "X-Hub-Signature-256"
    }
    resp = client.put("/api/signatures/github", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["enabled"] is True
    assert data["has_secret"] is True

    # 再次获取确认持久化
    resp = client.get("/api/signatures")
    github_tpl = next(tpl for tpl in resp.json() if tpl["source"] == "github")
    assert github_tpl["enabled"] is True
    assert github_tpl["has_secret"] is True


def _create_event(source: str = "github", event_type: str = "push") -> int:
    db = TestingSessionLocal()
    try:
        event = Event(
            source=source,
            event_type=event_type,
            payload="{\"id\": \"evt_123\"}",
            headers="{}",
            signature_valid=True,
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event.id
    finally:
        db.close()


def _create_dead_letter(
    event_id: int,
    *,
    reason: str = "timeout",
    last_error: str = "timeout",
    retry_count: int = 1,
    target_url: str = "https://example.com/webhook",
) -> int:
    db = TestingSessionLocal()
    try:
        item = DeadLetterEvent(
            event_id=event_id,
            target_url=target_url,
            reason=reason,
            last_error=last_error,
            retry_count=retry_count,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item.id
    finally:
        db.close()


def test_dlq_lifecycle():
    event_id = _create_event()

    # 强制转发失败，写入 DLQ
    with patch("app.forwarder.httpx.AsyncClient.post", side_effect=httpx.TimeoutException("timeout")):
        resp = client.post(f"/api/events/{event_id}/replay?target_url=https://example.com/webhook")
    assert resp.status_code == 200
    assert resp.json()["success"] is False

    dlq_resp = client.get("/api/dlq")
    assert dlq_resp.status_code == 200
    dlq_data = dlq_resp.json()
    assert dlq_data["total"] == 1
    assert len(dlq_data["items"]) == 1
    dlq_id = dlq_data["items"][0]["id"]

    success_response = SimpleNamespace(status_code=200, text="OK")
    with patch("app.forwarder.httpx.AsyncClient.post", new=AsyncMock(return_value=success_response)):
        replay_resp = client.post(f"/api/dlq/{dlq_id}/replay")
    assert replay_resp.status_code == 200
    assert replay_resp.json()["success"] is True

    dlq_after = client.get("/api/dlq")
    assert dlq_after.status_code == 200
    dlq_after_data = dlq_after.json()
    assert dlq_after_data["total"] == 0
    assert dlq_after_data["items"] == []


def test_dlq_batch_handles_duplicates(monkeypatch):
    event_id = _create_event()
    dlq_id = _create_dead_letter(event_id)

    monkeypatch.setattr("app.main.EventForwarder.replay_event", AsyncMock(return_value=True))
    resp = client.post("/api/dlq/replay/batch", json={"ids": [dlq_id, dlq_id]})
    assert resp.status_code == 200
    data = resp.json()
    assert dlq_id in data["success_ids"]
    assert str(dlq_id) in data["failed"]
    assert data["failed"][str(dlq_id)] == "Duplicate id ignored"


def test_dlq_filters_support_source_event_type_search_and_retry():
    event_github = _create_event("github", "push")
    event_stripe = _create_event("stripe", "invoice.paid")
    dlq_github = _create_dead_letter(
        event_github,
        reason="signature mismatch",
        last_error="signature mismatch",
        retry_count=1,
    )
    dlq_stripe = _create_dead_letter(
        event_stripe,
        reason="network timeout",
        last_error="network",
        retry_count=3,
    )

    resp = client.get("/api/dlq", params={"source": "github"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["event_id"] == event_github

    resp = client.get("/api/dlq", params={"event_type": "invoice.paid"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["event_id"] == event_stripe

    resp = client.get("/api/dlq", params={"min_retry": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == dlq_stripe

    resp = client.get("/api/dlq", params={"search": "signature"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == dlq_github


def test_signature_test_endpoint_requires_enabled_template():
    # 默认模板未启用时应提示错误
    resp = client.post("/api/signatures/github/test", json={"payload": {"foo": "bar"}})
    assert resp.status_code == 400

    update_payload = {
        "enabled": True,
        "secret": "secret-token",
        "signature_header": "X-Hub-Signature-256",
    }
    client.put("/api/signatures/github", json=update_payload)

    resp_ok = client.post(
        "/api/signatures/github/test",
        json={"payload": {"foo": "bar"}, "timestamp": 1700000000},
    )
    assert resp_ok.status_code == 200
    data = resp_ok.json()
    assert data["header"].startswith("X-Hub")
    assert data["value"].startswith("sha256=")

