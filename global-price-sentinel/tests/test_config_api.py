from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.models import MonitorConfigModel, SessionLocal


client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_config():
    db = SessionLocal()
    try:
        db.query(MonitorConfigModel).delete()
        db.commit()
    finally:
        db.close()
    yield
    db = SessionLocal()
    try:
        db.query(MonitorConfigModel).delete()
        db.commit()
    finally:
        db.close()


def test_get_default_monitor_config():
    response = client.get("/api/config/monitor")
    assert response.status_code == 200
    data = response.json()
    assert data["scheduler_mode"] == "cron"
    assert data["cron_expression"].count(" ") == 4
    assert data["interval_minutes"] == 720
    assert data["alert_channels"] == []


def test_update_monitor_config_interval_mode():
    payload = {
        "scheduler_mode": "interval",
        "cron_expression": "0 */12 * * *",
        "interval_minutes": 120,
        "proxy_enabled": True,
        "proxy_server": "http://proxy.local:8080",
        "proxy_username": "tester",
        "proxy_password": "secret",
        "alert_channels": [
            {
                "type": "webhook",
                "enabled": True,
                "webhook_url": "https://example.com/alert"
            },
            {
                "type": "email",
                "enabled": True,
                "recipients": ["ops@example.com"]
            }
        ]
    }

    update_resp = client.put("/api/config/monitor", json=payload)
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["scheduler_mode"] == "interval"
    assert updated["interval_minutes"] == 120
    assert updated["proxy_enabled"] is True
    assert any(channel["type"] == "email" for channel in updated["alert_channels"])

    # 再次获取确认持久化
    get_resp = client.get("/api/config/monitor")
    assert get_resp.status_code == 200
    persisted = get_resp.json()
    assert persisted["scheduler_mode"] == "interval"
    assert persisted["interval_minutes"] == 120
    assert persisted["proxy_server"] == "http://proxy.local:8080"


def test_update_requires_email_recipients():
    payload = {
        "scheduler_mode": "cron",
        "cron_expression": "0 1 * * *",
        "interval_minutes": 720,
        "proxy_enabled": False,
        "alert_channels": [
            {
                "type": "email",
                "enabled": True,
                "recipients": []
            }
        ]
    }

    response = client.put("/api/config/monitor", json=payload)
    assert response.status_code == 422

