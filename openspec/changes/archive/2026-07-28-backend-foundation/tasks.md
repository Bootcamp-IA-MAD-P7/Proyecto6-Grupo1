# Tasks: backend-foundation

- Proposal: [`proposal.md`](proposal.md)
- Spec: [`specs/`](specs/)
- Design: [`design.md`](design.md)

---

## T-001 Scaffold FastAPI project and dependencies

- Status: `[x]`
- Owner: `Backend / José`
- Dependencies: none
- Requirements covered: D-001, D-007
- Work:
  - Create `app/api/` directory structure as defined in design.md.
  - Create `app/api/requirements.txt` (or extend `pyproject.toml`) with: `fastapi`, `uvicorn[standard]`, `pydantic`, `joblib`, `scikit-learn`, `polars` (pinned versions matching the baseline environment).
  - Create `app/api/main.py` with FastAPI app factory and lifespan.
  - Create `app/api/config.py` with settings read from environment variables (model path, service version).
- Verification:
  ```bash
  pip install -r app/api/requirements.txt
  python -c "from app.api.main import app; print(app.title)"
  ```
- Acceptance: the application object is importable and configured without errors.

---

## T-002 Define Pydantic schemas from OpenAPI contract

- Status: `[x]`
- Owner: `Backend / José`
- Dependencies: `T-001`
- Requirements covered: R-001, R-002, R-006
- Work:
  - Create `app/api/schemas/request.py` with `PredictionRequest` (narrative: str with min_length=1 and regex pattern `\S`, optional client_request_id with max_length=100, no additional properties).
  - Create `app/api/schemas/response.py` with `PredictionResponse`, `Alternative`, `ErrorResponse` matching `docs/api/openapi.json` exactly.
  - Create `app/api/schemas/health.py` with `HealthResponse`.
  - All `predicted_class` and `class_label` fields SHALL use a `Literal` or `Enum` built from the 11 canonical classes in `config/cfpb_target_contract.json`.
- Verification:
  ```bash
  python -c "from app.api.schemas.request import PredictionRequest; print('OK')"
  python -c "from app.api.schemas.response import PredictionResponse; print('OK')"
  python -m pytest tests/unit/test_backend_schemas.py -v
  ```
- Acceptance: schemas import cleanly, reject invalid inputs (empty narrative, extra fields, long client_request_id), and accept valid ones.

---

## T-003 Implement predictor interface, MockPredictor, and BaselinePredictor

- Status: `[x]`
- Owner: `Backend / José`
- Dependencies: `T-002`
- Requirements covered: R-003, R-004, R-008
- Work:
  - Create `app/api/predictors/base.py` with `PredictorInterface` (abstract class) and `RawPrediction` dataclass.
  - Create `app/api/predictors/mock.py` with `MockPredictor` that returns a fixed canonical class, `confidence=None`, `model_version="mock-v0"`.
  - Create `app/api/predictors/baseline.py` with `BaselinePredictor` that:
    - Loads `models/cfpb_baseline.pkl` via joblib at initialization.
    - Extracts `vectorizer` and `model` from the dict.
    - Implements `predict(narrative)`: vectorizes → `predict_proba()` → builds `RawPrediction` with top class, confidence, and sorted alternatives.
    - Implements `is_available()` → True if artifact loaded.
  - Handle loading errors gracefully (log warning without narrative content, fallback to mock).
- Verification:
  ```bash
  python -m pytest tests/unit/test_predictors.py -v
  ```
- Acceptance: MockPredictor always returns valid output. BaselinePredictor returns valid predictions when artifact exists. Loading failure does not crash.

---

## T-004 Implement prediction service and routes

- Status: `[x]`
- Owner: `Backend / José`
- Dependencies: `T-003`
- Requirements covered: R-001, R-002, R-004, R-005, R-007
- Work:
  - Create `app/api/services/prediction_service.py`:
    - Accepts a `PredictorInterface` instance.
    - Orchestrates: call predictor → assign UUID → set created_at → determine review_required and review_reasons → build PredictionResponse.
    - review_required is True when confidence is None or below threshold (configurable, default: always true in mock mode).
  - Create `app/api/routes/predictions.py`:
    - POST `/api/v1/predictions` handler: validates request, calls service, returns 200 or error.
  - Create `app/api/routes/health.py`:
    - GET `/api/v1/health` handler: returns HealthResponse with status based on predictor availability.
  - Create `app/api/errors.py`:
    - Exception handlers that map validation errors and internal errors to `ErrorResponse`.
    - Never include narrative, stack trace, or internal paths in error messages.
  - Wire startup in `main.py`: load predictor (baseline or fallback mock), inject into service, register routes.
