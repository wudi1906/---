# Global Price Sentinel

跨境电商价格/库存监控自动化方案。基于 Playwright + FastAPI + SQLite，支持配置 SKU 列表、变更检测、自动报告与 Webhook 告警。

## 功能特性
- YAML 配置多站点多 SKU（URL + 选择器/正则）
- Playwright（或 httpx 回退）抓取最新价格/库存
- 变更检测与重试机制，失败自动记录日志
- HTML/CSV 报告生成，支持 7 天历史
- Web 控制面板（FastAPI + Tailwind）查看趋势
- Slack/Discord/钉钉 Webhook 推送

## 快速开始
```PowerShell
pwsh ./scripts/start.ps1
```

或使用 Docker：
```bash
docker compose up --build
```

首次运行会自动创建 SQLite 数据库、生成示例报告并启动本地服务（默认端口 `8101`）。

## 配置
编辑 `configs/targets.example.yml` 并复制为 `configs/targets.yml`。
```yaml
targets:
  - id: sample-sku-1
    url: https://example.com/products/sku-1
    name_selector: h1.product-title
    price_selector: span.price
    currency: USD
    threshold:
      price_change_pct: 5
  - id: sample-sku-2
    url: https://example.com/products/sku-2
    name_selector: h1
    price_regex: "\\$([0-9]+\\.[0-9]{2})"
    currency: USD
```

## 测试
```PowerShell
.\.venv\Scripts\pytest.exe
```

## KPI 与指标
- 抓取成功率 ≥ 95%
- 采集周期：默认 12 小时，可在 `.env` 中配置 `CRON_SCHEDULE`
- 报告生成时间（样例数据）：< 1.2s

## 演示资产
- `assets/demo.mp4`：15s 操作演示（占位）
- `assets/screenshots/`：控制面板截图
- `docs/ux/`：各地区视觉规范（Figma 链接占位）

## 仓库结构
```
global-price-sentinel/
├── app/
│   ├── main.py
│   ├── monitor.py
│   ├── models.py
│   ├── reporter.py
│   ├── scheduler.py
│   ├── settings.py
│   └── webhooks.py
├── configs/
│   ├── targets.example.yml
│   └── prompts/
├── reports/
├── screenshots/
├── scripts/
│   ├── start.ps1
│   └── start.sh
├── tests/
│   └── test_monitor.py
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── requirements.txt
└── .env.example
```

## 部署
- Docker Compose (默认 SQLite)
- Render/Fly.io：可使用 `Dockerfile`
- 定时任务：GitHub Actions + cron，通过 CLI `python -m app.scheduler` 触发

## 扩展方向
- 多区域代理池（BrightData、Oxylabs 等）
- Captcha 规避（2Captcha/Playwright stealth）
- 历史价格分析 & 策略建议
- KPI 接入 Grafana/Prometheus
