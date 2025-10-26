# 多地区高转化作品集总览

本仓库包含 6 个面向 Upwork/Fiverr 高需求软件开发项目的作品集模板。每个项目均提供：

- 架构说明、演示 GIF 占位、指标/KPI
- 一键启动脚本（PowerShell/Makefile）与 Docker Compose
- README、.env.example、测试用例
- 国际化设计稿参考（Figma 链接占位）

| 项目 | 描述 | 亮点 | Demo 端口 |
| --- | --- | --- | --- |
| Global Price Sentinel | Playwright 电商监控 & 报告 | 多区域代理、报告面板、Webhook 告警 | 8101 |
| Event Relay Hub | Webhook 汇聚与转发中台 | Stripe/GitHub 签名校验、事件重放 | 8202 |
| SaaS Northstar Dashboard | SaaS 指标看板 | CSV 导入、指标计算、移动端适配 | 8303 |
| Doc Knowledge Forge | 文档转知识库 | PDF/DOCX 转 Markdown、全文检索 | 8404 |
| A11y Component Atlas | 可访问性组件库 | WCAG 2.1 AA、Storybook 展示 | 8505 |
| Insight Viz Studio | 数据可视化工具 | CSV/JSON 上传、ECharts 图表、导出 | 8606 |

## 🚀 快速开始

### 方式 1：一键启动所有项目（推荐）

```PowerShell
cd "E:\Program Files\cursorproject\作品集"
.\启动所有项目.ps1
```

这将自动启动所有已完成的项目（项目1、2、3），然后访问：
- **主页**: http://localhost:8101
- **项目2**: http://localhost:8202
- **项目3**: http://localhost:8303

### 方式 2：使用 Docker Compose

```bash
docker compose up --build
```

### 方式 3：单独启动某个项目

```PowerShell
# 启动项目 1
cd .\global-price-sentinel
.\start.ps1

# 启动项目 2
cd .\event-relay-hub
.\start.ps1

# 启动项目 3
cd .\saas-northstar-dashboard
npm run dev
```

## 🛑 停止所有项目

```PowerShell
.\停止所有项目.ps1
```

## 📖 详细文档

- `运行指南.md` - 详细的运行步骤
- `功能详解.md` - 所有项目的功能说明
- `项目完成总结.md` - 完成情况和后续计划

## 💡 常见问题

### Q: 启动后看不到项目2和3？
A: 请使用 `启动所有项目.ps1` 脚本，它会同时启动所有项目。

### Q: 如何查看所有服务是否运行？
A: 访问 http://localhost:8101 主页，可以看到所有项目的状态。

### Q: 如何停止服务？
A: 运行 `停止所有项目.ps1` 脚本，或在启动窗口按 Ctrl+C。

## 🎯 项目完成状态

- ✅ 项目 1: Global Price Sentinel（100% 完成）
- ✅ 项目 2: Event Relay Hub（100% 完成）
- ✅ 项目 3: SaaS Northstar Dashboard（90% 完成）
- ⚙️ 项目 4-6: 架构完成，待实现

更多细节请查看各项目目录下的 README。
