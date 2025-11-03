"""签名模板管理服务"""
from __future__ import annotations

from typing import List, Optional
from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.models import SignatureTemplate, SignatureTemplateSchema, SignatureTemplateUpdate, SessionLocal
from app.verifiers import WebhookVerifier
import time
import hmac
import hashlib


DEFAULT_TEMPLATES = [
    {
        "source": "github",
        "display_name": "GitHub",
        "description": "使用 X-Hub-Signature-256 (HMAC SHA256) 校验 Webhook 请求",
        "signature_header": "X-Hub-Signature-256",
    },
    {
        "source": "stripe",
        "display_name": "Stripe",
        "description": "使用 Stripe-Signature (t=timestamp,v1=hash) 校验请求",
        "signature_header": "Stripe-Signature",
    },
    {
        "source": "custom",
        "display_name": "Custom",
        "description": "自定义 HMAC-SHA256 签名，需提供签名头部与密钥",
        "signature_header": "X-Signature",
    },
]


@contextmanager
def session_scope(session: Optional[Session] = None):
    provided = session is not None
    db = session or SessionLocal()
    try:
        yield db
        if not provided:
            db.commit()
    except Exception:
        if not provided:
            db.rollback()
        raise
    finally:
        if not provided:
            db.close()


class SignatureService:
    """签名模板业务逻辑"""

    @staticmethod
    def ensure_defaults(db: Session) -> None:
        for template in DEFAULT_TEMPLATES:
            exists = db.query(SignatureTemplate).filter(SignatureTemplate.source == template["source"]).first()
            if not exists:
                db.add(SignatureTemplate(**template))
        db.flush()

    @classmethod
    def list_templates(cls, session: Optional[Session] = None) -> List[SignatureTemplateSchema]:
        with session_scope(session) as db:
            cls.ensure_defaults(db)
            records = db.query(SignatureTemplate).order_by(SignatureTemplate.id).all()
            result: List[SignatureTemplateSchema] = []
            for record in records:
                result.append(
                    SignatureTemplateSchema(
                        id=record.id,
                        source=record.source,
                        display_name=record.display_name,
                        description=record.description,
                        enabled=record.enabled,
                        signature_header=record.signature_header,
                        has_secret=bool(record.secret),
                        updated_at=record.updated_at,
                    )
                )
            return result

    @classmethod
    def get_template(cls, source: str, session: Optional[Session] = None) -> Optional[SignatureTemplate]:
        with session_scope(session) as db:
            cls.ensure_defaults(db)
            template = db.query(SignatureTemplate).filter(SignatureTemplate.source == source).first()
            return template

    @classmethod
    def update_template(
        cls,
        source: str,
        payload: SignatureTemplateUpdate,
        session: Optional[Session] = None,
    ) -> SignatureTemplateSchema:
        with session_scope(session) as db:
            cls.ensure_defaults(db)
            template = db.query(SignatureTemplate).filter(SignatureTemplate.source == source).first()
            if not template:
                raise ValueError(f"Signature template for source '{source}' not found")

            template.enabled = payload.enabled
            if payload.secret is not None:
                template.secret = payload.secret.strip() or None
            if payload.signature_header is not None:
                template.signature_header = payload.signature_header.strip()

            db.add(template)
            db.flush()
            if session is not None:
                db.commit()
                db.refresh(template)

            return SignatureTemplateSchema(
                id=template.id,
                source=template.source,
                display_name=template.display_name,
                description=template.description,
                enabled=template.enabled,
                signature_header=template.signature_header,
                has_secret=bool(template.secret),
                updated_at=template.updated_at,
            )

    @classmethod
    def get_active_secret(
        cls,
        source: str,
        session: Optional[Session] = None,
    ) -> Optional[SignatureTemplate]:
        with session_scope(session) as db:
            cls.ensure_defaults(db)
            template = db.query(SignatureTemplate).filter(SignatureTemplate.source == source).first()
            if template and template.enabled and template.secret:
                return template
            return None

    @classmethod
    def generate_header_value(
        cls,
        source: str,
        payload: bytes,
        timestamp: Optional[int] = None,
        session: Optional[Session] = None,
    ) -> tuple[str, str]:
        """基于启用的签名模板生成测试请求头键值。

        Returns: (header_name, header_value)
        """
        with session_scope(session) as db:
            cls.ensure_defaults(db)
            tpl = db.query(SignatureTemplate).filter(SignatureTemplate.source == source).first()
            if not tpl:
                raise ValueError(f"Signature template for source '{source}' not found")

            header = (tpl.signature_header or "").strip() or {
                "github": "X-Hub-Signature-256",
                "stripe": "Stripe-Signature",
                "custom": "X-Signature",
            }.get(source, "X-Signature")

            if not tpl.enabled or not tpl.secret:
                raise ValueError("Signature validation is not enabled or secret missing")

            secret = tpl.secret
            if source == "github":
                sig = WebhookVerifier.generate_signature(payload, secret)
                return header, f"sha256={sig}"
            if source == "stripe":
                ts = timestamp or int(time.time())
                signed = f"{ts}.".encode() + payload
                mac = hmac.new(secret.encode(), msg=signed, digestmod=hashlib.sha256)
                return header, f"t={ts},v1={mac.hexdigest()}"

            # custom
            sig = WebhookVerifier.generate_signature(payload, secret)
            return header, sig

