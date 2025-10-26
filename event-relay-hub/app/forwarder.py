"""
事件转发器
"""
import json
import asyncio
from typing import Optional
import httpx

from app.models import Event, ForwardLog, SessionLocal
from app.settings import settings


class EventForwarder:
    """事件转发器"""
    
    async def forward_event(self, event: Event, target_url: str) -> bool:
        """
        转发事件到目标 URL
        
        Args:
            event: 事件对象
            target_url: 目标 URL
            
        Returns:
            是否成功
        """
        db = SessionLocal()
        log = ForwardLog(event_id=event.id, target_url=target_url)
        
        try:
            async with httpx.AsyncClient(timeout=settings.FORWARD_TIMEOUT) as client:
                # 准备 payload
                headers = {
                    "Content-Type": "application/json",
                    "X-Forwarded-From": settings.APP_NAME,
                    "X-Event-Source": event.source,
                    "X-Event-Type": event.event_type or "unknown"
                }
                
                # 发送请求
                response = await client.post(
                    target_url,
                    content=event.payload,
                    headers=headers
                )
                
                log.status_code = response.status_code
                log.success = response.status_code in (200, 201, 202, 204)
                
                if not log.success:
                    log.error_message = f"HTTP {response.status_code}: {response.text[:500]}"
        
        except httpx.TimeoutException:
            log.success = False
            log.error_message = "Request timeout"
        except Exception as e:
            log.success = False
            log.error_message = str(e)[:500]
        finally:
            # 更新事件转发状态
            event.forwarded = log.success
            
            # 保存日志
            db.add(log)
            db.commit()
            db.close()
        
        return log.success
    
    async def replay_event(self, event_id: int, target_url: Optional[str] = None) -> bool:
        """
        重放事件
        
        Args:
            event_id: 事件ID
            target_url: 目标 URL（可选，默认使用配置的转发URL）
            
        Returns:
            是否成功
        """
        db = SessionLocal()
        try:
            event = db.query(Event).filter(Event.id == event_id).first()
            if not event:
                return False
            
            url = target_url or settings.FORWARD_URL
            if not url:
                return False
            
            return await self.forward_event(event, url)
        finally:
            db.close()

