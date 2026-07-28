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
| Authentication / authorization | NOT implemented (pending decision) |
| CORS | NOT implemented (pending decision) |
| Rate limiting | NOT implemented (pending decision) |
| Database / persistence | NOT implemented |
| Docker | NOT implemented |
| RAG integration | Interface only (not implemented) |

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

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `APP_MODEL_PATH` | `models/cfpb_baseline.pkl` | Path to the joblib model artifact |
| `APP_SERVICE_VERSION` | `0.1.0` | Version reported in health endpoint |
| `APP_TAXONOMY_VERSION` | `1.0` | Taxonomy version in prediction responses |
| `APP_DEBUG` | `false` | Debug mode (do not use in production) |

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
│   └── prediction_service.py  # Orchestration: predictor → response
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
- Error responses use `ErrorResponse` schema (no stack traces, no paths)
- Model loaded from local filesystem only (no remote download)
- Configuration via environment variables (no secrets in code)

## Limitations

- No authentication or authorization
- No CORS headers (must be configured before frontend integration)
- No rate limiting
- No persistence or feedback collection
- Model artifact is gitignored and must exist locally to serve real predictions
- No formal model versioning/registry (artifact identified by config params)

## Related documents

- [OpenAPI contract](../../docs/api/openapi.json)
- [Target contract](../../config/cfpb_target_contract.json)
- [Security baseline](../../docs/security/security_baseline.md)
- [System blueprint](../../docs/architecture/system_blueprint.md)
- [OpenSpec change](../../openspec/changes/backend-foundation/)
