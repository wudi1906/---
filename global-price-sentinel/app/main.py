"""
FastAPI 主应用
"""
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pathlib import Path
from apscheduler.triggers.cron import CronTrigger

from app.settings import settings
from app.models import (
    init_db,
    get_db,
    PriceRecord,
    PriceRecordSchema,
    ReportSummary,
    TargetConfig,
    AlertLog,
    MonitorConfigSchema,
    MonitorConfigUpdate,
    MonitorJobRun,
    MonitorJobRunSchema,
    SchedulerStatusSchema,
    AlertTestRequest,
    AlertTestResponse,
)
from app.reporter import ReportGenerator
from app.monitor import run_monitor_cycle
import random
from app.config_service import ConfigService
from app.scheduler import scheduler_instance
from app.webhooks import AlertDispatcher


# 辅助函数：计算下次运行时间
def _compute_next_run_time(config: MonitorConfigSchema) -> Optional[datetime]:
    now = datetime.utcnow()
    if config.scheduler_mode == "interval":
        return now + timedelta(minutes=config.interval_minutes)

    try:
        trigger = CronTrigger.from_crontab(config.cron_expression, timezone=timezone.utc)
        next_fire = trigger.get_next_fire_time(None, now.replace(tzinfo=timezone.utc))
        return next_fire.replace(tzinfo=None) if next_fire else None
    except Exception as exc:  # pragma: no cover - 容错
        print(f"[scheduler] 无法解析 Cron 表达式 {config.cron_expression}: {exc}")
        return None


# 初始化应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="全球电商价格监控系统",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
app.mount("/screenshots", StaticFiles(directory=str(settings.SCREENSHOTS_DIR)), name="screenshots")
app.mount("/reports", StaticFiles(directory=str(settings.REPORTS_DIR)), name="reports")


