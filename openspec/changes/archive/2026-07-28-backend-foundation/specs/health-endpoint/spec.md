## Purpose

Expose a non-sensitive health endpoint that reports service status, reflecting whether
the model artifact is loaded (ok) or the service is operating in degraded mock mode.

## ADDED Requirements

### Requirement: Health endpoint reports service status
The service SHALL expose `GET /api/v1/health` returning a `HealthResponse` conforming to the contract in `docs/api/openapi.json`.

#### Scenario: Healthy service with loaded model
- **GIVEN** the service started with a valid baseline artifact
- **WHEN** GET `/api/v1/health` is called
- **THEN** the response is `{"status": "ok", "service_version": "<version>"}` with status 200

#### Scenario: Degraded service without model
- **GIVEN** the service started in mock mode because the artifact was unavailable
- **WHEN** GET `/api/v1/health` is called
- **THEN** the response is `{"status": "degraded", "service_version": "<version>"}` with status 200
