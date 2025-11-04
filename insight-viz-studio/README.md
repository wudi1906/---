# Insight Viz Studio | 数据可视化工作室

## Pain | 客户痛点
- Business teams must deliver executive-ready charts quickly; manual Excel/PPT work wastes hours and lacks consistency.  /  业务团队需要快速输出高质量图表，手工 Excel/PPT 制作耗时且风格不统一。
- Data arrives in CSV/JSON/Excel mixes, causing import errors and repetitive cleaning.  /  数据格式混杂，导入易出错且需重复清洗。
- Weekly/monthly reports demand PNG/PDF templates and brand alignment, often reworked from scratch.  /  周/月报需要模板与品牌一致性，常常需要从零排版。

## Solution | 解决方案
- Upload CSV/JSON/Excel, auto-parse schema, detect metrics/dimensions, recommend charts (line/bar/pie/funnel).  /  上传 CSV/JSON/Excel 自动解析字段并推荐折线、柱状、饼图、漏斗。
- Drag-and-drop dashboards with filters, annotations, theme tokens, live preview.  /  拖拽式仪表盘支持过滤器、注释、主题 Token，并实时预览。
- One-click export PNG/PDF/SVG with weekly/monthly templates, brand-safe typography.  /  一键导出 PNG/PDF/SVG，内置周/月报模板并保持品牌一致。
- Multi-language & currency formatting, optimised for 10k+ rows, supporting global teams.  /  支持多语言与货币格式，优化 1 万行以上数据性能，满足全球团队。

## Deliverables | 交付清单
- **Live Demo | 在线演示**: `http://localhost:8606`（含示例数据与导入脚本）。
- **Source & Pipeline | 源码与处理链**: FastAPI + Pandas + ECharts + Docker Compose。 / Async FastAPI backend with data pipeline.
- **Docs & Templates | 文档与模板**: 导入规范、图表配置指南、周/月报模板、API 文档。 / Import specs, chart guide, export templates, API docs.
- **Testing Assets | 测试资产**: Postman 集合、单元/集成测试、性能基准脚本。 / Postman flows, test suites, benchmarks。
- **Sample Data | 示例数据集**: `data/samples/` (sales.csv, user_growth.json, marketing.xlsx)。 / Ready-to-use datasets。
- **Quick Start | 快速开始**:
  ```bash
  cd insight-viz-studio
  .\start.bat    # Windows
  # or
  python -m uvicorn app.main:app --reload --port 8606
  ```
  Visit `http://localhost:8606` after ~10 seconds. / 约 10 秒后访问 `http://localhost:8606`。

## Timeline | 交付周期
1. **Discovery (Day 0)** — Confirm data formats, KPI list, export cadence, brand guidelines.  /  确认数据格式、指标清单、导出频率与品牌规范。
2. **PoC Demo (Day 2-4)** — Seed sample data, validate chart recommendations, preview export体验。 / 演示示例数据，验证图表推荐与导出体验。
3. **Hardening (Day 5-10)** — Connect production data, configure themes, automate reporting workflows.  /  接入真实数据，配置主题并自动化周/月报。
4. **Launch & Training (Day 10+)** — Deliver 源码、培训资料、自动化脚本与回滚预案。 / Ship code, training, automation scripts, rollback plan。

## SLA | 服务保障
- <1 hour response, 7/14/30 day remote warranty by package.  / 首次响应 <1 小时，提供 7/14/30 天远程质保。
- Frontend meets WCAG 2.1 AA（对比度 ≥4.5:1，键盘导航，RTL/多语言）。 / Compliant UI with accessible navigation。
- Performance optimization (sampling, virtual scroll, Workers) sustaining 50k+ rows.  / 采样、虚拟滚动与 Web Worker 优化，支撑 5 万行数据。
- Export module built on Puppeteer/wkhtmltopdf with font embedding & deployment best practices.  / 导出模块基于 Puppeteer/wkhtmltopdf，并附字体嵌入与部署建议。

## KPI | 成功指标
- First usable chart in ≤5 minutes, reporting time reduced by 70%.  / ≤5 分钟产出首个可用图表，报告制作时间下降 70%。
- PNG/PDF export <2s, automation success ≥95%.  / PNG/PDF 导出 <2 秒，自动化命中率 ≥95%。
- Template reuse ×3, team collaboration满意度显著提升。 / 模板复用率提升 3 倍，团队协作满意度大幅提升。

## FAQ | 常见问题
- **Real-time data integration? / 支持实时数据吗？**  \
  Premium 可接入数据库/API，支持定时刷新或实时推送。 / Premium tier connects databases/APIs for scheduled refresh.
- **Custom export templates? / 导出模板可否自定义？**  \
  模板引擎支持品牌色、Logo、封面、语种与货币格式。 / Template engine aligns branding。
- **Sensitive data handling? / 如何保障数据安全？**  \
  默认本地/私有部署，数据仅存临时目录，可启用自动清理与匿名策略。 / Local/private deployment with cleanup & anonymization options。

## CTA | 行动指引
- 📧 [Email – Book a Demo](mailto:you@example.com?subject=Insight%20Viz%20Studio%20Consultation) / 邮件预约演示
- 🗂 [Portal Overview](http://localhost:8101) / 门户导航与实时状态
- 📑 [Test Playbook](../PORTFOLIO_TEST_GUIDE.zh.md) / 验证剧本（中英对照）
- 🚀 [Local Demo](http://localhost:8606) / 本地体验入口

**Last Updated | 最近更新**：2025-11-03

