from pydantic import BaseModel


class TenantMetadata(BaseModel):
    tenant_id: str
    domain: str
    isolation_type: str  # schema | database
    schema_name: str | None = None
    database_name: str | None = None
    plan: str = "standard"
    region: str = "ap-south-1"
    status: str = "active"
