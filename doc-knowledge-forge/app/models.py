"""
数据模型
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

from app.settings import settings


Base = declarative_base()


class Document(Base):
    """文档表"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)
    file_path = Column(String(500), nullable=False)
    markdown_path = Column(String(500))
    
    title = Column(String(500))
    content = Column(Text)
    tags = Column(String(500))  # Comma-separated
    
    file_size = Column(Integer)
    page_count = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_filename', 'filename'),
        Index('idx_created', 'created_at'),
    )


# Pydantic 模型
class DocumentCreate(BaseModel):
    """文档创建"""
    filename: str
    original_name: str
    file_type: str
    file_path: str


class DocumentResponse(BaseModel):
    """文档响应"""
    id: int
    filename: str
    original_name: str
    file_type: str
    title: Optional[str]
    tags: Optional[str]
    file_size: Optional[int]
    page_count: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    """搜索结果"""
    document_id: int
    filename: str
    title: Optional[str]
    snippet: str
    highlights: List[str]
    relevance_score: float


class DocumentStats(BaseModel):
    """文档统计"""
    total_documents: int
    total_size: int
    by_type: dict
    recent_uploads: int


# 数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

