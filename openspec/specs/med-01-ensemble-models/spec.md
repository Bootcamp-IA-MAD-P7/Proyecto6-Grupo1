## Purpose

Compare ensemble classifiers against the CFPB Logistic Regression baseline using the contracted eleven canonical classes, the protected temporal split, and reproducible aggregate evidence.

## Requirements

### Requirement: Comparable ensemble models

The pipeline SHALL train Random Forest and XGBoost on the baseline's 70/15/15 temporal split and SHALL report validation macro F1, weighted F1, accuracy, macro precision, and macro recall.

#### Scenario: Same protected split

- **WHEN** an ensemble model is trained
- **THEN** it uses the same train, validation, and test partitions as the baseline

#### Scenario: Complete validation metrics

- **WHEN** training and validation complete
- **THEN** the report includes the agreed classification metrics for each compared model

### Requirement: Reusable ML components

Vectorization, evaluation, model wrappers, tuning, and visualization SHALL be reusable modules under `src/ml/` and SHALL accept configuration dictionaries where applicable.

#### Scenario: Independent imports

- **WHEN** a supported `src/ml/` component is imported
- **THEN** it can be used without depending on a training script

### Requirement: Protected hyperparameter optimization

Hyperparameter search SHALL use validation data and SHALL NOT use the protected test partition for model selection.

#### Scenario: Recorded best trial

- **WHEN** a tuning run completes
- **THEN** its selected parameters and validation result are recorded as aggregate evidence

### Requirement: Reproducible classification evidence

The pipeline SHALL produce aggregate comparison reports, confusion matrices, and feature-importance figures without CFPB narratives.

#### Scenario: Evidence without sensitive text

- **WHEN** a comparison report or figure is generated
- **THEN** it contains metrics, configurations, or labels only and no complaint narratives

### Requirement: Portable LightGBM reference

LightGBM MAY be evaluated as an additional comparison reference. It SHALL use CPU by default so that local and CI execution do not require OpenCL; GPU acceleration SHALL require an explicit compatible-environment option.

#### Scenario: Default portable execution

- **WHEN** LightGBM is trained without an explicit GPU option
- **THEN** it runs on CPU

#### Scenario: Explicit GPU acceleration

- **WHEN** a compatible environment invokes `--lgbm-gpu`
- **THEN** LightGBM may use the configured GPU device

### Requirement: Governed model selection

An ensemble comparison SHALL NOT be presented as selecting a production model when its agreed overfitting control has not passed.

#### Scenario: High validation gap

- **WHEN** a compared model exceeds the approved train-validation gap
- **THEN** the report records the limitation and defers selection to a subsequent governed change
