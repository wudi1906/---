# Doc Knowledge Forge

文档转知识库 - 将混乱的 PDF/DOCX 文档转换为可搜索的Markdown知识库。

## 功能特性

- 📄 **多格式支持**: PDF, DOCX, TXT, Markdown
- 🔄 **自动转换**: 智能转换为 Markdown 格式
- 🔍 **全文检索**: 支持中英文全文搜索
- 🏷️ **标签管理**: 自动提取关键词标签
- 📁 **目录树**: 层级展示文档结构
- 💡 **高亮显示**: 搜索结果高亮
- 📦 **批量导出**: 打包下载所有文档
- 🌐 **多语言**: 支持中文/英文/阿拉伯语

## 快速开始

```PowerShell
pwsh .\scripts\start.ps1 --install
```

访问: http://localhost:8404

## 技术栈

- **后端**: Python + FastAPI
- **文档解析**: pymupdf (PDF), docx2python (DOCX)
- **全文检索**: SQLite FTS5 或 Elasticsearch
- **前端**: Vanilla JS + Tailwind CSS

## 使用流程

1. **上传文档**: 拖拽或选择 PDF/DOCX 文件
2. **自动处理**: 系统提取文本并转换为 Markdown
3. **查看目录**: 左侧目录树浏览所有文档
4. **全文搜索**: 顶部搜索框输入关键词
5. **高亮查看**: 右侧内容区显示高亮结果
6. **导出归档**: 下载整理后的文档包

## 支持格式

| 格式 | 扩展名 | 说明 |
| --- | --- | --- |
| PDF | .pdf | 支持文本型PDF，扫描件需OCR |
| Word | .docx, .doc | 完整支持格式和图片 |
| Markdown | .md | 直接导入 |
| 文本 | .txt | UTF-8编码 |

## API 端点

- `POST /api/upload` - 上传文档
- `GET /api/documents` - 获取文档列表
- `GET /api/search?q=keyword` - 全文搜索
- `GET /api/document/{id}` - 获取文档内容
- `POST /api/export` - 导出归档

## 部署

```bash
docker compose up --build
```

## 扩展方向

- OCR 支持 (Tesseract)
- 向量检索 (Embedding + FAISS)
- AI 摘要生成
- 多租户隔离
- 版本控制

