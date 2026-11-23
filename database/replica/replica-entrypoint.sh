#!/usr/bin/env bash
set -e
PGDATA="${PGDATA:-/var/lib/postgresql/data}"

if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "Initializing standby from primary with pg_basebackup..."
  until pg_isready -h "$PRIMARY_HOST" -p "$PRIMARY_PORT"; do sleep 2; done
  pg_basebackup -h "$PRIMARY_HOST" -p "$PRIMARY_PORT" -D "$PGDATA" \
    -U "$REPLICATION_USER" -Fp -Xs -P -R
  chmod 0700 "$PGDATA"
fi

exec docker-entrypoint.sh postgres -c hot_standby=on
