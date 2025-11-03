# Event Relay Hub · Webhook 事件中台解决方案

[English Version](./README.en.md) | 中文版本

> **适用对象**：SaaS 平台、支付/物流聚合服务、需要统一管理多来源 Webhook 的技术团队
>
> **核心卖点**：多源接入 + 签名校验 + 转发队列 + 事件重放，一站式提升稳定性与可观测性。

---

## 1. 背景与痛点 · Background & Pain
- **第三方回调格式杂乱**：GitHub / Stripe / Notion / 自家服务格式不一，代码难维护。
- **签名验证与重试繁琐**：各自算法不同，失败难追踪，常漏单或重复。
- **缺少可视化与审计**：缺乏日志与告警，运营/售后无法快速定位问题。

## 2. 解决方案 · Solution & Value
- 一站式接入 GitHub / Stripe / Slack / 自定义源，自带签名模板，可视化启用/禁用。
- 事件持久化（SQLite / PostgreSQL），支持检索、重放、死信队列（DLQ）、速率限制。
- 仪表板 + API 双模式，可视化成功率、延迟、错误类型，支持导出报表。
- 字段映射与转发编排，将事件无缝推送至内网服务或第三方供应商。

## 3. 交付清单 · Deliverables
- 🖥️ **Live Demo**：`http://localhost:8202`（含示例事件，一键导入）。
- 📦 **源代码与 Docker 模板**：FastAPI 后端、队列/转发模块、Tailwind 仪表板。
- 📕 **文档套件**：部署指南、签名配置、告警策略、环境变量示例。
- 🧪 **API / Postman**：`http://localhost:8202/api/docs` 与 `postman/event_relay_hub.postman_collection.json`（内置“死信重放闭环”场景：重放失败→入 DLQ→批量重试→清空）。
- 🛠️ **运营控制台**：`http://localhost:8202/console/events` 支持筛选、分页、多选批量重放 / 删除 / 清空 DLQ；`/console/signatures` 管理签名模板。
- 📈 **运营报表模板**：成功率与延迟统计、DLQ 审计、Prometheus/Grafana 接入说明。
- 🛠️ **控制台页面**：
  - `http://localhost:8202/console/signatures` —— GitHub / Stripe / Custom 签名模板管理。
  - `http://localhost:8202/console/events` —— 最近事件、重放、死信队列查看与清理。

## 4. 实施流程与周期 · Process & Timeline
1. **需求澄清（Day 0）**：确认事件源、签名算法、转发目标、SLA、部署环境。
2. **PoC 演示（Day 3-5）**：交付 Demo（含示例事件/仪表板），联调签名与告警。
3. **功能完善（Day 6-12）**：接入真实源、配置重试/限流、部署测试/生产。
4. **验收交接（Day 12+）**：交付源代码、日志方案、应急预案，联合验收。

## 5. SLA 与质量保证 · SLA & Quality
- **响应承诺**：< 1 小时回复，24h 内安排项目启动会议。
- **可访问性**：仪表板符合 WCAG 2.1 AA，支持键盘导航、暗色模式、RTL。
- **性能与可靠性**：幂等处理 + 指数退避重试 + 死信队列，结构化日志与指标。
- **安全与合规**：签名严格校验、凭证在 `.env` 管理，可部署于你的 VPC。
- **交付后支持**：依套餐提供 7~30 天远程支持与运营陪跑。

## 6. KPI / 成功指标占位 · KPI & Outcomes
- 1 周上线 3 个关键源，目标转发成功率 ≥ 99.9%。
- 平均事件延迟 < 300ms，错误定位时间缩短 80%。
- 支持每日 10 万+ 事件吞吐，具备完整审计链路。

## 7. 常见问题 · FAQ
**Q1：是否支持内网/专线源？**  
A：支持部署在你的 VPC / Kubernetes，Premium 套餐可协助配置内网穿透或代理。

**Q2：可做字段映射或过滤吗？**  
A：Standard 起支持 JSONPath/正则过滤；Premium 可提供自定义脚本与多目标编排。

**Q3：如何确保事件不丢不重？**  
A：默认启用幂等校验、重试策略、DLQ，并输出审计日志；可选 RabbitMQ/Kafka 增强。

