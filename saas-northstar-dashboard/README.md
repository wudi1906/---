# SaaS Northstar Dashboard · SaaS 指标看板解决方案

[English Version](./README.en.md) | 中文版本

> **适用对象**：SaaS 创业者、增长团队、运营/财务分析师
>
> **核心卖点**：5 分钟导入数据，全天候可视化 MRR/ARR/Churn/LTV，支持团队协作与报告导出。

---

## 1. 背景与痛点 · Background & Pain
- 指标散落在 Stripe / Paddle / CRM / 财务表格，决策时难以聚合。
- 自建看板需要持续维护可视化、权限、可访问性，投入高。
- 每周/月 KPI 报告需手动整理，低效且易出错。

## 2. 解决方案 · Solution & Value
- 内置 B2B SaaS / B2C Growth 两套 KPI 模板，支持自定义字段映射与扩展。
- 多 CSV 导入向导（模板选择 → 上传 → 字段映射 → 预览），实时计算 MRR/ARR/Churn/CAC/LTV。
- 可访问性优先、暗色/浅色双主题，图表内置配色规范与导出 PNG / PDF（打印友好）。
- 数据校验与异常提示，避免因空值/币种错误导致指标失真；支持渠道获客与流失对比分析。

## 3. 交付清单 · Deliverables
- 🖥️ **Live Demo**：`http://localhost:8303`（含示例数据与 KPI 模板切换）。
- 📥 **多步导入中心**：`http://localhost:8303/import`，支持多 CSV 上传、自动匹配字段、预览校验。
- 📦 **源代码与部署脚本**：Next.js 14、Tailwind、Zustand 状态库、Docker/Vercel 配置。
- 📕 **使用文档**：部署指南、指标字典、导出流程、KPI 模板说明、字段映射手册。
- 🧪 **API / Postman**：`http://localhost:8303/api/templates`、`/api/import`、`/api/exports` 等接口及 `postman/saas_northstar_dashboard.postman_collection.json`（含导入→校验→导出闭环场景）。

## 4. 实施流程与周期 · Process & Timeline
1. **需求澄清（Day 0）**：确认指标范围、币种、数据源格式、协作角色、部署方式。
2. **PoC 演示（Day 2-4）**：提供 Demo（含示例数据），确认指标与可视化模板。
3. **功能完善（Day 5-10）**：接入真实数据、配置导出/周报、完成部署。
4. **验收交接（Day 10+）**：核对 KPI、交付操作手册/培训录屏、提供回滚方案。

## 5. SLA 与质量保证 · SLA & Quality
- < 1 小时响应，24h 内安排 Kick-off，按套餐提供 7~30 天支持。
- 仪表盘符合 WCAG 2.1 AA，支持键盘导航、屏幕阅读器、RTL 布局。
- 内置结构化日志、慢查询追踪、指标校验；导出速度 < 1s（标准数据量）。
- 部署可选 Vercel/Render/Docker，本地 `.env.local` 管理密钥，提供安全加固建议。

## 6. KPI / 成功指标占位 · KPI & Outcomes
- 3 天内交付在线看板，首轮会议即展示关键指标。
- 指标准确率 ≥ 99%，报告生成时间从小时级缩短到分钟级。
- 团队协作效率提升 2×，投资人/董事会汇报周期稳定。

## 7. 常见问题 · FAQ
**Q1：数据源只支持 CSV 吗？**  
A：Basic/Standard 默认 CSV；Premium 可对接 Stripe/Paddle/Chargebee/自定义 API，实现定时同步。

**Q2：团队成员如何协作？**  
A：Standard 起提供多用户角色管理；Premium 支持 SSO、权限分级与多租户。

**Q3：如何保障数据安全？**  
A：可部署在客户云环境，敏感信息保存在 `.env.local`，提供访问控制与安全审计建议。

## 8. CTA · 下一步行动
- 🔵 [Upwork · 立即咨询](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr · 套餐下单](https://www.fiverr.com/yourname)
- 📧 [Email · 预约演示](mailto:you@example.com?subject=SaaS%20Northstar%20Dashboard%20Consultation)
- 🚀 [本地 Demo · 立即体验](http://localhost:8303)

> “打造属于你的 SaaS 北极星指标看板，从数据到洞察只需一步。”

---

## 9. KPI 模板与导入流程指南
- **模板选择**：B2B SaaS 聚焦 MRR/ARR/Churn/LTV，B2C 面向订单/获客；可在首页下拉快速切换。
- **导入步骤**：模板 → 上传 CSV → 字段映射 → KPI/图表预览；所有步骤具备键盘导航与语义化反馈。
- **字段映射**：系统自动匹配同名列，可手动调整；支持查看示例 CSV，避免格式错误。
- **图表导出**：每个图表支持 PNG 下载与 PDF（浏览器打印）导出，便于周报/投资人分享。
- **API**：`GET /api/templates` 返回可用 KPI 模板及字段要求，便于自建脚本或外部工具对接。

## 10. 本地启动与测试 · Local Setup
- **安装依赖**：在 `saas-northstar-dashboard` 目录执行 `npm install`（依赖 `better-sqlite3`，需 Node.js ≥ 18）。
- **开发启动**：`npm run dev`，默认监听 `http://localhost:8303`。
- **运行测试**：`npm test`（Vitest，将校验导入计算逻辑与导出流程）。
- **数据库位置**：导入记录保存在 `data/dashboard.db`，可删除该文件以重置环境。
- **Postman 场景**：导入集合 `postman/saas_northstar_dashboard.postman_collection.json`，顺序执行“导入样例数据 → 查询最新导入 → 导出 CSV/Excel”即可验证全链路。

## 11. 故障排查 · Troubleshooting
- **导入返回 400**：检查必填数据集是否遗漏或未映射字段（接口将返回对应提示）。
- **警告较多**：API 仅跳过格式错误的行，下载导出文件可查看完整告警并修正源数据。
- **导出 404**：需先成功调用 `POST /api/import`；若多次导入，可使用 `GET /api/import/latest` 确认最新记录时间。
- **better-sqlite3 编译失败**：确保本地具备 Node.js 预编译二进制（Windows x64）或在具备构建工具链的环境下安装。
- **前端未刷新 KPI**：导入成功后仪表盘会自动更新，如仍展示旧数据，可执行浏览器硬刷新或再次调用导入接口。

