#!/usr/bin/env bash
set -euo pipefail

echo "Starting auth_service on :8001"
uvicorn services.auth_service.main:app --reload --port 8001 &

echo "Starting tenant_service on :8002"
uvicorn services.tenant_service.main:app --reload --port 8002 &

echo "Starting user_service on :8003"
uvicorn services.user_service.main:app --reload --port 8003 &

echo "Starting claims_service on :8004"
uvicorn services.claims_service.main:app --reload --port 8004 &

echo "Starting notification_service on :8005"
uvicorn services.notification_service.main:app --reload --port 8005 &

echo "Starting notification event worker"
python -m libs.events.worker &

echo "Starting api_gateway on :8000"
uvicorn services.api_gateway.main:app --reload --port 8000
