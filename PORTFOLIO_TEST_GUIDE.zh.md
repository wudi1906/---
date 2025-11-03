# 作品集（6 项目）功能讲解与测试指南

> 目的：帮助你或任何评审者在 15–30 分钟内系统体验全部能力；也可作为你讲解时的脚本。
>
> 前置：已运行 `.\\start-all.ps1`，`TEST_ALL.bat` 显示 6/6 [OK]；浏览器全屏 (F11)、缩放 100%。

---

## 总览
- 端口与角色：
  - P1 Global Price Sentinel — 8101（同时提供主入口 Portal 与 API/页面）
  - P2 Event Relay Hub — 8202
  - P3 SaaS Northstar Dashboard — 8303
  - P4 Doc Knowledge Forge — 8404
  - P5 A11y Component Atlas（Storybook）— 8505
  - P6 Insight Viz Studio — 8606
- 首页（Portal）：`http://localhost:8101`，包含：
  - 健康状态（6 绿点）
  - 快速导航（6 个项目）
  - 每卡片：USP 概要、指标卡、亮点清单、CTA（Live Demo / API / Import / Reset）

---

## P1 Global Price Sentinel（电商价格监控）
- 技术：Python / FastAPI / Playwright / SQLite
- 价值：多站点采集、阈值告警、对比报告（HTML/PDF）。

### 快速体验（5 分钟）
1. 打开 `http://localhost:8101` → 项目卡片 P1 → 点击 “Live Demo”。
2. 另开标签页（端口仍 8101）：
   - `http://localhost:8101/api/docs` 查看 API。
   - `http://localhost:8101/monitor/settings` 查看调度/代理/告警配置界面（如有）。
3. 回到 Portal → 点击 P1 “Import Demo”，2s 内提示成功。
4. 访问 `http://localhost:8101/reports/latest.html` 查看最新比价报告（折线/表格）。

### 功能点
- YAML 目标配置、抓取任务调度、代理池、阈值告警（Email/Webhook）、历史对比报告生成。

### 种子数据增强建议
- 5 个产品 × 3 站点 × 30 天价格轨迹；3 条阈值告警样例；2 份 HTML 报告快照。
- 位置：`global-price-sentinel/app/monitor.py` & `reporter.py`（新增 demo 生成函数）。

---

## P2 Event Relay Hub（Webhook 中枢/签名校验/重试与死信）
- 技术：Python / FastAPI / HMAC / SQLite
- 价值：统一接入 Stripe / GitHub / Slack 等事件，签名校验、条件路由、失败重试与 DLQ、可视化控制台。

### 快速体验（5 分钟）
1. Portal → P2 “Import Demo”。
2. 打开 `http://localhost:8202`（落地页）→ 顶部进入：
   - `http://localhost:8202/console/events` 事件控制台（应有多来源事件、状态、筛选）。
   - `http://localhost:8202/console/signatures` 签名设置。
3. `http://localhost:8202/api/docs` 查看 API。

### 种子数据增强建议
- 200 条事件：3 个来源（Stripe/GitHub/Slack）、多状态（成功/重试/死信），并带延迟/错误码分布。
- 增强 `tests/` 内验证用例，配合控制台过滤演示。

---

## P3 SaaS Northstar Dashboard（SaaS 指标仪表盘）
- 技术：Next.js / React / Tailwind / Chart.js
- 价值：开箱即用的北极星指标（MRR、NRR、留存、NPS），模板化导入与导出。

### 快速体验（5 分钟）
1. Portal → P3 “Import Demo”。
2. 打开 `http://localhost:8303`：应见 4 个指标卡、趋势图；
3. `http://localhost:8303/import`：CSV 导入向导（选择 B2B/B2C/Ecom 模板）。
4. `http://localhost:8303/api/health`：健康检查（已加 CORS 头）。

### 种子数据增强建议
- 12 个月 × 3 方案模板（B2B/B2C/Ecom）：MRR、ARR、NRR、活跃用户、留存、NPS；含 2 个对照分组。
- 预置 3 份 CSV 示例，导入后即时渲染 4 张图与 1 个对比表。

---

## P4 Doc Knowledge Forge（文档知识库/全文检索）
- 技术：Python / FastAPI / SQLite FTS / PyMuPDF
- 价值：批量上传 → Markdown 化 → 关键词/摘要 → 全文检索与高亮 → 在线浏览。

