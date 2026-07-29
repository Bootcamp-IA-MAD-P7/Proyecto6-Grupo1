# Backend API — Prediction Service

Service that receives complaint narratives and returns multiclass predictions
using the trained baseline model, conforming to `docs/api/openapi.json`.

## Status

| Capability | State |
|---|---|
| Prediction endpoint (POST /api/v1/predictions) | Implemented (mock + real) |
| Health endpoint (GET /api/v1/health) | Implemented |
| Baseline model loading (models/cfpb_baseline.pkl) | Implemented |
| Mock fallback when artifact missing | Implemented |
| Predictor interface for extensibility | Implemented |
| Feedback endpoint (POST /api/v1/feedback) | Implemented for local use |
| Aggregated feedback summary (GET /api/v1/feedback/summary) | Implemented for local use |
| Governed local persistence | Implemented with finite-retention SQLite |
| Authentication / authorization | NOT implemented (pending decision) |
| CORS | Local opt-in only; explicit origins, no credentials or wildcard |
| Request controls | 5,000-character maximum and 20 predictions/minute per temporary local client, configurable by environment |
| Response headers | `Cache-Control: no-store`, `Referrer-Policy: no-referrer`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` |
| Technical events | Local structured events without narrative, identity, IP, alternatives or individual confidence |
| Shared database / migrations | NOT implemented |
| Docker | NOT implemented |
| RAG integration | Not implemented |

The service and a reproducible local baseline artifact were smoke-tested on
2026-07-28. The evidence is aggregate only and is recorded in
[`reports/validation/backend_foundation_real_smoke.md`](../../reports/validation/backend_foundation_real_smoke.md).
ClaimVox can consume the service **only locally and under explicit
configuration**. This does not mean that the service is deployed,
authenticated, or production-ready.

## Installation

From the project root:

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install fastapi "uvicorn[standard]" pydantic pydantic-settings httpx joblib scikit-learn numpy
```

## Running locally

```bash
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

The service will:
- Load `models/cfpb_baseline.pkl` if available → real predictions, health = "ok"
- Fall back to mock mode if the artifact is missing → synthetic predictions, health = "degraded"

API docs available at: http://localhost:8000/docs

### Local ClaimVox integration

This is a local development path, not a deployment configuration. The canonical
Git Bash sequence, including the frontend variable and the health check, is in
the [ClaimVox local guide](../../docs/project_management/essential_delivery_guide.md).
To permit a ClaimVox development origin, set an explicit allowlist before
starting the API:

```bash
export APP_CORS_ALLOWED_ORIGINS="http://127.0.0.1:5173"
python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

Only local `localhost` or `127.0.0.1` origins are accepted. Do not use `*`,
credentials, a public domain, or a proxy as a substitute for a deployment
security policy. The checked-in [`.env.example`](.env.example) is a reference;
the actual environment remains local and ignored by Git.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `APP_MODEL_PATH` | `models/cfpb_baseline.pkl` | Path to the joblib model artifact |
| `APP_SERVICE_VERSION` | `0.1.0` | Version reported in health endpoint |
| `APP_TAXONOMY_VERSION` | `1.0` | Taxonomy version in prediction responses |
| `APP_DEBUG` | `false` | Debug mode (do not use in production) |
| `APP_CORS_ALLOWED_ORIGINS` | empty | Comma-separated local ClaimVox origins; cross-origin access stays disabled when absent |
| `APP_MAX_NARRATIVE_CHARACTERS` | `5000` | Local maximum narrative length; may reduce but not exceed the published contract maximum |
| `APP_PREDICTION_RATE_LIMIT_PER_MINUTE` | `20` | Best-effort requests per temporary local client and minute; resets with the process |

## Running tests

```bash
# Contract tests (validates responses against OpenAPI spec)
python -m unittest discover -s tests/contract -p "test_*.py" -v

# All tests
python -m unittest discover -s tests -p "test_*.py" -v
```

## Architecture

```text
app/api/
├── main.py              # App factory, lifespan (model loading)
├── config.py            # Settings from environment
├── errors.py            # Exception → safe ErrorResponse
├── routes/
│   ├── predictions.py   # POST /api/v1/predictions
│   └── health.py        # GET /api/v1/health
├── schemas/
│   ├── request.py       # PredictionRequest (from OpenAPI)
│   ├── response.py      # PredictionResponse, Alternative, ErrorResponse
│   └── health.py        # HealthResponse
├── services/
│   ├── prediction_service.py  # Orchestration: predictor → response
│   ├── feedback_service.py    # Local creation, retention and aggregation
│   └── feedback_repository.py # Governed local SQLite repository
└── predictors/
    ├── base.py          # PredictorInterface (abstract)
    ├── baseline.py      # Real model (TF-IDF + LogisticRegression)
    └── mock.py          # Synthetic fallback
```

The predictor interface allows swapping implementations without changing routes:
- `BaselinePredictor`: loads the .pkl, vectorizes, predicts
- `MockPredictor`: returns synthetic response with `model_version: "mock-v0"`
- Future: RAG or ensemble predictors implement the same interface

## Security

- Narratives are NEVER logged, persisted, or echoed in responses
- Prediction events contain only timestamp, rounded duration, status, predictor mode, model version and human-review flag
- Error responses use `ErrorResponse` schema (no stack traces, no paths)
- Model loaded from local filesystem only (no remote download)
- Configuration via environment variables (no secrets in code)

## Limitations

- No authentication or authorization
- Local CORS is opt-in through `APP_CORS_ALLOWED_ORIGINS`; it accepts only
  explicitly configured local origins, never wildcards or credentials
- Local in-memory rate limiting is not a distributed or production-grade abuse control
- Feedback persistence is local-only; there is no shared database, user
  history or endpoint for individual records
- Model artifact is gitignored and must exist locally to serve real predictions
- No formal model versioning/registry (artifact identified by config params)
- ClaimVox can use this service locally when both origins are explicitly
  configured. The end-to-end evidence is
  [`claimvox_local_inference_smoke.md`](../../reports/validation/claimvox_local_inference_smoke.md);
  this is not a deployed public API.

## Related documents

- [OpenAPI contract](../../docs/api/openapi.json)
- [Target contract](../../config/cfpb_target_contract.json)
- [Security baseline](../../docs/security/security_baseline.md)
- [System blueprint](../../docs/architecture/system_blueprint.md)
- [Archived OpenSpec change](../../openspec/changes/archive/2026-07-28-backend-foundation/)
- [Local backend smoke evidence](../../reports/validation/backend_foundation_real_smoke.md)
