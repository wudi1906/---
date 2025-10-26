"""
应用配置与环境变量管理
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用全局设置"""
    
    # 应用基础配置
    APP_NAME: str = "Global Price Sentinel"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8101
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./price_sentinel.db"
    
    # 监控配置
    CRON_SCHEDULE: str = "0 */12 * * *"  # 每12小时运行
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 5  # 秒
    
    # Playwright 配置
    HEADLESS: bool = True
    BROWSER_TIMEOUT: int = 30000  # 毫秒
    VIEWPORT_WIDTH: int = 1920
    VIEWPORT_HEIGHT: int = 1080
    
    # 代理配置（可选）
    PROXY_SERVER: Optional[str] = None
    PROXY_USERNAME: Optional[str] = None
    PROXY_PASSWORD: Optional[str] = None
    
    # Webhook 配置
    SLACK_WEBHOOK_URL: Optional[str] = None
    DISCORD_WEBHOOK_URL: Optional[str] = None
    DINGTALK_WEBHOOK_URL: Optional[str] = None
    
    # 报告配置
    REPORTS_DIR: Path = Path("./reports")
    SCREENSHOTS_DIR: Path = Path("./screenshots")
    HISTORY_DAYS: int = 7
    
    # 邮件配置（可选）
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 全局设置实例
settings = Settings()

# 确保目录存在
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
settings.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

