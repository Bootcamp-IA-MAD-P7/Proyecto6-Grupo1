# Design: packaging-and-deploy

## Context

The backend (FastAPI + baseline model) and frontend (React PWA ClaimVox) are
functional locally. Deployment requires containerisation, a shared database,
authentication, and a cloud host.

## Decisions

| ID | Decision | Rationale |
|---|---|---|
| D-001 | Docker Compose with 3 services | Single command deploys full stack; mirrors production topology |
| D-002 | Nginx reverse proxy on port 80 | Eliminates CORS; single entry point for frontend and API |
| D-003 | PostgreSQL 16 for persistence | Shared, multi-connection DB required for ADV-02; SQLite remains local fallback |
| D-004 | Minimum-privilege DB user | claimvox_app has SELECT/INSERT/DELETE only; admin creates schema |
| D-005 | JWT authentication | Simple token-based auth suitable for demo; no external IdP needed |
| D-006 | AWS EC2 t3.micro | Free tier eligible in eu-west-1; sufficient RAM for baseline model |

## Architecture

```text
:80 → Nginx (frontend container)
       ├── /          → React static files
       └── /api/*     → proxy_pass → backend:8000
                                      ├── /auth/login (public)
                                      ├── /health (public)
                                      └── /predictions (JWT required)
                                             ↓
                                       PostgreSQL:5432
```

## Risks and rollback

- EC2 termination removes the deployment instantly.
- Docker files can be removed from repo to revert.
- JWT secret in env var is acceptable for demo only.
