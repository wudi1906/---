"""
数据模型定义
"""
from datetime import datetime
from typing import Optional, List, Literal
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import (
    BaseModel,
    HttpUrl,
    Field,
    EmailStr,
    field_validator,
    model_validator,
    ValidationInfo,
    ConfigDict,
)

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


class MonitorJobRun(Base):
    """调度任务运行日志"""

    __tablename__ = "monitor_job_runs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), index=True, nullable=False)
    job_name = Column(String(200), nullable=False)
    status = Column(String(20), nullable=False)  # success / failed
    message = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at = Column(DateTime)
    duration_ms = Column(Integer)


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



class MonitorConfigModel(Base):
    """监控与告警配置表"""
    __tablename__ = "monitor_config"

    id = Column(Integer, primary_key=True, index=True)
    scheduler_mode = Column(String(20), default="cron")  # cron or interval
    cron_expression = Column(String(100), default=settings.CRON_SCHEDULE)
    interval_minutes = Column(Integer, default=720)
    proxy_enabled = Column(Boolean, default=False)
    proxy_server = Column(String(255))
    proxy_username = Column(String(128))
    proxy_password = Column(String(128))
    alert_channels = Column(Text, default="[]")  # JSON 字符串
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AlertChannelConfig(BaseModel):
    """告警渠道配置"""

    type: Literal["email", "webhook", "slack"] = Field(description="渠道类型")
    enabled: bool = Field(default=True, description="是否启用")
    name: Optional[str] = Field(default=None, description="渠道名称")
    recipients: Optional[List[EmailStr]] = Field(default=None, description="邮件收件人列表")
    webhook_url: Optional[HttpUrl] = Field(default=None, description="Webhook URL")

    @model_validator(mode="after")
    def _validate_channel(self):
        if not self.enabled:
            return self
        if self.type == "email":
            if not self.recipients:
                raise ValueError("Email 渠道需要至少一个收件人")
        else:
            if not self.webhook_url:
                raise ValueError(f"{self.type} 渠道需要有效的 webhook_url")
        return self


class MonitorConfigBase(BaseModel):
    scheduler_mode: Literal["cron", "interval"] = Field(default="cron", description="调度模式")
    cron_expression: str = Field(default=settings.CRON_SCHEDULE, description="Cron 表达式")
    interval_minutes: int = Field(default=720, ge=5, le=1440, description="调度间隔（分钟）")
    proxy_enabled: bool = Field(default=False, description="是否启用代理池")
    proxy_server: Optional[str] = Field(default=None, description="代理服务器地址")
    proxy_username: Optional[str] = Field(default=None, description="代理用户名")
    proxy_password: Optional[str] = Field(default=None, description="代理密码")
    alert_channels: List[AlertChannelConfig] = Field(default_factory=list, description="告警渠道配置")

    @field_validator("cron_expression")
    @classmethod
    def _validate_cron(cls, value: str, info: ValidationInfo):
        mode = info.data.get("scheduler_mode", "cron") if info.data else "cron"
        if mode == "cron":
            parts = value.split()
            if len(parts) != 5:
                raise ValueError("Cron 表达式必须包含5个字段")
        return value

    @model_validator(mode="after")
    def _validate_proxy(self):
        if self.proxy_enabled and not self.proxy_server:
            raise ValueError("启用代理时必须提供代理服务器地址")
        return self


class MonitorConfigUpdate(MonitorConfigBase):
    pass


class MonitorConfigSchema(MonitorConfigBase):
    id: int = Field(default=1, description="配置ID")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")

    model_config = ConfigDict(from_attributes=True)


class MonitorJobRunSchema(BaseModel):
    """调度任务运行记录"""

    id: int
    job_id: str
    job_name: str
    status: str
    message: Optional[str]
    started_at: datetime
    finished_at: Optional[datetime]
    duration_ms: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class SchedulerStatusSchema(BaseModel):
    """调度状态响应"""

    job_id: str
    job_name: str
    next_run_time: Optional[datetime]
    time_until_next_run_seconds: Optional[int]
    last_run: Optional[MonitorJobRunSchema]
    recent_runs: List[MonitorJobRunSchema] = Field(default_factory=list)


class AlertTestRequest(BaseModel):
    """告警渠道测试请求"""

    channel: Literal["email", "slack", "webhook"]
    payload: Optional[dict] = None


class AlertTestResponse(BaseModel):
    """告警渠道测试响应"""

    success: bool
    message: str
    detail: Optional[dict] = None


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

