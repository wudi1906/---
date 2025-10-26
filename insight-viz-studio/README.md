# Insight Viz Studio

数据可视化工具 - 上传 CSV/JSON 数据，自动生成交互式图表并导出。

## 功能特性

- 📊 **多图表类型**: 折线图、柱状图、饼图、散点图、漏斗图
- 📁 **多格式支持**: CSV, JSON, Excel (xlsx/xls)
- 🎨 **自定义样式**: 颜色、标题、标签自由配置
- 📸 **导出功能**: PNG, PDF, SVG 格式导出
- 📱 **响应式**: 自适应各种屏幕尺寸
- 🌐 **国际化**: 支持多语言和数字格式
- 🚀 **高性能**: 支持大数据集（50k+ 行）

## 快速开始

```PowerShell
pwsh .\scripts\start.ps1 --install
```

访问: http://localhost:8606

## 技术栈

- **后端**: Python + FastAPI
- **数据处理**: Pandas + NumPy
- **图表库**: ECharts 5
- **导出**: Puppeteer / wkhtmltopdf
- **前端**: Vanilla JS + Tailwind CSS

## 使用流程

1. **上传数据**: 选择 CSV/JSON/Excel 文件
2. **数据预览**: 查看前10行数据
3. **选择图表**: 选择合适的图表类型
4. **配置选项**: 设置标题、颜色、标签
5. **生成图表**: 实时预览交互式图表
6. **导出报告**: 下载 PNG/PDF 格式

## 示例数据

提供示例数据集在 `data/samples/`:
- `sales.csv` - 销售数据
- `user_growth.json` - 用户增长
- `marketing.xlsx` - 营销数据

## API 端点

- `POST /api/upload` - 上传数据文件
- `POST /api/chart` - 生成图表
- `POST /api/export/png` - 导出PNG
- `POST /api/export/pdf` - 导出PDF
- `GET /api/datasets` - 获取数据集列表

## 支持的图表类型

### 时间序列
- 折线图 (Line Chart)
- 面积图 (Area Chart)

### 分类对比
- 柱状图 (Bar Chart)
- 水平条形图 (Horizontal Bar)

### 占比分析
- 饼图 (Pie Chart)
- 环形图 (Donut Chart)

### 关系分析
- 散点图 (Scatter Plot)
- 气泡图 (Bubble Chart)

### 漏斗分析
- 漏斗图 (Funnel Chart)

## 数据格式示例

### CSV
```csv
date,revenue,users
2024-01-01,10000,120
2024-01-02,12000,135
```

### JSON
```json
[
  {"date": "2024-01-01", "revenue": 10000, "users": 120},
  {"date": "2024-01-02", "revenue": 12000, "users": 135}
]
```

## 导出配置

```python
export_config = {
    "format": "png",  # png, pdf, svg
    "width": 1200,
    "height": 800,
    "quality": 90,
    "background": "transparent"
}
```

## 部署

```bash
docker compose up --build
```

## 性能优化

- 数据采样（大数据集）
- 虚拟滚动（大表格）
- Web Worker（数据处理）
- 懒加载（图表渲染）

## 扩展方向

- 实时数据源接入
- 协作编辑
- 仪表板模板
- AI 图表推荐
- 数据清洗工具

