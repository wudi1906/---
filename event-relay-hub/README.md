# Event Relay Hub

通用 Webhook 事件汇聚与转发中台。支持 GitHub、Stripe、Notion 等第三方服务的 Webhook 接入，提供事件签名校验、存储查询、二次转发、速率限制等功能。

## 功能特性

- ✅ **多源接入**：支持 GitHub、Stripe、自定义 Webhook
- 🔐 **签名校验**：HMAC-SHA256 签名验证，确保事件真实性
- 💾 **事件存储**：PostgreSQL/SQLite 持久化，支持全文检索
- 🔄 **事件重放**：可重新触发任意历史事件
- 📊 **管理仪表板**：查看事件列表、筛选、统计
- 🚦 **速率限制**：防止滥用，可配置每分钟请求数
- 📡 **转发队列**：将事件转发到其他 Webhook URL
- 📖 **OpenAPI 文档**：Swagger/ReDoc 自动生成 API 文档

## 快速开始

### 方式 1：PowerShell 脚本

```PowerShell
pwsh ./scripts/start.ps1 --install
```

### 方式 2：Docker Compose

```bash
docker compose up --build
```

默认端口：`8202`

## 接入第三方 Webhook

### GitHub Webhook

1. 在 GitHub 仓库设置 Webhook:
   - Payload URL: `http://your-server:8202/webhook/github`
   - Content type: `application/json`
   - Secret: 配置在 `.env` 的 `GITHUB_WEBHOOK_SECRET`

2. 选择触发事件（如 push、pull_request）

### Stripe Webhook

1. 在 Stripe Dashboard 添加 Webhook:
   - Endpoint URL: `http://your-server:8202/webhook/stripe`
   - Events: 选择需要监听的事件

2. 将 Signing secret 配置到 `.env` 的 `STRIPE_WEBHOOK_SECRET`

### 自定义 Webhook

```bash
POST /webhook/custom
Content-Type: application/json
X-Signature: <HMAC-SHA256签名>

{
  "event": "user.created",
  "data": {...}
}
```

## API 端点

| 端点 | 方法 | 描述 |
| --- | --- | --- |
| `/webhook/github` | POST | 接收 GitHub Webhook |
| `/webhook/stripe` | POST | 接收 Stripe Webhook |
| `/webhook/custom` | POST | 接收自定义 Webhook |
| `/api/events` | GET | 查询事件列表 |
| `/api/events/{id}` | GET | 获取单个事件详情 |
| `/api/events/{id}/replay` | POST | 重放事件 |
| `/api/stats` | GET | 事件统计 |

## 配置

编辑 `.env` 文件：

```env
# 数据库
DATABASE_URL=postgresql://user:pass@localhost:5432/event_hub

# Webhook 密钥
GITHUB_WEBHOOK_SECRET=your_github_secret
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_secret

# 速率限制
RATE_LIMIT_PER_MINUTE=60

# 转发目标（可选）
FORWARD_URL=https://your-destination.com/webhook
```

## 仓库结构

```
event-relay-hub/
├── app/
│   ├── main.py              # FastAPI 主应用
│   ├── models.py            # 数据模型
│   ├── webhooks.py          # Webhook 处理器
│   ├── verifiers.py         # 签名校验
│   ├── forwarder.py         # 转发队列
│   ├── rate_limiter.py      # 速率限制
│   └── dashboard.py         # 仪表板路由
├── frontend/                # 仪表板前端
│   ├── index.html
│   └── app.js
├── tests/
│   ├── test_webhooks.py
│   └── test_verifiers.py
├── scripts/
│   ├── start.ps1
│   └── start.sh
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 测试

运行单元测试：

```PowerShell
.\.venv\Scripts\pytest.exe -v
```

模拟 GitHub Webhook：

```PowerShell
$body = @{
    repository = @{ full_name = "user/repo" }
    pusher = @{ name = "testuser" }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8202/webhook/github" `
    -Method POST `
    -Body $body `
    -ContentType "application/json" `
    -Headers @{ "X-Hub-Signature-256" = "sha256=..." }
```

## KPI 与指标

- 签名验证成功率：100%
- P95 响应延迟：< 200ms
- 并发吞吐量：> 200 rps
- 事件存储可靠性：100%

## 部署

- **Render/Fly.io**：使用 Dockerfile 一键部署
- **PostgreSQL**：推荐使用 Supabase、Neon 或自托管
- **负载均衡**：可部署多个实例，共享数据库

## 扩展方向

- 事件过滤规则引擎（基于 JSON Path）
- 多目标转发（Fan-out）
- 死信队列与重试策略
- Webhook 测试工具（Mock 服务器）
- 集成 Grafana/Prometheus 监控

