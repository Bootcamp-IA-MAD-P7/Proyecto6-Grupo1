#!/bin/sh
set -eu

: "${CLAIMVOX_DB_APP_PASSWORD:?CLAIMVOX_DB_APP_PASSWORD is required}"

psql --set=ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  --set=app_password="$CLAIMVOX_DB_APP_PASSWORD" <<'EOSQL'
SELECT format('CREATE ROLE claimvox_app LOGIN PASSWORD %L', :'app_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'claimvox_app')
\gexec
ALTER ROLE claimvox_app PASSWORD :'app_password';
EOSQL
