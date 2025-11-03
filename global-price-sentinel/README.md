# Global Price Sentinel · 电商价格监控旗舰方案

[English Version](./README.en.md) | 中文版本

> **适用对象**：跨境电商团队、品牌出海运营、竞品/渠道运营经理
>
> **核心卖点**：全天候价格监控、自动告警、趋势报告，交付最快 3 天上线。

---

## 1. 背景与痛点 · Background & Pain
- **SKU 多、平台多**：人工更新表格易漏价，无法实时追踪促销。
- **响应滞后**：竞争对手调价或库存变化，团队无法在小时级内反应。
- **缺少趋势洞察**：历史数据零散，无法支撑定价决策和利润评估。

## 2. 解决方案 · Solution & Value
- 自动化抓取 Amazon / 京东 / 淘宝 等多站点，同步对比多地区价格。
- 配置化阈值告警（Email / Webhook / Slack），分钟级推送负责人，支持多渠道并行触达。
- 可视化控制台 + 周报/月报（HTML / CSV），输出策略级趋势洞察。
- 代理池 + 重试机制 + 审计日志，全天候稳定运行并可追溯，支持启停与动态凭证。

## 3. 交付清单 · Deliverables
- 🖥️ **Live Demo**：`http://localhost:8101`（含示例数据，可一键导入）。
- ⚙️ **配置中心**：`http://localhost:8101/monitor/settings`，可视化配置调度、代理池与告警渠道。
- 📦 **源代码与安装脚本**：FastAPI 后端、Playwright 抓取、Tailwind UI 控制台。
- 📕 **文档套件**：部署指南、操作手册、告警配置说明、环境变量模板。
- 🧪 **Postman / API Docs**：`http://localhost:8101/api/docs` 与 Postman Collection。
- 📊 **报告模板**：HTML/PDF 周报、CSV 明细、Prometheus/Grafana 接入说明。

## 4. 实施流程与周期 · Process & Timeline
1. **需求澄清（Day 0）**：确认站点/SKU、告警阈值、部署环境、团队分工。
2. **原型演示（Day 2-4）**：交付 Demo（含示例数据），验收抓取准确率与告警逻辑。
3. **功能完善（Day 5-10）**：接入真实数据源、部署到指定环境、导入历史数据。
4. **验收交接（Day 10+）**：交付源代码/文档、培训、上线支持，准备回滚预案。

## 5. SLA 与质量保证 · SLA & Quality
- **响应承诺**：< 1 小时内回复、24h 内安排 Kick-off。
- **可访问性**：控制台符合 WCAG 2.1 AA，支持键盘操作、暗色模式、RTL。
- **性能与监控**：抓取失败自动重试，Prometheus 指标、结构化日志、慢请求追踪。
- **安全与合规**：凭证写入 `.env`，仅抓取公开页面，支持 GDPR 配置，日志可脱敏。
- **交付后支持**：按套餐提供 7~30 天远程支持与问题修复。

## 6. KPI / 成功指标占位 · KPI & Outcomes
- 3 周交付 MVP，上线后自动化覆盖 ≥ 20 SKU。
- 告警延迟 < 5 分钟，抓取成功率 ≥ 99%。
- 人力成本降低 30%，策略会议输入的价格洞察翻倍。

## 7. 常见问题 · FAQ
**Q1：支持登录站点或复杂反爬吗？**  
A：支持。可集成账号登录、验证码识别、代理池，高级套餐内含。

**Q2：告警渠道有哪些？**  
A：通过配置中心启用 Email / Webhook / Slack，可扩展 Teams、企业微信，并支持多渠道并行通知与日志记录。

**Q3：部署在自有环境安全吗？**  
A：提供 Docker 模板与加固建议，凭证独立管理，可选托管到你的 VPC 或 Render/Fly.io。

## 8. CTA · 下一步行动
- 🔵 [Upwork · 立即咨询](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr · 套餐下单](https://www.fiverr.com/yourname)
- 📧 [Email · 预约演示](mailto:you@example.com?subject=Global%20Price%20Sentinel%20Consultation)
- 🚀 [本地 Demo · 立即体验](http://localhost:8101)

> “价格监控，不再是繁琐任务。让系统替你盯住竞品，把时间用在策略与增长上。”

---

## 9. 配置中心 · Monitor Settings
- **访问入口**：`http://localhost:8101/monitor/settings`
- **调度模式**：支持 Cron 与自定义间隔（5-1440 分钟），保存后将作用于下次任务执行（定时调度需重启以应用新的计划）。
- **任务运行态看板**：新增「任务运行态」卡片，展示下次运行时间、倒计时、最近执行日志（成功/失败/耗时/消息），方便运营快速排障。
- **代理池管理**：可视化启停代理池，配置服务器与凭证即刻生效，用于应对风控与分布式抓取。
- **告警渠道**：勾选 Email / Slack / 自定义 Webhook，多渠道并行推送，所有告警会写入 `alert_logs` 表供审计；每个渠道旁新增“一键测试”按钮，便于校验 SMTP/Webhook 连通性。
- **API**：
  - `GET /api/config/monitor` 读取调度/代理/告警配置。
  - `PUT /api/config/monitor` 更新配置。
  - `GET /api/scheduler/status` 查询调度任务状态与最近执行日志。
  - `POST /api/alerts/test` 测试单一渠道（email/slack/webhook），返回 success / message / detail。
