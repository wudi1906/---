# Doc Knowledge Forge · 文档到知识库的一站式解决方案

[English Version](./README.en.md) | 中文版本

> **适用对象**：咨询/律所/制造业/教育等拥有大量 PDF、Word、手册资料的团队
>
> **核心卖点**：批量转换 → 自动标签 → 全文检索 → 在线高亮查看 → 批量导出，最快 3 天交付。

---

## 1. 背景与痛点 · Background & Pain
- 文件散落在网盘/邮箱/本地，检索耗时且不完整。
- 知识依赖个人经验，缺少统一归档、标签与版本管理。
- 项目交付/复盘需手动整理文档，效率低且易遗漏。

## 2. 解决方案 · Solution & Value
- 批量上传 PDF / DOCX / TXT / Markdown，自动转换为结构化 Markdown。
- 自动提取章节、关键词、标签，生成目录树 + 全文检索。
- 在线高亮查看、一键批量导出 ZIP，便于对外交付或内部归档。
- 可选向量检索、AI 摘要、OCR 扩展，支持高阶知识管理场景。

## 3. 交付清单 · Deliverables
- 🖥️ **Live Demo**：`http://localhost:8404`（含示例文档，可一键导入）。
- 📦 **源代码与脚本**：FastAPI 后端、解析/分块/向量化管道、Tailwind 前端、Docker Compose。
- 🧠 **RAG 管线**：Sentence-Transformers + 可选 FAISS，支持向量检索、片段高亮、分块可视化。
- 📕 **文档套件**：部署指南、标签配置说明、权限/日志手册、FAQ。
- 🧪 **API / Postman**：`http://localhost:8404/api/docs` 与更新后的 Postman 集合（含 `/api/docs/upload`、`/api/chunks/{id}`）。
- 📑 **导出模板**：Markdown/ZIP 批量导出配置、向量检索与 OCR 扩展指南。

## 4. 实施流程与周期 · Process & Timeline
1. **需求澄清（Day 0）**：确认文档格式/数量、标签策略、部署/安全要求。
2. **PoC 演示（Day 3-5）**：交付 Demo（示例文档），验证解析、检索、导出体验。
3. **功能完善（Day 6-12）**：接入真实文档库，部署测试/生产，完善权限与扩展。
4. **验收交接（Day 12+）**：交付源代码、脚本、培训资料，完成验收清单与回滚预案。

## 5. SLA 与质量保证 · SLA & Quality
- < 1 小时响应，按套餐提供 7~30 天支持，含中文/英文沟通。
- 前端符合 WCAG 2.1 AA，支持键盘导航、暗色模式、RTL 布局。
- 结构化日志、全文检索指标、慢查询监控；OCR/向量扩展提供性能基准。
- 默认本地/私有云部署，凭证写入 `.env`，可启用加密/审计/权限控制（Premium）。

## 6. KPI / 成功指标占位 · KPI & Outcomes
- 3 天内交付可用知识库 Demo，转换准确率 ≥ 98%。
- 文档检索时间从分钟级降至秒级，交付准备效率提升 2×。
- 项目复盘/交付材料整理时间减少 60%，知识复用率显著提升。

## 7. RAG · 分块向量检索说明
- **分块策略**：默认 800 字符窗口 + 200 重叠，自动对齐句末，兼容中英文混排。
- **嵌入模型**：`sentence-transformers/all-MiniLM-L6-v2`（可通过 `.env` 覆盖），内置 np-based 检索，自动降级。
- **核心接口**：
  - `POST /api/docs/upload`：Multipart 上传并同步完成解析→分块→向量化，返回每个文件的分块数量与关键词。
  - `GET /api/search?q=&top_k=`：语义检索，返回片段编号、得分、摘要及高亮关键词。
  - `GET /api/chunks/{chunk_id}`：提取指定分块原文，可用于前端高亮或导出。
- **前端体验**：上传进度提示、向量检索榜单、片段预览（高亮命中词）、一键跳转原文 Viewer。

```bash
# 示例：使用 curl 上传并检索
curl -F "files=@handbook.pdf" http://localhost:8404/api/docs/upload
curl "http://localhost:8404/api/search?q=policy&top_k=5"
curl http://localhost:8404/api/chunks/1
```

## 8. 常见问题 · FAQ
**Q1：支持扫描件 PDF 吗？**  
A：Premium 集成 OCR（Tesseract/第三方 API），支持多语言文字提取。

**Q2：标签和目录可自定义吗？**  
A：支持关键词映射、章节模板、内部词典对接，可视化配置界面。

**Q3：数据如何保障安全？**  
A：默认在内网/私有云部署，敏感数据不出企业网络，可启用登录审计、权限控制、数据加密。

## 9. CTA · 下一步行动
- 🔵 [Upwork · 立即咨询](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr · 套餐下单](https://www.fiverr.com/yourname)
- 📧 [Email · 预约演示](mailto:you@example.com?subject=Doc%20Knowledge%20Forge%20Consultation)
- 🚀 [本地 Demo · 立即体验](http://localhost:8404)

> “让散落文档秒变知识库，把时间留给创造价值。”

