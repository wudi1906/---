"""
Event Relay Hub 配置
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用设置"""
    
    APP_NAME: str = "Event Relay Hub"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8202
    
    # 数据库
    DATABASE_URL: str = "sqlite:///./event_hub.db"
    
    # Webhook 密钥
    GITHUB_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    CUSTOM_WEBHOOK_SECRET: Optional[str] = None
    
    # 速率限制
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_ENABLED: bool = True
    
    # Redis（用于速率限制，可选）
    REDIS_URL: Optional[str] = None
    
    # 转发配置
    FORWARD_ENABLED: bool = False
    FORWARD_URL: Optional[str] = None
    FORWARD_TIMEOUT: int = 10
    REPLAY_COOLDOWN_SECONDS: int = 30
    REPLAY_SUCCESS_TTL_SECONDS: int = 300
    
    # 事件保留
    RETENTION_DAYS: int = 30
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # pydantic v2 settings config（兼容大小写与多余键）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

