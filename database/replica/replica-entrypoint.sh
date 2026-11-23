
#!/usr/bin/env bash
set -e

PGDATA="${PGDATA:-/var/lib/postgresql/data}"

# Pastikan password tersedia untuk pg_basebackup
export PGPASSWORD="${REPLICATION_PASSWORD}"

if [ -z "$PGPASSWORD" ]; then
    echo "ERROR: REPLICATION_PASSWORD is empty"
    exit 1
fi

if [ ! -s "$PGDATA/PG_VERSION" ]; then
    echo "Initializing standby from primary with pg_basebackup..."

    until pg_isready -h "$PRIMARY_HOST" -p "$PRIMARY_PORT"; do
        echo "Waiting for PostgreSQL Primary..."
        sleep 2
    done

    pg_basebackup \
        -h "$PRIMARY_HOST" \
        -p "$PRIMARY_PORT" \
        -D "$PGDATA" \
        -U "$REPLICATION_USER" \
        -Fp \
        -Xs \
        -P \
        -R \
        -w

    chmod 0700 "$PGDATA"
fi

echo "Starting PostgreSQL Replica..."

exec docker-entrypoint.sh postgres -c hot_standby=on
