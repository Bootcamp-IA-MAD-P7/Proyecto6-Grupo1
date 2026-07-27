## Purpose

Expose an HTTP endpoint that receives a complaint narrative and returns a multiclass
prediction conforming to the OpenAPI contract (`docs/api/openapi.json`), using the
trained baseline model when available or a clearly-identified mock otherwise.

## ADDED Requirements

### Requirement: Prediction endpoint accepts PredictionRequest
The service SHALL expose `POST /api/v1/predictions` accepting a JSON body conforming to the `PredictionRequest` schema defined in `docs/api/openapi.json`.

#### Scenario: Valid narrative produces a prediction
- **GIVEN** the service is running and a predictor is loaded
- **WHEN** a client sends POST `/api/v1/predictions` with `{"narrative": "I was charged twice for a deposit into my checking account"}`
- **THEN** the response status is 200 and the body conforms to `PredictionResponse` with `predicted_class` being one of the 11 canonical labels from `config/cfpb_target_contract.json`

#### Scenario: Empty or whitespace-only narrative is rejected
- **GIVEN** the service is running
- **WHEN** a client sends POST `/api/v1/predictions` with `{"narrative": "   "}`
- **THEN** the response status is 422 and the body conforms to `ErrorResponse`

#### Scenario: Missing narrative field is rejected
- **GIVEN** the service is running
- **WHEN** a client sends POST `/api/v1/predictions` with `{}`
- **THEN** the response status is 400 and the body conforms to `ErrorResponse`

### Requirement: Prediction response conforms to PredictionResponse contract
The service SHALL return responses matching all required fields of `PredictionResponse`: `prediction_id` (UUID), `predicted_class` (canonical label), `alternatives` (array), `confidence` (number or null), `review_required` (boolean), `review_reasons` (array), `model_version` (non-empty string), `taxonomy_version` (non-empty string), `created_at` (ISO datetime), `warnings` (array).

#### Scenario: Response contains all required fields
- **GIVEN** a valid PredictionRequest is submitted
- **WHEN** the service processes it successfully
- **THEN** the response contains every field required by `PredictionResponse` and `predicted_class` belongs to the `CanonicalClass` enum

#### Scenario: Alternatives contain valid canonical labels
- **GIVEN** a valid PredictionRequest is submitted
- **WHEN** the service returns a successful prediction
- **THEN** every element in `alternatives` has a `class_label` from the 11 canonical classes and a `confidence` that is a number between 0 and 1 or null

#### Scenario: Response never echoes the narrative
- **GIVEN** any PredictionRequest
- **WHEN** the service returns any response (success or error)
- **THEN** the response body does not contain the narrative text from the request

### Requirement: Input validation and error responses
The service SHALL validate all inputs at the boundary and return errors conforming to `ErrorResponse` without exposing internal details or request content.

#### Scenario: Unexpected fields are rejected
- **GIVEN** the PredictionRequest schema has `additionalProperties: false`
- **WHEN** a client sends `{"narrative": "text", "extra_field": "value"}`
- **THEN** the response status is 400 and the body conforms to `ErrorResponse`

#### Scenario: client_request_id exceeding max length is rejected
- **GIVEN** the contract limits `client_request_id` to 100 characters
- **WHEN** a client sends a request with `client_request_id` of 101+ characters
- **THEN** the response status is 422 and the body conforms to `ErrorResponse`

#### Scenario: Error responses do not leak internal state
- **GIVEN** any invalid request
- **WHEN** the service returns an error
- **THEN** the `message` field contains a safe description, never the stack trace, model path, or narrative content

### Requirement: No narrative logging or persistence
The service SHALL NOT log, persist, or include the complaint narrative in any output other than the model's internal vectorization during prediction.

#### Scenario: Logs do not contain narrative text
- **GIVEN** a prediction is processed
- **WHEN** the service writes access or application logs
- **THEN** no log entry contains the `narrative` field value from the request

#### Scenario: No file-based persistence of narratives
- **GIVEN** the service processes predictions
- **WHEN** any file I/O occurs
- **THEN** no file written by the service contains narrative text
