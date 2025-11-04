"""
Insight Viz Studio 主应用
"""
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from app.settings import settings
import random
from fastapi.templating import Jinja2Templates


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
app.mount(
    "/i18n",
    StaticFiles(directory=str(Path(__file__).resolve().parent / "i18n")),
    name="i18n",
)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

SUPPORTED_LANGS = {"en", "zh"}


def _detect_language(request: Request) -> str:
    query_lang = request.query_params.get("lang")
    if query_lang in SUPPORTED_LANGS:
        return query_lang
    cookie_lang = request.cookies.get("portfolio_lang")
    if cookie_lang in SUPPORTED_LANGS:
        return cookie_lang
    header_lang = request.headers.get("Accept-Language", "").lower()
    if header_lang.startswith("zh"):
        return "zh"
    return "en"


def _load_translations(lang: str) -> dict:
    translations_path = Path(__file__).resolve().parent / "i18n"
    file_path = translations_path / f"p6.{lang}.json"
    fallback_path = translations_path / "p6.en.json"
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return json.loads(fallback_path.read_text(encoding="utf-8"))


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    print(f"✓ {settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
    print(f"  - 监听地址: http://{settings.HOST}:{settings.PORT}")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Homepage with language switcher"""
    lang = _detect_language(request)
    data = _load_translations(lang)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "lang": lang,
            "translations": data,
            "version": settings.APP_VERSION,
        },
    )


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