- Verification:
  ```bash
  python -m pytest tests/integration/test_prediction_endpoint.py -v
  python -m pytest tests/integration/test_health_endpoint.py -v
  ```
- Acceptance: full request-response cycle works with MockPredictor; with BaselinePredictor when artifact is present. Health endpoint reflects actual state. Error responses conform to contract.

---

## T-005 Contract tests against OpenAPI spec

- Status: `[x]`
- Owner: `Backend / José`
- Dependencies: `T-004`
- Requirements covered: R-002, R-006
- Work:
  - Create `tests/contract/test_backend_contract.py`:
    - Validate that 200 responses match `PredictionResponse` JSON Schema from `docs/api/openapi.json`.
    - Validate that error responses (400, 422) match `ErrorResponse` JSON Schema.
    - Validate that health response matches `HealthResponse` JSON Schema.
    - Verify `predicted_class` is always one of the 11 canonical labels.
    - Verify response never contains the narrative text submitted.
  - All test fixtures use synthetic narratives only (no CFPB data).
- Verification:
  ```bash
  python -m pytest tests/contract/test_backend_contract.py -v
  ```
- Acceptance: all contract tests pass. Schema validation uses the real `docs/api/openapi.json` file as source of truth.

---

## T-006 Documentation and integration readiness

- Status: `[x]`
- Owner: `Backend / José`
- Dependencies: `T-005`
- Requirements covered: proposal outcomes, CONTRIBUTING.md compliance
- Work:
  - Create or update `app/api/README.md` with:
    - How to install dependencies.
    - How to run the service locally (`uvicorn app.api.main:app --reload`).
    - How to run tests.
    - Environment variables and configuration.
    - Limitations and what is NOT implemented (auth, CORS, rate limiting, DB, Docker).
  - Update `CHANGELOG.md` with the backend-foundation entry.
  - Do NOT update `delivery_levels.md` status yet (requires passing verification in a merged PR).
- Verification:
  ```bash
  python scripts/quality/check_repository.py
  git diff --check
  npm exec -- openspec validate backend-foundation --type change --strict
  ```
- Acceptance: repository quality passes, OpenSpec validates, documentation accurately describes the implemented state without claiming unimplemented capabilities.

---

## Checklist de cierre

- [x] All contract tests pass with both MockPredictor and BaselinePredictor. Evidence: 33 focused baseline and backend tests passed on 2026-07-28.
- [x] Health endpoint reports correct status (ok/degraded). Evidence: mock contract test and local real-artifact smoke returned `degraded` and `ok` respectively.
- [x] No narrative appears in any log output or response body. Evidence: synthetic contract and local smoke assertions passed; no request-body logging is implemented.
- [x] Error responses conform to ErrorResponse schema. Evidence: contract tests cover invalid, missing and extra request fields.
- [x] `docs/api/openapi.json` is unchanged (service conforms to existing contract).
- [x] `config/cfpb_target_contract.json` canonical labels are the only valid prediction classes. Evidence: synthetic real-predictor and contract tests passed.
- [x] All tests use synthetic data exclusively.
- [x] OpenSpec validates strict. Evidence: `npm exec -- openspec validate backend-foundation --type change --strict` passed on 2026-07-28.
- [x] Repository quality check passes. Evidence: `python scripts/quality/check_repository.py` passed on 2026-07-28.
- [x] Documentation distinguishes implemented vs. mock vs. pending. Evidence: README, API guide, delivery levels, daily, NotebookLM sources and `backend_foundation_real_smoke.md` were reconciled on 2026-07-28.

---

## Continuity

Once this change is merged:

- `003/T-007` (integrate real service) can proceed: ClaimVox points to the live API.
- `ESS-04` moves to "En curso" and can be verified once frontend consumes real predictions.
- Future changes for auth, CORS, rate limiting, Docker, and RAG build on this foundation via new OpenSpec changes.
