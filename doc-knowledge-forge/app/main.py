"""
Doc Knowledge Forge 主应用
"""
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    init_db()
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
        <title>Doc Knowledge Forge</title>
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
                margin-bottom: 30px;
            }
            .upload-area {
                border: 2px dashed #cbd5e1;
                border-radius: 12px;
                padding: 60px 20px;
                text-align: center;
                transition: all 0.3s;
            }
            .upload-area:hover {
                border-color: #2563eb;
                background: #f8fafc;
            }
            .btn {
                display: inline-block;
                padding: 12px 32px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin: 10px;
                transition: all 0.2s;
            }
            .btn:hover {
                background: #1d4ed8;
                transform: translateY(-2px);
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .feature {
                padding: 20px;
                background: #f8fafc;
                border-radius: 8px;
            }
            .feature h3 {
                color: #2563eb;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📄 Doc Knowledge Forge</h1>
                <p style="font-size: 1.25rem; opacity: 0.95;">文档转知识库 - 智能检索系统</p>
            </div>

            <div class="card">
                <h2 style="margin-bottom: 20px;">上传文档</h2>
                <div class="upload-area">
                    <div style="font-size: 3rem; margin-bottom: 20px;">📎</div>
                    <p style="color: #64748b; margin-bottom: 20px;">
                        拖拽文件到此处或点击上传<br/>
                        支持格式: PDF, DOCX, DOC, TXT, MD
                    </p>
                    <input type="file" id="fileInput" multiple accept=".pdf,.docx,.doc,.txt,.md" style="display:none">
                    <button onclick="document.getElementById('fileInput').click()" 
                            style="padding: 12px 32px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                        选择文件
                    </button>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <h3>📄 多格式支持</h3>
                        <p>PDF、Word、TXT、Markdown</p>
                    </div>
                    <div class="feature">
                        <h3>🔍 全文检索</h3>
                        <p>支持中英文搜索与高亮</p>
                    </div>
                    <div class="feature">
                        <h3>🏷️ 自动标签</h3>
                        <p>智能提取关键词</p>
                    </div>
                    <div class="feature">
                        <h3>📦 批量导出</h3>
                        <p>打包下载Markdown文档</p>
                    </div>
                </div>
            </div>

            <div style="text-align: center;">
                <a href="/api/docs" class="btn">📘 API 文档</a>
                <a href="/api/documents" class="btn">📝 文档列表</a>
                <a href="/api/stats" class="btn">📊 统计信息</a>
            </div>
        </div>

        <script>
            document.getElementById('fileInput').addEventListener('change', async (e) => {
                const files = e.target.files;
                if (!files.length) return;
                
                const formData = new FormData();
                for (let file of files) {
                    formData.append('files', file);
                }
                
                try {
                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    alert(`成功上传 ${result.uploaded} 个文件！`);
                    window.location.href = '/api/documents';
                } catch (error) {
                    alert('上传失败: ' + error.message);
                }
            });
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
    db: Session = Depends(get_db)
):
    """获取文档列表"""
    docs = db.query(Document).order_by(desc(Document.created_at)).limit(limit).offset(offset).all()
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

