"""Focused tests for the governed PG-11 selection boundary."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import polars as pl

from scripts.ml.evaluate_model_selection import (
    DEFAULT_POLICY_PATH,
    ModelSelectionInputError,
    apply_grouped_search_limit,
    execute_search,
    load_selection_policy,
    load_selection_training_partition,
    parse_args,
    phase_settings,
    validate_training_input_path,
)


class InputBoundaryTests(unittest.TestCase):
    def test_rejects_corpus_validation_and_test_paths(self):
        for name in ("cfpb_training.parquet", "validation.parquet", "test.parquet"):
            with self.assertRaises(ModelSelectionInputError):
                validate_training_input_path(Path(name))

    def test_requires_group_column(self):
        frame = pl.DataFrame(
            {
                "complaint_what_happened": ["synthetic text"],
                "product_canonical": ["Credit card"],
            }
        )
        with patch("scripts.ml.evaluate_model_selection.pl.read_parquet", return_value=frame):
            with self.assertRaisesRegex(ModelSelectionInputError, "narrative_hash"):
                load_selection_training_partition(Path("train.parquet"))

    def test_loads_only_selection_columns(self):
        frame = pl.DataFrame(
            {
                "complaint_what_happened": ["synthetic text"],
                "product_canonical": ["Credit card"],
                "narrative_hash": ["synthetic-group"],
                "date_received": ["2026-01-01"],
            }
        )
        with patch("scripts.ml.evaluate_model_selection.pl.read_parquet", return_value=frame):
            result = load_selection_training_partition(Path("train.parquet"))
        self.assertEqual(
            result.columns,
            ["complaint_what_happened", "product_canonical", "narrative_hash"],
        )

    def test_fast_linear_policy_has_approved_two_phase_budget(self):
        policy = load_selection_policy(DEFAULT_POLICY_PATH)
        self.assertEqual(policy["candidate"]["family"], "LogisticRegression")
        self.assertEqual(policy["phase_a_tuning"]["maximum_training_rows"], 50_000)
        self.assertEqual(policy["phase_a_tuning"]["n_splits"], 3)
        self.assertEqual(policy["phase_a_tuning"]["max_trials"], 30)
        self.assertEqual(policy["phase_b_full_cv"]["n_splits"], 5)
        self.assertFalse(policy["phase_b_full_cv"]["retuning_allowed"])

    def test_exposes_only_the_approved_phase_settings(self):
        policy = load_selection_policy(DEFAULT_POLICY_PATH)
        self.assertEqual(phase_settings(policy, "search")["n_splits"], 3)
        self.assertEqual(phase_settings(policy, "full_cv")["n_splits"], 5)
        with self.assertRaises(ModelSelectionInputError):
            phase_settings(policy, "retune")

    def test_rejects_non_linear_candidates_at_the_cli_boundary(self):
        with patch("sys.argv", ["evaluate_model_selection.py", "--candidate", "xgb"]):
            with self.assertRaises(SystemExit):
                parse_args()

    def test_grouped_search_limit_keeps_complete_groups_under_budget(self):
        frame = pl.DataFrame(
            {
                "complaint_what_happened": ["synthetic"] * 8,
                "product_canonical": ["Credit card"] * 4 + ["Mortgage"] * 4,
                "narrative_hash": ["a", "a", "b", "b", "c", "c", "d", "d"],
            }
        )
        sample = apply_grouped_search_limit(
            frame,
            {"maximum_training_rows": 4, "sampling_seed": 42},
        )
        self.assertLessEqual(sample.height, 4)
        self.assertEqual(
            sample.group_by("narrative_hash").len().get_column("len").to_list(),
            [2, 2],
        )

    def test_search_execution_writes_only_schema_conforming_aggregate(self):
        frame = pl.DataFrame(
            {
                "complaint_what_happened": ["alpha token"] * 3 + ["beta token"] * 3,
                "product_canonical": ["Credit card", "Credit card", "Credit card", "Mortgage", "Mortgage", "Mortgage"],
                "narrative_hash": ["a", "b", "c", "d", "e", "f"],
            }
        )
        policy = load_selection_policy(DEFAULT_POLICY_PATH)
        output_path = Path("reports/validation/synthetic-fast-linear-search.json")
        tuning_result = {
            "best_params": {"C": 1.0},
            "macro_f1_mean": 0.5,
            "macro_f1_std": 0.01,
            "class_limitations": [],
            "n_trials": 30,
        }
        with patch(
            "scripts.ml.evaluate_model_selection.tune_logistic_regression_cv",
            return_value=tuning_result,
        ), patch.object(Path, "write_text") as write_text:
            evidence = execute_search(frame, policy, output_path)
        self.assertEqual(evidence["candidate_family"], "LogisticRegression")
        self.assertFalse(evidence["decision_boundary"]["champion_declared"])
        self.assertEqual(evidence["optimization"]["trials_completed"], 30)
        write_text.assert_called_once()


if __name__ == "__main__":
    unittest.main()
