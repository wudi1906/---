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
from app.signature_service import SignatureService


class WebhookHandler:
    """Webhook 处理器"""
    
    def __init__(self, db: Session):
        self.db = db
        self.forwarder = EventForwarder()
    
    def _resolve_signature(self, source: str, default_header: str, settings_secret: Optional[str]) -> tuple[str, Optional[str], bool]:
        template = SignatureService.get_template(source, session=self.db)
        header = default_header
        secret = settings_secret
        required = False

        if template:
            header = template.signature_header or default_header
            if template.enabled:
                required = True
                secret = template.secret
        elif settings_secret:
            required = True

        return header, secret, required

    async def handle_github(self, request: Request) -> Dict[str, Any]:
        """处理 GitHub Webhook"""
        # 读取原始 payload
        payload = await request.body()

        header_name, secret, required = self._resolve_signature("github", "X-Hub-Signature-256", settings.GITHUB_WEBHOOK_SECRET)
        signature = request.headers.get(header_name, '')
        event_type = request.headers.get('X-GitHub-Event', 'unknown')

        if required and not secret:
            raise HTTPException(status_code=401, detail="Signature secret not configured")

        signature_valid = True
        if required and secret:
            signature_valid = WebhookVerifier.verify_github(payload, signature, secret)
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
        header_name, secret, required = self._resolve_signature("stripe", "Stripe-Signature", settings.STRIPE_WEBHOOK_SECRET)
        signature = request.headers.get(header_name, '')

        if required and not secret:
            raise HTTPException(status_code=401, detail="Signature secret not configured")

        signature_valid = True
        if required and secret:
            signature_valid = WebhookVerifier.verify_stripe(payload, signature, secret)
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
        header_name, secret, required = self._resolve_signature("custom", "X-Signature", settings.CUSTOM_WEBHOOK_SECRET)
        signature = request.headers.get(header_name, '')

        if required and not secret:
            raise HTTPException(status_code=401, detail="Signature secret not configured")

        signature_valid = True
        if required and secret:
            signature_valid = WebhookVerifier.verify_custom(payload, signature, secret)
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