### 快速体验（5 分钟）
1. Portal → P4 “Import Demo”。
2. 打开 `http://localhost:8404`：顶部英雄区展示 USP、指标卡、三步工作流；底部导航按钮直接跳转到检索 / 上传 / 结果板块。
3. 在“Full-Text + Semantic Search”卡片输入 `policy`、`OKR` 等关键词 → 观察相关度评分、片段预览。
4. “Document Intake & Conversion” 区尝试导入/重置或查看上传进度；关注右侧“Knowledge Operations Console”的 API / Exports / Integrations。
5. 滚动到“Recent Uploads”板块 → 查看标签、时间、大小，必要时删除或下载 Markdown。

### 种子数据增强建议
- 20 份文档（政策/指南/FAQ/设计稿提取），每类 5 份；
- 附带标签/作者/更新时间元数据；搜索权重与命中率演示；
- Demo Seeds 可再补 3 条“知识运维 Insight”案例（如 Governance / Automation / Integration）。

---

## P5 A11y Component Atlas（可访问性组件库/Storybook）
- 技术：React / Radix UI / Storybook / Vitest
- 价值：WCAG 2.1 AA 组件示例与交互测试，便于快速落地 Design System。

### 快速体验（3 分钟）
1. 打开 `http://localhost:8505`（Storybook）。
2. 选择 Button/Input/Modal/Tabs，切换暗色主题；
3. 观察 toolbar 的可访问性检查（axe 插件如已启用）。

### 种子数据增强建议
- 为每个组件补齐：键盘操作说明、屏读文本（aria-* 示例）、失败/边界状态。

---

## P6 Insight Viz Studio（可视化报表工作室）
- 技术：Python / FastAPI / ECharts / Pandas
- 价值：从 CSV/JSON 快速生成品牌化图表与报告，支持模板、主题与定时导出。

### 快速体验（5 分钟）
1. Portal → P6 “Import Demo”。
2. 打开 `http://localhost:8606`：英雄区有卖点列表、三张指标卡、四步工作流，按钮直达上传区/图表画廊/数据集控制台。
3. 在 “Upload Data File” 卡片导入样例 CSV（或点击 Import Demo），随后 `loadDatasets()` 自动刷新表格。
4. “Smart Chart Gallery” 展示双图表：收入增长 + 留存折线面积图、品类贡献环形图；可作为截图素材。
5. “Dataset Console” 查看 Demo 文件列表；底部 “Use Cases & Templates” 了解场景话术。

### 种子数据增强建议
- 4 套图表模板（销售、运营、用户、财务），每套 3–4 张图；
- 2 份周报/⽉报导出模板与定时脚本样例；
- Demo Seeds 可增加更多 dataset（如 `sample_finance.csv`, `sample_marketing.csv`），刷新 Dataset Console 的丰富度。

---

## 链接与交互流审计
- 现状：所有 “Live Demo / API Docs / Import / Reset” 均在新标签页或当前卡片触发；不同端口是**独立服务**的体现，便于真实微服务/多技术栈演示。
- 改进建议：
  1) 为“Live Demo/Docs”保持 `target="_blank"`，避免用户离开 Portal；
  2) 提供“回到首页”固定浮动按钮；
  3) 选做：使用反向代理把 `/p1/*` `/p2/*` 聚合到 8101（Nginx/Traefik 或 Node 代理），形成“同域多子路径”。

---

## 常见问题与排查
- 绿点未亮：对应服务未起或 CORS（已为 P3 修复）。重启：`.\\stop-all.ps1` → `.\\start-all.ps1`。
- 页面空白：未导入 Demo。先点 Import，再刷新页面。
- 报表无数据：检查 seeds 是否写入（可看 DB 文件时间戳）。

---

## GitHub 展示与观感
- 可以公开展示本仓库；建议：
  - 顶部 README 添加 “项目矩阵 + 一键启动 + 5 分钟视频” 三要素；
  - 截图与视频仅呈现你的作品与功能，不出现第三方平台 Logo/链接；
  - License 可用 MIT；提交记录与注释保持“个人署名、一致风格、无外部品牌”。
- 观感预期：评审者可在 10 分钟内看到“从数据抓取/事件中枢/仪表盘/知识库/组件库/可视化”的**端到端交付能力**，证明技术深度与全栈落地力。

---

## 下一步落地（建议按优先级）
1) 种子数据增强（P1/P2/P3/P4/P6），让图表/控制台“开箱即亮眼”。
2) 统一返回按钮与顶部浮动导航，进一步提升导览效率。
3) 选做：把多端口经反向代理聚合为 8101 子路径，获得“单域项目”的浏览体验。
4) 为 P5 增补更多 A11y 场景与测试示例。

---

*最后更新：{{today}}*
