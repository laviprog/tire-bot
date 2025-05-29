#!/bin/bash
set -e

# waiting for redis
./scripts/wait-for-it.sh "$REDIS_HOST:$REDIS_PORT" --timeout=30 --strict -- echo "Redis is up."

# waiting for postgres
./scripts/wait-for-it.sh "$PG_HOST:$PG_PORT" --timeout=30 --strict -- echo "Postgres is up - running migrations..."

# running migration
alembic upgrade head

exec "$@"
