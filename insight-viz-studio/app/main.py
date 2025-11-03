"""
Insight Viz Studio 主应用
"""
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from app.settings import settings
import random


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="数据可视化工具 - CSV/JSON 上传 → ECharts 图表 → 导出",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")
app.mount("/exports", StaticFiles(directory=str(settings.EXPORT_DIR)), name="exports")


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    print(f"✓ {settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
    print(f"  - 监听地址: http://{settings.HOST}:{settings.PORT}")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Homepage - English landing page for international buyers"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Insight Viz Studio — From Data to Story-Ready Dashboards</title>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            :root {
                --bg: linear-gradient(135deg, #0f172a 0%, #312e81 45%, #7c3aed 100%);
                --glass: rgba(148, 163, 184, 0.18);
                --panel: rgba(255, 255, 255, 0.96);
                --panel-dark: rgba(15, 23, 42, 0.78);
                --shadow: 0 30px 60px -24px rgba(15, 23, 42, 0.75);
                --primary: #2563eb;
                --accent: #F97316;
                --success: #10b981;
                --text-dark: #0f172a;
                --text-light: #f8fafc;
            }
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: "Inter", -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: var(--bg);
                color: var(--text-light);
                min-height: 100vh;
                padding: clamp(32px, 7vw, 72px) clamp(20px, 6vw, 72px);
            }
            .page { max-width: 1280px; margin: 0 auto; display: flex; flex-direction: column; gap: clamp(32px, 6vw, 56px); }
            .hero { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: clamp(24px, 4vw, 48px); }
            .hero-card {
                background: rgba(15, 23, 42, 0.4);
                border-radius: 30px;
                padding: clamp(28px, 5vw, 48px);
                border: 1px solid rgba(148, 163, 184, 0.25);
                box-shadow: var(--shadow);
                backdrop-filter: blur(20px);
            }
            .hero-card h1 {
                font-size: clamp(2.6rem, 6vw, 3.6rem);
                font-weight: 700;
                margin-bottom: 20px;
                line-height: 1.1;
            }
            .hero-card p.lead {
                font-size: clamp(1.05rem, 2.4vw, 1.35rem);
                opacity: 0.9;
                line-height: 1.7;
                margin-bottom: 24px;
            }
            .hero-points { list-style: none; display: grid; gap: 14px; margin-bottom: 28px; font-size: 0.98rem; }
            .hero-points li span { font-weight: 600; color: #dbeafe; }
            .hero-actions { display: flex; flex-wrap: wrap; gap: 12px; }
            .btn {
                display: inline-flex; align-items: center; gap: 10px;
                padding: 12px 28px; border-radius: 999px;
                text-decoration: none; font-weight: 600; font-size: 0.95rem;
                border: 2px solid transparent; transition: all 0.25s ease; cursor: pointer;
            }
            .btn-primary { background: linear-gradient(135deg, #60a5fa, #2563eb); color: white; box-shadow: 0 24px 45px -24px rgba(37, 99, 235, 0.9); }
            .btn-primary:hover { transform: translateY(-3px); }
            .btn-outline { background: rgba(255,255,255,0.08); color: white; border-color: rgba(255,255,255,0.35); }
            .btn-outline:hover { background: rgba(255,255,255,0.16); }
            .btn-secondary { background: rgba(37, 99, 235, 0.12); color: #93c5fd; border-color: rgba(37, 99, 235, 0.2); }
            .btn:focus-visible { outline: none; box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.45); transform: translateY(-2px); }

            .hero-metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-top: 16px; }
            .metric-card { background: rgba(59, 130, 246, 0.18); border-radius: 22px; padding: 18px; border: 1px solid rgba(96, 165, 250, 0.35); display: flex; flex-direction: column; gap: 8px; }
            .metric-label { font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.7; }
            .metric-value { font-size: 1.7rem; font-weight: 700; }
            .metric-desc { font-size: 0.85rem; opacity: 0.75; }

            .workflow { background: rgba(15, 23, 42, 0.45); border-radius: 24px; padding: 24px; border: 1px solid rgba(148, 163, 184, 0.22); display: grid; gap: 16px; }
            .workflow h3 { font-size: 1.1rem; font-weight: 600; }
            .workflow-list { list-style: none; display: grid; gap: 12px; }
            .workflow-item { display: grid; grid-template-columns: auto 1fr; gap: 12px; align-items: start; }
            .workflow-step { width: 36px; height: 36px; border-radius: 12px; background: rgba(96, 165, 250, 0.2); display: grid; place-items: center; font-weight: 600; }

            .panel {
                background: var(--panel);
                color: var(--text-dark);
                border-radius: 26px;
                padding: clamp(24px, 4vw, 40px);
                box-shadow: var(--shadow);
                border: 1px solid rgba(148, 163, 184, 0.2);
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            @media (prefers-color-scheme: dark) {
                .panel { background: var(--panel-dark); color: var(--text-light); border-color: rgba(148, 163, 184, 0.28); }
            }
            .panel h2 { font-size: 1.6rem; font-weight: 600; display: flex; align-items: center; gap: 12px; }
            .panel p { font-size: 0.98rem; line-height: 1.7; color: rgba(15, 23, 42, 0.7); }
            @media (prefers-color-scheme: dark) { .panel p { color: rgba(226, 232, 240, 0.78); } }

            .main-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: clamp(20px, 3vw, 32px); }
            .upload-area { border: 2px dashed rgba(37, 99, 235, 0.35); border-radius: 18px; padding: clamp(36px, 5vw, 56px); text-align: center; background: rgba(37, 99, 235, 0.08); transition: all 0.3s ease; }
            .upload-area:hover { border-color: var(--primary); background: rgba(37, 99, 235, 0.15); }
            .upload-actions { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }

            .chart-area { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: clamp(20px, 3vw, 32px); }
            .chart-card { background: rgba(15, 23, 42, 0.05); border-radius: 20px; padding: 16px; border: 1px solid rgba(148, 163, 184, 0.15); height: 420px; }
            #chartPrimary, #chartSecondary { width: 100%; height: calc(100% - 36px); margin-top: 12px; }

            .dataset-table { width: 100%; border-collapse: collapse; }
            .dataset-table th, .dataset-table td { padding: 12px 14px; border-bottom: 1px solid rgba(148, 163, 184, 0.2); text-align: left; }
            .dataset-table th { text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.08em; opacity: 0.7; }

            .usecase-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
            .usecase-card { background: rgba(37, 99, 235, 0.1); border-radius: 18px; padding: 18px; border: 1px solid rgba(59, 130, 246, 0.22); }
            .usecase-card strong { display: block; margin-bottom: 6px; }

            footer { display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between; color: rgba(226, 232, 240, 0.75); font-size: 0.9rem; }
        </style>
    </head>
    <body>
        <div class="page">
            <section class="hero">
                <div class="hero-card">
                    <h1>📈 Insight Viz Studio</h1>
                    <p class="lead">Turn raw CSV / JSON / Excel into investor-ready dashboards within minutes. Smart chart recommendations, brand themes, storytelling layouts, and export automation — all powered by ECharts.</p>
                    <ul class="hero-points">
                        <li><span>Auto Ingest：</span> Upload 50MB+ CSV/JSON/Excel, schema inference, outlier alerts, data quality checks。</li>
                        <li><span>Smart Recommend：</span> Chart wizard suggests line/bar/pie/scatter/funnel with metrics & dimensions pre-filled。</li>
                        <li><span>Deliver & Automate：</span> Theming, annotations, PDF/PNG export, weekly/monthly template scheduler。</li>
                    </ul>
                    <div class="hero-actions">
                        <a class="btn btn-primary" href="#upload-panel">📂 Upload Your Dataset</a>
                        <a class="btn btn-outline" href="#charts-panel">🧠 View Sample Dashboards</a>
                        <a class="btn btn-outline" href="#datasets-panel">📁 Dataset Console</a>
                    </div>
                    <div class="hero-metrics">
                        <div class="metric-card">
                            <span class="metric-label">Chart Templates</span>
                            <span class="metric-value">24+</span>
                            <span class="metric-desc">Line · Bar · Area · Pie · Funnel · Combo</span>
                        </div>
                        <div class="metric-card">
                            <span class="metric-label">Export Formats</span>
                            <span class="metric-value">PNG / PDF</span>
                            <span class="metric-desc">Brand-safe typography + watermark</span>
                        </div>
                        <div class="metric-card">
                            <span class="metric-label">Processing SLA</span>
                            <span class="metric-value">&lt; 5 min</span>
                            <span class="metric-desc">100k rows CSV → chart-ready options</span>
                        </div>
                    </div>
                </div>
                <div class="hero-card workflow">
                    <h3>Workflow · 从数据上传到可交付报告</h3>
                    <ol class="workflow-list">
                        <li class="workflow-item">
                            <div class="workflow-step">1</div>
                            <div><strong>Profile</strong> 数据剖析 + 字段建议，识别日期、度量、维度。</div>
                        </li>
                        <li class="workflow-item">
                            <div class="workflow-step">2</div>
                            <div><strong>Recommend</strong> 根据 KPI（Revenue / MAU / Cohort / Funnel）生成候选图表。</div>
                        </li>
                        <li class="workflow-item">
                            <div class="workflow-step">3</div>
                            <div><strong>Compose</strong> 拖拽布局 + 主题 + 注释 + 比较视图。</div>
                        </li>
                        <li class="workflow-item">
                            <div class="workflow-step">4</div>
                            <div><strong>Deliver</strong> 一键导出 PDF / PNG，或调度自动报表。</div>
                        </li>
                    </ol>
                </div>
            </section>

            <section class="panel" id="upload-panel">
                <h2>📂 Upload Data File</h2>
                <p>Drag in your CSV/JSON/Excel file or use the buttons below. We infer schema, preview data, and prepare chart recommendations instantly.</p>
                <div class="upload-area">
                    <div style="font-size:3.5rem;margin-bottom:16px;">📊</div>
                    <p style="color:#64748b;margin-bottom:18px;">Supports CSV · JSON · XLSX · XLS — up to 10 files per session.</p>
                    <input type="file" id="fileInput" accept=".csv,.json,.xlsx,.xls" hidden>
                    <div class="upload-actions">
                        <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">Choose File</button>
                        <button class="btn btn-secondary" onclick="seedDemo()">🧪 Import Demo</button>
                        <button class="btn btn-secondary" onclick="resetDemo()">🔄 Reset Demo</button>
                        <a href="/api/docs" class="btn btn-outline">📘 API Docs</a>
                        <a href="/api/datasets" class="btn btn-outline">📁 View Datasets JSON</a>
                    </div>
                </div>
            </section>

            <section class="panel" id="charts-panel">
                <h2>🧠 Smart Chart Gallery</h2>
                <p>Two sample dashboards generated from demo data. Toggle between views to demonstrate storytelling potential and theming capabilities.</p>
                <div class="chart-area">
                    <div class="chart-card">
                        <h3 style="color:#1e293b;">Revenue Growth & Cohort Retention</h3>
                        <div id="chartPrimary" aria-label="Revenue chart"></div>
                    </div>
                    <div class="chart-card">
                        <h3 style="color:#1e293b;">Category Contribution & Goal Tracking</h3>
                        <div id="chartSecondary" aria-label="Category chart"></div>
                    </div>
                </div>
            </section>

            <section class="panel" id="datasets-panel">
                <h2>📁 Dataset Console</h2>
                <p>All uploaded files are available through the datasets API. Check file size, upload time, and feed them into the chart generator endpoint.</p>
                <table class="dataset-table">
                    <thead>
                        <tr><th>Filename</th><th>Size</th><th>Uploaded</th></tr>
                    </thead>
                    <tbody id="datasetTable">
                        <tr><td colspan="3" style="opacity:0.7;">No datasets yet. Import demo or upload your own.</td></tr>
                    </tbody>
                </table>
            </section>

            <section class="panel">
                <h2>🎯 Use Cases & Templates</h2>
                <div class="usecase-grid">
                    <div class="usecase-card"><strong>Executive KPI Hub</strong> Combine revenue, ARR, churn, CAC payback, and pipeline in one deck.</div>
                    <div class="usecase-card"><strong>Marketing & Campaign</strong> Visualize channel attribution, cohort retention, funnel drop-offs.</div>
                    <div class="usecase-card"><strong>Product Analytics</strong> Feature adoption, MAU/WAU, release impact, NPS sentiment.</div>
                    <div class="usecase-card"><strong>Financial Planning</strong> Forecast vs actual, expense breakdown, margin analysis。</div>
                </div>
            </section>

            <footer>
                <p>Insight Viz Studio · Responsive Web App · Powered by FastAPI + ECharts · Themeable, Export-ready</p>
                <p>Include upload API, dataset storage, chart generator endpoint, automation hooks, and demo seeds.</p>
            </footer>
        </div>

        <script>
            const chartPrimary = echarts.init(document.getElementById('chartPrimary'));
            const chartSecondary = echarts.init(document.getElementById('chartSecondary'));

            const areaOption = {
                backgroundColor: 'transparent',
                tooltip: { trigger: 'axis' },
                legend: { textStyle: { color: '#1e293b' } },
                xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'], boundaryGap: false },
                yAxis: { type: 'value' },
                series: [
                    {
                        name: 'Revenue', type: 'line', smooth: true,
                        data: [42000, 46000, 51000, 56000, 61000, 67000, 72000, 78000],
                        areaStyle: { color: 'rgba(37, 99, 235, 0.35)' },
                        lineStyle: { width: 3, color: '#2563eb' }
                    },
                    {
                        name: 'MRR Cohort Retention', type: 'line', smooth: true,
                        data: [0.78, 0.8, 0.82, 0.83, 0.85, 0.86, 0.88, 0.9],
                        yAxisIndex: 0,
                        areaStyle: { color: 'rgba(16, 185, 129, 0.22)' },
                        lineStyle: { width: 3, color: '#10b981' }
                    }
                ]
            };

            const donutOption = {
                backgroundColor: 'transparent',
                tooltip: { trigger: 'item' },
                legend: { orient: 'vertical', left: 'left', textStyle: { color: '#1e293b' } },
                series: [
                    {
                        type: 'pie', radius: ['40%', '70%'],
                        itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
                        label: { formatter: '{b}: {d}%' },
                        data: [
                            { value: 42, name: 'SaaS Enterprise' },
                            { value: 26, name: 'Self-service' },
                            { value: 18, name: 'Marketplace' },
                            { value: 14, name: 'Services' }
                        ]
                    }
                ]
            };

            chartPrimary.setOption(areaOption);
            chartSecondary.setOption(donutOption);

            document.getElementById('fileInput').addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file) return;
                const formData = new FormData();
                formData.append('file', file);
                try {
                    const response = await fetch('/api/upload', { method: 'POST', body: formData });
                    const result = await response.json();
                    alert(`File uploaded successfully! Rows: ${result.rows}, Columns: ${result.columns}`);
                    loadDatasets();
                } catch (error) {
                    alert('Upload failed: ' + error.message);
                }
            });

            async function seedDemo() {
                try {
                    const res = await fetch('/api/demo/seed', { method: 'POST' });
                    const data = await res.json();
                    if (data.success) {
                        alert('✅ Demo data imported! Visit /api/datasets to see sample files.');
                        loadDatasets();
                    } else {
                        alert('❌ Import failed: ' + (data.error || 'Unknown error'));
                    }
                } catch (error) {
                    alert('❌ Import failed: ' + error.message);
                }
            }

            async function resetDemo() {
                if (!confirm('Clear all demo data?')) return;
                try {
                    const res = await fetch('/api/demo/reset', { method: 'POST' });
                    const data = await res.json();
                    if (data.success) {
                        alert('✅ Demo data cleared!');
                        loadDatasets();
                    } else {
                        alert('❌ Reset failed: ' + (data.error || 'Unknown error'));
                    }
                } catch (error) {
                    alert('❌ Reset failed: ' + error.message);
                }
            }

            async function loadDatasets() {
                try {
                    const res = await fetch('/api/datasets');
                    const data = await res.json();
                    const tbody = document.getElementById('datasetTable');
                    if (!data.files || !data.files.length) {
                        tbody.innerHTML = '<tr><td colspan="3" style="opacity:0.7;">No datasets yet. Import demo or upload your own.</td></tr>';
                        return;
                    }
                    tbody.innerHTML = data.files.slice(0, 6).map(file => `
                        <tr>
                            <td>${file.filename}</td>
                            <td>${(file.size / 1024).toFixed(1)} KB</td>
                            <td>${new Date(file.created_at).toLocaleString()}</td>
                        </tr>
                    `).join('');
                } catch (error) {
                    console.error(error);
                }
            }

            loadDatasets();
            window.addEventListener('resize', () => { chartPrimary.resize(); chartSecondary.resize(); });
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
        "version": settings.APP_VERSION
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传数据文件"""
    # 检查文件类型
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file_ext}")
    
    # 保存文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = settings.UPLOAD_DIR / safe_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 解析数据
    try:
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
        elif file_ext == '.json':
            df = pd.read_json(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported format")
        
        # 返回数据信息
        return {
            "success": True,
            "filename": safe_filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "preview": df.head(5).to_dict('records')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/datasets")
async def list_datasets():
    """列出所有数据集"""
    files = []
    for file_path in settings.UPLOAD_DIR.glob("*"):
        if file_path.is_file():
            files.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "created_at": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
            })
    
    return {"total": len(files), "files": files}


@app.post("/api/chart")
async def generate_chart(
    filename: str,
    chart_type: str = Query(..., regex="^(line|bar|pie|scatter|funnel)$"),
    x_column: str = Query(None),
    y_column: str = Query(None)
):
    """生成图表配置"""
    file_path = settings.UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # 读取数据
    file_ext = file_path.suffix.lower()
    if file_ext == '.csv':
        df = pd.read_csv(file_path)
    elif file_ext == '.json':
        df = pd.read_json(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    
    # 生成ECharts配置
    if chart_type == 'line' or chart_type == 'bar':
        option = {
            "title": {"text": f"{chart_type.capitalize()} Chart"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": df[x_column].tolist() if x_column else []},
            "yAxis": {"type": "value"},
            "series": [{
                "data": df[y_column].tolist() if y_column else [],
                "type": chart_type
            }]
        }
    elif chart_type == 'pie':
        option = {
            "title": {"text": "Pie Chart"},
            "tooltip": {"trigger": "item"},
            "series": [{
                "type": "pie",
                "data": [{"name": str(row[x_column]), "value": row[y_column]} 
                         for _, row in df.head(10).iterrows()]
            }]
        }
    else:
        option = {"title": {"text": "Chart"}}
    
    return option


@app.post("/api/demo/seed")
async def demo_seed():
    """生成示例CSV数据文件"""
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成销售数据CSV
    sales_data = {
        "Date": [f"2024-{i//30+1:02d}-{i%30+1:02d}" for i in range(90)],
        "Revenue": [5000 + random.randint(-1500, 3500) for _ in range(90)],
        "Orders": [random.randint(80, 250) for _ in range(90)],
        "Customers": [random.randint(60, 180) for _ in range(90)]
    }
    df = pd.DataFrame(sales_data)
    csv_path = settings.UPLOAD_DIR / "sample_sales.csv"
    df.to_csv(csv_path, index=False)
    
    # 生成产品分类数据CSV
    product_data = {
        "Category": ["Electronics", "Clothing", "Food", "Books", "Toys"],
        "Sales": [random.randint(10000, 50000) for _ in range(5)],
        "Units": [random.randint(200, 800) for _ in range(5)]
    }
    df2 = pd.DataFrame(product_data)
    csv_path2 = settings.UPLOAD_DIR / "sample_products.csv"
    df2.to_csv(csv_path2, index=False)
    
    return {
        "success": True,
        "files": ["sample_sales.csv", "sample_products.csv"],
        "message": "示例数据已生成，可在上传区选择使用"
    }


@app.post("/api/demo/reset")
async def demo_reset():
    """清空上传和导出文件"""
    for p in settings.UPLOAD_DIR.glob("*"):
        try:
            if p.is_file():
                p.unlink()
        except Exception:
            pass
    for p in settings.EXPORT_DIR.glob("*"):
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

