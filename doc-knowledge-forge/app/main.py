"""
Doc Knowledge Forge 主应用
"""
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.settings import settings
from app.models import (
    init_db, get_db, Document, DocumentResponse,
    DocumentCreate, SearchResult, DocumentStats
)
from app.parser import parse_document, DocumentParser


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="文档转知识库系统 - PDF/DOCX → Markdown → 检索",
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
app.mount("/outputs", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="outputs")

templates_dir = Path(__file__).resolve().parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

# 模板目录
# 模板目录
templates_dir = Path(__file__).resolve().parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    init_db()
    print(f"✓ {settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
    print(f"  - 监听地址: http://{settings.HOST}:{settings.PORT}")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/demo/seed")
async def demo_seed(db: Session = Depends(get_db)):
    """导入示例数据"""
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    samples = [
        ("Company_Handbook.pdf", "公司员工手册，包含行为准则与福利政策。", "txt"),
        ("API_Guide.docx", "REST API 使用指南，介绍鉴权与错误码。", "txt"),
        ("Marketing_Plan.md", "市场推广计划，季度目标与渠道策略。", "md"),
        ("Q3_Report.pdf", "第三季度业务报告，营收与增长数据。", "txt"),
        ("Product_FAQ.txt", "产品常见问题，安装配置与故障排除。", "txt"),
    ]

    created_ids: List[int] = []
    for original_name, text, ext in samples:
        safe_filename = original_name
        file_ext = ext
        file_path = settings.UPLOAD_DIR / safe_filename
        file_path.write_text(text, encoding="utf-8")

        parsed = parse_document(str(file_path), file_ext)
        keywords = DocumentParser.extract_keywords(parsed.get("text", ""))
        markdown_content = DocumentParser.text_to_markdown(
            parsed.get("text", ""), parsed.get("title")
        )

        md_filename = file_path.stem + ".md"
        md_path = settings.OUTPUT_DIR / md_filename
        md_path.write_text(markdown_content, encoding="utf-8")

        doc = Document(
            filename=safe_filename,
            original_name=original_name,
            file_type=file_ext,
            file_path=str(file_path),
            markdown_path=str(md_path),
            title=parsed.get("title") or file_path.stem,
            content=parsed.get("text", "")[:10000],
            tags=",".join(keywords),
            file_size=file_path.stat().st_size,
            page_count=parsed.get("page_count", 0),
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        created_ids.append(doc.id)

    return {"success": True, "seeded": len(created_ids), "document_ids": created_ids}


@app.post("/api/demo/reset")
async def demo_reset(db: Session = Depends(get_db)):
    """清空示例数据与生成文件"""
    # 清库
    docs = db.query(Document).all()
    for d in docs:
        db.delete(d)
    db.commit()

    # 清文件
    for p in settings.UPLOAD_DIR.glob("*"):
        try:
            if p.is_file():
                p.unlink()
        except Exception:
            pass
    for p in settings.OUTPUT_DIR.glob("*"):
        try:
            if p.is_file():
                p.unlink()
        except Exception:
            pass

    return {"success": True}


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/upload")
async def upload_documents(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """上传文档"""
    uploaded_docs = []
    
    for file in files:
        # 检查文件类型
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            continue
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = settings.UPLOAD_DIR / safe_filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 解析文档
        parsed = parse_document(str(file_path), file_ext)
        
        # 提取关键词
        keywords = DocumentParser.extract_keywords(parsed.get("text", ""))
        
        # 转换为Markdown
        markdown_content = DocumentParser.text_to_markdown(
            parsed.get("text", ""),
            parsed.get("title")
        )
        
        # 保存Markdown
        md_filename = safe_filename.rsplit('.', 1)[0] + '.md'
        md_path = settings.OUTPUT_DIR / md_filename
        md_path.write_text(markdown_content, encoding='utf-8')
        
        # 保存到数据库
        doc = Document(
            filename=safe_filename,
            original_name=file.filename,
            file_type=file_ext,
            file_path=str(file_path),
            markdown_path=str(md_path),
            title=parsed.get("title"),
            content=parsed.get("text", "")[:10000],  # 限制内容长度
            tags=",".join(keywords),
            file_size=file_path.stat().st_size,
            page_count=parsed.get("page_count", 0)
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        uploaded_docs.append(doc.id)
    
    return {
        "success": True,
        "uploaded": len(uploaded_docs),
        "document_ids": uploaded_docs
    }


@app.get("/api/documents", response_model=List[DocumentResponse])
async def get_documents(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    tag: Optional[str] = Query(None, description="按标签过滤，模糊匹配"),
    db: Session = Depends(get_db)
):
    """获取文档列表，可选标签过滤"""
    query = db.query(Document)
    if tag:
        query = query.filter(Document.tags.like(f"%{tag}%"))
    docs = query.order_by(desc(Document.created_at)).limit(limit).offset(offset).all()
    return docs


@app.get("/api/documents/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: int, db: Session = Depends(get_db)):
    """获取单个文档"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@app.get("/api/documents/{doc_id}/markdown")
async def get_document_markdown(doc_id: int, db: Session = Depends(get_db)):
    """获取文档的Markdown内容"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not doc.markdown_path or not Path(doc.markdown_path).exists():
        raise HTTPException(status_code=404, detail="Markdown file not found")
    
    return FileResponse(
        path=doc.markdown_path,
        filename=f"{Path(doc.original_name).stem}.md",
        media_type="text/markdown"
    )


@app.get("/api/search")
async def search_documents(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """搜索文档"""
    # 简单的全文搜索（使用LIKE）
    query = db.query(Document).filter(
        (Document.title.like(f"%{q}%")) | (Document.content.like(f"%{q}%"))
    ).limit(limit).all()
    
    results = []
    for doc in query:
        # 生成摘要片段
        content = doc.content or ""
        index = content.lower().find(q.lower())
        
        if index != -1:
            start = max(0, index - 100)
            end = min(len(content), index + 100)
            snippet = content[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(content):
                snippet = snippet + "..."
        else:
            snippet = content[:200] if content else ""
        
        results.append(SearchResult(
            document_id=doc.id,
            filename=doc.original_name,
            title=doc.title,
            snippet=snippet,
            highlights=[q],
            relevance_score=1.0
        ))
    
    return results


@app.get("/view/{doc_id}", response_class=HTMLResponse)
async def view_document(doc_id: int, request: Request, db: Session = Depends(get_db)):
    """在线查看文档（Markdown 原文渲染为文本预览）"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return templates.TemplateResponse("viewer.html", {"request": request, "doc_id": doc_id, "title": doc.title or doc.original_name})


@app.get("/api/stats", response_model=DocumentStats)
async def get_stats(db: Session = Depends(get_db)):
    """获取统计信息"""
    total = db.query(func.count(Document.id)).scalar()
    total_size = db.query(func.sum(Document.file_size)).scalar() or 0
    
    # 按类型统计
    by_type = {}
    for file_type, count in db.query(Document.file_type, func.count(Document.id)).group_by(Document.file_type).all():
        by_type[file_type] = count
    
    # 最近24小时上传数
    cutoff = datetime.utcnow() - timedelta(hours=24)
    recent = db.query(func.count(Document.id)).filter(Document.created_at >= cutoff).scalar()
    
    return DocumentStats(
        total_documents=total,
        total_size=total_size,
        by_type=by_type,
        recent_uploads=recent
    )


@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """删除文档"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # 删除文件
    if doc.file_path and Path(doc.file_path).exists():
        os.remove(doc.file_path)
    if doc.markdown_path and Path(doc.markdown_path).exists():
        os.remove(doc.markdown_path)
    
    # 删除数据库记录
    db.delete(doc)
    db.commit()
    
    return {"success": True, "message": "Document deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

