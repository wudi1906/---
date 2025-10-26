"""
监控器单元测试
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.models import TargetConfig
from app.monitor import PriceMonitor


@pytest.fixture
def sample_target():
    """示例监控目标"""
    return TargetConfig(
        id="test-product-1",
        url="https://example.com/product/123",
        name_selector="h1.product-title",
        price_selector="span.price",
        currency="USD",
        threshold_pct=5.0,
        enabled=True
    )


@pytest.mark.asyncio
async def test_fetch_price_success(sample_target):
    """测试价格抓取成功场景"""
    with patch('app.monitor.async_playwright') as mock_playwright:
        # 模拟 Playwright 行为
        mock_page = AsyncMock()
        mock_page.goto = AsyncMock()
        mock_page.wait_for_timeout = AsyncMock()
        mock_page.screenshot = AsyncMock()
        mock_page.close = AsyncMock()
        
        # 模拟页面元素
        mock_name_elem = AsyncMock()
        mock_name_elem.text_content = AsyncMock(return_value="Test Product")
        
        mock_price_elem = AsyncMock()
        mock_price_elem.text_content = AsyncMock(return_value="$99.99")
        
        mock_page.query_selector = AsyncMock(side_effect=[mock_name_elem, mock_price_elem])
        
        # 模拟浏览器
        mock_browser = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_browser.close = AsyncMock()
        
        mock_playwright_instance = AsyncMock()
        mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
        mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
        
        # 执行测试
        monitor = PriceMonitor()
        monitor.browser = mock_browser
        
        result = await monitor.fetch_price(sample_target)
        
        assert result["success"] is True
        assert result["target_id"] == "test-product-1"
        assert result["product_name"] == "Test Product"
        assert result["price"] == 99.99
        assert result["currency"] == "USD"


@pytest.mark.asyncio
async def test_fetch_price_with_regex():
    """测试使用正则表达式解析价格"""
    target = TargetConfig(
        id="test-product-2",
        url="https://example.com/product/456",
        price_regex=r"\$([0-9]+\.[0-9]{2})",
        currency="USD",
        enabled=True
    )
    
    with patch('app.monitor.async_playwright') as mock_playwright:
        mock_page = AsyncMock()
        mock_page.goto = AsyncMock()
        mock_page.wait_for_timeout = AsyncMock()
        mock_page.content = AsyncMock(return_value="<div>Price: $49.99</div>")
        mock_page.screenshot = AsyncMock()
        mock_page.close = AsyncMock()
        mock_page.query_selector = AsyncMock(return_value=None)
        
        mock_browser = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_browser.close = AsyncMock()
        
        mock_playwright_instance = AsyncMock()
        mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
        mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
        
        monitor = PriceMonitor()
        monitor.browser = mock_browser
        
        result = await monitor.fetch_price(target)
        
        assert result["success"] is True
        assert result["price"] == 49.99


@pytest.mark.asyncio
async def test_fetch_price_timeout():
    """测试页面加载超时"""
    target = TargetConfig(
        id="test-product-3",
        url="https://example.com/timeout",
        price_selector="span.price",
        currency="USD",
        enabled=True
    )
    
    with patch('app.monitor.async_playwright') as mock_playwright:
        mock_page = AsyncMock()
        mock_page.goto = AsyncMock(side_effect=Exception("Timeout"))
        mock_page.close = AsyncMock()
        
        mock_browser = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_browser.close = AsyncMock()
        
        mock_playwright_instance = AsyncMock()
        mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
        mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
        
        monitor = PriceMonitor()
        monitor.browser = mock_browser
        
        result = await monitor.fetch_price(target)
        
        assert result["success"] is False
        assert "抓取失败" in result["error_message"]


def test_target_config_validation():
    """测试配置验证"""
    # 正常配置
    config = TargetConfig(
        id="valid-id",
        url="https://example.com",
        currency="USD",
        enabled=True
    )
    assert config.id == "valid-id"
    assert config.threshold_pct == 5.0  # 默认值
    
    # 无效URL应该抛出验证错误
    with pytest.raises(Exception):
        TargetConfig(
            id="invalid-url",
            url="not-a-valid-url",
            currency="USD"
        )

