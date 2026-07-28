## 1. Correct the configuration boundary

- [x] 1.1 Separate TF-IDF settings from Logistic Regression settings in
  `scripts/ml/train_baseline.py` and restore defaults that match the approved
  baseline policy and its prepared local partitions.
- [x] 1.2 Add focused synthetic regression coverage for artifact creation and
  unsupported-key protection.

## 2. Verify local training and backend readiness

- [x] 2.1 Run the focused tests and the existing baseline tests. Evidence:
  `python -m unittest tests.unit.test_cfpb_baseline tests.contract.test_backend_contract -v`
  passed 33 tests on 2026-07-28 (Python 3.11 local environment).
- [x] 2.2 Create a local ignored artifact from the real prepared corpus, writing
  any smoke report under `models/` rather than replacing versioned evidence.
  Evidence: 1.372.751/294.161/294.161 approved local partitions and
  `models/cfpb_baseline.pkl` reproduced on 2026-07-28.
- [x] 2.3 Use that artifact to smoke-test backend health and prediction without
  exposing any input narrative. Evidence: health `ok`, prediction `200`,
  `baseline-lr-C0.1-f8000`, numeric confidence, canonical output and no echo.

## 3. Evidence and closure

- [x] 3.1 Add a safe aggregated validation report for the training and backend
  smoke test; update only documentation whose meaning changes.
- [x] 3.2 Run repository quality and strict OpenSpec validation. Evidence:
  `python scripts/quality/check_repository.py` and
  `npm exec -- openspec validate fix-baseline-vectorizer-config --type change --strict`
  passed on 2026-07-28.
