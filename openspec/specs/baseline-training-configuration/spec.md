## Purpose

Ensure the approved TF-IDF plus Logistic Regression baseline can create a local
artifact reproducibly without mixing incompatible configuration options.

## Requirements

### Requirement: Training separates vectorizer and classifier configuration

The baseline command SHALL pass only valid TF-IDF settings to its vectorizer.
Classifier settings SHALL remain model metadata and SHALL NOT be forwarded to
`TfidfVectorizer`.

Defaults SHALL match the approved baseline policy: `C=0.1`, 8,000 features,
`min_df=3`, `max_df=0.8`, n-grams `(1, 2)`, and sublinear TF enabled. They SHALL
use the approved local train, validation, and protected-test partitions; an unsplit
corpus MAY only be used through an explicit legacy input argument.

#### Scenario: Approved baseline configuration trains

- **GIVEN** a valid local dataset containing only contracted canonical labels
- **WHEN** the baseline command runs with its approved configuration
- **THEN** it creates a joblib artifact with vectorizer, classifier, and metadata without unsupported-keyword errors

#### Scenario: Default command uses the approved policy and partitions

- **WHEN** the command runs without tuning or data-path overrides
- **THEN** its parameters and inputs match the approved policy and prepared partitions

### Requirement: Regression coverage uses synthetic data

The repository SHALL include focused coverage of this configuration boundary with
synthetic data only.

#### Scenario: Synthetic training regression test

- **GIVEN** a temporary synthetic dataset
- **WHEN** the regression test executes the training path
- **THEN** it completes without CFPB narratives or a versioned model artifact
