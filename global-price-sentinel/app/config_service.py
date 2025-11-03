"""监控配置服务"""
from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Optional

from sqlalchemy.orm import Session

from app.models import (
    SessionLocal,
    MonitorConfigModel,
    MonitorConfigSchema,
    MonitorConfigUpdate,
)


DEFAULT_ALERT_CHANNELS = []


@contextmanager
def _session_scope(session: Optional[Session] = None):
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


class ConfigService:
    """监控配置读写封装"""

    @staticmethod
    def _ensure_config(db: Session) -> MonitorConfigModel:
        config = db.get(MonitorConfigModel, 1)
        if not config:
            config = MonitorConfigModel(
                id=1,
                scheduler_mode="cron",
                cron_expression="0 */12 * * *",
                interval_minutes=720,
                proxy_enabled=False,
                alert_channels=json.dumps(DEFAULT_ALERT_CHANNELS, ensure_ascii=False),
            )
            db.add(config)
            db.commit()
            db.refresh(config)
        return config

    @staticmethod
    def _deserialize(model: MonitorConfigModel) -> MonitorConfigSchema:
        channels_raw = []
        if model.alert_channels:
            try:
                channels_raw = json.loads(model.alert_channels)
            except json.JSONDecodeError:
                channels_raw = []
        data = {
            "id": model.id,
            "scheduler_mode": model.scheduler_mode or "cron",
            "cron_expression": model.cron_expression or "0 */12 * * *",
            "interval_minutes": model.interval_minutes or 720,
            "proxy_enabled": bool(model.proxy_enabled),
            "proxy_server": model.proxy_server,
            "proxy_username": model.proxy_username,
            "proxy_password": model.proxy_password,
            "alert_channels": channels_raw or DEFAULT_ALERT_CHANNELS,
            "updated_at": model.updated_at,
        }
        return MonitorConfigSchema(**data)

    @classmethod
    def get_config(cls, session: Optional[Session] = None) -> MonitorConfigSchema:
        with _session_scope(session) as db:
            config = cls._ensure_config(db)
            return cls._deserialize(config)

    @classmethod
    def update_config(
        cls,
        payload: MonitorConfigUpdate,
        session: Optional[Session] = None,
    ) -> MonitorConfigSchema:
        with _session_scope(session) as db:
            config = cls._ensure_config(db)
            config.scheduler_mode = payload.scheduler_mode
            config.cron_expression = payload.cron_expression
            config.interval_minutes = payload.interval_minutes
            config.proxy_enabled = payload.proxy_enabled
            config.proxy_server = payload.proxy_server
            config.proxy_username = payload.proxy_username
            config.proxy_password = payload.proxy_password
            config.alert_channels = json.dumps(
                [channel.model_dump(mode="json") for channel in payload.alert_channels],
                ensure_ascii=False,
            )
            db.add(config)
            db.commit()
            db.refresh(config)
            return cls._deserialize(config)


