## ADDED Requirements

### Requirement: Explicit local inference configuration

ClaimVox SHALL use a real prediction HTTP client only when an explicit local API
base URL is configured. Without that configuration, it SHALL retain the existing
clearly identified mock client.

#### Scenario: Default mock mode

- **GIVEN** no local API base URL is configured
- **WHEN** a user submits a valid narrative
- **THEN** ClaimVox uses the contract-valid mock client and identifies its result as simulated

#### Scenario: Configured local API mode

- **GIVEN** a valid local API base URL is configured
- **WHEN** a user submits a valid narrative while connected
- **THEN** ClaimVox sends only the contract `PredictionRequest` to `POST /api/v1/predictions`

### Requirement: Browser-to-service request is safe and contract-validated

The HTTP transport SHALL use JSON, validate every response through the existing
TypeScript contract parser, and expose only safe error categories to the interface.

#### Scenario: Contract-valid response

- **GIVEN** the API returns a conformant `PredictionResponse`
- **WHEN** the transport receives it
- **THEN** ClaimVox renders the returned class, alternatives, confidence, and review state

#### Scenario: Failed or incompatible response

- **GIVEN** the request fails, times out, is rejected, or returns an incompatible response
- **WHEN** ClaimVox handles the outcome
- **THEN** it shows a safe accessible error without response internals, URLs, or narrative text

### Requirement: Local CORS access is least-privilege

The backend SHALL allow cross-origin browser access only for explicitly configured
local origins. It SHALL NOT use a wildcard origin or enable credentialed requests
for this integration.

#### Scenario: Allowed local origin

- **GIVEN** a local ClaimVox origin appears in the backend allowlist
- **WHEN** it sends an allowed preflight or prediction request
- **THEN** the backend accepts that origin according to the configured policy

#### Scenario: Unconfigured origin

- **GIVEN** an origin is absent from the allowlist
- **WHEN** it attempts cross-origin access
- **THEN** the backend does not grant CORS access

### Requirement: End-to-end evidence uses synthetic input only

The repository SHALL record aggregate, reproducible evidence of the configured
local browser-to-service path without storing CFPB narratives, model binaries,
credentials, or browser request logs.

#### Scenario: Local integration verification

- **GIVEN** a local API and an explicitly configured ClaimVox client
- **WHEN** the end-to-end verification runs with synthetic input
- **THEN** the evidence records configuration, status categories, review state, and checks without request text
