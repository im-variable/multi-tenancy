from .context import TenantContext, parse_tenant_from_jwt
from .db import create_tenant_engine, resolve_database_url
from .models import TenantMetadata


def get_tenant_metadata(tenant_id: str):
    # Lazy import prevents circular import with libs.db.repositories.
    from .store import get_tenant_metadata as _get_tenant_metadata

    return _get_tenant_metadata(tenant_id)

__all__ = [
    "TenantContext",
    "TenantMetadata",
    "create_tenant_engine",
    "get_tenant_metadata",
    "parse_tenant_from_jwt",
    "resolve_database_url",
]
