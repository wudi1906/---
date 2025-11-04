# Global Price Sentinel | 全球价格哨兵

## Pain | 客户痛点
- Multi-SKU brands cannot track global marketplace prices in real time; spreadsheets miss flash promotions.  /  多 SKU 品牌难以及时跟踪全球电商价格，表格维护容易错过限时活动。
- Pricing teams lack automated alerts and historical insights, leading to slow reactions and unclear ROI.  /  定价团队缺少自动告警与历史洞察，响应滞后且难以评估投资回报。
- Compliance teams worry about stability, retry logic, and audit logs when scraping at scale.  /  合规/运营团队担心大规模爬取的稳定性、重试机制与审计日志。

## Solution | 解决方案
- Playwright-powered scraping with proxy pool, captcha handling, and rate limiting for Amazon/JD/Taobao.  /  Playwright + 代理池 + 验证码/限流策略，稳定抓取亚马逊、京东、淘宝等站点。
- Configurable thresholds and multi-channel alerts (Email / Webhook / Slack) with delivery logs.  /  可配置阈值，多渠道告警（邮件/Webhook/Slack），并记录投递日志。
- Visual console + weekly/monthly HTML/PDF reports, CSV exports, Prometheus metrics, and Grafana dashboards.  /  可视化控制台、周/月报 HTML/PDF、CSV 导出，附带 Prometheus 指标与 Grafana 仪表板。

## Deliverables | 交付清单
- **Demo & Console | 演示与控制台**: `http://localhost:8101` 含示例数据；`/monitor/settings` 配置调度、代理与告警。
- **APIs & Docs | API 与文档**: Swagger (`/api/docs`)、Postman 集合、部署与操作手册。
- **Reports | 报表模板**: HTML/PDF 趋势报告、CSV 明细、Prometheus/Grafana 集成指南。
- **Source & Scripts | 源码与脚本**: FastAPI + SQLAlchemy 后端、Playwright 爬虫、Tailwind 管理界面、一键启动脚本。

**Quick Start | 快速开始**
```bash
cd global-price-sentinel
./start.ps1   # Windows
# 或者
./start.sh    # Linux / Mac
```
访问 `http://localhost:8101` 即可体验；控制台中的 “导入示例数据” 按钮可刷新样本。

## Timeline | 交付周期
1. **Discovery (Day 0)** — Confirm target marketplaces, SKUs, alert thresholds, deployment environment.  /  确认站点、SKU、告警阈值与部署环境。
2. **PoC Demo (Day 2-4)** — 演示示例抓取、阈值触发、告警投递，验证准确度。
3. **Feature Hardening (Day 5-10)** — 接入真实数据、完善报表、优化代理/重试策略。
4. **Launch & Training (Day 10+)** — 交付源码、培训和回滚方案，准备周/月报模板。

## SLA | 服务保障
- <1 hour response, kickoff within 24h · 首次响应 <1 小时，24 小时内安排启动会议。
- WCAG 2.1 AA console, keyboard friendly, dark mode, RTL-ready.  /  控制台符合 WCAG 2.1 AA，支持键盘操作、暗色模式与 RTL。
- Structured logging, retry/backoff, Prometheus metrics, slow query trace.  /  结构化日志、重试退避、Prometheus 指标、慢查询追踪。
- Credentials stored in `.env`, GDPR-ready, Docker templates with hardening checklist.  /  凭据集中于 `.env`，符合 GDPR，附 Docker 模板与安全加固清单。

## KPI | 成功指标
- MVP delivered within 3 weeks, automate ≥20 SKUs after launch.  /  3 周内交付 MVP，上线后自动化监控 ≥20 个 SKU。
- Alert latency <5 minutes, scraping success rate ≥99%.  /  告警延迟 <5 分钟，抓取成功率 ≥99%。
- Reduce manual monitoring effort by 30%, double actionable pricing insights.  /  监控人力减少 30%，策略会议可用的价格洞察翻倍。

## FAQ | 常见问题
- **Support login-only marketplaces? / 能否抓取登录站点？**  \
  Yes—advanced packages include账号登录、验证码处理、代理池策略。 / 支持账号登录、验证码处理与代理池策略（进阶套餐）。
- **Alert channels available? / 支持哪些告警渠道？**  \
  Email / Webhook / Slack by default, extendable to Teams/WeCom with logging.  / 默认支持邮件、Webhook、Slack，可扩展 Teams/企业微信并记录投递日志。
- **How is it deployed? / 如何部署？**  \
  Docker Compose templates or deploy to Render/Fly.io/AWS; credentials managed independently.  / 提供 Docker Compose 模板，可部署至自有服务器或 Render/Fly.io/AWS，凭据自主管理。

## CTA | 立即行动
- 📧 [Book a Demo](mailto:you@example.com?subject=Global%20Price%20Sentinel%20Consultation) / 邮件预约演示
- 🗂 [Portal Overview](http://localhost:8101) / 门户导航与实时状态
- 📑 [Test Playbook](../PORTFOLIO_TEST_GUIDE.zh.md) / 验证剧本（中英对照）
- 🚀 [Local Demo](http://localhost:8101) / 本地体验入口

**Last Updated | 最近更新**：2025-11-03

