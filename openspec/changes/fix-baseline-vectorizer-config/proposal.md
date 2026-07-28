## Why

The reproducible baseline training command fails before vectorization because its
configuration mixes TF-IDF options with Logistic Regression options. This blocks
creation of the local, ignored artifact required to verify the real backend path.

## Tracking

- Jira: `PG-3`.

## What Changes

- Separate vectorizer-only configuration from classifier metadata in the baseline
  training command.
- Add a synthetic regression test proving that training accepts the approved
  baseline configuration and produces a serializable artifact.
- Preserve the existing model family, split policy, target contract, metrics
  reports, and protected-test policy.

## Capabilities

### New Capabilities

- `baseline-training-configuration`: ensures the approved baseline configuration
  can be executed reproducibly without passing unsupported options to TF-IDF.

### Modified Capabilities

- None.

## Impact

- Affected code: `scripts/ml/train_baseline.py`, optionally the vectorizer wrapper,
  and focused synthetic tests.
- No API, dataset, target-label, dependency, frontend, or infrastructure change.
- Tracking: Jira `PG-3`; the resulting ignored local artifact will be used only to
  verify the already-merged backend foundation (`PG-5`).
