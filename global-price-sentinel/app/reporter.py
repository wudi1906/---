"""
报告生成模块
"""
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List
from jinja2 import Template
from sqlalchemy import func, desc

from app.settings import settings
from app.models import PriceRecord, ReportSummary, SessionLocal


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>价格监控报告 - {{ report_date }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', 'Roboto', -apple-system, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            background: #f8fafc;
            padding: 24px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            font-size: 2rem;
            margin-bottom: 8px;
            color: #0f172a;
        }
        .meta {
            color: #64748b;
            margin-bottom: 32px;
            font-size: 0.875rem;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .card h2 {
            font-size: 1.25rem;
            margin-bottom: 16px;
            color: #2563eb;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
        }
        th {
            background: #f1f5f9;
            font-weight: 600;
            color: #475569;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .price-up { color: #dc2626; font-weight: 600; }
        .price-down { color: #16a34a; font-weight: 600; }
        .price-stable { color: #64748b; }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-success { background: #dcfce7; color: #166534; }
        .badge-error { background: #fee2e2; color: #991b1b; }
        .footer {
            text-align: center;
            margin-top: 48px;
            color: #94a3b8;
            font-size: 0.875rem;
        }
        @media (max-width: 768px) {
            body { padding: 16px; }
            h1 { font-size: 1.5rem; }
            .card { padding: 16px; }
            table { font-size: 0.875rem; }
            th, td { padding: 8px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Global Price Sentinel 监控报告</h1>
        <div class="meta">
            报告日期: {{ report_date }} | 监控周期: {{ days }} 天 | 总记录数: {{ total_records }}
        </div>
        
        <div class="card">
            <h2>📊 价格趋势摘要</h2>
            <table>
                <thead>
                    <tr>
                        <th>产品ID</th>
                        <th>产品名称</th>
                        <th>最新价格</th>
                        <th>价格变动</th>
                        <th>最低价</th>
                        <th>最高价</th>
                        <th>平均价</th>
                        <th>记录数</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in summaries %}
                    <tr>
                        <td><strong>{{ item.target_id }}</strong></td>
                        <td>{{ item.product_name or '-' }}</td>
                        <td>{{ "%.2f"|format(item.latest_price) if item.latest_price else '-' }} {{ item.currency }}</td>
                        <td>
                            {% if item.price_change_pct is not none %}
                                {% if item.price_change_pct > 0 %}
                                    <span class="price-up">+{{ "%.2f"|format(item.price_change_pct) }}%</span>
                                {% elif item.price_change_pct < 0 %}
                                    <span class="price-down">{{ "%.2f"|format(item.price_change_pct) }}%</span>
                                {% else %}
                                    <span class="price-stable">0%</span>
                                {% endif %}
                            {% else %}
                                -
                            {% endif %}
                        </td>
                        <td>{{ "%.2f"|format(item.min_price) if item.min_price else '-' }}</td>
                        <td>{{ "%.2f"|format(item.max_price) if item.max_price else '-' }}</td>
                        <td>{{ "%.2f"|format(item.avg_price) if item.avg_price else '-' }}</td>
                        <td>{{ item.total_records }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h2>📝 最近记录</h2>
            <table>
                <thead>
                    <tr>
                        <th>时间</th>
                        <th>产品ID</th>
                        <th>价格</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {% for record in recent_records[:20] %}
                    <tr>
                        <td>{{ record.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                        <td>{{ record.target_id }}</td>
                        <td>
                            {% if record.price %}
                                {{ "%.2f"|format(record.price) }} {{ record.currency }}
                            {% else %}
                                -
                            {% endif %}
                        </td>
                        <td>
                            {% if record.success %}
                                <span class="badge badge-success">成功</span>
                            {% else %}
                                <span class="badge badge-error">失败</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by {{ app_name }} v{{ app_version }}</p>
            <p>{{ report_date }}</p>
        </div>
    </div>
</body>
</html>
"""


class ReportGenerator:
    """报告生成器"""
    
    @staticmethod
    def generate_summary(days: int = 7) -> List[ReportSummary]:
        """生成价格趋势摘要"""
        db = SessionLocal()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # 获取所有目标ID
            target_ids = db.query(PriceRecord.target_id).filter(
                PriceRecord.created_at >= cutoff_date
            ).distinct().all()
            
            summaries = []
            for (target_id,) in target_ids:
                records = db.query(PriceRecord).filter(
                    PriceRecord.target_id == target_id,
                    PriceRecord.success == True,
                    PriceRecord.price.isnot(None),
                    PriceRecord.created_at >= cutoff_date
                ).order_by(desc(PriceRecord.created_at)).all()
                
                if not records:
                    continue
                
                prices = [r.price for r in records if r.price]
                latest = records[0]
                
                # 计算价格变动
                price_change_pct = None
                if len(records) >= 2 and records[-1].price:
                    old_price = records[-1].price
                    new_price = latest.price
                    price_change_pct = ((new_price - old_price) / old_price) * 100
                
                summary = ReportSummary(
                    target_id=target_id,
                    product_name=latest.product_name,
                    latest_price=latest.price,
                    price_change_pct=price_change_pct,
                    min_price=min(prices) if prices else None,
                    max_price=max(prices) if prices else None,
                    avg_price=sum(prices) / len(prices) if prices else None,
                    currency=latest.currency,
                    last_updated=latest.created_at,
                    total_records=len(records)
                )
                summaries.append(summary)
            
            return summaries
        finally:
            db.close()
    
    @staticmethod
    def generate_html_report(days: int = 7) -> Path:
        """生成 HTML 报告"""
        summaries = ReportGenerator.generate_summary(days)
        
        # 获取最近记录
        db = SessionLocal()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            recent_records = db.query(PriceRecord).filter(
                PriceRecord.created_at >= cutoff_date
            ).order_by(desc(PriceRecord.created_at)).limit(50).all()
            
            total_records = db.query(func.count(PriceRecord.id)).filter(
                PriceRecord.created_at >= cutoff_date
            ).scalar()
        finally:
            db.close()
        
        # 渲染模板
        template = Template(HTML_TEMPLATE)
        html_content = template.render(
            report_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            days=days,
            total_records=total_records,
            summaries=summaries,
            recent_records=recent_records,
            app_name=settings.APP_NAME,
            app_version=settings.APP_VERSION
        )
        
        # 保存文件
        report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        report_path = settings.REPORTS_DIR / report_name
        report_path.write_text(html_content, encoding="utf-8")
        
        # 同时保存为 latest.html
        latest_path = settings.REPORTS_DIR / "latest.html"
        latest_path.write_text(html_content, encoding="utf-8")
        
        return report_path
    
    @staticmethod
    def generate_csv_report(days: int = 7) -> Path:
        """生成 CSV 报告"""
        db = SessionLocal()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            records = db.query(PriceRecord).filter(
                PriceRecord.created_at >= cutoff_date
            ).order_by(desc(PriceRecord.created_at)).all()
            
            report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            report_path = settings.REPORTS_DIR / report_name
            
            with open(report_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    '时间', '产品ID', '产品名称', '价格', '货币', 
                    '库存状态', '状态', '错误信息'
                ])
                
                for record in records:
                    writer.writerow([
                        record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        record.target_id,
                        record.product_name or '',
                        record.price if record.price else '',
                        record.currency,
                        record.stock_status or '',
                        '成功' if record.success else '失败',
                        record.error_message or ''
                    ])
            
            return report_path
        finally:
            db.close()

