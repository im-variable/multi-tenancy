from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from .context import TenantContext


def resolve_database_url(context: TenantContext, base_url: str) -> str:
    """
    Schema tenants share base_url. Database tenants switch DB name in URL.
    """
    if context.isolation_type == "database" and context.database_name:
        # Minimal URL swap for scaffold purposes.
        head, _, _ = base_url.rpartition("/")
        return f"{head}/{context.database_name}"
    return base_url


def create_tenant_engine(context: TenantContext, base_url: str) -> Engine:
    tenant_url = resolve_database_url(context, base_url)
    engine = create_engine(tenant_url, future=True)

    if context.isolation_type == "schema" and context.schema_name:
        with engine.connect() as conn:
            conn.execute(text(f'SET search_path TO "{context.schema_name}"'))
            conn.commit()

    return engine
