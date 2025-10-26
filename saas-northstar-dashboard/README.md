# SaaS Northstar Dashboard

SaaS 关键指标看板 - 快速掌握 MRR/ARR/Churn/LTV 等核心业务指标。

## 功能特性

- 📊 **核心指标**: MRR, ARR, Churn Rate, LTV, CAC
- 📈 **趋势图表**: Chart.js 可视化，支持多时间段
- 📥 **CSV 导入**: 批量导入订阅/退款/获客数据
- 💱 **多币种**: 支持 USD/EUR/GBP/CNY 切换
- 📱 **响应式**: 移动端优先设计，适配各种屏幕
- 🌙 **暗色模式**: 支持亮/暗主题切换
- 📸 **导出功能**: 导出图表为 PNG 图片

## 快速开始

```bash
npm install
npm run dev
```

访问: http://localhost:8303

## 技术栈

- **前端**: Next.js 14 (App Router) + React 18
- **样式**: Tailwind CSS 3
- **图表**: Chart.js 4
- **状态管理**: Zustand
- **数据处理**: Papaparse (CSV 解析)
- **图表导出**: html2canvas

## 项目结构

```
saas-northstar-dashboard/
├── app/
│   ├── page.tsx              # 主Dashboard
│   ├── import/page.tsx       # CSV导入页
│   └── layout.tsx            # 布局
├── components/
│   ├── MetricCard.tsx        # 指标卡片
│   ├── TrendChart.tsx        # 趋势图表
│   ├── CohortTable.tsx       # 留存表
│   └── ThemeToggle.tsx       # 主题切换
├── lib/
│   ├── metrics.ts            # 指标计算
│   ├── parser.ts             # CSV解析
│   └── store.ts              # 状态管理
├── data/samples/             # 示例数据
│   ├── subscriptions.csv
│   ├── churn.csv
│   └── acquisition.csv
└── public/
```

## 指标计算公式

### MRR (Monthly Recurring Revenue)
```
MRR = Sum(当月活跃订阅金额)
```

### ARR (Annual Recurring Revenue)
```
ARR = MRR × 12
```

### Churn Rate (流失率)
```
Churn Rate = (期初客户数 - 期末客户数) / 期初客户数 × 100%
```

### LTV (Lifetime Value)
```
LTV = ARPU / Churn Rate
```

### CAC (Customer Acquisition Cost)
```
CAC = 营销支出 / 新增客户数
```

## 示例数据格式

### subscriptions.csv
```csv
date,customer_id,plan,amount,currency
2024-01-01,C001,Pro,99,USD
2024-01-01,C002,Basic,29,USD
```

### churn.csv
```csv
date,customer_id,reason
2024-01-15,C003,price
```

### acquisition.csv
```csv
date,channel,cost,customers
2024-01-01,google_ads,5000,50
```

## 部署

### Vercel (推荐)

```bash
npm run build
vercel deploy
```

### Docker

```bash
docker build -t saas-dashboard .
docker run -p 8303:3000 saas-dashboard
```

## 环境变量

创建 `.env.local`：

```env
NEXT_PUBLIC_DEFAULT_CURRENCY=USD
NEXT_PUBLIC_DATE_FORMAT=YYYY-MM-DD
```

## 扩展方向

- 集成 Stripe/Paddle API 自动导入
- 预测性分析（使用 ML 预测 Churn）
- 多租户支持
- 实时数据同步（WebSocket）
- 邮件定时报告

