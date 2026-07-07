import json
import os

import redis

from .models import TenantMetadata

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6380/0")
TENANT_CACHE_TTL_SECONDS = 300


def _redis_client() -> redis.Redis:
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


def get_cached_tenant(tenant_id: str) -> TenantMetadata | None:
    try:
        client = _redis_client()
        raw = client.get(f"tenant:{tenant_id}")
        if not raw:
            return None
        data = json.loads(raw)
        return TenantMetadata(**data)
    except redis.RedisError:
        return None


def set_cached_tenant(tenant: TenantMetadata) -> None:
    try:
        client = _redis_client()
        client.setex(
            f"tenant:{tenant.tenant_id}",
            TENANT_CACHE_TTL_SECONDS,
            json.dumps(tenant.model_dump()),
        )
    except redis.RedisError:
        return
