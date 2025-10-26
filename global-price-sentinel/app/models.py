"""
数据模型定义
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, HttpUrl, Field

from app.settings import settings


Base = declarative_base()


class PriceRecord(Base):
    """价格记录表"""
    __tablename__ = "price_records"
    
    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(String(100), index=True, nullable=False)
    url = Column(String(500), nullable=False)
    product_name = Column(String(200))
    price = Column(Float)
    currency = Column(String(10), default="USD")
    stock_status = Column(String(50))
    screenshot_path = Column(String(500))
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<PriceRecord {self.target_id}: {self.price} {self.currency}>"


class AlertLog(Base):
    """告警日志表"""
    __tablename__ = "alert_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(String(100), index=True)
    alert_type = Column(String(50))  # price_change, stock_out, error
    message = Column(Text)
    old_price = Column(Float)
    new_price = Column(Float)
    sent_to = Column(String(200))  # webhook URLs
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


# Pydantic 模型
class TargetConfig(BaseModel):
    """监控目标配置"""
    id: str = Field(..., description="唯一标识")
    url: HttpUrl = Field(..., description="目标URL")
    name_selector: Optional[str] = Field(None, description="产品名称CSS选择器")
    price_selector: Optional[str] = Field(None, description="价格CSS选择器")
    price_regex: Optional[str] = Field(None, description="价格正则表达式")
    stock_selector: Optional[str] = Field(None, description="库存状态选择器")
    currency: str = Field(default="USD", description="货币单位")
    threshold_pct: float = Field(default=5.0, description="价格变动阈值百分比")
    enabled: bool = Field(default=True, description="是否启用")


class PriceRecordSchema(BaseModel):
    """价格记录响应模型"""
    id: int
    target_id: str
    url: str
    product_name: Optional[str]
    price: Optional[float]
    currency: str
    stock_status: Optional[str]
    success: bool
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReportSummary(BaseModel):
    """报告摘要"""
    target_id: str
    product_name: Optional[str]
    latest_price: Optional[float]
    price_change_pct: Optional[float]
    min_price: Optional[float]
    max_price: Optional[float]
    avg_price: Optional[float]
    currency: str
    last_updated: datetime
    total_records: int


# 数据库引擎和会话
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

