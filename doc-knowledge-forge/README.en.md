# Doc Knowledge Forge — Document to Knowledge Base One-Stop Solution

> **Target Audience**: Consulting/law firms/manufacturing/education teams with massive PDF, Word, manual materials
>
> **Core Value**: Batch conversion → auto-tagging → full-text search → online highlight viewing → batch export, delivered in as fast as 3 days

[中文版本 Chinese Version](./README.md)

---

## 1. Pain Points

- Files scattered across cloud storage/email/local drives, search is time-consuming and incomplete
- Knowledge depends on personal experience, lacks unified archiving, tagging, and version management
- Project delivery/retrospective requires manual document compilation — low efficiency and easy to miss items

## 2. Solution & Value

- Batch upload PDF / DOCX / TXT / Markdown, auto-convert to structured Markdown
- Auto-extract chapters, keywords, tags, generate table of contents tree + full-text search
- Online highlight viewing, one-click batch export ZIP, convenient for external delivery or internal archiving
- Optional vector search, AI summarization, OCR extensions, support advanced knowledge management scenarios

## 3. Deliverables

- 🖥️ **Live Demo**: `http://localhost:8404` (with sample documents, one-click import)
- 📦 **Source Code & Scripts**: FastAPI backend, parsing/chunking/vectorization pipeline, Tailwind frontend, Docker Compose
- 🧠 **RAG Pipeline**: Sentence-Transformers + optional FAISS, supports vector search, snippet highlighting, chunk visualization
- 📕 **Documentation Suite**: Deployment guide, tag config instructions, permissions/logging manual, FAQ
- 🧪 **API / Postman**: `http://localhost:8404/api/docs` and updated Postman collection (includes `/api/docs/upload`, `/api/chunks/{id}`)
- 📑 **Export Templates**: Markdown/ZIP batch export config, vector search and OCR extension guide

## 4. Timeline & Process

1. **Requirements Clarification (Day 0)**: Confirm document formats/quantities, tagging strategy, deployment/security requirements
2. **PoC Demo (Day 3-5)**: Deliver demo (sample documents), validate parsing, search, export experience
3. **Feature Completion (Day 6-12)**: Connect real document library, deploy test/production, complete permissions and extensions
4. **Acceptance & Handover (Day 12+)**: Deliver source code, scripts, training materials, complete acceptance checklist and rollback plan

## 5. SLA & Quality Assurance

- **Response Commitment**: <1 hour reply, 7~30 days support based on package tier, English/Chinese communication
- **Accessibility**: Frontend complies with WCAG 2.1 AA, supports keyboard navigation, dark mode, RTL layout
- **Performance**: Structured logging, full-text search metrics, slow query monitoring; OCR/vector extensions provide performance benchmarks
- **Security**: Default local/private cloud deployment, credentials in `.env`, can enable encryption/audit/access control (Premium)

## 6. KPI & Outcomes

- Deliver usable knowledge base demo in 3 days, conversion accuracy ≥98%
- Document search time reduced from minutes to seconds, delivery preparation efficiency improved 2×
- Project retrospective/delivery material compilation time reduced by 60%, knowledge reuse rate significantly improved

## 7. FAQ

**Q1: Support scanned PDFs?**  
A: Premium integrates OCR (Tesseract/third-party API), supports multilingual text extraction.

**Q2: Can tags and table of contents be customized?**  
A: Supports keyword mapping, chapter templates, internal dictionary integration, visual config interface.

**Q3: How to ensure data security?**  
A: Default deployment on intranet/private cloud, sensitive data doesn't leave enterprise network, can enable login audit, permission control, data encryption.

## 8. Why Choose Me?

✅ **Fast Response**: <1 hour reply, clear milestones, transparent progress  
✅ **Platform Protection**: Fiverr/Upwork transaction guarantee, escrow payment  
✅ **Best Practices**: RAG pipeline, Sentence-Transformers, WCAG 2.1 AA compliance  
✅ **Proven Delivery**: Complete test suite, Docker-ready, production-grade code

## 9. Next Steps

- 🔵 [Upwork — Hire Me](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr — View Packages](https://www.fiverr.com/yourname)
- 📧 [Email — Book Demo](mailto:you@example.com?subject=Doc%20Knowledge%20Forge%20Consultation)
- 🚀 [Local Demo — Try Now](http://localhost:8404)

> "Turn scattered documents into a knowledge base in seconds — invest time in creating value."

---

## Quick Start

```bash
cd doc-knowledge-forge
.\start.bat    # Windows
# or
python -m uvicorn app.main:app --reload --port 8404
```

Visit `http://localhost:8404` after 10 seconds.

**Note**: First launch will download embedding model (~200MB), please stay connected; models and uploaded files are cached to `app/.cache`, `uploads/` and SQLite database, can be cleaned as needed.

## Tech Stack

- **Backend**: Python 3.10+, FastAPI
- **Document Parsing**: pymupdf (PDF), python-docx (Word)
- **Search**: SQLite FTS5, Sentence-Transformers
- **Vector Store**: In-memory numpy (FAISS ready)
- **Frontend**: Vanilla JavaScript, Tailwind CSS
- **Deployment**: Docker, uvicorn

---

**Last Updated**: 2025-11-03

