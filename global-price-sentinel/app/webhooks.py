"""
Webhook 通知模块
"""
import requests
from typing import Optional
from datetime import datetime

from app.settings import settings
from app.models import AlertLog, SessionLocal


class WebhookNotifier:
    """Webhook 通知器"""
    
    @staticmethod
    def send_slack(message: str, title: str = "价格告警") -> bool:
        """发送 Slack 通知"""
        if not settings.SLACK_WEBHOOK_URL:
            return False
        
        payload = {
            "text": f"*{title}*\n{message}",
            "username": settings.APP_NAME,
            "icon_emoji": ":chart_with_downwards_trend:"
        }
        
        try:
            resp = requests.post(settings.SLACK_WEBHOOK_URL, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            print(f"Slack 通知失败: {e}")
            return False
    
    @staticmethod
    def send_discord(message: str, title: str = "价格告警") -> bool:
        """发送 Discord 通知"""
        if not settings.DISCORD_WEBHOOK_URL:
            return False
        
        payload = {
            "content": f"**{title}**\n{message}"
        }
        
        try:
            resp = requests.post(settings.DISCORD_WEBHOOK_URL, json=payload, timeout=10)
            return resp.status_code == 204
        except Exception as e:
            print(f"Discord 通知失败: {e}")
            return False
    
    @staticmethod
    def send_dingtalk(message: str, title: str = "价格告警") -> bool:
        """发送钉钉通知"""
        if not settings.DINGTALK_WEBHOOK_URL:
            return False
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"### {title}\n{message}"
            }
        }
        
        try:
            resp = requests.post(settings.DINGTALK_WEBHOOK_URL, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            print(f"钉钉通知失败: {e}")
            return False
    
    @classmethod
    def notify_price_change(
        cls, 
        target_id: str, 
        product_name: str,
        old_price: float, 
        new_price: float,
        currency: str = "USD"
    ):
        """通知价格变动"""
        change_pct = ((new_price - old_price) / old_price) * 100
        direction = "下降" if change_pct < 0 else "上涨"
        
        message = (
            f"**{product_name}** ({target_id})\n"
            f"价格{direction}: {abs(change_pct):.2f}%\n"
            f"旧价: {old_price:.2f} {currency}\n"
            f"新价: {new_price:.2f} {currency}\n"
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        sent_to = []
        if cls.send_slack(message):
            sent_to.append("slack")
        if cls.send_discord(message):
            sent_to.append("discord")
        if cls.send_dingtalk(message):
            sent_to.append("dingtalk")
        
        # 记录告警日志
        db = SessionLocal()
        try:
            log = AlertLog(
                target_id=target_id,
                alert_type="price_change",
                message=message,
                old_price=old_price,
                new_price=new_price,
                sent_to=",".join(sent_to)
            )
            db.add(log)
            db.commit()
        finally:
            db.close()
        
        return len(sent_to) > 0


def check_and_alert(target_id: str, threshold_pct: float = 5.0):
    """检查价格变动并发送告警"""
    from sqlalchemy import desc
    
    db = SessionLocal()
    try:
        # 获取最近两条成功记录
        records = db.query(PriceRecord).filter(
            PriceRecord.target_id == target_id,
            PriceRecord.success == True,
            PriceRecord.price.isnot(None)
        ).order_by(desc(PriceRecord.created_at)).limit(2).all()
        
        if len(records) < 2:
            return
        
        new_record, old_record = records[0], records[1]
        
        if new_record.price and old_record.price:
            change_pct = abs((new_record.price - old_record.price) / old_record.price) * 100
            
            if change_pct >= threshold_pct:
                WebhookNotifier.notify_price_change(
                    target_id=target_id,
                    product_name=new_record.product_name or "未知产品",
                    old_price=old_record.price,
                    new_price=new_record.price,
                    currency=new_record.currency
                )
    finally:
        db.close()

