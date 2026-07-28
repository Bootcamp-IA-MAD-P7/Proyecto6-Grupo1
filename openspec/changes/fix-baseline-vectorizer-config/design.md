## Context

`train_baseline.py` builds one dictionary containing both TF-IDF and classifier
settings, then passes it to `VectorizerConfig`. `TfidfVectorizer` rejects settings
such as `model`, `solver`, and `C`, so no local artifact is created.

## Decision

The training command SHALL construct a dedicated `vectorizer_config` containing
only supported TF-IDF keys: `max_features`, `min_df`, `max_df`, `ngram_range`, and
`sublinear_tf`. Classifier settings remain in the artifact metadata and the
evaluation report, but are not passed to `VectorizerConfig`.

The command defaults SHALL reproduce the evaluated baseline policy already
recorded in `reports/validation/cfpb_baseline.md`: `C=0.1`, 8,000 features,
`min_df=3`, `max_df=0.8`, unigrams plus bigrams, and sublinear TF. Other values
remain explicit CLI experiments and must not be presented as the evaluated
baseline.

The command SHALL also load the three prepared, group-isolated local partitions
by default. The old unsplit corpus path remains an explicit legacy option only;
it cannot silently replace the policy-approved train, validation, and protected
test inputs.

## Verification

- A synthetic test invokes the training path with a small temporary Parquet input
  and asserts that it writes a joblib artifact containing vectorizer, model, and
  config.
- The existing real local training command is rerun with output under ignored
  `models/`; it must not overwrite versioned official reports.
- Existing baseline tests and repository quality remain green.

## Non-goals

- No change to class labels, language policy, splitting, model family,
  hyperparameters, acceptance thresholds, official metrics, or backend routes.
- No raw dataset, artifact, or narrative is added to Git.
