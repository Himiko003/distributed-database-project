# Distributed Database Project – UTS SBDT

## Services
- FastAPI: http://localhost:8000 and Swagger: http://localhost:8000/docs
- PostgreSQL Primary: localhost:5432
- PostgreSQL Read Replica: localhost:5433
- Keycloak: http://localhost:8080

## Local development credentials
- PostgreSQL app user: `app_user` / `app_password_dev`
- Keycloak admin: `admin` / `admin_dev_password`
- Keycloak realm user: `mahasiswa` / `mahasiswa123`

These are development-only credentials. Do not use them in production.

## Start
```powershell
docker compose up -d --build
docker compose ps
```

## Stop
```powershell
docker compose down
```

To remove all local database data and reset volumes:
```powershell
docker compose down -v
```

## Authentication note
At this bootstrap stage, the API checks for the presence of a Bearer token only.
Cryptographic JWT signature and issuer validation against Keycloak JWKS must be added
before claiming full SSO security or using this outside a local demonstration.
