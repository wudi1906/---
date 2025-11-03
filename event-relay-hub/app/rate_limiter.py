"""应用限流器，支持 slowapi 缺失时的降级。"""

from typing import Callable, Any

try:
    from slowapi import Limiter  # type: ignore
    from slowapi.util import get_remote_address  # type: ignore
except ImportError:  # pragma: no cover - 用于降级
    Limiter = None  # type: ignore

    def get_remote_address(request: Any) -> str:  # type: ignore
        if request and getattr(request, "client", None):
            return request.client.host or "anonymous"
        return "anonymous"

    class DummyLimiter:  # 简单降级实现
        def __init__(self) -> None:
            self.enabled = False

        def limit(self, *_args, **_kwargs) -> Callable:
            def decorator(func: Callable) -> Callable:
                return func

            return decorator

    limiter = DummyLimiter()
else:
    from app.settings import settings

    def get_rate_limit_key(request):
        """根据请求提取 IP."""
        return get_remote_address(request)

    limiter = Limiter(
        key_func=get_rate_limit_key,
        default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"] if settings.RATE_LIMIT_ENABLED else [],
        enabled=settings.RATE_LIMIT_ENABLED,
        storage_uri="memory://",
    )
