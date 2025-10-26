"""
Rate Limiter
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.settings import settings


def get_rate_limit_key(request):
    """Get rate limit key based on IP address"""
    return get_remote_address(request)


# Create limiter with simplified config
limiter = Limiter(
    key_func=get_rate_limit_key,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"] if settings.RATE_LIMIT_ENABLED else [],
    enabled=settings.RATE_LIMIT_ENABLED,
    storage_uri="memory://"  # Use in-memory storage instead of Redis
)
