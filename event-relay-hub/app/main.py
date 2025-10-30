"""
Event Relay Hub 主应用
"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Request, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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
import random
import json


# 创建应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="通用 Webhook 事件汇聚与转发中台",
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

# 静态文件
try:
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
except:
    pass  # frontend 目录可能不存在


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
async def root():
    """根路径 - 显示欢迎页"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Event Relay Hub</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                padding: 20px;
            }
            .container { text-align: center; max-width: 600px; }
            h1 { font-size: 3rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
            p { font-size: 1.25rem; margin-bottom: 2rem; opacity: 0.95; }
            .links { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
            .btn {
                padding: 12px 32px;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.2s;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
            .endpoints {
                margin-top: 3rem;
                background: rgba(255,255,255,0.1);
                padding: 24px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
                text-align: left;
            }
            .endpoints h3 { margin-bottom: 12px; }
            .endpoints code {
                display: block;
                background: rgba(0,0,0,0.2);
                padding: 8px 12px;
                border-radius: 4px;
                margin: 8px 0;
                font-family: 'Courier New', monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📡 Event Relay Hub</h1>
            <p>Webhook 事件汇聚与转发中台</p>
            
            <div class="links">
                <a href="/api/docs" class="btn">📘 API 文档</a>
                <a href="/api/events?limit=10" class="btn">📝 事件列表</a>
                <a href="/api/stats" class="btn">📊 统计信息</a>
            </div>
            
            <div class="endpoints">
                <h3>Webhook 端点</h3>
                <code>POST /webhook/github</code>
                <code>POST /webhook/stripe</code>
                <code>POST /webhook/custom</code>
            </div>
        </div>
    </body>
    </html>
    """


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


@app.post("/api/demo/seed")
async def demo_seed(db: Session = Depends(get_db)):
    """导入示例事件数据"""
    sources = ["stripe", "github", "slack"]
    event_types_map = {
        "stripe": ["payment.succeeded", "subscription.created", "invoice.paid"],
        "github": ["push", "pull_request", "issue_comment"],
        "slack": ["message.im", "app_mention", "reaction_added"]
    }
    
    created_count = 0
    for days_ago in range(7, 0, -1):
        for source in sources:
            for event_type in random.sample(event_types_map[source], k=random.randint(1, 3)):
                event = Event(
                    source=source,
                    event_type=event_type,
                    payload=json.dumps({"id": f"evt_{random.randint(1000,9999)}", "data": "sample"}),
                    headers=json.dumps({"X-Source": source.title()}),
                    signature_valid=random.choice([True, True, True, False]),
                    created_at=datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
                )
                db.add(event)
                created_count += 1
                
                # 添加转发日志
                if random.random() > 0.3:
                    log = ForwardLog(
                        event_id=None,  # 稍后会关联
                        target_url="https://api.example.com/webhook",
                        status_code=random.choice([200, 200, 200, 500]),
                        success=random.choice([True, True, True, False]),
                        created_at=event.created_at
                    )
                    db.add(log)
    
    db.commit()
    return {"success": True, "seeded_events": created_count}


@app.post("/api/demo/reset")
async def demo_reset(db: Session = Depends(get_db)):
    """清空所有事件数据"""
    db.query(Event).delete()
    db.query(ForwardLog).delete()
    db.commit()
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

