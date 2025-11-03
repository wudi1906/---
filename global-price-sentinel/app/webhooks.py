"""告警通知模块"""
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import requests
from typing import Optional, List
from datetime import datetime

from app.settings import settings
from app.models import AlertLog, SessionLocal, PriceRecord
from app.config_service import ConfigService


def _send_email(subject: str, body: str, recipients: List[str]) -> bool:
    if not settings.SMTP_HOST or not settings.SMTP_FROM:
        print("[告警] SMTP 配置缺失，无法发送邮件")
        return False

    message = MIMEText(body, "plain", "utf-8")
    message["From"] = formataddr((settings.APP_NAME, settings.SMTP_FROM))
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    try:
        if settings.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM, recipients, message.as_string())
        server.quit()
        return True
    except Exception as exc:  # pragma: no cover - 网络异常难以覆盖
        print(f"[告警] 邮件发送失败: {exc}")
        return False


class AlertDispatcher:
    """综合告警派发器"""
    
    @staticmethod
    def _send_webhook(url: str, payload: dict, expected_status: int = 200) -> bool:
        try:
            resp = requests.post(url, json=payload, timeout=10)
            return resp.status_code == expected_status
        except Exception as exc:  # pragma: no cover - 网络异常
            print(f"[告警] Webhook 发送失败: {exc}")
            return False

    @classmethod
    def _send_slack(cls, webhook_url: str, message: str, title: str = "价格告警") -> bool:
        payload = {
            "text": f"*{title}*\n{message}",
            "username": settings.APP_NAME,
            "icon_emoji": ":chart_with_downwards_trend:"
        }
        return cls._send_webhook(webhook_url, payload, expected_status=200)
    
    @staticmethod
    def _send_generic_webhook(webhook_url: str, message: str, title: str = "价格告警") -> bool:
        payload = {
            "title": title,
            "message": message,
            "source": settings.APP_NAME
        }
        return AlertDispatcher._send_webhook(webhook_url, payload)

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

        sent_to: List[str] = []
        config = ConfigService.get_config()
        channels = [channel for channel in config.alert_channels if channel.enabled]

        for channel in channels:
            if channel.type == "email":
                if channel.recipients and _send_email("价格告警", message, list(channel.recipients)):
                    sent_to.append("email")
            elif channel.type == "slack":
                if channel.webhook_url and cls._send_slack(channel.webhook_url, message):
                    sent_to.append("slack")
            elif channel.type == "webhook":
                if channel.webhook_url and cls._send_generic_webhook(channel.webhook_url, message):
                    sent_to.append("webhook")
        
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

    @classmethod
    def test_channel(cls, channel: str, payload: Optional[dict] = None) -> tuple[bool, str, dict]:
        """测试单一告警渠道连通性，返回 (success, message, detail)。"""

        payload = payload or {}
        config = ConfigService.get_config()

        if channel == "email":
            recipients = payload.get("recipients")
            if not recipients:
                email_channel = next((c for c in config.alert_channels if c.type == "email" and c.enabled), None)
                recipients = list(email_channel.recipients) if email_channel and email_channel.recipients else None
            if not recipients:
                return False, "未配置邮件收件人，无法发送测试邮件", {}

            subject = payload.get("subject") or f"[{settings.APP_NAME}] 邮件告警连通性测试"
            message = payload.get("message") or "这是一次 SMTP 连通性测试。"
            success = _send_email(subject, message, list(recipients))
            return success, ("发送成功" if success else "发送失败"), {"recipients": recipients}

        if channel == "slack":
            webhook_url = payload.get("webhook_url")
            if not webhook_url:
                slack_channel = next((c for c in config.alert_channels if c.type == "slack" and c.enabled), None)
                webhook_url = slack_channel.webhook_url if slack_channel and slack_channel.webhook_url else None
            if not webhook_url:
                return False, "未配置 Slack Webhook URL", {}

            message = payload.get("message") or "Slack 通知连通性测试"
            title = payload.get("title") or "Slack Alert Test"
            success = cls._send_slack(webhook_url, message, title)
            return success, ("发送成功" if success else "发送失败"), {"webhook_url": webhook_url}

        if channel == "webhook":
            webhook_url = payload.get("webhook_url")
            if not webhook_url:
                hook_channel = next((c for c in config.alert_channels if c.type == "webhook" and c.enabled), None)
                webhook_url = hook_channel.webhook_url if hook_channel and hook_channel.webhook_url else None
            if not webhook_url:
                return False, "未配置 Webhook URL", {}

            message = payload.get("message") or "Webhook 通知连通性测试"
            title = payload.get("title") or "Webhook Alert Test"
            success = cls._send_generic_webhook(webhook_url, message, title)
            return success, ("发送成功" if success else "发送失败"), {"webhook_url": webhook_url}

        return False, "不支持的渠道类型", {}


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
                AlertDispatcher.notify_price_change(
                    target_id=target_id,
                    product_name=new_record.product_name or "未知产品",
                    old_price=old_record.price,
                    new_price=new_record.price,
                    currency=new_record.currency
                )
    finally:
        db.close()

