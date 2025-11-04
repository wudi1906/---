# Event Relay Hub | 事件中枢平台

## Pain | 客户痛点
- Third-party Webhooks (GitHub/Stripe/Notion/custom) use inconsistent payloads and signature algorithms, making maintenance fragile.  /  第三方 Webhook（GitHub、Stripe、Notion、自定义服务）格式与签名算法各异，导致维护成本高、易出错。
- Missing visibility: no dashboards, retries, or DLQ reports; support teams cannot locate failures quickly.  /  缺少可视化、重试与 DLQ 报告，支持团队难以及时定位失败事件。
- Replaying or forwarding events requires ad-hoc scripts, risking duplicates or data loss.  /  事件重放/转发依赖临时脚本，容易出现重复或丢失。

## Solution | 解决方案
- Unified intake supporting GitHub / Stripe / Slack / custom sources with signature templates and visual toggles.  /  支持多源接入并内置签名模板，可视化启停管理。
- Event persistence (SQLite/PostgreSQL), idempotent handling, exponential backoff, DLQ, search, replay, batch forwarding.  /  事件持久化、幂等处理、指数退避、DLQ、检索与批量重放/转发。
- Operational console + REST APIs showing success rate, latency, error breakdown, and Prometheus metrics.  /  控制台 + API 同步呈现成功率、延迟、错误类型，并输出 Prometheus 指标。
- Field mapping & workflows push events to internal services, message queues, or external vendors.  /  字段映射与编排可将事件推送至内部服务、消息队列或第三方平台。

## Deliverables | 交付清单
- **Live Demo | 在线演示**: `http://localhost:8202`（附示例事件，一键导入）。
- **Operations Console | 运维控制台**: `/console/events` 过滤/分页/批量重放；`/console/signatures` 管理签名模板。
- **Docs & APIs | 文档与接口**: Swagger (`/api/docs`)、Postman 集合、部署指南、告警策略、环境变量模板。
- **Reports | 智能报表**: 成功率/延迟统计、DLQ 审计、Prometheus + Grafana 集成手册。
- **Source & Docker | 源码与 Docker**: FastAPI 后端、队列/转发模块、Tailwind 仪表盘、Docker Compose。

**Quick Start | 快速开始**
```bash
cd event-relay-hub
./start.ps1   # Windows
# 或
./start.sh    # Linux / Mac
```
10 秒后访问 `http://localhost:8202`；控制台提供示例事件导入/重置按钮。

## Timeline | 交付周期
1. **Discovery (Day 0)** — Confirm event sources, signature schemes, forwarding targets, SLA, deployment scope.  /  确认事件来源、签名算法、转发目标、SLA 与部署范围。
2. **PoC Demo (Day 3-5)** — Showcase dashboard, alert pipeline, DLQ replay loop with sample data.  /  PoC 演示仪表盘、告警链路与 DLQ 重放。
3. **Hardening (Day 6-12)** — Connect production sources, configure retry/rate limit, finalize logging & metrics.  /  接入真实源、配置重试/限流，完善日志与监控。
4. **Launch & Training (Day 12+)** — Deliver source, runbooks, emergency plan, and joint acceptance.  /  提交源码、运维手册、应急预案，协助验收上线。

## SLA | 服务保障
- <1 hour response, kickoff within 24h.  /  首次响应 <1 小时，24 小时内启动项目。
- WCAG 2.1 AA dashboard, keyboard accessible, dark mode, RTL-friendly.  /  符合 WCAG 2.1 AA，支持键盘、暗色与 RTL。
- Idempotent pipeline with retry/backoff, DLQ, structured logging, Prometheus metrics.  /  幂等处理、重试退避、DLQ、结构化日志与 Prometheus 指标。
- Credentials isolated in `.env`, deployable in VPC/Kubernetes, optional private network tunnel support.  /  凭据独立 `.env`，支持 VPC/K8s 部署，可选内网穿透支持。

## KPI | 成功指标
- Go live with 3 core sources within 1 week; forwarding success rate ≥99.9%.  /  1 周内上线 3 个核心来源，转发成功率 ≥99.9%。
- Average event latency <300ms; troubleshooting time reduced by 80%.  /  平均事件延迟 <300ms，故障定位时间缩短 80%。
- Sustain 100k+ events/day with full audit trail.  /  单日支撑 10 万级事件并保持完整审计。

## FAQ | 常见问题
- **Support private network sources? / 支持内网或专线来源吗？**  \
  Yes—Premium package assists with VPC/K8s deployment and network tunneling.  /  是，进阶套餐可协助 VPC/K8s 部署与内网穿透。
- **Field mapping & filtering? / 支持字段映射与过滤吗？**  \
  Standard tier provides JSONPath/regex; Premium enables custom scripting & multi-target orchestration.  /  Standard 支持 JSONPath/正则过滤，Premium 提供自定义脚本与多目标编排。
- **Prevent duplication or loss? / 如何避免重复或丢失？**  \
  Built-in idempotency keys, retry, DLQ, and audit logs; optional RabbitMQ/Kafka integration.  /  内置幂等键、重试、DLQ 与审计日志，可选 RabbitMQ/Kafka 增强。

## CTA | 立即行动
- 📧 [Book a Demo](mailto:you@example.com?subject=Event%20Relay%20Hub%20Consultation) / 邮件预约演示
- 🗂 [Portal Overview](http://localhost:8101) / 门户导航与实时状态
- 📑 [Test Playbook](../PORTFOLIO_TEST_GUIDE.zh.md) / 验证剧本（中英对照）
- 🚀 [Local Demo](http://localhost:8202) / 本地体验入口

**Last Updated | 最近更新**：2025-11-03

