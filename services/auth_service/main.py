import os
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Auth Service", version="0.1.0")

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_TTL_MIN = 60


class LoginRequest(BaseModel):
    email: str
    password: str
    tenant_id: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "auth_service"}


@app.post("/auth/login")
def login(payload: LoginRequest) -> dict[str, str]:
    # Scaffold check only. Replace with proper identity verification.
    if payload.password != "secret":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    now = datetime.now(UTC)
    claims = {
        "sub": payload.email,
        "tenant_id": payload.tenant_id,
        "roles": ["admin"],
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_TTL_MIN)).timestamp()),
    }
    token = jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
