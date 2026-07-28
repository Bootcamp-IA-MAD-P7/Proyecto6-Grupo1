## Purpose

Ensure the approved TF-IDF plus Logistic Regression baseline can create a local
artifact reproducibly without mixing incompatible configuration options.

## ADDED Requirements

### Requirement: Training separates vectorizer and classifier configuration

The baseline training command SHALL pass only valid TF-IDF settings to its
vectorizer wrapper. Classifier settings SHALL be retained as model metadata and
shall not be forwarded to `TfidfVectorizer`.

The command defaults SHALL match the versioned baseline policy: `C=0.1`, 8,000
features, `min_df=3`, `max_df=0.8`, n-grams `(1, 2)`, and sublinear TF enabled.

The command defaults SHALL use the policy-approved local train, validation, and
protected-test partitions. An unsplit corpus MAY only be used via an explicit
legacy input argument.

#### Scenario: Approved baseline configuration trains

- **GIVEN** a valid local training dataset with the contracted canonical labels
- **WHEN** the baseline command runs with its approved configuration
- **THEN** it creates a joblib artifact containing a vectorizer, a classifier, and
  configuration metadata without an unsupported-keyword error.

#### Scenario: Default command reproduces the evaluated baseline policy

- **WHEN** the baseline command is invoked without model-tuning arguments
- **THEN** its configuration matches the documented evaluated baseline policy.

#### Scenario: Default command uses approved partitions

- **WHEN** the baseline command is invoked without data-path overrides
- **THEN** it reads the prepared train, validation, and protected-test files
  rather than recomputing a split from the unsplit corpus.

### Requirement: Regression coverage uses synthetic data

The repository SHALL contain focused automated coverage for this configuration
boundary using synthetic data only.

#### Scenario: Synthetic training regression test

- **GIVEN** a synthetic temporary dataset
- **WHEN** the regression test executes the training path
- **THEN** it completes without using CFPB narratives or producing a versioned
  model artifact.
