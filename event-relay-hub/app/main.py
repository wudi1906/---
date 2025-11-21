"""
Event Relay Hub 主应用
"""
from datetime import datetime, timedelta
from typing import List, Optional
import json
import uuid
import random
from fastapi import FastAPI, Request, Depends, Query, HTTPException, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.settings import settings
from app.models import (
    init_db, get_db, Event, EventResponse, 
    EventStats, ReplayResponse, ForwardLog
)
from app.webhooks import WebhookHandler
from app.forwarder import EventForwarder
from app.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from pathlib import Path

# 创建应用
app = FastAPI(
    title="Payment Webhook Debugger",
    version=settings.APP_VERSION,
    description="Stripe Payment & GitHub Webhook Relay/Debugger",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 添加速率限制中间件
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件与模板
try:
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
except:
    pass

templates_dir = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    init_db()
    print(f"✓ {settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
    print(f"  - 监听地址: http://{settings.HOST}:{settings.PORT}")
    print(f"  - API文档: http://{settings.HOST}:{settings.PORT}/api/docs")


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """速率限制异常处理"""
    return {
        "error": "Rate limit exceeded",
        "detail": str(exc)
    }


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """根路径 - 显示仪表盘"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/simulate/stripe")
async def simulate_stripe_event(
    payload: dict = Body(..., example={"type": "payment_intent.succeeded"}),
    db: Session = Depends(get_db)
):
    """
    [New Feature] Simulate a Stripe Event
    Generates a mock Stripe payload and injects it into the system.
    """
    event_type = payload.get("type", "payment_intent.succeeded")
    
    # Construct mock payload based on type
    mock_id = f"evt_sim_{uuid.uuid4().hex[:16]}"
    timestamp = int(datetime.utcnow().timestamp())
    
    mock_data = {
        "id": mock_id,
        "object": "event",
        "api_version": "2023-10-16",
        "created": timestamp,
        "type": event_type,
        "data": {
            "object": {
                "id": f"pi_{uuid.uuid4().hex[:14]}",
                "object": "payment_intent",
                "amount": random.randint(1000, 50000),
                "currency": "usd",
                "status": "succeeded" if "succeeded" in event_type else "requires_payment_method",
                "payment_method": f"pm_{uuid.uuid4().hex[:14]}"
            }
        },
        "livemode": False,
        "pending_webhooks": 1,
        "request": {
            "id": f"req_{uuid.uuid4().hex[:14]}",
            "idempotency_key": f"idem_{uuid.uuid4().hex[:14]}"
        }
    }

    # Inject into DB
    event = Event(
        source="stripe (simulated)",
        event_type=event_type,
        payload=json.dumps(mock_data, indent=2),
        headers=json.dumps({
            "User-Agent": "Stripe/1.0 (+https://stripe.com/docs/webhooks)",
            "Stripe-Signature": "t=1234567890,v1=simulated_signature",
            "Content-Type": "application/json"
        }),
        signature_valid=True # Simulated events are always valid
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    
    # Trigger forwarding if enabled
    # (Optional: In a real debugger, you might NOT want to forward simulations, 
    # but here we do to show the full flow)
    if settings.FORWARD_ENABLED and settings.FORWARD_URL:
        forwarder = EventForwarder()
        await forwarder.forward_event(event, settings.FORWARD_URL)

    return {"success": True, "event_id": event.id, "type": event_type}


@app.get("/api/health")
async def health_check():

    """健康检查"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/webhook/github")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    """接收 GitHub Webhook"""
    handler = WebhookHandler(db)
    return await handler.handle_github(request)


@app.post("/webhook/stripe")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """接收 Stripe Webhook"""
    handler = WebhookHandler(db)
    return await handler.handle_stripe(request)


@app.post("/webhook/custom")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def custom_webhook(request: Request, db: Session = Depends(get_db)):
    """接收自定义 Webhook"""
    handler = WebhookHandler(db)
    return await handler.handle_custom(request)


@app.get("/api/events", response_model=List[EventResponse])
async def get_events(
    source: Optional[str] = Query(None, description="事件源"),
    event_type: Optional[str] = Query(None, description="事件类型"),
    days: int = Query(7, ge=1, le=90, description="查询天数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数量"),
    db: Session = Depends(get_db)
):
    """获取事件列表"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = db.query(Event).filter(Event.created_at >= cutoff_date)
    
    if source:
        query = query.filter(Event.source == source)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    events = query.order_by(desc(Event.created_at)).limit(limit).all()
    return events


@app.get("/api/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """获取单个事件详情"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/api/events/{event_id}/replay", response_model=ReplayResponse)
async def replay_event(
    event_id: int,
    target_url: Optional[str] = Query(None, description="目标URL"),
    db: Session = Depends(get_db)
):
    """重放事件"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    forwarder = EventForwarder()
    url = target_url or settings.FORWARD_URL
    
    if not url:
        raise HTTPException(status_code=400, detail="No target URL provided")
    
    success = await forwarder.replay_event(event_id, url)
    
    return ReplayResponse(
        success=success,
        message="Event replayed successfully" if success else "Replay failed",
        event_id=event_id
    )


@app.get("/api/stats", response_model=EventStats)
async def get_stats(db: Session = Depends(get_db)):
    """获取事件统计"""
    total = db.query(func.count(Event.id)).scalar()
    
    # 按来源统计
    by_source = {}
    for source, count in db.query(Event.source, func.count(Event.id)).group_by(Event.source).all():
        by_source[source] = count
    
    # 按事件类型统计
    by_event_type = {}
    for event_type, count in db.query(Event.event_type, func.count(Event.id)).group_by(Event.event_type).limit(10).all():
        if event_type:
            by_event_type[event_type] = count
    
    # 最近24小时
    cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_24h = db.query(func.count(Event.id)).filter(Event.created_at >= cutoff).scalar()
    
    # 签名成功率
    total_with_sig = db.query(func.count(Event.id)).scalar()
    valid_sig = db.query(func.count(Event.id)).filter(Event.signature_valid == True).scalar()
    sig_success_rate = (valid_sig / total_with_sig * 100) if total_with_sig > 0 else 0.0
    
    return EventStats(
        total_events=total,
        by_source=by_source,
        by_event_type=by_event_type,
        recent_24h=recent_24h,
        signature_success_rate=sig_success_rate
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

