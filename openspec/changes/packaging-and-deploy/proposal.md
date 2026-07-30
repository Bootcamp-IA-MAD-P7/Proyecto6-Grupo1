# Proposal: packaging-and-deploy

## Why

The full stack (backend + frontend + DB) runs locally but has no reproducible
containerised deployment. ADV-01, ADV-02 and ADV-03 require Docker images,
PostgreSQL with minimum privilege, and a verifiable cloud URL.

## Measurable outcomes

1. `docker compose up` starts backend, frontend and PostgreSQL with health checks.
2. Health endpoint returns `ok` when model is loaded.
3. PostgreSQL schema uses minimum-privilege app user.
4. EC2 instance serves the app on port 80.
5. JWT login protects prediction endpoint.

## Non-goals

- Production-grade auth (OAuth, user database)
- HTTPS/TLS or custom domain
- CI/CD automatic deploy pipeline
- Model registry or versioned artifact download

## Affected delivery-level IDs

| ID | Impact |
|---|---|
| ADV-01 | Docker images, healthcheck, reproducible execution |
| ADV-02 | PostgreSQL schema, migrations, minimum privilege |
| ADV-03 | EC2 deployment, smoke test, rollback |

## Privacy and security impact

- Narratives never stored in PostgreSQL.
- JWT secret and DB credentials via environment variables.
- Non-root container user.
- App DB user has SELECT/INSERT only.

## Capabilities

- `docker-deployment`: three-container Docker Compose setup with Nginx proxy.
- `postgres-persistence`: PostgreSQL schema for predictions and feedback metadata.
- `jwt-authentication`: login endpoint with demo users and protected routes.
- `cloud-hosting`: EC2 t3.micro deployment with healthcheck.

## Tracking

- Jira: `PG-15`.
