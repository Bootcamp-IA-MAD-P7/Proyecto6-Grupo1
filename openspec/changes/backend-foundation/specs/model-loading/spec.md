## Purpose

Load the trained baseline artifact (`models/cfpb_baseline.pkl`) at startup for real
inference, or fall back gracefully to mock mode when the artifact is unavailable.

## ADDED Requirements

### Requirement: Real prediction using baseline artifact
When the baseline artifact (`models/cfpb_baseline.pkl`) is available, the service SHALL load it and produce real predictions using the trained TF-IDF vectorizer and LogisticRegression model.

#### Scenario: Baseline artifact loaded at startup
- **GIVEN** the file `models/cfpb_baseline.pkl` exists and is a valid joblib artifact containing `vectorizer`, `model`, and `config`
- **WHEN** the service starts
- **THEN** the service loads the artifact and sets `model_version` to a value identifying the baseline (not "mock-v0")

#### Scenario: Real predictions use model probabilities
- **GIVEN** the baseline artifact is loaded
- **WHEN** a valid narrative is submitted
- **THEN** `predicted_class` matches the class with highest model probability, `confidence` is a number between 0 and 1, and `alternatives` reflect model output sorted by confidence descending

### Requirement: Mock fallback when artifact is unavailable
When the baseline artifact is not available (file missing, corrupted, or loading error), the service SHALL operate in mock mode, returning synthetic responses clearly identified as mock.

#### Scenario: Service starts without artifact
- **GIVEN** the file `models/cfpb_baseline.pkl` does not exist
- **WHEN** the service starts
- **THEN** the service logs a warning (without narrative content), starts successfully in mock mode, and health endpoint reports `status: "degraded"`

#### Scenario: Mock response is clearly identified
- **GIVEN** the service is running in mock mode
- **WHEN** a valid PredictionRequest is submitted
- **THEN** `model_version` is `"mock-v0"`, `confidence` is `null`, `review_required` is `true`, `review_reasons` includes `"confidence_unavailable"`, and `warnings` includes a message indicating mock mode
