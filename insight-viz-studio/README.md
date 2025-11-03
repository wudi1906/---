# Insight Viz Studio

[English Version](./README.en.md) | 中文版本

数据可视化工具 - 上传 CSV/JSON 数据，自动生成交互式图表并导出。

---

## 1. 背景与痛点 · Background & Pain
- 业务团队需要快速输出报告，但手动制图耗时且不统一。
- 多格式（CSV/JSON/Excel）数据混用，导入易出错或需反复清洗。
- PNG/PDF/周报模板需要手动排版，品牌一致性难以保证。

## 2. 解决方案 · Solution & Value
- 上传 CSV/JSON/Excel，自动解析字段并推荐折线/柱状/饼图等合适图表。
- 拖拽式配置面板，实时预览交互式图表，支持主题、颜色、过滤器。
- 一键导出 PNG/PDF/SVG，内置周报/月报模板，保持品牌一致。
- 支持多语言、货币格式、万级数据性能优化，满足全球团队需求。

## 3. 交付清单 · Deliverables
- 🖥️ **Live Demo**：`http://localhost:8606`（含示例数据与导入脚本）。
- 📦 **源代码**：FastAPI 后端、Pandas 处理、ECharts 可视化、Docker Compose。
- 📕 **文档**：导入规范、图表配置指南、导出模板、API 文档。
- 🧪 **测试资产**：Postman 集合、单元/集成测试脚本、性能基准。
- 📁 **示例数据集**：`data/samples/`（sales.csv、user_growth.json、marketing.xlsx）。

## 4. 实施流程与周期 · Process & Timeline
1. **需求澄清（Day 0）**：确认数据源格式、图表类型、导出模板、品牌规范。
2. **PoC 演示（Day 2-4）**：提供 Demo（示例数据），验证图表推荐、导出体验。
3. **功能完善（Day 5-10）**：接入真实数据、配置主题、部署测试/生产环境。
4. **验收交接（Day 10+）**：交付代码与文档、培训、周报自动化脚本、回滚方案。

## 5. SLA 与质量保证 · SLA & Quality
- < 1 小时响应；按套餐提供 7~30 天支持与问题修复。
- 前端符合 WCAG 2.1 AA，对比度≥4.5:1、键盘可达、RTL/多语言。
- 性能优化：数据采样、虚拟滚动、Web Worker、懒加载，支持 50k+ 行。
- 导出模块基于 Puppeteer/wkhtmltopdf，提供跨平台部署与字体嵌入建议。

## 6. KPI / 成功指标占位 · KPI & Outcomes
- 5 分钟内生成首个可用图表，报告制作时间缩短 70%。
- PNG/PDF 导出耗时 < 2 秒，周报自动化命中率 ≥ 95%。
- 模板复用率提升 3×，团队协作满意度提升。

## 7. 常见问题 · FAQ
**Q1：支持实时数据或 API 接入吗？**  
A：Premium 套餐可对接数据库/API，支持定时刷新或实时推送。

**Q2：能否自定义导出模板？**  
A：提供模板引擎，可配置品牌色、Logo、封面，支持多语言与货币格式。

**Q3：如何处理敏感数据？**  
A：默认本地/私有部署，数据仅存于临时目录，可启用自动清理与脱敏策略。

## 8. CTA · 下一步行动
- 🔵 [Upwork · 立即咨询](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr · 套餐下单](https://www.fiverr.com/yourname)
- 📧 [Email · 预约演示](mailto:you@example.com?subject=Insight%20Viz%20Studio%20Consultation)
- 🚀 [本地 Demo · 立即体验](http://localhost:8606)

---

### 快速开始 · Quick Start

```powershell
pwsh .\scripts\start.ps1 --install
```

### 技术栈 · Tech Stack

- Python + FastAPI · Pandas/NumPy 数据处理
- ECharts 5 可视化 · Puppeteer / wkhtmltopdf 导出
- Vanilla JS + Tailwind CSS 前端

### 关键流程 · User Flow

1. 上传数据 → 2. 预览与清洗 → 3. 选择图表 → 4. 配置样式 → 5. 生成可视化 → 6. 导出报告

### API 概览 · Key Endpoints

- `POST /api/upload` — 上传数据文件
- `POST /api/chart` — 生成图表配置
- `POST /api/export/png|pdf` — 导出报告
- `GET /api/datasets` — 获取数据集列表

### 示例导出配置 · Export Config

```python
export_config = {
    "format": "png",
    "width": 1200,
    "height": 800,
    "quality": 90,
    "background": "transparent"
}
```

