"""
Doc Knowledge Forge 配置
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用设置"""
    
    APP_NAME: str = "Doc Knowledge Forge"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8404
    
    # 数据库
    DATABASE_URL: str = "sqlite:///./docs_forge.db"
    
    # 文件存储
    UPLOAD_DIR: Path = Path("./uploads")
    OUTPUT_DIR: Path = Path("./outputs")
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    
    # 支持的文件类型
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".doc", ".txt", ".md"}
    
    # OCR配置（可选）
    ENABLE_OCR: bool = False
    OCR_LANGUAGE: str = "eng+chi_sim"
    
    # 搜索配置
    SEARCH_RESULTS_LIMIT: int = 50
    HIGHLIGHT_LENGTH: int = 200
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

# 确保目录存在
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

