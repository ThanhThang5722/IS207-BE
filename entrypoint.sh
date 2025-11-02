#!/bin/sh
set -e

echo "Waiting for database to be ready..."
python - <<'PY'
import os, time
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/fastapi_db")
for i in range(60):
    try:
        engine = create_engine(DATABASE_URL)
        conn = engine.connect()
        conn.close()
        print("Database is available")
        break
    except Exception as exc:
        print(f"Waiting for DB ({i+1}/60): {exc}")
        time.sleep(1)
else:
    print("Timed out waiting for the database")
    raise SystemExit(1)
PY

echo "Checking database schema/migrations state..."
# ensure PGPASSWORD is set for psql checks
: "${POSTGRES_PASSWORD:=}"
if [ -z "$POSTGRES_PASSWORD" ]; then
    # try to parse from DATABASE_URL
    DBURL="$DATABASE_URL"
    POSTGRES_PASSWORD=$(echo "$DBURL" | sed -E 's#postgresql://[^:]+:([^@]+)@.*#\1#')
fi
export PGPASSWORD="$POSTGRES_PASSWORD"

ALEMBIC_EXISTS=$(psql -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM information_schema.tables WHERE table_name='alembic_version';" 2>/dev/null || true)
USERS_EXISTS=$(psql -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM information_schema.tables WHERE table_name='users';" 2>/dev/null || true)

if [ "$ALEMBIC_EXISTS" = "1" ]; then
    echo "alembic_version table exists — running 'alembic upgrade head'"
    python -m alembic upgrade head
else
    if [ "$USERS_EXISTS" = "1" ]; then
        echo "Schema already present but alembic_version missing — stamping head to avoid duplicate-creates"
        python -m alembic stamp head
    else
        echo "No schema detected — running 'alembic upgrade head'"
        python -m alembic upgrade head
    fi
fi

# Apply SQL initialization/seed file if present (idempotent SQL with IF NOT EXISTS/ON CONFLICT)
if [ -f "/code/sql/init.sql" ]; then
    echo "Applying SQL init script /code/sql/init.sql..."
    # If POSTGRES_* env vars are available use them, else try parsing DATABASE_URL
    : "${POSTGRES_USER:=}":
    : "${POSTGRES_PASSWORD:=}":
    : "${POSTGRES_DB:=}":
    if [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ]; then
        echo "POSTGRES env vars missing in web container; attempting to parse DATABASE_URL"
        # expected format: postgresql://user:password@host:port/dbname
        DBURL="$DATABASE_URL"
        USER=$(echo "$DBURL" | sed -E 's#postgresql://([^:]+):.*#\1#')
        PASS=$(echo "$DBURL" | sed -E 's#postgresql://[^:]+:([^@]+)@.*#\1#')
        DBNAME=$(echo "$DBURL" | sed -E 's#postgresql://[^/]+/.+#\0#' | sed -E 's#.*:5432/##')
        if [ -z "$USER" ] || [ -z "$PASS" ] || [ -z "$DBNAME" ]; then
            echo "Failed to determine DB credentials from DATABASE_URL. Skipping SQL init."
        else
            export PGPASSWORD="$PASS"
            psql -h db -U "$USER" -d "$DBNAME" -f /code/sql/init.sql || echo "psql returned non-zero exit code"
        fi
    else
        export PGPASSWORD="$POSTGRES_PASSWORD"
        psql -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /code/sql/init.sql || echo "psql returned non-zero exit code"
    fi
fi

echo "Starting application"
exec "$@"
