"""
Webhook 处理器
"""
import json
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from app.models import Event, EventCreate
from app.verifiers import WebhookVerifier
from app.settings import settings
from app.forwarder import EventForwarder


class WebhookHandler:
    """Webhook 处理器"""
    
    def __init__(self, db: Session):
        self.db = db
        self.forwarder = EventForwarder()
    
    async def handle_github(self, request: Request) -> Dict[str, Any]:
        """处理 GitHub Webhook"""
        # 读取原始 payload
        payload = await request.body()
        
        # 获取签名
        signature = request.headers.get('X-Hub-Signature-256', '')
        event_type = request.headers.get('X-GitHub-Event', 'unknown')
        
        # 验证签名
        signature_valid = False
        if settings.GITHUB_WEBHOOK_SECRET:
            signature_valid = WebhookVerifier.verify_github(
                payload,
                signature,
                settings.GITHUB_WEBHOOK_SECRET
            )
        else:
            # 如果未配置密钥，跳过验证（仅用于开发）
            signature_valid = True
        
        if not signature_valid:
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # 解析 payload
        try:
            payload_json = json.loads(payload)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # 存储事件
        event = Event(
            source="github",
            event_type=event_type,
            payload=payload.decode('utf-8'),
            headers=json.dumps(dict(request.headers)),
            signature_valid=signature_valid
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        
        # 异步转发
        if settings.FORWARD_ENABLED and settings.FORWARD_URL:
            await self.forwarder.forward_event(event, settings.FORWARD_URL)
        
        return {
            "success": True,
            "event_id": event.id,
            "source": "github",
            "event_type": event_type
        }
    
    async def handle_stripe(self, request: Request) -> Dict[str, Any]:
        """处理 Stripe Webhook"""
        payload = await request.body()
        signature = request.headers.get('Stripe-Signature', '')
        
        # 验证签名
        signature_valid = False
        if settings.STRIPE_WEBHOOK_SECRET:
            signature_valid = WebhookVerifier.verify_stripe(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET
            )
        else:
            signature_valid = True
        
        if not signature_valid:
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # 解析 payload
        try:
            payload_json = json.loads(payload)
            event_type = payload_json.get('type', 'unknown')
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # 存储事件
        event = Event(
            source="stripe",
            event_type=event_type,
            payload=payload.decode('utf-8'),
            headers=json.dumps(dict(request.headers)),
            signature_valid=signature_valid
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        
        # 异步转发
        if settings.FORWARD_ENABLED and settings.FORWARD_URL:
            await self.forwarder.forward_event(event, settings.FORWARD_URL)
        
        return {
            "success": True,
            "event_id": event.id,
            "source": "stripe",
            "event_type": event_type
        }
    
    async def handle_custom(self, request: Request) -> Dict[str, Any]:
        """处理自定义 Webhook"""
        payload = await request.body()
        signature = request.headers.get('X-Signature', '')
        
        # 验证签名
        signature_valid = False
        if settings.CUSTOM_WEBHOOK_SECRET:
            signature_valid = WebhookVerifier.verify_custom(
                payload,
                signature,
                settings.CUSTOM_WEBHOOK_SECRET
            )
        else:
            signature_valid = True
        
        if not signature_valid:
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # 解析 payload
        try:
            payload_json = json.loads(payload)
            event_type = payload_json.get('event', 'unknown')
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # 存储事件
        event = Event(
            source="custom",
            event_type=event_type,
            payload=payload.decode('utf-8'),
            headers=json.dumps(dict(request.headers)),
            signature_valid=signature_valid
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        
        # 异步转发
        if settings.FORWARD_ENABLED and settings.FORWARD_URL:
            await self.forwarder.forward_event(event, settings.FORWARD_URL)
        
        return {
            "success": True,
            "event_id": event.id,
            "source": "custom",
            "event_type": event_type
        }

