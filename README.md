# Portfolio Overview | 全栈作品集概览

## Pain | 客户痛点
- Buyers struggle to verify delivery capability quickly; demos are inconsistent across repositories.  /  买家难以在短时间内验证交付能力，各仓库 Demo 体验不一致。
- Cross-border stakeholders need bilingual assets and unified onboarding scripts to unblock procurement decisions.  /  跨境团队需要中英双语资产与统一启动脚本，才能顺畅推动采购决策。

## Solution | 解决方案
- Six production-ready showcases with reproducible KPI narratives, Postman verification flows, and real-time health dashboards.  /  六个生产级项目，提供可复现的 KPI 叙事、Postman 验证流程与实时健康面板。
- One-click scripts (`start-all.ps1`, `TEST_ALL.bat`, `stop-all.ps1`) plus bilingual documentation, Fiverr gig copy, and screenshot playbooks.  /  一键启动/测试/停止脚本，配套中英双语文档、Fiverr 套餐文案与截图剧本。
- Unified CTA portal at `http://localhost:8101` exposing live status, demo seeding/reset controls, and trust badges.  /  统一门户 `http://localhost:8101` 展示实时状态、示例数据导入/重置与信任徽章。

## Deliverables | 交付清单
**Project Matrix | 项目矩阵**

| Project / 项目 | Core Value / 核心价值 | Highlights / 亮点 | Port |
| --- | --- | --- | --- |
| [Global Price Sentinel](./global-price-sentinel/README.en.md) | E-commerce price monitoring 电商价格监控 | Playwright scraping · Proxy pool · Alerts | 8101 |
| [Event Relay Hub](./event-relay-hub/README.en.md) | Webhook relay 事件中枢 | Stripe/GitHub signature · DLQ · Replay | 8202 |
| [SaaS Northstar Dashboard](./saas-northstar-dashboard/README.en.md) | SaaS KPI dashboard 指标看板 | MRR/ARR/Churn/LTV · CSV import | 8303 |
| [Doc Knowledge Forge](./doc-knowledge-forge/README.en.md) | Document → Knowledge base 文档知识库 | PDF/DOCX ingestion · FTS · RAG | 8404 |
| [A11y Component Atlas](./a11y-component-atlas/README.en.md) | Accessible React components 可访问性组件库 | WCAG 2.1 AA · Storybook · axe | 8505 |
| [Insight Viz Studio](./insight-viz-studio/README.en.md) | Data viz studio 数据可视化 | CSV/JSON upload · ECharts · Export | 8606 |

**Operations | 运维**
- `start-all.ps1` launch suite · `TEST_ALL.bat` health check · `stop-all.ps1` shutdown.  /  `start-all.ps1` 启动全套，`TEST_ALL.bat` 健康检测，`stop-all.ps1` 一键停止。
- Demo portal highlights CTA, package badges, live status, and demo seed/reset buttons.  /  门户展示 CTA、套餐徽章、实时状态与示例数据导入/重置。

**Assets | 资料包**
- README + API docs + Postman + Fiverr packages in EN / 中文 for every project.  /  每个项目含 README、API 文档、Postman 集合与中英 Fiverr 套餐。
- Screenshot & video checklist, publishing guide, and KPI narrative scripts (`screenshots/`, `FIVERR_READY_REPORT.md`).  /  截图与录屏清单、发布指南、KPI 叙事脚本。

**Quick Start | 快速开始**
```powershell
cd "E:\\Program Files\\cursorproject\\作品集"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\\start-all.ps1
```
Visit `http://localhost:8101` after 30–60s · Run `.\\TEST_ALL.bat` to verify · `.\\stop-all.ps1` to stop all services.  /  30–60 秒后访问门户，执行 `.\\TEST_ALL.bat` 验证，`.\\stop-all.ps1` 结束全部服务。

## Timeline | 交付周期
1. **Discovery (Day 0)** — Align pain points, KPIs, data access, and visual tone.  /  需求澄清：确认痛点、指标、数据接入与视觉调性。
2. **PoC Demo (Day 2-4)** — Seed sample data, review health dashboards, validate CTA + gig messaging.  /  PoC 演示：导入示例数据，审查健康面板与 CTA/套餐文案。
3. **Hardening (Day 5-10)** — Connect real data, finalize bilingual docs, polish visuals & Storybook flows.  /  强化阶段：接入真实数据，完善双语文档与可视化体验。
4. **Launch (Day 10+)** — Deliver source, training, and Fiverr-ready assets; support go-live and publishing.  /  上线交付：提交源码、培训资料与 Fiverr 素材，协助正式发布。

## SLA | 服务保障
- <1 hour first response, kickoff scheduled within 24h.  /  首次响应 <1 小时，24 小时内安排 Kick-off。
- 7 / 14 / 30 day remote warranty aligned with Basic / Standard / Premium tiers.  /  Basic/Standard/Premium 套餐对应 7 / 14 / 30 天远程质保。
- WCAG 2.1 AA, structured logging, retry/backoff, Docker deployment guides, and security hardening recommendations.  /  符合 WCAG 2.1 AA，提供结构化日志、重试策略、Docker 部署与安全加固建议。

## KPI | 成功指标
- Launch all six demos with seeded data in ≤3 days.  /  ≤3 天上线所有演示环境。
- Alert & health latency under 5 minutes.  /  告警与健康监控延迟 <5 分钟。
- ≥99% automated test pass rate and scrape/import success.  /  自动化测试与抓取/导入成功率 ≥99%。
- Fiverr gig assets (copy + screenshots) ready in under one week.  /  <1 周完成 Fiverr 套餐文案与截图素材。

## FAQ | 常见问题
- **How do I launch the demos? | 如何启动 Demo？**  \
  Run `start-all.ps1`, then browse `http://localhost:8101`; use portal buttons to import/reset demo data.  /  运行 `start-all.ps1`，访问门户并使用按钮导入或重置示例数据。
- **Can I request customization? | 是否支持定制？**  \
  Yes—FastAPI, Next.js, React, Storybook, and Docker-based architecture is modular for industry-specific features.  /  是的，基于 FastAPI 与 Next.js 的模块化架构，便于扩展行业功能。
- **What technologies are covered? | 技术栈有哪些？**  \
  Python, TypeScript/React, Playwright, ECharts, Tailwind, Storybook, Postman, Docker.  /  Python、TypeScript/React、Playwright、ECharts、Tailwind、Storybook、Postman、Docker。

## CTA | 行动指引
- 📧 [Email – Book a Demo](mailto:you@example.com?subject=Portfolio%20Demo%20Request) / 邮件预约演示
- 🗂 [Portal – Explore Projects](http://localhost:8101) / 门户总览与实时状态
- 📑 [Verification Playbook](./PORTFOLIO_TEST_GUIDE.zh.md) / 验证剧本（中英对照）
- 🚀 [Launch Local Demo](http://localhost:8101) / 本地一键体验

---

### Appendix | 附录
- [FIVERR_READY_REPORT.md](./FIVERR_READY_REPORT.md) — progress checklist · 进度与检查清单
- [PORTFOLIO_TEST_GUIDE.zh.md](./PORTFOLIO_TEST_GUIDE.zh.md) — verification playbook · 验证剧本
- [fiverr-listings/](./fiverr-listings/) — package copy & add-ons · 套餐文案与增值服务
- [screenshots/README.md](./screenshots/README.md) — capture workflow · 截图与录屏流程

**Last Updated | 最近更新**：2025-11-03

