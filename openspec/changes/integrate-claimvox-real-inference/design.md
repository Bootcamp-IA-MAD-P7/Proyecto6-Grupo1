## Context

`PG-4` delivers ClaimVox as a React PWA with a typed mock prediction client.
`PG-5` delivers the local FastAPI service and verifies it against a reproducible
baseline artifact, but the browser has no opt-in path to call it. The two projects
already share `docs/api/openapi.json` and the TypeScript contract, so this change
can use that boundary without changing the model, target taxonomy, or API schema.

The browser and local API normally run on different development origins. The
integration therefore needs a deliberately narrow development CORS configuration
and a configuration mechanism that keeps the production-safe mock default.

## Goals / Non-Goals

**Goals:**

- Provide an explicit local configuration that selects an HTTP prediction client.
- Send only `PredictionRequest.narrative` to the versioned endpoint and validate
  every response before rendering it.
- Represent loading, unavailable service, validation, malformed response, mock,
  and human-review states accessibly.
- Permit reproducible local browser-to-API verification using synthetic input and
  no committed model artifact or narrative.

**Non-Goals:**

- Authentication, authorization, real administration, persistence, feedback,
  CORS for public deployment, rate limiting, Docker, cloud deployment, or RAG.
- Changing `docs/api/openapi.json`, the eleven-class contract, the baseline
  policy, protected-test metrics, or selecting a production Champion.
- Automatic complaint routing or a decision without human review.

## Decisions

### Explicit client selection by build-time environment

Use a Vite `VITE_PREDICTION_API_BASE_URL` value to opt into the HTTP client. If
it is absent, ClaimVox continues using `createMockPredictionClient`; this keeps
the existing prototype usable offline and prevents a browser from silently sending
narratives to an unknown endpoint.

An alternative was making the API URL mandatory. It is rejected because the PWA
currently has an intentional mock-only demonstration mode and no deployed API.

### Contract client owns fetch and error mapping

Create a small HTTP transport under `services/` and pass it to the existing
`createContractPredictionClient`. It uses `POST /api/v1/predictions`, JSON only,
an abort timeout, and maps only safe status categories to `PredictionClientError`.
The page receives no raw response body or URL-specific error detail.

An alternative was calling `fetch` inside `ClassificationPage`; it is rejected
because it would bypass the tested contract boundary and make mock/real selection
harder to test.

### Narrow local CORS origin list

The FastAPI service reads an explicit comma-separated allowlist such as
`APP_CORS_ALLOWED_ORIGINS=http://127.0.0.1:4173,http://localhost:4173`. It does
not enable a wildcard origin, credentials, or a public production policy. The
default remains no cross-origin browser access until a local developer sets the
allowlist deliberately.

An alternative was a Vite development proxy. It is rejected because it would
hide the actual browser/API origin boundary and would not verify the API's CORS
behaviour.

### Real results remain advisory

The result view MUST use `review_required` and `review_reasons` returned by the
service. A real `model_version` can be shown as technical traceability, but the
page never labels a response as a final routing decision. Mock mode retains its
visible mock marker.

## Risks / Trade-offs

- [A local artifact is absent] → Health is degraded or prediction returns mock;
  the UI explains the unavailable service and does not fabricate a real result.
- [CORS configuration is too broad] → Explicit origins only, no wildcard or
  credentials, and backend tests cover the default and allowed behaviour.
- [A malformed API response reaches the UI] → Existing runtime contract parser
  rejects it and the page exposes a safe error.
- [A user submits sensitive text] → Existing minimisation notice remains;
  no client logging, persistence, screenshots, or committed test text is added.
- [PWA is offline] → Existing offline behaviour blocks submission rather than
  generating a simulated real prediction.

## Migration and rollback

The mock remains the default. Local developers opt in by setting the frontend API
base URL and matching backend allowlist, then can remove either setting to return
to mock mode. Reverting this change restores the current mock-only browser flow;
no data migration or artifact deletion is required.

## Open Questions

- A future deployment change must define trusted origins, TLS, authentication,
  rate limits, and operational retention separately.
- Whether the end-to-end demo uses a local artifact or a controlled shared
  environment remains a deployment decision outside this change.
