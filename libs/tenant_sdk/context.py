from dataclasses import dataclass
from typing import Any

import jwt


@dataclass
class TenantContext:
    tenant_id: str
    isolation_type: str
    schema_name: str | None = None
    database_name: str | None = None


def parse_tenant_from_jwt(token: str, secret: str, algorithm: str = "HS256") -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=[algorithm])
