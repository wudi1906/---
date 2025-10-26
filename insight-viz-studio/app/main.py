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
    """主页"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Insight Viz Studio</title>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
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
            .card {
                background: white;
                border-radius: 16px;
                padding: 40px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .upload-area {
                border: 2px dashed #cbd5e1;
                border-radius: 12px;
                padding: 60px 20px;
                text-align: center;
                margin-bottom: 30px;
            }
            .btn {
                display: inline-block;
                padding: 12px 32px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                margin: 10px;
            }
            .btn:hover {
                background: #1d4ed8;
            }
            #chart { width: 100%; height: 500px; margin-top: 30px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📈 Insight Viz Studio</h1>
                <p style="font-size: 1.25rem; opacity: 0.95;">数据可视化工具</p>
            </div>

            <div class="card">
                <h2 style="margin-bottom: 20px;">上传数据文件</h2>
                <div class="upload-area">
                    <div style="font-size: 3rem; margin-bottom: 20px;">📊</div>
                    <p style="color: #64748b; margin-bottom: 20px;">
                        上传 CSV、JSON 或 Excel 文件<br/>
                        自动生成交互式图表
                    </p>
                    <input type="file" id="fileInput" accept=".csv,.json,.xlsx,.xls">
                    <button onclick="document.getElementById('fileInput').click()" class="btn">
                        选择文件
                    </button>
                </div>
                
                <div id="chart"></div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/api/docs" class="btn">📘 API 文档</a>
                    <a href="/api/datasets" class="btn">📁 数据集列表</a>
                </div>
            </div>
        </div>

        <script>
            const chart = echarts.init(document.getElementById('chart'));
            
            // 示例图表
            const option = {
                title: { text: '示例数据可视化', left: 'center' },
                tooltip: { trigger: 'axis' },
                xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] },
                yAxis: { type: 'value' },
                series: [{
                    data: [820, 932, 901, 934, 1290, 1330, 1320],
                    type: 'line',
                    smooth: true,
                    itemStyle: { color: '#2563eb' }
                }]
            };
            chart.setOption(option);
            
            // 文件上传处理
            document.getElementById('fileInput').addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file) return;
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    alert(`文件上传成功！行数: ${result.rows}, 列数: ${result.columns}`);
                } catch (error) {
                    alert('上传失败: ' + error.message);
                }
            });
            
            window.addEventListener('resize', () => chart.resize());
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

