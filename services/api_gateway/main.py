import os

import httpx
import jwt
from fastapi import FastAPI, Header, HTTPException, Request, Response

app = FastAPI(title="API Gateway", version="0.1.0")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
TENANT_SERVICE_URL = os.getenv("TENANT_SERVICE_URL", "http://localhost:8002")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8003")
CLAIMS_SERVICE_URL = os.getenv("CLAIMS_SERVICE_URL", "http://localhost:8004")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8005")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

UPSTREAMS = {
    "auth": AUTH_SERVICE_URL,
    "tenant": TENANT_SERVICE_URL,
    "user": USER_SERVICE_URL,
    "claims": CLAIMS_SERVICE_URL,
    "notification": NOTIFICATION_SERVICE_URL,
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "api_gateway"}


@app.get("/gateway/tenant-context")
def tenant_context(authorization: str = Header()) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1]
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc

    tenant_id = claims.get("tenant_id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id missing in JWT")

    with httpx.Client(timeout=5) as client:
        resp = client.get(f"{TENANT_SERVICE_URL}/tenants/{tenant_id}")
        if resp.status_code >= 400:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Tenant lookup failed: {resp.text}",
            )
        tenant = resp.json()

    return {"tenant": tenant, "claims": claims}


@app.get("/gateway/upstreams")
def upstreams() -> dict[str, str]:
    return UPSTREAMS


@app.api_route("/gateway/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(service: str, path: str, request: Request, authorization: str | None = Header(default=None)) -> Response:
    base_url = UPSTREAMS.get(service)
    if not base_url:
        raise HTTPException(status_code=404, detail=f"Unknown service '{service}'")

    headers = dict(request.headers)
    headers.pop("host", None)

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        try:
            claims = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            tenant_id = claims.get("tenant_id")
            if tenant_id:
                headers["X-Tenant-ID"] = tenant_id
        except jwt.PyJWTError as exc:
            raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc

    query = f"?{request.url.query}" if request.url.query else ""
    target = f"{base_url}/{path}{query}"
    body = await request.body()

    async with httpx.AsyncClient(timeout=30) as client:
        upstream_resp = await client.request(
            method=request.method,
            url=target,
            headers=headers,
            content=body if body else None,
        )

    return Response(
        content=upstream_resp.content,
        status_code=upstream_resp.status_code,
        media_type=upstream_resp.headers.get("content-type"),
    )
