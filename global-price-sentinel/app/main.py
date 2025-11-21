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
    # 确保报告目录存在并有最新报告，避免门户“View Report”404
    settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    latest_report = settings.REPORTS_DIR / "latest.html"
    if not latest_report.exists():
        try:
            ReportGenerator.generate_html_report()
            print("  - 已自动生成初始 HTML 报告")
        except Exception as exc:  # pragma: no cover - 仅日志
            print(f"  - 初始报告生成失败: {exc}")
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
        <title>Developer Portfolio - Professional Solutions</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            :root {
                --primary-blue: #3b5bdb;
                --primary-light: #5c7cfa;
                --bg-main: #ffffff;
                --bg-section: #f8f9fa;
                --text-dark: #212529;
                --text-gray: #495057;
                --text-light: #868e96;
                --border-color: #dee2e6;
                --card-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
                --card-shadow-hover: 0 8px 24px rgba(59, 91, 219, 0.15);
            }
            
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: var(--bg-main);
                min-height: 100vh;
                color: var(--text-dark);
                line-height: 1.6;
            }
            
            /* Decorative Shapes */
            .decoration {
                position: fixed;
                border-radius: 50%;
                opacity: 0.4;
                z-index: 0;
            }
            .decoration.circle-1 {
                width: 300px;
                height: 300px;
                background: linear-gradient(135deg, #a5d8ff 0%, #74c0fc 100%);
                top: 10%;
                right: 5%;
            }
            .decoration.circle-2 {
                width: 250px;
                height: 250px;
                background: linear-gradient(135deg, #b2f2bb 0%, #8ce99a 100%);
                bottom: 15%;
                left: 8%;
            }
            .decoration.square-1 {
                width: 200px;
                height: 200px;
                background: linear-gradient(135deg, #ffd43b 0%, #fcc419 100%);
                border-radius: 20px;
                bottom: 25%;
                right: 10%;
                opacity: 0.3;
            }
            .decoration.square-2 {
                width: 180px;
                height: 180px;
                background: linear-gradient(135deg, #e599f7 0%, #cc5de8 100%);
                border-radius: 20px;
                top: 40%;
                left: 5%;
                opacity: 0.3;
            }
            
            .container { 
                max-width: 1400px; 
                margin: 0 auto;
                position: relative;
                z-index: 1;
                padding: 80px 32px;
            }
            
            header { 
                text-align: center; 
                margin-bottom: 72px;
            }
            
            header h1 { 
                font-size: clamp(2.5rem, 5vw, 3.75rem);
                font-weight: 800;
                margin-bottom: 20px;
                color: var(--primary-blue);
                letter-spacing: -0.02em;
            }
            
            header p { 
                color: var(--text-gray); 
                font-size: 1.25rem;
                font-weight: 400;
                max-width: 700px;
                margin: 0 auto 12px;
            }
            
            header .subtitle {
                color: var(--text-light);
                font-size: 1rem;
                font-weight: 500;
            }
            
            .projects-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 28px;
                max-width: 1300px;
                margin: 0 auto;
            }
            
            @media (max-width: 1200px) {
                .projects-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
            
            @media (max-width: 768px) {
                .projects-grid {
                    grid-template-columns: 1fr;
                }
                .container {
                    padding: 40px 20px;
                }
            }
            .project-card {
                background: white;
                border: 2px solid var(--border-color);
                border-radius: 16px;
                padding: 32px;
                position: relative;
                overflow: visible;
                box-shadow: var(--card-shadow);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .project-card:hover {
                box-shadow: var(--card-shadow-hover);
                transform: translateY(-4px);
                border-color: var(--primary-light);
            }
            .project-content { 
                display: flex; 
                flex-direction: column; 
                gap: 20px; 
                height: 100%;
            }
            .project-header { 
                display: flex; 
                justify-content: space-between; 
                align-items: flex-start;
                margin-bottom: 8px;
            }
            .project-meta { 
                display: flex; 
                gap: 16px; 
                align-items: flex-start; 
                flex: 1;
            }
            .project-icon { 
                font-size: 3rem; 
                line-height: 1;
                flex-shrink: 0;
            }
            .project-info {
                flex: 1;
            }
            .project-title { 
                font-size: 1.5rem; 
                font-weight: 700;
                color: var(--text-dark);
                margin-bottom: 4px;
                line-height: 1.3;
            }
            .project-subtitle {
                font-size: 0.9rem;
                color: var(--text-light);
                font-weight: 500;
            }
            .status-chip {
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                background: #e7f5ff;
                color: var(--primary-blue);
                white-space: nowrap;
            }
            .description { 
                line-height: 1.7; 
                font-size: 0.95rem; 
                color: var(--text-gray);
                flex-grow: 1;
            }
            .features-list {
                list-style: none;
                padding: 0;
                margin: 12px 0;
            }
            .features-list li {
                padding: 6px 0 6px 20px;
                position: relative;
                font-size: 0.9rem;
                color: var(--text-gray);
            }
            .features-list li::before {
                content: '✓';
                position: absolute;
                left: 0;
                color: var(--primary-blue);
                font-weight: bold;
            }
            .tech-stack { 
                display: flex; 
                flex-wrap: wrap; 
                gap: 8px; 
                margin-top: 4px;
            }
            .tag {
                padding: 5px 12px;
                border-radius: 6px;
                background: var(--bg-section);
                color: var(--text-gray);
                font-size: 0.8rem;
                font-weight: 500;
                border: 1px solid var(--border-color);
            }
            .actions { 
                display: flex; 
                gap: 12px; 
                margin-top: auto;
                padding-top: 12px;
            }
            .btn {
                flex: 1;
                padding: 12px 20px;
                border-radius: 8px;
                border: 2px solid transparent;
                font-weight: 600;
                font-size: 0.9rem;
                cursor: pointer;
                transition: all 0.2s ease;
                text-decoration: none;
                display: inline-block;
                text-align: center;
            }
            .btn:disabled { opacity: 0.5; cursor: not-allowed; }
            .btn-primary { 
                background: var(--primary-blue); 
                color: white;
                border-color: var(--primary-blue);
            }
            .btn-primary:hover:not(:disabled) { 
                background: var(--primary-light);
                border-color: var(--primary-light);
            }
            .btn-secondary { 
                background: white; 
                color: var(--primary-blue);
                border-color: var(--primary-blue);
            }
            .btn-secondary:hover:not(:disabled) { 
                background: var(--primary-blue);
                color: white;
            }
            
            footer { 
                margin-top: 80px; 
                padding-top: 40px;
                border-top: 2px solid var(--border-color);
                text-align: center; 
                color: var(--text-light); 
            }
            footer p {
                margin-bottom: 16px;
                font-size: 0.95rem;
            }
            footer .link-row { 
                display: flex; 
                flex-wrap: wrap; 
                justify-content: center; 
                gap: 12px; 
                margin-top: 16px; 
            }
            footer a { 
                text-decoration: none; 
                padding: 10px 20px; 
                border-radius: 8px; 
                background: var(--bg-section); 
                color: var(--primary-blue); 
                font-weight: 600; 
                transition: all 0.2s;
                border: 1px solid var(--border-color);
            }
            footer a:hover { 
                background: var(--primary-blue);
                color: white;
                border-color: var(--primary-blue);
            }
            .toast {
                position: fixed;
                top: 24px;
                right: 24px;
                padding: 14px 18px;
                border-radius: 14px;
                background: #0f172a;
                color: white;
                opacity: 0;
                transform: translateY(-20px);
                transition: all 0.3s ease;
                font-size: 0.95rem;
            }
            .toast.show { opacity: 1; transform: translateY(0); }
        </style>
    </head>
    <body>
        <!-- Decorative Shapes -->
        <div class="decoration circle-1"></div>
        <div class="decoration circle-2"></div>
        <div class="decoration square-1"></div>
        <div class="decoration square-2"></div>
        
        <div class="container">
            <header>
                <h1>Professional Solutions Portfolio</h1>
                <p>Six Production-Ready Projects for Upwork & Fiverr Success</p>
                <div class="subtitle">Web Scraping · Event Systems · SaaS Dashboards · AI Document Processing · Accessibility · Data Visualization</div>
            </header>

            <div class="projects-grid">
                <article class="project-card">
                    <div class="project-content">
                        <div class="project-header">
                            <div class="project-meta">
                                <span class="project-icon">🔍</span>
                                <div class="project-info">
                                    <h2 class="project-title">Global Price Sentinel</h2>
                                    <div class="project-subtitle">E-commerce Price Monitoring System</div>
                                </div>
                            </div>
                            <span class="status-chip">● Running</span>
                        </div>
                        <p class="description">
                            Professional web scraping solution for e-commerce price tracking. Automated data collection with Playwright, 
                            generates beautiful HTML/Excel reports, and supports webhook notifications for price changes.
                        </p>
                        <ul class="features-list">
                            <li>Automated price monitoring across multiple platforms</li>
                            <li>Visual trend reports with historical data analysis</li>
                            <li>RESTful API with comprehensive documentation</li>
                            <li>Webhook integration for real-time alerts</li>
                        </ul>
                        <div class="tech-stack">
                            <span class="tag">Python</span>
                            <span class="tag">Playwright</span>
                            <span class="tag">FastAPI</span>
                            <span class="tag">SQLite</span>
                        </div>
                        <div class="actions">
                            <a class="btn btn-primary" href="/api/docs" target="_blank" rel="noreferrer">API Documentation</a>
                            <button class="btn btn-secondary" data-generate-report>Generate Report</button>
                        </div>
                    </div>
                </article>

                <article class="project-card">
                    <div class="project-content">
                        <div class="project-header">
                            <div class="project-meta">
                                <span class="project-icon">📡</span>
                                <div class="project-info">
                                    <h2 class="project-title">Event Relay Hub</h2>
                                    <div class="project-subtitle">Webhook Testing & Event Simulation</div>
                                </div>
                            </div>
                            <span class="status-chip">● Ready</span>
                        </div>
                        <p class="description">
                            Developer-friendly webhook debugger for payment systems. Simulate Stripe, GitHub, and custom events 
                            with signature validation, rate limiting, and complete event timeline tracking.
                        </p>
                        <ul class="features-list">
                            <li>One-click event simulation for major platforms</li>
                            <li>Signature verification and request forwarding</li>
                            <li>Built-in rate limiting and retry mechanisms</li>
                            <li>Real-time event timeline visualization</li>
                        </ul>
                        <div class="tech-stack">
                            <span class="tag">Python</span>
                            <span class="tag">FastAPI</span>
                            <span class="tag">Redis</span>
                            <span class="tag">PostgreSQL</span>
                        </div>
                        <div class="actions">
                            <a class="btn btn-primary" href="http://localhost:8202" target="_blank" rel="noreferrer">Launch Project</a>
                            <a class="btn btn-secondary" href="http://localhost:8202/api/docs" target="_blank" rel="noreferrer">API Documentation</a>
                        </div>
                    </div>
                </article>

                <article class="project-card">
                    <div class="project-content">
                        <div class="project-header">
                            <div class="project-meta">
                                <span class="project-icon">📊</span>
                                <div class="project-info">
                                    <h2 class="project-title">SaaS Northstar Dashboard</h2>
                                    <div class="project-subtitle">Business Metrics & Analytics Platform</div>
                                </div>
                            </div>
                            <span class="status-chip">● Ready</span>
                        </div>
                        <p class="description">
                            Enterprise-grade SaaS metrics dashboard built with Next.js and Tailwind CSS. Track MRR, ARR, churn rate, 
                            and customer lifetime value with interactive charts and CSV data import capabilities.
                        </p>
                        <ul class="features-list">
                            <li>Real-time KPI cards with trend indicators</li>
                            <li>Interactive Chart.js visualizations</li>
                            <li>Flexible CSV data import workflow</li>
                            <li>Responsive design for all devices</li>
                        </ul>
                        <div class="tech-stack">
                            <span class="tag">Next.js</span>
                            <span class="tag">React</span>
                            <span class="tag">Tailwind CSS</span>
                            <span class="tag">Chart.js</span>
                        </div>
                        <div class="actions">
                            <a class="btn btn-primary" href="http://localhost:8303" target="_blank" rel="noreferrer">Launch Dashboard</a>
                            <a class="btn btn-secondary" href="http://localhost:8303/showcase" target="_blank" rel="noreferrer">View Showcase</a>
                        </div>
                    </div>
                </article>

                <article class="project-card">
                    <div class="project-content">
                        <div class="project-header">
                            <div class="project-meta">
                                <span class="project-icon">📄</span>
                                <div class="project-info">
                                    <h2 class="project-title">Doc Knowledge Forge</h2>
                                    <div class="project-subtitle">AI-Powered Document Management</div>
                                </div>
                            </div>
                            <span class="status-chip">● Ready</span>
                        </div>
                        <p class="description">
                            Intelligent document processing pipeline that converts PDF and DOCX files into searchable Markdown knowledge base. 
                            Features AI-powered summaries, tag management, full-text search, and multi-format export.
                        </p>
                        <ul class="features-list">
                            <li>Automated PDF/DOCX to Markdown conversion</li>
                            <li>AI-generated document summaries</li>
                            <li>Full-text search with tag filtering</li>
                            <li>Export to multiple formats (HTML, PDF, Markdown)</li>
                        </ul>
                        <div class="tech-stack">
                            <span class="tag">FastAPI</span>
                            <span class="tag">PyMuPDF</span>
                            <span class="tag">OpenAI</span>
                            <span class="tag">Tailwind CSS</span>
                        </div>
                        <div class="actions">
                            <a class="btn btn-primary" href="http://localhost:8404" target="_blank" rel="noreferrer">Launch Platform</a>
                            <a class="btn btn-secondary" href="http://localhost:8404/api/docs" target="_blank" rel="noreferrer">API Documentation</a>
                        </div>
                    </div>
                </article>

                <article class="project-card">
                    <div class="project-content">
                        <div class="project-header">
                            <div class="project-meta">
                                <span class="project-icon">♿</span>
                                <div class="project-info">
                                    <h2 class="project-title">A11y Component Atlas</h2>
                                    <div class="project-subtitle">Accessible React Component Library</div>
                                </div>
                            </div>
                            <span class="status-chip">● Ready</span>
                        </div>
                        <p class="description">
                            WCAG 2.1 AA compliant React component library with comprehensive accessibility testing. 
                            Includes Storybook documentation, audit score cards, and best practice guidelines for inclusive design.
                        </p>
                        <ul class="features-list">
                            <li>Fully accessible components with ARIA support</li>
                            <li>Built-in accessibility audit scoring</li>
                            <li>Keyboard navigation and screen reader tested</li>
                            <li>Interactive Storybook documentation</li>
                        </ul>
                        <div class="tech-stack">
                            <span class="tag">React</span>
                            <span class="tag">Storybook</span>
                            <span class="tag">TypeScript</span>
                            <span class="tag">Vitest</span>
                        </div>
                        <div class="actions">
                            <a class="btn btn-primary" href="http://localhost:8505" target="_blank" rel="noreferrer">Open Storybook</a>
                            <a class="btn btn-secondary" href="http://localhost:8505" target="_blank" rel="noreferrer">View Components</a>
                        </div>
                    </div>
                </article>

                <article class="project-card">
                    <div class="project-content">
                        <div class="project-header">
                            <div class="project-meta">
                                <span class="project-icon">📈</span>
                                <div class="project-info">
                                    <h2 class="project-title">Insight Viz Studio</h2>
                                    <div class="project-subtitle">Interactive Data Visualization Platform</div>
                                </div>
                            </div>
                            <span class="status-chip">● Ready</span>
                        </div>
                        <p class="description">
                            Transform raw CSV/Excel data into stunning interactive visualizations. Create geographic maps with marker clustering, 
                            advanced ECharts analytics, and export publication-ready graphics in PNG/PDF formats.
                        </p>
                        <ul class="features-list">
                            <li>Drag-and-drop CSV/Excel file upload</li>
                            <li>Interactive Folium maps with clustering</li>
                            <li>Advanced ECharts visualizations</li>
                            <li>High-quality PNG/PDF export options</li>
                        </ul>
                        <div class="tech-stack">
                            <span class="tag">FastAPI</span>
                            <span class="tag">Folium</span>
                            <span class="tag">ECharts</span>
                            <span class="tag">Pandas</span>
                        </div>
                        <div class="actions">
                            <a class="btn btn-primary" href="http://localhost:8606" target="_blank" rel="noreferrer">Launch Studio</a>
                            <a class="btn btn-secondary" href="http://localhost:8606/api/docs" target="_blank" rel="noreferrer">API Documentation</a>
                        </div>
                    </div>
                </article>
            </div>

            <footer>
                <p><strong>Main Portal</strong> hosted on Global Price Sentinel · Port 8101</p>
                <div class="link-row">
                    <a href="/api/health" target="_blank">System Health</a>
                    <a href="/api/summary" target="_blank">Price Summary</a>
                    <a href="/api/records" target="_blank">Data Records</a>
                </div>
                <small style="display:block;margin-top:20px;color:#868e96;">Professional Portfolio v1.0.0 · Built for Upwork & Fiverr Excellence</small>
            </footer>
        </div>
        <div class="toast" id="toast"></div>
        <script>
            const toast = document.getElementById('toast');
            function showToast(message) {
                toast.textContent = message;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 3200);
            }

            async function ensureReport() {
                const btn = document.querySelector('[data-generate-report]');
                if (!btn) return;
                btn.addEventListener('click', async () => {
                    btn.disabled = true;
                    btn.textContent = '生成中…';
                    try {
                        const res = await fetch('/api/report/generate?format=html', { method: 'POST' });
                        const data = await res.json();
                        if (data.report_url) {
                            window.open(data.report_url, '_blank');
                            showToast('最新报告已生成');
                        } else {
                            window.open('/reports/latest.html', '_blank');
                        }
                    } catch (err) {
                        showToast('生成失败，请稍后再试');
                    } finally {
                        btn.disabled = false;
                        btn.textContent = 'View Report';
                    }
                });
            }

            ensureReport();
        </script>
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
    format: str = Query("html", regex="^(html|csv|xlsx)$", description="报告格式")
):
    """生成报告"""
    try:
        if format == "html":
            report_path = ReportGenerator.generate_html_report(days=days)
        elif format == "xlsx":
            report_path = ReportGenerator.generate_excel_report(days=days)
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
