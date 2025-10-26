"""
签名校验测试
"""
import pytest
from app.verifiers import WebhookVerifier


def test_github_signature():
    """测试 GitHub 签名验证"""
    payload = b'{"test": "data"}'
    secret = "my_secret_key"
    
    # 生成正确的签名
    signature = WebhookVerifier.generate_signature(payload, secret)
    full_signature = f"sha256={signature}"
    
    # 验证应该成功
    assert WebhookVerifier.verify_github(payload, full_signature, secret) is True
    
    # 错误的签名应该失败
    assert WebhookVerifier.verify_github(payload, "sha256=wrong", secret) is False
    
    # 错误的格式应该失败
    assert WebhookVerifier.verify_github(payload, "wrong_format", secret) is False


def test_stripe_signature():
    """测试 Stripe 签名验证"""
    payload = b'{"id": "evt_test"}'
    secret = "whsec_test_secret"
    timestamp = "1634567890"
    
    # 生成签名
    signed_payload = f"{timestamp}.".encode() + payload
    signature = WebhookVerifier.generate_signature(signed_payload, secret)
    full_signature = f"t={timestamp},v1={signature}"
    
    # 验证应该成功
    assert WebhookVerifier.verify_stripe(payload, full_signature, secret) is True
    
    # 错误的签名应该失败
    assert WebhookVerifier.verify_stripe(payload, f"t={timestamp},v1=wrong", secret) is False


def test_custom_signature():
    """测试自定义签名验证"""
    payload = b'{"event": "test"}'
    secret = "custom_secret"
    
    # 生成签名
    signature = WebhookVerifier.generate_signature(payload, secret)
    
    # 验证应该成功
    assert WebhookVerifier.verify_custom(payload, signature, secret) is True
    
    # 错误的签名应该失败
    assert WebhookVerifier.verify_custom(payload, "wrong_signature", secret) is False


def test_empty_secret():
    """测试空密钥"""
    payload = b'{"test": "data"}'
    
    assert WebhookVerifier.verify_github(payload, "sha256=any", "") is False
    assert WebhookVerifier.verify_stripe(payload, "t=123,v1=any", "") is False
    assert WebhookVerifier.verify_custom(payload, "any", "") is False

