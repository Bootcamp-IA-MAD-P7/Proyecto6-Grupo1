# Tasks: packaging-and-deploy

- Proposal: [`proposal.md`](proposal.md)
- Spec: [`specs/`](specs/)
- Design: [`design.md`](design.md)

---

## T-001 Docker Compose with three services

- Status: `[ ]`
- Owner: `Backend / José`
- Requirements covered: ADV-01
- Verification: `docker compose up` starts all 3 containers healthy.

## T-002 PostgreSQL schema with minimum privilege

- Status: `[ ]`
- Owner: `Backend / José`
- Requirements covered: ADV-02
- Verification: App user can INSERT/SELECT but not DROP/CREATE.

## T-003 JWT authentication

- Status: `[x]`
- Owner: `Backend / José`
- Verification: Login returns token; predictions reject unauthenticated requests.

## T-004 AWS EC2 deployment

- Status: `[ ]`
- Owner: `Backend / José`
- Requirements covered: ADV-03
- Verification: `curl http://<EC2-IP>/api/v1/health` returns ok.

## Checklist de cierre

- [ ] Docker Compose runs full stack with healthchecks.
- [ ] PostgreSQL uses minimum-privilege app user.
- [x] JWT protects prediction endpoint.
- [ ] EC2 instance accessible on port 80 with versioned smoke and rollback evidence.
- [x] Narratives never stored in DB.
