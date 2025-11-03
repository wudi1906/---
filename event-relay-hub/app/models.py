"""
数据模型
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Index, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field, ConfigDict

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


class SignatureTemplate(Base):
    """签名验证模板"""

    __tablename__ = "signature_templates"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(100), default="")
    description = Column(Text)
    enabled = Column(Boolean, default=False)
    secret = Column(String(255))
    signature_header = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DeadLetterEvent(Base):
    """死信队列"""

    __tablename__ = "dead_letter_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True, nullable=False)
    target_url = Column(String(500))
    reason = Column(Text)
    last_error = Column(Text)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


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
    forward_success: int = 0
    forward_failed: int = 0
    dead_letters: int = 0


class ReplayResponse(BaseModel):
    """单次事件重放结果"""

    success: bool
    message: str
    event_id: int
    retry_after: Optional[int] = None
    last_attempt_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    notes: Optional[str] = None


class PaginatedEvents(BaseModel):
    """事件分页响应"""

    total: int
    page: int
    page_size: int
    items: List[EventResponse]


class BulkReplayRequest(BaseModel):
    """批量重放请求体"""

    ids: List[int] = Field(min_length=1, description="事件ID列表")
    target_url: Optional[str] = Field(default=None, description="覆盖目标URL")


class BulkReplayResult(BaseModel):
    """批量重放返回体"""

    success_ids: List[int]
    failed: Dict[int, str]
    notes: Dict[int, str] = Field(default_factory=dict)


class SignatureTemplateSchema(BaseModel):
    """签名模板响应"""

    id: int
    source: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    enabled: bool = False
    signature_header: Optional[str] = None
    has_secret: bool = False
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SignatureTemplateUpdate(BaseModel):
    """签名模板更新"""

    enabled: bool = Field(default=False)
    secret: Optional[str] = Field(default=None, description="签名密钥")
    signature_header: Optional[str] = Field(default=None, description="签名头部键名")


class DeadLetterSchema(BaseModel):
    """死信队列项"""

    id: int
    event_id: int
    source: str
    event_type: Optional[str]
    target_url: Optional[str]
    reason: Optional[str]
    last_error: Optional[str]
    retry_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    payload_preview: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class PaginatedDeadLetters(BaseModel):
    """死信分页响应"""

    total: int
    page: int
    page_size: int
    items: List[DeadLetterSchema]


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

