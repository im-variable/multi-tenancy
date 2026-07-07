# Hybrid Multi-Tenant Microservices Starter

Production-oriented starter for a SaaS platform that supports both:
- schema-per-tenant isolation (shared PostgreSQL)
- database-per-tenant isolation (dedicated PostgreSQL DB per tenant)

## Services

- `api_gateway`: edge entrypoint and tenant context forwarding
- `auth_service`: login and JWT issuing with `tenant_id`
- `tenant_service`: tenant metadata lookup and provisioning stubs
- `user_service`: tenant-aware user APIs
- `claims_service`: tenant-aware claims APIs
- `notification_service`: tenant-aware notification APIs
- `libs/tenant_sdk`: shared tenant context and DB routing primitives
- `libs/db`: SQLAlchemy models and DB repository layer
- `libs/events`: async Kafka publisher + worker for tenant events

## Tech

- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Redis
- Kafka

## Quick start

1. Create Python env and install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start infra:

```bash
docker compose -f infra/docker-compose.yml up -d
```

3. Apply DB migration:

```bash
./scripts/migrate.sh
```

4. Run all services + worker:

```bash
./scripts/dev_run.sh
```

Events are published to Kafka topic `tenant-events` (auto-created by local broker config).

5. Or run services manually (example):

```bash
uvicorn services.auth_service.main:app --reload --port 8001
uvicorn services.tenant_service.main:app --reload --port 8002
uvicorn services.api_gateway.main:app --reload --port 8000
```

6. Try login:

```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@acme.com","password":"secret","tenant_id":"tenant_acme"}'
```

7. Proxy to downstream through gateway:

```bash
curl http://localhost:8000/gateway/user/users/me \
  -H "Authorization: Bearer <token>"
```

## Container images

Each service has its own Dockerfile:
- `services/api_gateway/Dockerfile`
- `services/auth_service/Dockerfile`
- `services/tenant_service/Dockerfile`
- `services/user_service/Dockerfile`
- `services/claims_service/Dockerfile`
- `services/notification_service/Dockerfile`

## Initial roadmap mapping

- Phase 1: gateway + auth + tenant service + tenant SDK (included)
- Phase 2: hybrid provisioning/routing (scaffolded in tenant SDK and tenant service)
- Phase 3: business services/events (service stubs included)
- Phase 4: observability and hardening (k8s base manifests included)
# multi-tenancy
