# Design: backend-foundation

## Context

The project has a trained baseline model (`models/cfpb_baseline.pkl`) consisting of a
TF-IDF vectorizer and LogisticRegression classifier serialized with joblib. The React
PWA (ClaimVox) is integrated in `dev` consuming a local mock. A service is needed to
bridge the model artifact with the frontend via the contract defined in
`docs/api/openapi.json`.

Constraints from the project:

- Python 3.12 is the established runtime for ML and scripts.
- The artifact is a Python/scikit-learn object loadable only from Python.
- The OpenAPI contract is already defined and must not be modified.
- Architecture principles require domain-infrastructure separation (system blueprint).
- Security prohibits narrative logging, narrative persistence, and error detail exposure.

## Framework decision: FastAPI

| Criterion | FastAPI | Flask | Django | Node.js |
|---|---|---|---|---|
| Native Python .pkl loading | Yes | Yes | Yes | No (requires Python bridge) |
| Built-in OpenAPI generation | Yes (automatic) | No (extension) | No (extension) | No |
| Request validation with types | Yes (Pydantic) | No | Partial (DRF) | Partial (Joi/Zod) |
| Async support | Yes (ASGI) | Limited | Limited | Yes |
| Minimal for a service without DB | Yes | Yes | No (heavy) | Yes |
| Team Python familiarity | High | High | Medium | Low |
| Dependency footprint | Small | Small | Large | N/A (different runtime) |

**Decision**: FastAPI with Uvicorn. The model artifact is Python-native, the team uses
Python 3.12, and FastAPI provides automatic OpenAPI docs and Pydantic validation that
map directly to the existing contract schemas. This is the lightest path to a
contract-compliant service.

**Status**: Proposed. Pending team confirmation. If the team rejects FastAPI, the
predictor interface (R-008) ensures the framework choice does not affect domain logic.

## Architecture

```text
app/api/
├── main.py                  # FastAPI application factory, lifespan, startup
├── routes/
│   ├── predictions.py       # POST /api/v1/predictions
│   └── health.py            # GET /api/v1/health
├── schemas/
│   ├── request.py           # PredictionRequest (Pydantic, from OpenAPI)
│   ├── response.py          # PredictionResponse, Alternative, ErrorResponse
│   └── health.py            # HealthResponse
├── services/
│   └── prediction_service.py  # Orchestrates predictor call, builds response
├── predictors/
│   ├── base.py              # PredictorInterface (abstract)
│   ├── baseline.py          # BaselinePredictor (loads .pkl, vectorizes, predicts)
│   └── mock.py              # MockPredictor (returns synthetic response)
├── config.py                # Settings from environment variables
└── errors.py                # Exception handlers mapping to ErrorResponse
```

### Layer responsibilities

| Layer | Responsibility | Does NOT do |
|---|---|---|
| **Routes** | HTTP parsing, validation, response serialization | Business logic, model loading |
| **Schemas** | Data shapes, constraints, serialization | Logic, I/O |
| **Services** | Orchestration: call predictor, build PredictionResponse, assign UUID, timestamp | HTTP concerns, model internals |
| **Predictors** | Load artifact, vectorize input, produce raw prediction | HTTP, response formatting |
| **Config** | Read env vars, paths, feature flags | Hard-coded values |
| **Errors** | Map exceptions to safe ErrorResponse | Expose internals |

### Predictor interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class RawPrediction:
    predicted_class: str
    confidence: float | None
    alternatives: list[dict]  # [{"class_label": str, "confidence": float|None}]
    model_version: str

class PredictorInterface(ABC):
    @abstractmethod
    def predict(self, narrative: str) -> RawPrediction:
        """Produce a classification for the given narrative text."""

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the predictor is ready to serve predictions."""
```

- `BaselinePredictor`: loads `models/cfpb_baseline.pkl`, calls `vectorizer.transform()` + `model.predict_proba()`, returns top class with confidence and sorted alternatives.
- `MockPredictor`: returns a fixed canonical class with `confidence=None`, `model_version="mock-v0"`.
- Future RAG or enhanced predictor: implements the same interface, injected via config.

### Startup flow

```text
1. Read config (model path from env or default)
2. Try loading artifact from configured path
   ├── Success → use BaselinePredictor, health = "ok"
   └── Failure → log warning (no narrative), use MockPredictor, health = "degraded"
3. Inject selected predictor into prediction_service
4. Start Uvicorn
```

## Decisions

| ID | Decision | Rationale |
|---|---|---|
| D-001 | FastAPI + Uvicorn | Python-native artifact, automatic OpenAPI, Pydantic validation, lightweight |
| D-002 | Predictor interface with dependency injection | Allows mock/real/RAG swap without route changes (R-008) |
| D-003 | Artifact loaded at startup, not per-request | LogisticRegression is thread-safe for predict; avoids repeated I/O |
| D-004 | Mock fallback on load failure, not service crash | Allows CI/tests without artifact; health reports "degraded" |
| D-005 | No narrative in logs | Security baseline and threat model mandate body logging prohibition |
| D-006 | Schemas derive from OpenAPI contract | Single source of truth; Pydantic models mirror the contract |
| D-007 | Service placed in `app/api/` | Aligns with existing `app/` structure (README mentions `api/` as future) |

## Consequences

- The backend is Python-only; a future BFF or gateway would be a separate concern.
- The service is stateless (no DB); feedback and persistence are separate changes.
- The predictor interface allows adding RAG without modifying existing code (Open/Closed).
- Tests can inject MockPredictor regardless of artifact availability.
- CORS, auth, and rate limiting are not implemented; they will require separate decisions.

## Risks and rollback

| Risk | Mitigation |
|---|---|
| Artifact format changes (scikit-learn version) | Pin scikit-learn version in requirements; validate artifact schema at load |
| FastAPI rejected by team | Interface design is framework-agnostic; routes are thin wrappers |
| Model latency unexpected | LogisticRegression inference is <10ms; monitor in health check if needed |
| Pydantic schema drift from OpenAPI | Tests compare schema against `docs/api/openapi.json` |

Rollback: the service is a new addition. Removing it requires deleting `app/api/` and reverting any frontend integration pointing to it.

## Security

- Narrative never written to logs (structured logging with redaction).
- Error responses use `ErrorResponse` schema: `error_code`, `message`, `request_id`. No stack traces.
- Model loaded from local filesystem only (`models/` directory). No remote download.
- No secrets in code; configuration via environment variables.
- CORS, rate limiting, and auth are deferred (open decisions).

## Testing strategy

| Level | What | Tool |
|---|---|---|
| Unit | Predictor logic, service orchestration, schema validation | pytest |
| Contract | Response schema vs `docs/api/openapi.json` | schemathesis or manual JSON Schema validation |
| Integration | Full HTTP request/response cycle with MockPredictor | pytest + httpx (TestClient) |
| Smoke | Health endpoint reachable | curl / httpx |

All tests use synthetic narratives only. No CFPB data in test fixtures.

## Documentation impact

| Document | Change needed |
|---|---|
| `README.md` | Update "Backend e inferencia" status from "No iniciados" to "En curso" |
| `app/README.md` | Document `api/` structure and how to run the service |
| `docs/project_management/delivery_levels.md` | Update ESS-04 status to "En curso" when service passes contract tests |
| `CHANGELOG.md` | Add entry for backend-foundation |
