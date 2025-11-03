# Global Price Sentinel — E-commerce Price Monitoring Solution

> **Target Audience**: Cross-border e-commerce teams, brand overseas operations, competitive/channel operations managers
>
> **Core Value**: 24/7 price monitoring, auto-alerts, trend reports — delivered in as fast as 3 days

[中文版本 Chinese Version](./README.md)

---

## 1. Pain Points

- **Multiple SKUs, multiple platforms**: Manual spreadsheet updates miss prices, can't track real-time promotions
- **Delayed response**: Competitor price changes or stock fluctuations — teams can't react within hours
- **Lack of trend insights**: Historical data is scattered, can't support pricing decisions and profit evaluation

## 2. Solution & Value

- Automated scraping of Amazon / JD / Taobao and more, synchronize multi-region price comparisons
- Configurable threshold alerts (Email / Webhook / Slack), minute-level push to stakeholders, support multi-channel parallel delivery
- Visual console + weekly/monthly reports (HTML / CSV), output strategy-level trend insights
- Proxy pool + retry mechanism + audit logs, 24/7 stable operation with full traceability, support start/stop and dynamic credentials

## 3. Deliverables

- 🖥️ **Live Demo**: `http://localhost:8101` (with sample data, one-click import)
- ⚙️ **Config Center**: `http://localhost:8101/monitor/settings`, visual configuration of scheduling, proxy pool, and alert channels
- 📦 **Source Code & Scripts**: FastAPI backend, Playwright scraping, Tailwind UI console
- 📕 **Documentation Suite**: Deployment guide, operation manual, alert config instructions, environment variable templates
- 🧪 **Postman / API Docs**: `http://localhost:8101/api/docs` and Postman Collection
- 📊 **Report Templates**: HTML/PDF weekly reports, CSV details, Prometheus/Grafana integration guide

## 4. Timeline & Process

1. **Requirements Clarification (Day 0)**: Confirm sites/SKUs, alert thresholds, deployment environment, team roles
2. **PoC Demo (Day 2-4)**: Deliver demo (with sample data), validate scraping accuracy and alert logic
3. **Feature Completion (Day 5-10)**: Connect real data sources, deploy to target environment, import historical data
4. **Acceptance & Handover (Day 10+)**: Deliver source code/docs, training, go-live support, prepare rollback plan

## 5. SLA & Quality Assurance

- **Response Commitment**: <1 hour reply, 24h kickoff meeting scheduled
- **Accessibility**: Console complies with WCAG 2.1 AA, supports keyboard navigation, dark mode, RTL
- **Performance & Monitoring**: Auto-retry on scrape failure, Prometheus metrics, structured logging, slow request tracking
- **Security & Compliance**: Credentials in `.env`, only scrape public pages, GDPR-ready, logs can be anonymized
- **Post-Delivery Support**: 7~30 days remote support and bug fixes based on package tier

## 6. KPI & Outcomes

- Deliver MVP in 3 weeks, automate ≥20 SKUs after launch
- Alert latency <5 minutes, scraping success rate ≥99%
- Reduce labor costs by 30%, double pricing insights for strategy meetings

## 7. FAQ

**Q1: Support logged-in sites or complex anti-bot systems?**  
A: Yes. Can integrate account login, CAPTCHA solving, proxy pool — included in advanced packages.

**Q2: What alert channels are available?**  
A: Enable Email / Webhook / Slack via config center, can extend to Teams, WeCom, and support multi-channel parallel notifications with logging.

**Q3: Is it safe to deploy in your own environment?**  
A: Provides Docker templates and hardening recommendations, credentials managed independently, optional hosting in your VPC or Render/Fly.io.

## 8. Why Choose Me?

✅ **Fast Response**: <1 hour reply, clear milestones, transparent progress  
✅ **Platform Protection**: Fiverr/Upwork transaction guarantee, escrow payment  
✅ **Best Practices**: WCAG 2.1 AA, Material Design 3, Apple HIG compliance  
✅ **Proven Delivery**: All projects production-ready with tests, docs, and Docker support

## 9. Next Steps

- 🔵 [Upwork — Hire Me](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr — View Packages](https://www.fiverr.com/yourname)
- 📧 [Email — Book Demo](mailto:you@example.com?subject=Global%20Price%20Sentinel%20Consultation)
- 🚀 [Local Demo — Try Now](http://localhost:8101)

> "Price monitoring shouldn't be a tedious task. Let the system watch competitors for you — invest time in strategy and growth."

---

## Quick Start

```bash
cd global-price-sentinel
.\start.ps1    # Windows
# or
./start.sh     # Linux/Mac
```

Visit `http://localhost:8101` after 10 seconds.

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy
- **Scraping**: Playwright (Chromium)
- **Database**: SQLite (PostgreSQL ready)
- **UI**: Tailwind CSS, vanilla JavaScript
- **Deployment**: Docker, Docker Compose

---

**Last Updated**: 2025-11-03

