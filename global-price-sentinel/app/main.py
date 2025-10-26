"""
FastAPI 主应用
"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.settings import settings
from app.models import (
    init_db, get_db, PriceRecord, PriceRecordSchema, 
    ReportSummary, TargetConfig
)
from app.reporter import ReportGenerator
from app.monitor import run_monitor_cycle


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
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Developer Portfolio - Upwork/Fiverr Projects</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 60px;
            }
            .header h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            .header p {
                font-size: 1.25rem;
                opacity: 0.95;
            }
            .projects-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 30px;
                margin-bottom: 40px;
            }
            .project-card {
                background: white;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transition: transform 0.3s, box-shadow 0.3s;
                position: relative;
                overflow: hidden;
            }
            .project-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            }
            .project-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #667eea, #764ba2);
            }
            .project-header {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
            }
            .project-icon {
                font-size: 2.5rem;
                margin-right: 15px;
            }
            .project-info h2 {
                font-size: 1.5rem;
                color: #1e293b;
                margin-bottom: 5px;
            }
            .project-info .status {
                display: inline-block;
                padding: 3px 10px;
                background: #10b981;
                color: white;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
            }
            .project-info .status.pending {
                background: #f59e0b;
            }
            .project-description {
                color: #64748b;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            .project-tech {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 20px;
            }
            .tech-tag {
                padding: 4px 12px;
                background: #f1f5f9;
                color: #475569;
                border-radius: 6px;
                font-size: 0.85rem;
            }
            .project-links {
                display: flex;
                gap: 10px;
            }
            .btn {
                flex: 1;
                padding: 12px 20px;
                text-align: center;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.2s;
                border: none;
                cursor: pointer;
            }
            .btn-primary {
                background: #2563eb;
                color: white;
            }
            .btn-primary:hover {
                background: #1d4ed8;
            }
            .btn-secondary {
                background: #f1f5f9;
                color: #475569;
            }
            .btn-secondary:hover {
                background: #e2e8f0;
            }
            .btn-disabled {
                background: #e2e8f0;
                color: #94a3b8;
                cursor: not-allowed;
            }
            .footer {
                text-align: center;
                color: white;
                padding: 40px 20px;
            }
            .footer h3 {
                font-size: 1.5rem;
                margin-bottom: 15px;
            }
            .footer p {
                opacity: 0.9;
                margin-bottom: 10px;
            }
            .quick-links {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
            }
            .quick-link {
                display: inline-block;
                padding: 12px 30px;
                background: rgba(255,255,255,0.2);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                backdrop-filter: blur(10px);
                font-weight: 600;
                transition: all 0.2s;
            }
            .quick-link:hover {
                background: rgba(255,255,255,0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Developer Portfolio</h1>
                <p>6个高质量作品集项目 - Upwork & Fiverr 高需求方向</p>
            </div>

            <div class="projects-grid">
                <!-- Project 1 -->
                <div class="project-card">
                    <div class="project-header">
                        <div class="project-icon">🔍</div>
                        <div class="project-info">
                            <h2>Global Price Sentinel</h2>
                            <span class="status">Running</span>
                        </div>
                    </div>
                    <p class="project-description">
                        跨境电商价格监控系统。使用 Playwright 自动抓取商品价格，生成趋势报告，支持 Webhook 告警。
                    </p>
                    <div class="project-tech">
                        <span class="tech-tag">Python</span>
                        <span class="tech-tag">Playwright</span>
                        <span class="tech-tag">FastAPI</span>
                        <span class="tech-tag">SQLite</span>
                    </div>
                    <div class="project-links">
                        <a href="/api/docs" class="btn btn-primary">API Docs</a>
                        <a href="/reports/latest.html" class="btn btn-secondary">View Report</a>
                    </div>
                </div>

                <!-- Project 2 -->
                <div class="project-card">
                    <div class="project-header">
                        <div class="project-icon">📡</div>
                        <div class="project-info">
                            <h2>Event Relay Hub</h2>
                            <span class="status">Ready</span>
                        </div>
                    </div>
                    <p class="project-description">
                        Webhook 事件汇聚中台。支持 GitHub/Stripe 等第三方事件接入、签名验证、存储与转发。
                    </p>
                    <div class="project-tech">
                        <span class="tech-tag">Python</span>
                        <span class="tech-tag">FastAPI</span>
                        <span class="tech-tag">PostgreSQL</span>
                        <span class="tech-tag">Redis</span>
                    </div>
                    <div class="project-links">
                        <a href="http://localhost:8202" class="btn btn-primary" target="_blank">Open Project</a>
                        <a href="http://localhost:8202/api/docs" class="btn btn-secondary" target="_blank">API Docs</a>
                    </div>
                </div>

                <!-- Project 3 -->
                <div class="project-card">
                    <div class="project-header">
                        <div class="project-icon">📊</div>
                        <div class="project-info">
                            <h2>SaaS Northstar Dashboard</h2>
                            <span class="status">Ready</span>
                        </div>
                    </div>
                    <p class="project-description">
                        SaaS 关键指标看板。展示 MRR、ARR、Churn、LTV 等核心业务指标，支持 CSV 数据导入。
                    </p>
                    <div class="project-tech">
                        <span class="tech-tag">Next.js</span>
                        <span class="tech-tag">React</span>
                        <span class="tech-tag">Tailwind</span>
                        <span class="tech-tag">Chart.js</span>
                    </div>
                    <div class="project-links">
                        <a href="http://localhost:8303" class="btn btn-primary" target="_blank">Open Project</a>
                        <a href="#" class="btn btn-secondary">View Demo</a>
                    </div>
                </div>

                <!-- Project 4 -->
                <div class="project-card">
                    <div class="project-header">
                        <div class="project-icon">📄</div>
                        <div class="project-info">
                            <h2>Doc Knowledge Forge</h2>
                            <span class="status pending">In Progress</span>
                        </div>
                    </div>
                    <p class="project-description">
                        文档转知识库系统。支持 PDF/DOCX 转 Markdown，全文检索，标签管理，批量导出。
                    </p>
                    <div class="project-tech">
                        <span class="tech-tag">Python</span>
                        <span class="tech-tag">FastAPI</span>
                        <span class="tech-tag">pymupdf</span>
                        <span class="tech-tag">SQLite FTS</span>
                    </div>
                    <div class="project-links">
                        <a href="#" class="btn btn-disabled">Coming Soon</a>
                        <a href="#" class="btn btn-secondary">View Docs</a>
                    </div>
                </div>

                <!-- Project 5 -->
                <div class="project-card">
                    <div class="project-header">
                        <div class="project-icon">♿</div>
                        <div class="project-info">
                            <h2>A11y Component Atlas</h2>
                            <span class="status pending">In Progress</span>
                        </div>
                    </div>
                    <p class="project-description">
                        可访问性组件库。符合 WCAG 2.1 AA 标准的 React 组件集合，包含完整的 Storybook 文档。
                    </p>
                    <div class="project-tech">
                        <span class="tech-tag">React</span>
                        <span class="tech-tag">Radix UI</span>
                        <span class="tech-tag">Storybook</span>
                        <span class="tech-tag">Vitest</span>
                    </div>
                    <div class="project-links">
                        <a href="#" class="btn btn-disabled">Coming Soon</a>
                        <a href="#" class="btn btn-secondary">View Docs</a>
                    </div>
                </div>

                <!-- Project 6 -->
                <div class="project-card">
                    <div class="project-header">
                        <div class="project-icon">📈</div>
                        <div class="project-info">
                            <h2>Insight Viz Studio</h2>
                            <span class="status pending">In Progress</span>
                        </div>
                    </div>
                    <p class="project-description">
                        数据可视化工具。上传 CSV/JSON 数据，自动生成交互式图表，支持 PNG/PDF 导出。
                    </p>
                    <div class="project-tech">
                        <span class="tech-tag">Python</span>
                        <span class="tech-tag">FastAPI</span>
                        <span class="tech-tag">ECharts</span>
                        <span class="tech-tag">Pandas</span>
                    </div>
                    <div class="project-links">
                        <a href="#" class="btn btn-disabled">Coming Soon</a>
                        <a href="#" class="btn btn-secondary">View Docs</a>
                    </div>
                </div>
            </div>

            <div class="footer">
                <h3>Quick Links</h3>
                <p>快速访问所有项目的文档和资源</p>
                <div class="quick-links">
                    <a href="/api/docs" class="quick-link">📘 API Documentation</a>
                    <a href="/api/records" class="quick-link">📝 Monitor Records</a>
                    <a href="/api/summary" class="quick-link">📊 Summary Stats</a>
                    <a href="/api/health" class="quick-link">💚 Health Check</a>
                </div>
                <p style="margin-top: 30px; opacity: 0.7;">
                    Developer Portfolio v1.0.0 | Built for Upwork & Fiverr
                </p>
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
