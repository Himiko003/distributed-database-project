
#!/usr/bin/env bash
set -e

PGDATA="${PGDATA:-/var/lib/postgresql/data}"

if [ ! -s "$PGDATA/PG_VERSION" ]; then
    echo "Initializing standby from primary..."

    until pg_isready -h "$PRIMARY_HOST" -p "$PRIMARY_PORT"; do
        echo "Waiting for PostgreSQL Primary..."
        sleep 5
    done

    export PGPASSWORD="$REPLICATION_PASSWORD"

    pg_basebackup \
        -h "$PRIMARY_HOST" \
        -p "$PRIMARY_PORT" \
        -D "$PGDATA" \
        -U "$REPLICATION_USER" \
        -Fp \
        -Xs \
        -P \
        -R

    chmod 0700 "$PGDATA"

    echo "Standby initialization completed."
fi

exec docker-entrypoint.sh postgres -c hot_standby=on
