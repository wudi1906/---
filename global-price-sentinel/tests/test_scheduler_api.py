from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import SessionLocal, MonitorJobRun, MonitorConfigModel


client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_tables():
    db = SessionLocal()
    try:
        db.query(MonitorJobRun).delete()
        db.query(MonitorConfigModel).delete()
        db.commit()
    finally:
        db.close()
    yield
    db = SessionLocal()
    try:
        db.query(MonitorJobRun).delete()
        db.query(MonitorConfigModel).delete()
        db.commit()
    finally:
        db.close()


def _seed_job_run(status: str = "success"):
    db = SessionLocal()
    try:
        # create config to ensure interval mode predictable
        config = MonitorConfigModel(
            id=1,
            scheduler_mode="interval",
            cron_expression="0 */12 * * *",
            interval_minutes=60,
            proxy_enabled=False,
            alert_channels="[]",
        )
        db.merge(config)

        started_at = datetime.utcnow() - timedelta(minutes=5)
        finished_at = started_at + timedelta(minutes=1)
        run = MonitorJobRun(
            job_id="monitor_task",
            job_name="Price Monitor Task",
            status=status,
            message="测试运行",
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=int((finished_at - started_at).total_seconds() * 1000),
        )
        db.add(run)
        db.commit()
    finally:
        db.close()


def test_scheduler_status_returns_recent_runs():
    _seed_job_run()

    response = client.get("/api/scheduler/status?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "monitor_task"
    assert data["job_name"] == "Price Monitor Task"
    assert data["last_run"]["status"] == "success"
    assert isinstance(data["recent_runs"], list)
    assert len(data["recent_runs"]) == 1
    # interval mode => next run 应为未来时间，允许容差
    assert data["next_run_time"] is not None
    assert data["time_until_next_run_seconds"] is None or data["time_until_next_run_seconds"] >= 0


def test_alerts_test_endpoint_success(monkeypatch):
    def fake_test_channel(channel, payload):
        return True, "发送成功", {"channel": channel}

    monkeypatch.setattr("app.webhooks.AlertDispatcher.test_channel", fake_test_channel)

    resp = client.post("/api/alerts/test", json={"channel": "email", "payload": {"recipients": ["ops@example.com"]}})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["message"] == "发送成功"
    assert data["detail"]["channel"] == "email"


def test_alerts_test_endpoint_failure(monkeypatch):
    def fake_test_channel(channel, payload):
        return False, "未配置渠道", {}

    monkeypatch.setattr("app.webhooks.AlertDispatcher.test_channel", fake_test_channel)

    resp = client.post("/api/alerts/test", json={"channel": "slack", "payload": {}})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is False
    assert "未配置渠道" in data["message"]
