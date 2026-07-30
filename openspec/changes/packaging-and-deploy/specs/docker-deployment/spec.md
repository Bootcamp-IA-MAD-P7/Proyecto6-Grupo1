## Purpose

Provide reproducible containerised deployment of the full ClaimVox stack with
health monitoring, minimum-privilege database, and cloud hosting.

## ADDED Requirements

### Requirement: Reproducible Docker execution
The project SHALL provide a Docker Compose configuration that starts backend, frontend, and database with a single command and reports healthy status.

#### Scenario: Full stack starts with docker compose
- **GIVEN** Docker and Docker Compose are installed
- **WHEN** `docker compose up` is executed from the project root
- **THEN** three containers start (backend, frontend, db) and all report healthy within 60 seconds

#### Scenario: Health endpoint confirms model loaded
- **GIVEN** the model artifact is present in the backend image
- **WHEN** GET `/api/v1/health` is called
- **THEN** the response contains `status: ok`

### Requirement: PostgreSQL with minimum privilege
The database SHALL use a dedicated application user with only the permissions required for runtime operation.

#### Scenario: App user cannot create or drop tables
- **GIVEN** the backend connects as claimvox_app
- **WHEN** it attempts CREATE TABLE or DROP TABLE
- **THEN** the operation is denied by PostgreSQL

#### Scenario: Narratives are never stored
- **GIVEN** a prediction is processed
- **WHEN** metadata is persisted to the database
- **THEN** only prediction_id, predicted_class, confidence, model_version, and timestamps are stored

### Requirement: Cloud deployment accessible on port 80
The application SHALL be deployed to a cloud instance accessible via HTTP on port 80 with the same Docker Compose configuration.

#### Scenario: Smoke test from external client
- **GIVEN** the EC2 instance is running with docker compose
- **WHEN** an external client calls GET `http://<public-ip>/api/v1/health`
- **THEN** the response is 200 with status ok or degraded

### Requirement: JWT authentication for predictions
The prediction endpoint SHALL require a valid JWT token obtained via the login endpoint.

#### Scenario: Unauthenticated prediction rejected
- **GIVEN** no Authorization header is sent
- **WHEN** POST `/api/v1/predictions` is called
- **THEN** the response is 401 Unauthorized

#### Scenario: Authenticated prediction accepted
- **GIVEN** a valid Bearer token from POST `/api/v1/auth/login`
- **WHEN** POST `/api/v1/predictions` is called with the token
- **THEN** the response is 200 with a valid PredictionResponse
