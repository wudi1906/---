# Insight Viz Studio — Data Visualization Tool

> **Target Audience**: Business teams needing quick chart reports but lacking coding skills
>
> **Core Value**: Upload CSV/JSON → auto-generate interactive charts → export PNG/PDF, first chart in 5 minutes

[中文版本 Chinese Version](./README.md)

---

## 1. Pain Points

- Business teams need to output reports quickly, but manual charting is time-consuming and inconsistent
- Multiple formats (CSV/JSON/Excel) mixed use, import errors or requires repeated cleaning
- PNG/PDF/weekly report templates need manual layout, brand consistency hard to guarantee

## 2. Solution & Value

- Upload CSV/JSON/Excel, auto-parse fields and recommend suitable charts (line/bar/pie, etc.)
- Drag-and-drop config panel, real-time preview interactive charts, support themes, colors, filters
- One-click export PNG/PDF/SVG, built-in weekly/monthly report templates, maintain brand consistency
- Support multi-language, currency formats, 10k+ data performance optimization, meet global team needs

## 3. Deliverables

- 🖥️ **Live Demo**: `http://localhost:8606` (with sample data and import scripts)
- 📦 **Source Code**: FastAPI backend, Pandas processing, ECharts visualization, Docker Compose
- 📕 **Documentation**: Import specifications, chart config guide, export templates, API docs
- 🧪 **Test Assets**: Postman collection, unit/integration test scripts, performance benchmarks
- 📁 **Sample Datasets**: `data/samples/` (sales.csv, user_growth.json, marketing.xlsx)

## 4. Timeline & Process

1. **Requirements Clarification (Day 0)**: Confirm data source formats, chart types, export templates, brand guidelines
2. **PoC Demo (Day 2-4)**: Provide demo (sample data), validate chart recommendations, export experience
3. **Feature Completion (Day 5-10)**: Connect real data, configure themes, deploy test/production environments
4. **Acceptance & Handover (Day 10+)**: Deliver code and docs, training, weekly report automation scripts, rollback plan

## 5. SLA & Quality Assurance

- **Response Commitment**: <1 hour reply, 7~30 days support and bug fixes based on package tier
- **Accessibility**: Frontend complies with WCAG 2.1 AA, contrast ≥4.5:1, keyboard accessible, RTL/multi-language
- **Performance Optimization**: Data sampling, virtual scrolling, Web Worker, lazy loading, supports 50k+ rows
- **Export Module**: Based on Puppeteer/wkhtmltopdf, provides cross-platform deployment and font embedding recommendations

## 6. KPI & Outcomes

- Generate first usable chart in 5 minutes, report creation time reduced by 70%
- PNG/PDF export time <2 seconds, weekly report automation hit rate ≥95%
- Template reuse rate improved 3×, team collaboration satisfaction improved

## 7. FAQ

**Q1: Support real-time data or API integration?**  
A: Premium package can connect databases/APIs, support scheduled refresh or real-time push.

**Q2: Can export templates be customized?**  
A: Provides template engine, can configure brand colors, logos, covers, support multi-language and currency formats.

**Q3: How to handle sensitive data?**  
A: Default local/private deployment, data only stored in temp directory, can enable auto-cleanup and anonymization strategies.

## 8. Why Choose Me?

✅ **Fast Response**: <1 hour reply, clear milestones, transparent progress  
✅ **Platform Protection**: Fiverr/Upwork transaction guarantee, escrow payment  
✅ **Best Practices**: ECharts 5, Pandas data processing, FastAPI async backend  
✅ **Proven Delivery**: Production-ready with sample data, Docker deployment configs

## 9. Next Steps

- 🔵 [Upwork — Hire Me](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr — View Packages](https://www.fiverr.com/yourname)
- 📧 [Email — Book Demo](mailto:you@example.com?subject=Insight%20Viz%20Studio%20Consultation)
- 🚀 [Local Demo — Try Now](http://localhost:8606)

> "From data to charts in minutes — empower your team with instant insights."

---

## Quick Start

```bash
cd insight-viz-studio
.\start.bat    # Windows
# or
python -m uvicorn app.main:app --reload --port 8606
```

Visit `http://localhost:8606` after 10 seconds.

## Tech Stack

- **Backend**: Python 3.10+, FastAPI
- **Data Processing**: Pandas, NumPy
- **Visualization**: ECharts 5
- **Export**: Puppeteer / wkhtmltopdf (optional)
- **Frontend**: Vanilla JavaScript, Tailwind CSS
- **Deployment**: Docker, uvicorn

---

**Last Updated**: 2025-11-03

