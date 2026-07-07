from collections.abc import Mapping

from libs.db.repositories import get_tenant_by_id

from .cache import get_cached_tenant, set_cached_tenant
from .models import TenantMetadata


# Replace with DB-backed repository in production.
TENANT_REGISTRY: Mapping[str, TenantMetadata] = {
    "tenant_acme": TenantMetadata(
        tenant_id="tenant_acme",
        domain="acme.example.com",
        isolation_type="schema",
        schema_name="tenant_acme",
        plan="pro",
    ),
    "tenant_enterprise": TenantMetadata(
        tenant_id="tenant_enterprise",
        domain="enterprise.example.com",
        isolation_type="database",
        database_name="tenant_enterprise_db",
        plan="enterprise",
    ),
}


def get_tenant_metadata(tenant_id: str) -> TenantMetadata:
    cached = get_cached_tenant(tenant_id)
    if cached is not None:
        return cached

    db_tenant = get_tenant_by_id(tenant_id)
    if db_tenant is not None:
        set_cached_tenant(db_tenant)
        return db_tenant

    fallback = TENANT_REGISTRY.get(tenant_id)
    if fallback is not None:
        set_cached_tenant(fallback)
        return fallback

    raise KeyError(f"Unknown tenant_id: {tenant_id}")
