#!/usr/bin/env bash
set -euo pipefail

DATABASE_URL="${MASTER_DATABASE_URL:-postgresql://postgres:postgres@localhost:5434/master_db}"

echo "Applying migration 001_init_master.sql to ${DATABASE_URL}"
psql "${DATABASE_URL}" -f migrations/001_init_master.sql
echo "Migration complete."
