# Portfolio Test Playbook | 作品集测试指南

> **Goal | 目的**: Help reviewers experience all six projects in 15–30 minutes with consistent scripts and bilingual cues.  /  在 15–30 分钟内用统一脚本体验全部六个项目，便于内外部评审。
> **Preflight | 前置准备**: Run `.\\start-all.ps1`, verify `TEST_ALL.bat` 显示 6/6 [OK]，浏览器全屏 F11、缩放 100%。

---

## Portal Overview | 门户总览 (`http://localhost:8101`)
- Toggle top-right language switch (`中文` / `English`); preference stored in URL/localStorage.  /  右上角语言切换器支持中文/英文并记忆偏好。
- Project matrix cards display USP, metrics, highlights, CTA (Live Demo / API / Import / Reset).  /  卡片包含卖点、指标、亮点与 CTA。
- Health bar应 6 个绿点：8101~8606；异常端口会弹出重试提示。  /  健康状态 6 个绿点，异常时显示提示。
- `Import Demo`/`Reset Demo` buttons call seed/reset API；Portal 控制台同步写入日志。  /  导入/重置按钮调用后端，并在日志区显示结果。

---

## P1 Global Price Sentinel — 电商价格监控 (Port 8101)
- **Tech | 技术**: Python · FastAPI · Playwright · SQLite
- **Value | 价值**: 多站点价格采集、阈值告警、HTML/PDF 报告。

### Quick Tour | 快速体验 (~5 min)
1. Portal → Card CTA `Import Demo` 导入样例任务。 / 导入示例数据。
2. 打开 `http://localhost:8101/monitor/settings`，左右切换语言验证配置表单。  /  Switch between CN/EN on settings page.
3. Inspect "任务运行态" 面板，修改调度/代理/告警参数并保存、触发 Email/Slack/Webhook 测试。 /  Edit scheduling & alert channels and trigger test buttons.
4. 返回 Portal → `http://localhost:8101/reports/latest.html` 查看最新 HTML 报告。 /  Review the generated price report.

### Seed Suggestions | 种子增强
- 5 Products × 3 Sites × 30 Days 历史价格 + 3 条告警样例 + 2 份 HTML 报告。 / 更多 SKU/站点/告警示例。
- 实现位置：`global-price-sentinel/app/monitor.py` 与 `reporter.py`。 / Extend demo generation scripts.

---

## P2 Event Relay Hub — Webhook 中枢 (Port 8202)
- **Tech | 技术**: Python · FastAPI · HMAC · SQLite
- **Value | 价值**: 统一接入 Stripe/GitHub/Slack，自带签名校验、DLQ、重放与可视化。

### Quick Tour | 快速体验 (~5 min)
1. Portal → `Import Demo` 注入示例事件。 / Seed sample events.
2. 打开 `http://localhost:8202` 切换语言，查看卖点卡片与 Endpoint 列表。 / Review localized landing page.
3. 测试 `/api/docs`、`/console/events`、导入/重置弹窗（语言随切换更新）。
4. Portal 健康指示需转为绿色；若灰色检查服务或 CORS。 / Ensure health dot turns green.

### Seed Suggestions | 种子增强
- 200 events across Stripe/GitHub/Slack with success/retry/DLQ 状态与延迟分布。 / Enrich dataset for analytics.
- 扩展 `tests/` 覆盖字段映射、重放流程。 / Add unit/integration tests.

---

## P3 SaaS Northstar Dashboard — SaaS 指标仪表盘 (Port 8303)
- **Tech | 技术**: Next.js · React · Tailwind · Chart.js
- **Value | 价值**: MRR/ARR/Churn/LTV 可视化，CSV 导入向导与自动报表。

### Quick Tour | 快速体验 (~5 min)
1. Portal → `Import Demo` 加载 B2B SaaS 模板。 / Seed demo metrics.
2. 打开 `http://localhost:8303?lang=en`，查看 KPI 卡片、趋势图、Language Switcher。 / Inspect localized dashboard.
3. 访问 `/import`，按步骤完成 Template → Upload → Mapping → Preview；确认提示随语言变化。 / Walk through import wizard.
4. 调用 `/api/docs` 与 `/api/datasets` 验证 API；Portal 健康指示需保持绿色。

### Seed Suggestions | 种子增强
- 12 个月 × B2B/B2C 模板 + CSV 示例 + Scheduled Export。 / Provide full-year datasets and export schedule.

---

