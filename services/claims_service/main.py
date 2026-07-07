from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from libs.tenant_sdk import get_tenant_metadata

app = FastAPI(title="Claims Service", version="0.1.0")


class ClaimCreateRequest(BaseModel):
    title: str
    amount: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "claims_service"}


@app.post("/claims")
def create_claim(payload: ClaimCreateRequest, x_tenant_id: str = Header(alias="X-Tenant-ID")) -> dict:
    try:
        tenant = get_tenant_metadata(x_tenant_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "claim_id": "clm_001",
        "tenant_id": tenant.tenant_id,
        "title": payload.title,
        "amount": payload.amount,
        "status": "created",
    }
