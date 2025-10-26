"""
Webhook 处理器测试
"""
import pytest
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models import Base, get_db, Event
from app.verifiers import WebhookVerifier


# 测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_event_hub.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """覆盖数据库依赖"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_github_webhook():
    """测试 GitHub Webhook 接收"""
    payload = {
        "repository": {"full_name": "user/repo"},
        "pusher": {"name": "testuser"}
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "push",
        "X-Hub-Signature-256": "sha256=dummy"  # 实际测试中应该使用正确的签名
    }
    
    response = client.post("/webhook/github", json=payload, headers=headers)
    
    # 如果没有配置密钥，应该接受请求
    assert response.status_code in (200, 401)


def test_stripe_webhook():
    """测试 Stripe Webhook 接收"""
    payload = {
        "id": "evt_test",
        "type": "payment_intent.succeeded",
        "data": {"object": {}}
    }
    
    headers = {
        "Content-Type": "application/json",
        "Stripe-Signature": "t=1234567890,v1=dummy"
    }
    
    response = client.post("/webhook/stripe", json=payload, headers=headers)
    
    assert response.status_code in (200, 401)


def test_custom_webhook():
    """测试自定义 Webhook 接收"""
    payload = {
        "event": "user.created",
        "data": {"user_id": 123}
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Signature": "dummy"
    }
    
    response = client.post("/webhook/custom", json=payload, headers=headers)
    
    assert response.status_code in (200, 401)


def test_get_events():
    """测试获取事件列表"""
    response = client.get("/api/events?limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_stats():
    """测试获取统计信息"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_events" in data
    assert "by_source" in data
    assert "signature_success_rate" in data


def test_health_check():
    """测试健康检查"""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

