# PG-11 delivery execution approval

- Date: `2026-07-29`
- Approver: Miguel, project coordinator
- Approved environment: Colab
- Candidate: `xgb`
- Input boundary: full approved local `train.parquet` only
- Cross-validation: `StratifiedGroupKFold`, `narrative_hash`, five folds, seed `42`
- Tuning budget: up to 30 trials
- Time limit: none

The approval does not permit loading reserved `validation` for selection or
retuning, loading protected `test`, declaring a Champion, changing the local
baseline used by ClaimVox, or publishing raw data, narratives, model binaries,
credentials, or sensitive logs.

The resulting evidence remains incomplete unless the complete execution finishes
and passes the versioned delivery schema and subsequent human review.
