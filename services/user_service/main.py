from fastapi import FastAPI, Header, HTTPException

from libs.tenant_sdk import get_tenant_metadata

app = FastAPI(title="User Service", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "user_service"}


@app.get("/users/me")
def get_me(x_tenant_id: str = Header(alias="X-Tenant-ID")) -> dict[str, str]:
    try:
        tenant = get_tenant_metadata(x_tenant_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "tenant_id": tenant.tenant_id,
        "user_id": "user_123",
        "email": "user@example.com",
        "name": "Default User",
    }