@app.on_event("startup")
async def startup_event():
    """启动时初始化数据库"""
    init_db()
    print(f"✓ {settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
    print(f"  - 监听地址: http://{settings.HOST}:{settings.PORT}")
    print(f"  - API文档: http://{settings.HOST}:{settings.PORT}/api/docs")


@app.get("/", response_class=HTMLResponse)
async def root():
    """根路径 - 显示统一门户"""
    portal_path = Path(__file__).resolve().parents[2] / "PORTAL_REDESIGN.html"
    if portal_path.exists():
        return portal_path.read_text(encoding="utf-8")
    return "<html><body><h1>Portal not found</h1><p>请确保 PORTAL_REDESIGN.html 存在于作品集根目录。</p></body></html>"


@app.get("/monitor/settings", response_class=HTMLResponse)
async def monitor_settings_page():
    template_path = Path(__file__).resolve().parent / "templates" / "monitor_settings.html"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return HTMLResponse(
        "<h1>Monitor settings UI 未找到</h1><p>请检查 templates/monitor_settings.html 是否存在。</p>",
        status_code=404,
    )


@app.get("/api/config/monitor", response_model=MonitorConfigSchema)
async def get_monitor_config():
    return ConfigService.get_config()


@app.put("/api/config/monitor", response_model=MonitorConfigSchema)
async def update_monitor_config(payload: MonitorConfigUpdate):
    return ConfigService.update_config(payload)


@app.get("/api/scheduler/status", response_model=SchedulerStatusSchema)
async def get_scheduler_status(limit: int = Query(5, ge=1, le=50), db: Session = Depends(get_db)):
    config = ConfigService.get_config()
    next_run = _compute_next_run_time(config)

    # 如果调度器已启动，使用实际下一次运行时间
    if scheduler_instance:
        job = scheduler_instance.get_job("monitor_task")
        if job and job.next_run_time:
            next_run = job.next_run_time.replace(tzinfo=None)

    runs = (
        db.query(MonitorJobRun)
        .filter(MonitorJobRun.job_id == "monitor_task")
        .order_by(desc(MonitorJobRun.started_at))
        .limit(limit)
        .all()
    )

    last_run = runs[0] if runs else None
    time_until = None
    if next_run:
        time_until = int(max((next_run - datetime.utcnow()).total_seconds(), 0))

    return SchedulerStatusSchema(
        job_id="monitor_task",
        job_name="Price Monitor Task",
        next_run_time=next_run,
        time_until_next_run_seconds=time_until,
        last_run=MonitorJobRunSchema.model_validate(last_run) if last_run else None,
        recent_runs=[MonitorJobRunSchema.model_validate(run) for run in runs],
    )


@app.post("/api/alerts/test", response_model=AlertTestResponse)
async def test_alert_channel(payload: AlertTestRequest):
    success, message, detail = AlertDispatcher.test_channel(payload.channel, payload.payload or {})
    return AlertTestResponse(success=success, message=message, detail=detail)


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/records", response_model=List[PriceRecordSchema])
async def get_records(
    target_id: Optional[str] = Query(None, description="目标产品ID"),
    days: int = Query(7, ge=1, le=90, description="查询天数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数量"),
    db: Session = Depends(get_db)
):
    """获取价格记录"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = db.query(PriceRecord).filter(PriceRecord.created_at >= cutoff_date)
    
    if target_id:
        query = query.filter(PriceRecord.target_id == target_id)
    
    records = query.order_by(desc(PriceRecord.created_at)).limit(limit).all()
    return records


@app.get("/api/summary", response_model=List[ReportSummary])
async def get_summary(
    days: int = Query(7, ge=1, le=90, description="统计天数")
):
    """获取价格趋势摘要"""
    summaries = ReportGenerator.generate_summary(days=days)
    return summaries


@app.post("/api/monitor/run")
async def trigger_monitor(targets: List[TargetConfig]):
    """手动触发监控（用于测试）"""
    try:
        records = await run_monitor_cycle(targets)
        return {
            "success": True,
            "message": f"监控完成，共 {len(records)} 条记录",
            "records": len(records)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/report/generate")
async def generate_report(
    days: int = Query(7, ge=1, le=90, description="报告天数"),
    format: str = Query("html", regex="^(html|csv)$", description="报告格式")
):
    """生成报告"""
    try:
        if format == "html":
            report_path = ReportGenerator.generate_html_report(days=days)
        else:
            report_path = ReportGenerator.generate_csv_report(days=days)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "report_url": f"/reports/{report_path.name}",
            "download_url": f"/api/report/download?file={report_path.name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/report/download")
async def download_report(file: str):
    """下载报告文件"""
    file_path = settings.REPORTS_DIR / file
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="报告文件不存在")
    
    return FileResponse(
        path=file_path,
        filename=file,
        media_type="application/octet-stream"
    )


@app.post("/api/demo/seed")
async def demo_seed(db: Session = Depends(get_db)):
    """导入示例监控数据"""
    targets = [
        {"id": "amazon-laptop", "name": "ThinkPad X1 Carbon", "base_price": 1299.99, "url": "https://amazon.com/laptop"},
        {"id": "jd-phone", "name": "iPhone 15 Pro", "base_price": 7999.00, "url": "https://jd.com/iphone"},
        {"id": "taobao-watch", "name": "Apple Watch Series 9", "base_price": 2999.00, "url": "https://taobao.com/watch"},
    ]
    
    created_count = 0
    for t in targets:
        # 生成30天历史数据
        for days_ago in range(30, 0, -1):
            variance = random.uniform(-0.15, 0.15)
            price = round(t["base_price"] * (1 + variance), 2)
            record = PriceRecord(
                target_id=t["id"],
                url=t["url"],
                product_name=t["name"],
                price=price,
                currency="USD" if "amazon" in t["id"] else "CNY",
                stock_status="in_stock" if random.random() > 0.1 else "low_stock",
                success=True,
                created_at=datetime.utcnow() - timedelta(days=days_ago)
            )
            db.add(record)
            created_count += 1
        
        # 添加告警示例
        if random.random() > 0.5:
            alert = AlertLog(
                target_id=t["id"],
                alert_type="price_change",
                message=f"{t['name']} 价格下降 8%",
                old_price=t["base_price"],
                new_price=t["base_price"] * 0.92,
                sent_to="webhook://example.com/alert",
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
            )
            db.add(alert)
    
    db.commit()
    return {"success": True, "seeded_records": created_count, "targets": len(targets)}


@app.post("/api/demo/reset")
async def demo_reset(db: Session = Depends(get_db)):
    """清空所有监控数据"""
    db.query(PriceRecord).delete()
    db.query(AlertLog).delete()
    db.commit()
    
    # 清理截图和报告文件
    for p in settings.SCREENSHOTS_DIR.glob("*"):
        try:
            if p.is_file():
                p.unlink()
        except Exception:
            pass
    for p in settings.REPORTS_DIR.glob("*"):
        try:
            if p.is_file():
                p.unlink()
        except Exception:
            pass
    
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
