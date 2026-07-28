## Purpose

Load the trained baseline artifact (`models/cfpb_baseline.pkl`) at startup for real
inference, or fall back gracefully to mock mode when the artifact is unavailable.

## Requirements

### Requirement: Real prediction using baseline artifact

When the baseline artifact is available, the service SHALL load it and produce real
predictions using the trained TF-IDF vectorizer and Logistic Regression model.

#### Scenario: Baseline artifact loaded at startup

- **GIVEN** `models/cfpb_baseline.pkl` is a valid joblib artifact containing `vectorizer`, `model`, and `config`
- **WHEN** the service starts
- **THEN** it loads the artifact and sets `model_version` to a value other than `mock-v0`

#### Scenario: Real predictions use model probabilities

- **GIVEN** the baseline artifact is loaded
- **WHEN** a valid narrative is submitted
- **THEN** `predicted_class` matches the highest model probability, `confidence` is between 0 and 1, and alternatives are sorted by confidence

### Requirement: Mock fallback when artifact is unavailable

When the artifact is missing, corrupted, or cannot be loaded, the service SHALL
operate in mock mode and identify synthetic responses clearly.

#### Scenario: Service starts without artifact

- **GIVEN** `models/cfpb_baseline.pkl` is unavailable
- **WHEN** the service starts
- **THEN** it starts in mock mode, logs no narrative content, and health reports `degraded`

#### Scenario: Mock response is clearly identified

- **GIVEN** the service is running in mock mode
- **WHEN** a valid request is submitted
- **THEN** `model_version` is `mock-v0`, confidence is null, review is required, and warnings identify mock mode
