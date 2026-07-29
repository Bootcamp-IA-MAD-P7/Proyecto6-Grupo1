"""Cross-contract synthetic checks for fast linear PG-11 boundaries."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.ml.evaluate_model_selection import (
    DEFAULT_POLICY_PATH,
    ModelSelectionInputError,
    load_selection_policy,
    phase_settings,
    validate_training_input_path,
)
from tests.unit.test_fast_linear_full_cv_schema import valid_evidence


ROOT = Path(__file__).resolve().parents[2]
FULL_CV_SCHEMA_PATH = ROOT / "reports" / "validation" / "cfpb_fast_linear_full_cv.schema.json"


class FastLinearSelectionBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load_selection_policy(DEFAULT_POLICY_PATH)
        cls.full_cv_validator = Draft202012Validator(
            json.loads(FULL_CV_SCHEMA_PATH.read_text(encoding="utf-8"))
        )

    def test_uses_only_train_with_grouped_three_and_five_fold_profiles(self):
        validate_training_input_path(Path("train.parquet"))
        for name in ("cfpb_training.parquet", "validation.parquet", "test.parquet"):
            with self.assertRaises(ModelSelectionInputError):
                validate_training_input_path(Path(name))

        self.assertEqual(self.policy["grouping"]["group_column"], "narrative_hash")
        self.assertEqual(phase_settings(self.policy, "search")["n_splits"], 3)
        self.assertEqual(phase_settings(self.policy, "full_cv")["n_splits"], 5)

    def test_phase_b_is_frozen_and_cannot_promote_a_champion(self):
        full_cv = phase_settings(self.policy, "full_cv")
        self.assertEqual(full_cv["parameters_source"], "phase_a_frozen")
        self.assertFalse(full_cv["retuning_allowed"])
        self.assertFalse(self.policy["selection"]["champion_declared_automatically"])
        self.assertFalse(self.policy["data_scope"]["validation_allowed_for_selection"])
        self.assertFalse(self.policy["data_scope"]["protected_test_allowed_for_selection"])

    def test_full_cv_evidence_requires_eleven_classes_and_strict_gap(self):
        evidence = valid_evidence()
        self.assertEqual(len(evidence["per_class_metrics"]), 11)
        self.assertLess(evidence["metrics"]["train_fold_macro_f1_gap"], 0.05)
        self.assertEqual(list(self.full_cv_validator.iter_errors(evidence)), [])


if __name__ == "__main__":
    unittest.main()
