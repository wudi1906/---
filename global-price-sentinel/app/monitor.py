"""
价格监控核心逻辑
"""
import re
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout

from app.settings import settings
from app.models import TargetConfig, PriceRecord, SessionLocal


class PriceMonitor:
    """价格监控器"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        playwright = await async_playwright().start()
        
        browser_args = {
            "headless": settings.HEADLESS,
            "args": []
        }
        
        # 配置代理
        if settings.PROXY_SERVER:
            browser_args["proxy"] = {
                "server": settings.PROXY_SERVER,
                "username": settings.PROXY_USERNAME,
                "password": settings.PROXY_PASSWORD
            }
        
        self.browser = await playwright.chromium.launch(**browser_args)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.browser:
            await self.browser.close()
    
    async def fetch_price(self, target: TargetConfig) -> Dict[str, Any]:
        """
        抓取单个目标的价格信息
        
        Args:
            target: 目标配置
            
        Returns:
            包含价格信息的字典
        """
        page: Optional[Page] = None
        result = {
            "target_id": target.id,
            "url": str(target.url),
            "success": False,
            "error_message": None,
            "product_name": None,
            "price": None,
            "currency": target.currency,
            "stock_status": None,
            "screenshot_path": None
        }
        
        try:
            page = await self.browser.new_page(
                viewport={"width": settings.VIEWPORT_WIDTH, "height": settings.VIEWPORT_HEIGHT}
            )
            
            # 导航到目标URL
            await page.goto(str(target.url), timeout=settings.BROWSER_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)  # 等待动态内容加载
            
            # 提取产品名称
            if target.name_selector:
                try:
                    name_elem = await page.query_selector(target.name_selector)
                    if name_elem:
                        result["product_name"] = (await name_elem.text_content()).strip()
                except Exception as e:
                    print(f"提取产品名称失败: {e}")
            
            # 提取价格
            price_text = None
            if target.price_selector:
                try:
                    price_elem = await page.query_selector(target.price_selector)
                    if price_elem:
                        price_text = (await price_elem.text_content()).strip()
                except Exception as e:
                    print(f"提取价格失败: {e}")
            
            # 使用正则表达式解析价格
            if price_text or target.price_regex:
                if not price_text:
                    price_text = await page.content()
                
                pattern = target.price_regex if target.price_regex else r'[\$€£¥]?\s?([0-9,]+\.?[0-9]*)'
                match = re.search(pattern, price_text)
                if match:
                    price_str = match.group(1).replace(',', '')
                    result["price"] = float(price_str)
            
            # 提取库存状态
            if target.stock_selector:
                try:
                    stock_elem = await page.query_selector(target.stock_selector)
                    if stock_elem:
                        result["stock_status"] = (await stock_elem.text_content()).strip()
                except Exception as e:
                    print(f"提取库存状态失败: {e}")
            
            # 截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{target.id}_{timestamp}.png"
            screenshot_path = settings.SCREENSHOTS_DIR / screenshot_name
            await page.screenshot(path=str(screenshot_path), full_page=False)
            result["screenshot_path"] = str(screenshot_path)
            
            result["success"] = True
            
        except PlaywrightTimeout:
            result["error_message"] = f"页面加载超时: {target.url}"
        except Exception as e:
            result["error_message"] = f"抓取失败: {str(e)}"
        finally:
            if page:
                await page.close()
        
        return result
    
    async def monitor_targets(self, targets: list[TargetConfig]) -> list[PriceRecord]:
        """
        批量监控多个目标
        
        Args:
            targets: 目标配置列表
            
        Returns:
            价格记录列表
        """
        records = []
        db = SessionLocal()
        
        try:
            for target in targets:
                if not target.enabled:
                    continue
                
                print(f"正在监控: {target.id} - {target.url}")
                
                # 重试机制
                for attempt in range(settings.MAX_RETRIES):
                    result = await self.fetch_price(target)
                    
                    if result["success"]:
                        break
                    
                    if attempt < settings.MAX_RETRIES - 1:
                        print(f"重试 {attempt + 1}/{settings.MAX_RETRIES}...")
                        await asyncio.sleep(settings.RETRY_DELAY)
                
                # 保存记录
                record = PriceRecord(**result)
                db.add(record)
                db.commit()
                db.refresh(record)
                records.append(record)
                
                print(f"✓ {target.id}: {result.get('price', 'N/A')} {result['currency']}")
                
        finally:
            db.close()
        
        return records


async def run_monitor_cycle(targets: list[TargetConfig]):
    """运行一次完整的监控周期"""
    async with PriceMonitor() as monitor:
        records = await monitor.monitor_targets(targets)
        print(f"\n监控完成: 共 {len(records)} 条记录")
        return records