## P4 Doc Knowledge Forge — 文档知识库 (Port 8404)
- **Tech | 技术**: FastAPI · SQLite FTS5 · PyMuPDF
- **Value | 价值**: 批量导入 PDF/DOCX/TXT → Markdown → 全文检索/标签/导出。

### Quick Tour | 快速体验 (~5 min)
1. Portal → `Import Demo` 上传示例文档。 / Seed demo docs.
2. 访问 `http://localhost:8404?lang=zh`，测试语言切换、搜索高亮、目录树。 / Validate localized experience.
3. 在 “文档接入与转换” 导入/重置样例；在右侧控制台下载 Markdown/ZIP。 / Try upload/reset & export.
4. 查看“知识运营控制台” API/Exports 快捷入口。 / Open API/Export shortcuts.

### Seed Suggestions | 种子增强
- 20+ 文档（策略/指南/FAQ/设计稿）+ 标签/作者/更新时间。 / Expand library variety.
- 增加 “Insight” 案例说明向量检索/OCR 加值。 / Document optional AI upgrades.

---

## P5 A11y Component Atlas — 可访问性组件库 (Port 8505)
- **Tech | 技术**: React · Storybook 8 · Radix UI · Tailwind
- **Value | 价值**: WCAG 2.1 AA 组件（Button/Input/Modal/Tabs/Menu）+ vitest-axe 检查。

### Quick Tour | 快速体验 (~5 min)
1. 运行 `npm run storybook` (默认 8505，端口占用自动升至 8506)。 / Launch Storybook locally.
2. 使用工具栏 Language (🌐) 切换英文/中文；观察 Button/Menu/Modal/Tabs 文案联动。 / Verify globe toolbar toggles locales.
3. 打开 Docs + Canvas 确认 `useI18n` 正常（无错误提示）。 / Ensure no provider errors.
4. 如需运行测试：`npm test`（vitest-axe）确保无无障碍回归。 / Optional vitest run.

### Seed Suggestions | 种子增强
- 为更多组件补充示例及翻译，如 Input、Menu。 / Add extra localized stories.
- 维护 `chromatic` / `lighthouse` 脚本确保视觉回归。 / Run visual regression pipeline.

---

## P6 Insight Viz Studio — 数据可视化工作室 (Port 8606)
- **Tech | 技术**: FastAPI · Pandas · ECharts
- **Value | 价值**: CSV/JSON/Excel → 智能图表推荐 → PNG/PDF 导出。

### Quick Tour | 快速体验 (~5 min)
1. Portal → `Import Demo` 导入销售/增长/营销数据集。 / Seed sample datasets.
2. 打开 `http://localhost:8606?lang=en`，体验上传 CSV、拖拽编排、主题切换。 / Try upload + layout.
3. 实测 PNG/PDF 导出按钮（确保 <2s 返回）；查看 Dataset Console 列表。 / Validate export speed & dataset list.
4. 切换至 `?lang=zh` 验证落地页与提示语。 / Check localized strings.

### Seed Suggestions | 种子增强
- 增补营销/财务/用户维度模板 + weekly/monthly 模板。 / Add more templates & report layouts。

---

## Link & Flow Audit | 链接与交互审计
- 所有 Live Demo / Docs / API 链接均应打开对应端口；检查 404 或跨域。 / Verify each CTA resolves correctly.
- 控制台导入/重置按钮执行后需提示成功/失败。 / Ensure toast messages show success/error.
- Portal 快速导航需一眼看到 6 项目；若屏幕较小可折叠滚动条截图。 / Confirm all cards visible for hero screenshot.

---

## Presentation Tips | 展示建议
- **Screenshots | 截图建议**: Portal Hero、每项目核心看板、语言切换前后对比、Storybook Canvas。 / Capture portal, key dashboards, language toggle, Storybook.
- **Video Script | 视频脚本**: 录制 Portal → P1/P3/P4/P6 快速操作流程（导入/切换语言/导出）。 / Record sequential walkthrough focusing on import/export and localization.
- **Data Reset | 数据重置**: 展示 `Reset Demo` 后再次 `Import Demo`，证明流程稳定。 / Show reset + re-import stability.

---

## Appendix | 附录
- `start-all.ps1` / `stop-all.ps1` / `TEST_ALL.bat` — 环境启动、停止、健康检查脚本。 / One-click ops scripts.
- `screenshots/shotlist.md` — 详细截图/录屏脚本。 / Detailed capture checklist.
- `PORTFOLIO_TEST_GUIDE.zh.md` 保留此双语版本即可取代旧版中文脚本。 / This bilingual playbook supersedes previous notes.

**Last Updated | 最近更新**：2025-11-03
