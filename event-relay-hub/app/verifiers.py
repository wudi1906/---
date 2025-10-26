"""
Webhook 签名校验
"""
import hmac
import hashlib
from typing import Optional


class WebhookVerifier:
    """Webhook 签名校验器"""
    
    @staticmethod
    def verify_github(payload: bytes, signature: str, secret: str) -> bool:
        """
        验证 GitHub Webhook 签名
        
        GitHub 使用 HMAC-SHA256，签名格式为: sha256=<hash>
        """
        if not signature or not secret:
            return False
        
        if not signature.startswith('sha256='):
            return False
        
        expected_signature = signature[7:]  # 移除 'sha256=' 前缀
        
        # 计算 HMAC
        mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
        computed_signature = mac.hexdigest()
        
        return hmac.compare_digest(computed_signature, expected_signature)
    
    @staticmethod
    def verify_stripe(payload: bytes, signature: str, secret: str) -> bool:
        """
        验证 Stripe Webhook 签名
        
        Stripe 使用 HMAC-SHA256，签名格式为: t=timestamp,v1=<hash>
        """
        if not signature or not secret:
            return False
        
        # 解析签名
        sig_items = {}
        for item in signature.split(','):
            key, value = item.split('=', 1)
            sig_items[key] = value
        
        if 'v1' not in sig_items or 't' not in sig_items:
            return False
        
        timestamp = sig_items['t']
        expected_signature = sig_items['v1']
        
        # 构造签名载荷
        signed_payload = f"{timestamp}.".encode() + payload
        
        # 计算 HMAC
        mac = hmac.new(secret.encode(), msg=signed_payload, digestmod=hashlib.sha256)
        computed_signature = mac.hexdigest()
        
        return hmac.compare_digest(computed_signature, expected_signature)
    
    @staticmethod
    def verify_custom(payload: bytes, signature: str, secret: str) -> bool:
        """
        验证自定义 Webhook 签名
        
        使用简单的 HMAC-SHA256
        """
        if not signature or not secret:
            return False
        
        mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
        computed_signature = mac.hexdigest()
        
        return hmac.compare_digest(computed_signature, signature)
    
    @staticmethod
    def generate_signature(payload: bytes, secret: str) -> str:
        """生成签名（用于测试）"""
        mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
        return mac.hexdigest()

