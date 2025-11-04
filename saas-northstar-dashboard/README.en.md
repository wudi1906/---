# SaaS Northstar Dashboard | SaaS 北极星指标看板

## Pain | 客户痛点
- Metrics scattered across Stripe/Paddle/CRM/finance sheets; stakeholders cannot align on a single source of truth.  /  指标散落在 Stripe、Paddle、CRM、财务表格中，团队难以统一视角。
- Building custom dashboards requires heavy investment in charts, permissions, accessibility, and maintenance.  /  自建看板需投入大量可视化、权限、可访问性与维护成本。
- Weekly/monthly KPI reports are compiled manually, leading to slow response and human error.  /  周/月报靠人工整合，效率低且易出错。

## Solution | 解决方案
- Built-in B2B SaaS & B2C Growth templates with configurable field mapping; import CSV/JSON in minutes.  /  内置 B2B/B2C KPI 模板与字段映射，几分钟内导入 CSV/JSON。
- Multi-step wizard (template → upload → mapping → preview) auto-calculates MRR/ARR/Churn/LTV/CAC.  /  多步导入向导自动计算 MRR/ARR/Churn/LTV/CAC。
- Accessibility-first Next.js app with light/dark themes, chart presets, PNG/PDF export, and collaboration notes.  /  基于 Next.js 的可访问性体验，支持明暗主题、图表预设、PNG/PDF 导出与协作备注。
- Data validation, anomaly detection, and scheduled exports keep weekly reports accurate and automate investor decks.  /  数据校验与异常提醒确保周报准确，可定时导出投资人材料。

## Deliverables | 交付清单
- **Live Demo | 在线演示**: `http://localhost:8303` 支持 KPI 模板切换与示例数据。
- **Import Wizard | 导入中心**: `/import` 多 CSV 上传、自动字段匹配、预览确认。
- **Docs & APIs | 文档与接口**: Swagger (`/api/templates`, `/api/import`, `/api/exports`)、Postman 流程、指标字典、导出流程指南。
- **Source & Deployment | 源码与部署**: Next.js 14 + Tailwind + Zustand、Docker/Vercel 配置、CI 建议。

**Quick Start | 快速开始**
```bash
cd saas-northstar-dashboard
npm install
npm run dev
```
10 秒后访问 `http://localhost:8303`，导入示例模板即可体验完整流程。

## Timeline | 交付周期
1. **Discovery (Day 0)** — Confirm metric scope, currency, data source formats, collaboration workflow.  /  确认指标范围、币种、数据源格式与协作流程。
2. **PoC Demo (Day 2-4)** — Provide sample dashboard with seeded data, review KPI layout and storytelling.  /  交付示例看板，审查 KPI 结构与叙事。
3. **Hardening (Day 5-10)** — Connect production data, set up scheduled exports, polish charts and accessibility.  /  接入真实数据，配置定时导出，优化图表与可访问性。
4. **Launch & Training (Day 10+)** — Deliver source, operations handbook, training video, rollback plan.  /  提交源码与运维手册，录制培训，提供回滚方案。

## SLA | 服务保障
- <1 hour response, kickoff within 24h, 7/14/30 day support by package tier.  /  首次响应 <1 小时，24 小时内 Kick-off，并提供 7/14/30 天远程支持。
- WCAG 2.1 AA compliant UI, keyboard navigation, screen reader labels, RTL support.  /  UI 符合 WCAG 2.1 AA，支持键盘、读屏、RTL。
- Structured logging, slow query tracing, automated tests, export speed <1s (standard volume).  /  结构化日志、慢查询排查、自动化测试，标准数据量导出 <1 秒。
- Secrets isolated in `.env.local`, Docker + Vercel templates with security hardening checklist.  /  凭据集中 `.env.local`，提供 Docker/Vercel 配置与安全加固清单。

## KPI | 成功指标
- Deliver live dashboard within 3 days; showcase key KPIs in first stakeholder meeting.  /  3 天内交付在线看板，于首次会议展示核心指标。
- Metric accuracy ≥99%; report generation time reduced from hours to minutes.  /  指标准确率 ≥99%，周报生成从数小时缩短至分钟级。
- 2× collaboration efficiency, predictable investor/board reporting cadence.  /  协同效率提升 2 倍，投资人/董事会汇报节奏稳定。

## FAQ | 常见问题
- **Only CSV supported? / 是否仅支持 CSV？**  \
  Basic/Standard ship with CSV; Premium connects Stripe/Paddle/Chargebee/custom APIs for scheduled sync.  /  Basic/Standard 支持 CSV，Premium 可对接 Stripe/Paddle/Chargebee/API 定时同步。
- **Team collaboration? / 团队如何协作？**  \
  Standard adds role management; Premium enables SSO, permission hierarchy, multi-tenancy.  /  Standard 提供角色管理，Premium 支持 SSO、权限分级与多租户。
- **Data security? / 数据安全如何保障？**  \
  Deploy in customer cloud, secrets in `.env.local`, optional SOC2-ready hardening checklist.  /  可部署在客户云环境，凭据保存在 `.env.local`，提供安全加固建议。

## CTA | 立即行动
- 📧 [Book a Demo](mailto:you@example.com?subject=SaaS%20Northstar%20Dashboard%20Consultation) / 邮件预约演示
- 🗂 [Portal Overview](http://localhost:8101) / 门户导航与实时状态
- 📑 [Test Playbook](../PORTFOLIO_TEST_GUIDE.zh.md) / 验证剧本（中英对照）
- 🚀 [Local Demo](http://localhost:8303) / 本地体验入口

**Last Updated | 最近更新**：2025-11-03

