## Why

ClaimVox is already a usable React PWA prototype and `PG-5` now verifies the
FastAPI prediction service locally, but the user-facing flow still returns only a
clearly labelled mock. Connecting the two in a controlled local configuration is
the remaining essential step to demonstrate a real prediction with human review,
without confusing it with a deployed operational decision.

## Tracking

- Jira: `PG-6`.

## What Changes

- Configure ClaimVox to call the existing `POST /api/v1/predictions` endpoint
  only when an explicit local API base URL is provided; preserve the mock as the
  safe default for demos and unavailable services.
- Validate the HTTP response against the existing TypeScript prediction contract
  before it is rendered, and show safe, accessible states for unavailable,
  malformed, or failed responses.
- Preserve the narrative-only request boundary, the explicit human-review
  requirement, privacy notices, and the prohibition on automatic routing.
- Add focused frontend and contract verification plus aggregate evidence for the
  local end-to-end path.

## Capabilities

### New Capabilities

- `claimvox-inference-integration`: controlled browser-to-local-service
  integration, including configuration, failure handling, and evidence.

### Modified Capabilities

- `complaint-routing-interface`: the prediction client can select a validated
  real service response when explicitly configured, while retaining mock mode.

## Impact

- Affected code: `app/interface` prediction client, configuration, classification
  flow and focused tests; no baseline, backend route, or OpenAPI schema change is
  planned.
- Delivery impact: advances `ESS-04` from partial backend/frontend foundations
  toward a verifiable end-to-end flow; it does not by itself verify deployment,
  authentication, feedback, database, MLOps, or a production Champion.
- Privacy and security: the browser sends only the user-provided narrative to the
  configured local API; no CFPB narrative, audio, credential, or response log may
  be committed, and failures must not expose request text or internal paths.
