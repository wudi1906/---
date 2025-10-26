"""
Insight Viz Studio 配置
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用设置"""
    
    APP_NAME: str = "Insight Viz Studio"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8606
    
    # 文件存储
    UPLOAD_DIR: Path = Path("./uploads")
    EXPORT_DIR: Path = Path("./exports")
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # 支持的文件类型
    ALLOWED_EXTENSIONS: set = {".csv", ".json", ".xlsx", ".xls"}
    
    # 图表配置
    DEFAULT_CHART_WIDTH: int = 1200
    DEFAULT_CHART_HEIGHT: int = 800
    MAX_ROWS_DISPLAY: int = 50000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

# 确保目录存在
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.EXPORT_DIR.mkdir(parents=True, exist_ok=True)

