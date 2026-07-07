from sqlalchemy import select

from libs.tenant_sdk.models import TenantMetadata

from .master_models import Tenant
from .session import get_session


def get_tenant_by_id(tenant_id: str) -> TenantMetadata | None:
    with get_session() as session:
        row = session.execute(select(Tenant).where(Tenant.tenant_id == tenant_id)).scalar_one_or_none()
        if row is None:
            return None
        return TenantMetadata(
            tenant_id=row.tenant_id,
            domain=row.domain,
            isolation_type=row.isolation_type,
            schema_name=row.schema_name,
            database_name=row.database_name,
            plan=row.plan,
            region=row.region,
            status=row.status,
        )
