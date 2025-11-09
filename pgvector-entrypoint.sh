#!/usr/bin/env bash
set -euo pipefail

: "${PGDATA:=/var/lib/postgresql/18/docker}"
: "${POSTGRES_DB:=postgres}"

if [ ! -s "$PGDATA/PG_VERSION" ]; then
  mkdir -p /docker-entrypoint-initdb.d
  cat > /docker-entrypoint-initdb.d/000-enable-vector.sql <<'SQL'
CREATE EXTENSION IF NOT EXISTS vector;
SQL
fi

exec docker-entrypoint.sh "$@"
