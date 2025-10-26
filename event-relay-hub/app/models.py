"""
数据模型
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Index, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field

from app.settings import settings


Base = declarative_base()


class Event(Base):
    """事件记录表"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), index=True, nullable=False)  # github, stripe, custom
    event_type = Column(String(100), index=True)
    payload = Column(Text, nullable=False)  # JSON string
    headers = Column(Text)  # JSON string of headers
    signature_valid = Column(Boolean, default=False)
    forwarded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_source_created', 'source', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Event {self.id}: {self.source}/{self.event_type}>"


class ForwardLog(Base):
    """转发日志表"""
    __tablename__ = "forward_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True)
    target_url = Column(String(500))
    status_code = Column(Integer)
    success = Column(Boolean, default=False)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# Pydantic 模型
class EventCreate(BaseModel):
    """创建事件请求"""
    source: str
    event_type: Optional[str] = None
    payload: Dict[str, Any]
    headers: Optional[Dict[str, str]] = None


class EventResponse(BaseModel):
    """事件响应"""
    id: int
    source: str
    event_type: Optional[str]
    payload: str
    signature_valid: bool
    forwarded: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class EventStats(BaseModel):
    """事件统计"""
    total_events: int
    by_source: Dict[str, int]
    by_event_type: Dict[str, int]
    recent_24h: int
    signature_success_rate: float


class ReplayResponse(BaseModel):
    """重放响应"""
    success: bool
    message: str
    event_id: int


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

