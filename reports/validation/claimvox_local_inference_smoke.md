# ClaimVox local inference smoke test

Date: `2026-07-28`
OpenSpec change: `integrate-claimvox-real-inference`
Jira: `PG-6`

## Purpose

Verify the live local boundary between the ClaimVox development server and the
FastAPI prediction service without storing a complaint narrative, browser logs,
model artifact, credentials, or response body.

## Local configuration

| Component | Local value | State |
| --- | --- | --- |
| ClaimVox development origin | `http://127.0.0.1:5173` | Served locally |
| FastAPI service | `http://127.0.0.1:8000` | Healthy |
| Backend CORS allowlist | ClaimVox development and preview origins | Explicit local opt-in |
| Frontend API selection | `VITE_PREDICTION_API_BASE_URL` | Present in served frontend module |

No wildcard origin, credentials, public domain, proxy, or deployment setting was
used. The local baseline artifact remains ignored by Git.

## Aggregate results

| Check | Result |
| --- | --- |
| ClaimVox `/classify` route | HTTP `200` |
| Served frontend module contains configured local API value | Yes |
| `OPTIONS /api/v1/predictions` from ClaimVox origin | HTTP `200` |
| Preflight grants ClaimVox origin | Yes |
| `POST /api/v1/predictions` with synthetic input | HTTP `200` |
| Response uses a non-mock model mode | Yes |
| Predicted class belongs to the canonical taxonomy | Yes |
| Confidence is available | Yes |
| Alternatives returned | `10` |
| Human review remains required | Yes |
| Response echoes submitted text | No |

## Privacy assertions

- The request used synthetic text only; the text itself is intentionally not
  recorded here.
- No CFPB narrative, request body, response body, browser log, credential, or
  model artifact is versioned as evidence.
- The prediction endpoint did not echo the submitted synthetic text.

## Human visual confirmation

After the protocol-level checks, a human opened the local ClaimVox flow, used
the built-in synthetic example, and confirmed that the visible result is labelled
`Prediction response` rather than `Mock response`, while `Human review required`
remains visible. No screenshot or submitted text was retained.
