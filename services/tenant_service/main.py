from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from libs.db.master_models import Tenant
from libs.db.session import get_session
from libs.tenant_sdk import get_tenant_metadata

app = FastAPI(title="Tenant Service", version="0.1.0")


class ProvisionRequest(BaseModel):
    tenant_id: str


class TenantCreateRequest(BaseModel):
    tenant_id: str
    domain: str
    isolation_type: str
    schema_name: str | None = None
    database_name: str | None = None
    plan: str = "standard"
    region: str = "ap-south-1"
    status: str = "active"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "tenant_service"}


@app.post("/tenants")
def create_tenant(payload: TenantCreateRequest) -> dict[str, str]:
    with get_session() as session:
        existing = session.get(Tenant, payload.tenant_id)
        if existing:
            raise HTTPException(status_code=409, detail="tenant_id already exists")

        tenant = Tenant(**payload.model_dump())
        session.add(tenant)
        session.commit()
    return {"tenant_id": payload.tenant_id, "status": "created"}


@app.get("/tenants/{tenant_id}")
def get_tenant(tenant_id: str) -> dict:
    try:
        return get_tenant_metadata(tenant_id).model_dump()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/tenants/{tenant_id}/provision")
def provision_tenant(tenant_id: str, payload: ProvisionRequest) -> dict[str, str]:
    if tenant_id != payload.tenant_id:
        raise HTTPException(status_code=400, detail="Path/body tenant mismatch")

    # Stub for phase-2 automation.
    tenant = get_tenant_metadata(tenant_id)
    if tenant.isolation_type == "schema":
        action = "create schema + run migrations + seed baseline"
    else:
        action = "create database + run migrations + seed baseline"

    return {"tenant_id": tenant_id, "planned_action": action, "status": "accepted"}
