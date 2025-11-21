"""
Insight Viz Studio 主应用
"""
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster

from app.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="数据可视化工具 - CSV/JSON 上传 → ECharts 图表/地图 → 导出",
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
        <title>Insight Viz Studio - Data Visualization</title>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
            .brand-gradient { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); }
            #map-frame { width: 100%; height: 500px; border: none; border-radius: 12px; }
        </style>
    </head>
    <body class="bg-slate-50 text-slate-800">
        
        <!-- Header -->
        <header class="brand-gradient text-white py-6 shadow-lg mb-8">
            <div class="container mx-auto px-6 flex justify-between items-center">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">📈</span>
                    <div>
                        <h1 class="text-2xl font-bold">Insight Viz Studio</h1>
                        <p class="text-blue-100 text-sm opacity-90">Turn CSVs into Interactive Charts & Maps</p>
                    </div>
                </div>
                <div>
                    <a href="/api/docs" class="bg-white/20 hover:bg-white/30 transition px-4 py-2 rounded-lg text-sm font-medium backdrop-blur-sm">API Docs</a>
                </div>
            </div>
        </header>

        <div class="container mx-auto px-6">
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                <!-- Left Panel: Controls -->
                <div class="lg:col-span-1 space-y-6">
                    
                    <!-- Upload Card -->
                    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                        <h2 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <span class="bg-blue-100 text-blue-600 p-1.5 rounded">1</span> Upload Data
                        </h2>
                        
                        <div class="border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:bg-slate-50 transition cursor-pointer" onclick="document.getElementById('fileInput').click()">
                            <div class="text-4xl mb-2">📄</div>
                            <p class="text-slate-500 text-sm mb-2">Click to upload CSV/Excel</p>
                            <p class="text-xs text-slate-400">Supports .csv, .xlsx (Max 10MB)</p>
                        </div>
                        <input type="file" id="fileInput" accept=".csv,.json,.xlsx,.xls" class="hidden">
                        
                        <div id="fileInfo" class="hidden mt-4 p-3 bg-green-50 border border-green-100 rounded-lg flex items-center gap-3">
                            <div class="text-green-600">✅</div>
                            <div class="text-sm overflow-hidden">
                                <div id="fileName" class="font-medium text-green-900 truncate">data.csv</div>
                                <div id="fileStats" class="text-green-700 text-xs">100 rows • 5 cols</div>
                            </div>
                        </div>
                    </div>

                    <!-- Configuration Card -->
                    <div id="configCard" class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 opacity-50 pointer-events-none transition-opacity">
                        <h2 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <span class="bg-blue-100 text-blue-600 p-1.5 rounded">2</span> Configure
                        </h2>
                        
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-1">Viz Type</label>
                                <div class="grid grid-cols-2 gap-2">
                                    <button onclick="setVizType('chart')" id="btn-chart" class="viz-type-btn px-3 py-2 rounded-lg border text-sm font-medium bg-blue-50 border-blue-200 text-blue-700">Chart</button>
                                    <button onclick="setVizType('map')" id="btn-map" class="viz-type-btn px-3 py-2 rounded-lg border text-sm font-medium border-slate-200 text-slate-600 hover:bg-slate-50">Map</button>
                                </div>
                            </div>

                            <!-- Chart Config -->
                            <div id="chartConfig" class="space-y-3">
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Chart Type</label>
                                    <select id="chartType" class="w-full rounded-lg border-slate-300 text-sm">
                                        <option value="bar">Bar Chart</option>
                                        <option value="line">Line Chart</option>
                                        <option value="pie">Pie Chart</option>
                                        <option value="scatter">Scatter Plot</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">X Axis (Category)</label>
                                    <select id="xAxis" class="w-full rounded-lg border-slate-300 text-sm"></select>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Y Axis (Value)</label>
                                    <select id="yAxis" class="w-full rounded-lg border-slate-300 text-sm"></select>
                                </div>
                            </div>

                            <!-- Map Config -->
                            <div id="mapConfig" class="space-y-3 hidden">
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Map Style</label>
                                    <select id="mapType" class="w-full rounded-lg border-slate-300 text-sm">
                                        <option value="heatmap">Heatmap (Density)</option>
                                        <option value="markers">Markers (Locations)</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Latitude Column</label>
                                    <select id="latCol" class="w-full rounded-lg border-slate-300 text-sm"></select>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Longitude Column</label>
                                    <select id="lonCol" class="w-full rounded-lg border-slate-300 text-sm"></select>
                                </div>
                            </div>
                            
                            <button onclick="generateViz()" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium shadow-md hover:shadow-lg transition-all">
                                ✨ Generate Visualization
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Right Panel: Visualization -->
                <div class="lg:col-span-2">
                    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 min-h-[600px] flex flex-col">
                        <div class="flex justify-between items-center mb-4">
                            <h2 class="text-lg font-bold text-slate-800">Preview</h2>
                            <div class="flex gap-2">
                                <button class="text-sm text-slate-500 hover:text-blue-600">Download PNG</button>
                                <button class="text-sm text-slate-500 hover:text-blue-600">Export JSON</button>
                            </div>
                        </div>
                        
                        <div id="vizContainer" class="flex-grow bg-slate-50 rounded-lg border border-slate-100 relative flex items-center justify-center overflow-hidden">
                            <div id="placeholder" class="text-center text-slate-400">
                                <div class="text-5xl mb-3">📊</div>
                                <p>Upload data and configure settings<br>to see visualization</p>
                            </div>
                            
                            <!-- Chart Container -->
                            <div id="chart" class="w-full h-full hidden p-4"></div>
                            
                            <!-- Map Container (Iframe) -->
                            <iframe id="mapFrame" class="w-full h-full hidden border-0"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let currentFile = null;
            let currentColumns = [];
            let chartInstance = null;

            function setVizType(type) {
                // UI Toggle
                document.querySelectorAll('.viz-type-btn').forEach(b => {
                    b.classList.remove('bg-blue-50', 'border-blue-200', 'text-blue-700');
                    b.classList.add('border-slate-200', 'text-slate-600');
                });
                const activeBtn = document.getElementById(`btn-${type}`);
                activeBtn.classList.add('bg-blue-50', 'border-blue-200', 'text-blue-700');
                activeBtn.classList.remove('border-slate-200', 'text-slate-600');

                // Config Toggle
                if (type === 'chart') {
                    document.getElementById('chartConfig').classList.remove('hidden');
                    document.getElementById('mapConfig').classList.add('hidden');
                } else {
                    document.getElementById('chartConfig').classList.add('hidden');
                    document.getElementById('mapConfig').classList.remove('hidden');
                }
            }

            // File Upload
            document.getElementById('fileInput').addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file) return;
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const res = await fetch('/api/upload', { method: 'POST', body: formData });
                    const data = await res.json();
                    
                    if (data.success) {
                        currentFile = data.filename;
                        currentColumns = data.column_names;
                        
                        // Update UI
                        document.getElementById('fileName').textContent = data.filename;
                        document.getElementById('fileStats').textContent = `${data.rows} rows • ${data.columns} cols`;
                        document.getElementById('fileInfo').classList.remove('hidden');
                        document.getElementById('configCard').classList.remove('opacity-50', 'pointer-events-none');
                        
                        // Populate Selects
                        const selects = ['xAxis', 'yAxis', 'latCol', 'lonCol'];
                        selects.forEach(id => {
                            const sel = document.getElementById(id);
                            sel.innerHTML = currentColumns.map(c => `<option value="${c}">${c}</option>`).join('');
                        });

                        // Auto-detect Lat/Lon
                        const latMatch = currentColumns.find(c => c.toLowerCase().includes('lat'));
                        const lonMatch = currentColumns.find(c => c.toLowerCase().includes('lon') || c.toLowerCase().includes('lng'));
                        if (latMatch) document.getElementById('latCol').value = latMatch;
                        if (lonMatch) document.getElementById('lonCol').value = lonMatch;
                    }
                } catch (err) {
                    alert('Upload failed');
                }
            });

            async function generateViz() {
                const isMap = !document.getElementById('mapConfig').classList.contains('hidden');
                document.getElementById('placeholder').classList.add('hidden');
                
                if (isMap) {
                    // Generate Map
                    document.getElementById('chart').classList.add('hidden');
                    const frame = document.getElementById('mapFrame');
                    frame.classList.remove('hidden');
                    
                    const lat = document.getElementById('latCol').value;
                    const lon = document.getElementById('lonCol').value;
                    const type = document.getElementById('mapType').value;
                    
                    frame.src = `/api/map/generate?filename=${currentFile}&lat_col=${lat}&lon_col=${lon}&map_type=${type}`;
                    
                } else {
                    // Generate Chart
                    document.getElementById('mapFrame').classList.add('hidden');
                    const div = document.getElementById('chart');
                    div.classList.remove('hidden');
                    
                    if (chartInstance) chartInstance.dispose();
                    chartInstance = echarts.init(div);
                    
                    const type = document.getElementById('chartType').value;
                    const x = document.getElementById('xAxis').value;
                    const y = document.getElementById('yAxis').value;
                    
                    const res = await fetch(`/api/chart?filename=${currentFile}&chart_type=${type}&x_column=${x}&y_column=${y}`);
                    const option = await res.json();
                    chartInstance.setOption(option);
                    chartInstance.resize();
                }
            }
            
            window.addEventListener('resize', () => {
                if (chartInstance) chartInstance.resize();
            });
        </script>
    </body>
    </html>
    """


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


@app.get("/api/map/generate")
async def generate_map(
    filename: str,
    lat_col: str,
    lon_col: str,
    map_type: str = "heatmap"
):
    """生成交互式地图 HTML"""
    file_path = settings.UPLOAD_DIR / filename
    if not file_path.exists():
        return HTMLResponse("<h3>File not found</h3>")

    try:
        # 读取数据
        file_ext = file_path.suffix.lower()
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
        elif file_ext == '.json':
            df = pd.read_json(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            return HTMLResponse("<h3>Unsupported file format</h3>")

        # 验证列
        if lat_col not in df.columns or lon_col not in df.columns:
            return HTMLResponse(f"<h3>Columns {lat_col}/{lon_col} not found</h3>")

        # 清洗数据 (去除无效经纬度)
        df = df.dropna(subset=[lat_col, lon_col])
        # 简单的范围验证
        df = df[
            (df[lat_col] >= -90) & (df[lat_col] <= 90) &
            (df[lon_col] >= -180) & (df[lon_col] <= 180)
        ]
        
        if len(df) == 0:
            return HTMLResponse("<h3>No valid location data found</h3>")

        # 计算中心点
        center_lat = df[lat_col].mean()
        center_lon = df[lon_col].mean()

        # 创建地图
        m = folium.Map(location=[center_lat, center_lon], zoom_start=4, tiles="CartoDB positron")

        if map_type == "heatmap":
            # 热力图
            data = df[[lat_col, lon_col]].values.tolist()
            HeatMap(data, radius=15).add_to(m)
        else:
            # 标记聚合
            marker_cluster = MarkerCluster().add_to(m)
            # 限制最多显示 1000 个点以保证性能
            for idx, row in df.head(1000).iterrows():
                folium.Marker(
                    location=[row[lat_col], row[lon_col]],
                    popup=f"Row {idx}",
                ).add_to(marker_cluster)

        # 返回 HTML
        return HTMLResponse(m.get_root().render())

    except Exception as e:
        return HTMLResponse(f"<h3>Error generating map: {str(e)}</h3>")


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
                "type": chart_type,
                "itemStyle": {"color": "#3b82f6"},
                "areaStyle": {"opacity": 0.1} if chart_type == 'line' else None
            }],
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True}
        }
    elif chart_type == 'pie':
        option = {
            "title": {"text": "Pie Chart"},
            "tooltip": {"trigger": "item"},
            "series": [{
                "type": "pie",
                "radius": ['40%', '70%'],
                "data": [{"name": str(row[x_column]), "value": row[y_column]} 
                         for _, row in df.head(10).iterrows()]
            }]
        }
    elif chart_type == 'scatter':
        option = {
             "title": {"text": "Scatter Plot"},
             "tooltip": {"trigger": "item"},
             "xAxis": {},
             "yAxis": {},
             "series": [{
                 "symbolSize": 10,
                 "data": df[[x_column, y_column]].values.tolist(),
                 "type": "scatter",
                 "itemStyle": {"color": "#ef4444"}
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

