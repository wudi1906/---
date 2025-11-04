# Doc Knowledge Forge | 文档知识锻炉

## Pain | 客户痛点
- Documents scattered across cloud drives/email/local folders; searching is slow and incomplete.  /  文档分散在网盘、邮箱、本地，检索缓慢且不完整。
- Knowledge relies on tribal memory; no unified tagging, versioning, or audit trail.  /  知识积累依赖个人经验，缺少统一标签、版本与审计体系。
- Project delivery and retrospectives require manual compilation, consuming hours and risking omissions.  /  项目交付与复盘需人工整理材料，耗时且容易遗漏。

## Solution | 解决方案
- Batch ingest PDF/DOCX/TXT/Markdown, auto-convert to structured Markdown, generate cover metadata.  /  支持批量上传 PDF/DOCX/TXT/Markdown 并自动转为结构化 Markdown。
- Auto-extract chapters, keywords, tags, and build table-of-contents + full-text search (SQLite FTS5).  /  自动抽取章节、关键词与标签，生成目录树与全文检索。
- Inline preview with highlighted matches, bulk ZIP export for delivery, optional vector search & summarization.  /  在线高亮预览、批量 ZIP 导出，可选向量检索与摘要增强。

## Deliverables | 交付清单
- **Live Demo | 在线演示**: `http://localhost:8404`（含示例文档，一键导入/重置）。
- **Pipeline | 处理流程**: FastAPI + parsing/chunking/vectorization，支持 RAG 扩展。
- **Docs & APIs | 文档与接口**: Swagger (`/api/docs`)、Postman 集合、标签配置指南、权限与日志手册。
- **Export & Extensions | 导出与扩展**: Markdown/ZIP 批量导出模板，向量检索、OCR、AI 摘要配置指南。

**Quick Start | 快速开始**
```bash
cd doc-knowledge-forge
./start.bat        # Windows
# or
python -m uvicorn app.main:app --reload --port 8404
```
首次启动会下载嵌入模型 (~200MB)，请保持网络；缓存位于 `app/.cache`、`uploads/`、SQLite 数据库，可按需清理。

## Timeline | 交付周期
1. **Discovery (Day 0)** — Confirm formats, volume, tagging strategy, security requirements.  /  确认文档格式/规模、标签策略与安全诉求。
2. **PoC Demo (Day 3-5)** — Present sample parsing/search/export flows.  /  演示示例文档的解析、检索与导出。
3. **Hardening (Day 6-12)** — Connect production library, enable permissions/OCR/vector extensions.  /  接入真实文档库，启用权限、OCR、向量等扩展。
4. **Launch & Training (Day 12+)** — Deliver源码、运维脚本、培训材料、回滚预案。  /  提交源码、脚本与培训资料，提供回滚方案。

## SLA | 服务保障
- <1 hour response, bilingual communication, 7/14/30 day warranty by package.  /  首次响应 <1 小时，提供中英文支持，按套餐提供 7/14/30 天质保。
- WCAG 2.1 AA frontend, keyboard + dark mode + RTL.  /  前端符合 WCAG 2.1 AA，支持键盘、暗色、RTL。
- Structured logging, full-text metrics, slow query tracing; OCR/vector add-ons含性能基准。  /  结构化日志、全文检索指标、慢查询监控；OCR/向量模块提供性能基线。
- Default private deployment, credentials in `.env`, optional encryption/audit/role-based access.  /  默认内网部署，凭据集中 `.env`，可选加密、审计、角色控制。

## KPI | 成功指标
- Deliver usable knowledge base demo in 3 days, conversion accuracy ≥98%.  /  3 天交付可用演示，转换准确率 ≥98%。
- Search time reduced from minutes to seconds, delivery prep efficiency doubled.  /  检索耗时由分钟降至秒级，交付材料准备效率翻倍。
- Retro/hand-off compilation time reduced by 60%, knowledge reuse significantly improved.  /  复盘/交接整理时间减少 60%，知识复用显著提升。

## FAQ | 常见问题
- **Support scanned PDFs? / 支持扫描 PDF 吗？**  \
  Premium integrates OCR (Tesseract/3rd-party API) with multilingual extraction.  /  Premium 集成 OCR（Tesseract/第三方 API），支持多语言识别。
- **Custom tags & TOC? / 能否自定义标签与目录？**  \
  Yes—keyword mapping, chapter templates, dictionary import, visual config UI.  /  支持关键词映射、章节模板、词典导入与可视化配置。
- **Data security? / 数据安全如何保障？**  \
  Deploy in intranet/private cloud, sensitive data stays on-prem, optional login audit + encryption.  /  默认内网/私有云部署，敏感数据不出企业，可启用登录审计与加密。

## CTA | 立即行动
- 📧 [Book a Demo](mailto:you@example.com?subject=Doc%20Knowledge%20Forge%20Consultation) / 邮件预约演示
- 🗂 [Portal Overview](http://localhost:8101) / 门户导航与实时状态
- 📑 [Test Playbook](../PORTFOLIO_TEST_GUIDE.zh.md) / 验证剧本（中英对照）
- 🚀 [Local Demo](http://localhost:8404) / 本地体验入口

**Last Updated | 最近更新**：2025-11-03