## 8. CTA · 下一步行动
- 🔵 [Upwork · 立即咨询](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr · 套餐下单](https://www.fiverr.com/yourname)
- 📧 [Email · 预约演示](mailto:you@example.com?subject=Event%20Relay%20Hub%20Consultation)
- 🚀 [本地 Demo · 立即体验](http://localhost:8202)

> “把散乱的 Webhook 管理交给事件中台，让你的团队专注业务迭代。”

---

## 9. 签名预设与死信控制台
- **签名管理**：访问 `http://localhost:8202/console/signatures`，可视化设置 GitHub / Stripe / Custom 的密钥与签名头部；启用后强制校验，未启用时沿用 `.env` 变量或开发模式。
- **事件控制台**：`http://localhost:8202/console/events` 展示最近事件、手动重放表单、DLQ 列表，可直接重试或删除死信。
- **API**：
  - `GET /api/signatures`、`PUT /api/signatures/{source}` —— 管理签名模板。
  - `POST /api/signatures/{source}/test` —— 基于当前模板生成示例签名头，便于 Postman/CI 联调。
  - `GET /api/dlq`、`POST /api/dlq/{id}/replay`、`DELETE /api/dlq/{id}` —— 死信读取与清理。
  - `POST /api/events/replay/batch`、`POST /api/dlq/replay/batch`、`POST /api/dlq/clear` —— 批量重试与一键清空操作。
- **兼容性**：若 `.env` 中已有 `*_WEBHOOK_SECRET`，仍可作为回退方案；当模板启用并设置密钥时将优先使用（不会在 API 中回显明文）。

## 10. 本地启动与测试 · Local Setup
- **一键启动**：在仓库根目录执行 `./启动所有项目.ps1`，自动拉起本项目与其他作品。单独启动可运行 `cd event-relay-hub && ./.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8202`。
- **运行单元测试**：`cd event-relay-hub && ./.venv/Scripts/python.exe -m pytest`（当前 19/19 通过，包含批量重放、DLQ 生命周期、签名测试等用例）。
- **导入 Postman 集合**：使用 `postman/event_relay_hub.postman_collection.json`，保留默认环境变量：
  - `baseUrl = http://localhost:8202`
  - `failureTarget = http://127.0.0.1:65535/webhook`（强制连接失败，验证死信流程）
  - `successTarget = https://example.com/webhook`（示例成功目标，可按需替换）
- **执行“死信重放闭环”场景**：顺序运行 Step 1~8，可验证“重放失败→写入 DLQ→批量重放→清空”全链路，脚本将自动写入 `eventId` / `dlqId`。
- **签名模拟**：在 Postman 中调用“生成测试签名头”请求或访问控制台“测试签名”按钮，内容与 README 保持一致，便于第三方回放。

### 10.1 可访问性与前端校验
- 控制台遵循 WCAG 2.1 AA：键盘可达、aria-live 提示、对比度≥4.5。
- 批量按钮在请求期间自动禁用并显示 `aria-busy`，Toast 使用 polite 区域播报。
- 筛选条件与分页尺寸保存在 `localStorage`，刷新后自动恢复，避免误操作。

### 10.2 数据维护建议
- 默认数据库为 `event-relay-hub/event_hub.db`（SQLite）。若需重置，可删除该文件或调用 `POST /api/demo/reset`。
- Demo 导入使用 `POST /api/demo/seed`，默认写入近 7 天示例事件及模拟转发日志。

## 11. 故障排查 · Troubleshooting
- **批量重放部分失败**：API 会返回 `failed` 字典，例如 `Duplicate id ignored`。根据提示重新选择未成功的 ID，或确认事件是否已删除。
- **签名测试返回 400**：确保目标模板已启用且配置密钥；可通过控制台或 `PUT /api/signatures/{source}` 更新后再调用 `POST /api/signatures/{source}/test`。
- **DLQ 清空提示 0 条**：可能是重放成功后已自动删除，或数据库已被 `reset`。可通过 `GET /api/dlq` 验证当前状态。
- **429 速率限制**：默认 60 req/min，可在 `.env` 设置 `RATE_LIMIT_PER_MINUTE` 或配置 Redis 共享限流。
- **依赖告警**：FastAPI / SQLAlchemy 的 DeprecationWarning 属上游提醒，当前行为已在 pytest 验证，通过升级框架即可消除。

