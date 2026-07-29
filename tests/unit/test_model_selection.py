"""Focused tests for the governed PG-11 selection boundary."""

from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch

import numpy as np
import polars as pl

from scripts.ml.evaluate_model_selection import (
    DELIVERY_PROFILE,
    DEFAULT_POLICY_PATH,
    DEFAULT_DELIVERY_APPROVAL_PATH,
    ModelSelectionInputError,
    PILOT_PROFILE,
    apply_pilot_limit,
    build_delivery_evidence,
    load_selection_policy,
    load_selection_training_partition,
    resolve_execution_profile,
    validate_and_write_delivery_evidence,
    validate_delivery_approval,
    validate_delivery_output_path,
    validate_training_input_path,
)
from src.ml import tuning


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

    def test_pilot_limit_is_deterministic_and_bounded(self):
        frame = pl.DataFrame({"value": list(range(10))})
        policy = {"maximum_training_rows": 4, "sampling_seed": 42}
        first = apply_pilot_limit(frame, policy)
        second = apply_pilot_limit(frame, policy)
        self.assertEqual(first.height, 4)
        self.assertEqual(first.to_dicts(), second.to_dicts())

    def test_pilot_policy_has_approved_budget(self):
        policy = load_selection_policy(DEFAULT_POLICY_PATH)
        self.assertEqual(policy["pilot"]["maximum_training_rows"], 20_000)
        self.assertEqual(policy["pilot"]["n_splits"], 3)
        self.assertEqual(policy["pilot"]["max_trials_per_candidate"], 5)

    def test_delivery_profile_uses_the_full_versioned_budget(self):
        profile = resolve_execution_profile(
            load_selection_policy(DEFAULT_POLICY_PATH), DELIVERY_PROFILE
        )
        self.assertEqual(profile["name"], DELIVERY_PROFILE)
        self.assertEqual(profile["n_splits"], 5)
        self.assertEqual(profile["n_trials"], 30)
        self.assertTrue(profile["may_verify_delivery_criteria"])

    def test_delivery_rejects_a_reduced_tuning_budget(self):
        policy = load_selection_policy(DEFAULT_POLICY_PATH)
        policy["optimization"]["max_trials_per_candidate"] = 5
        with self.assertRaisesRegex(ModelSelectionInputError, "reduced tuning budget"):
            resolve_execution_profile(policy, DELIVERY_PROFILE)

    def test_delivery_rejects_incompatible_grouped_cross_validation_policy(self):
        for field, unsafe_value in (
            ("strategy", "StratifiedKFold"),
            ("group_column", "synthetic_group"),
            ("n_splits", 3),
        ):
            policy = load_selection_policy(DEFAULT_POLICY_PATH)
            policy["cross_validation"][field] = unsafe_value
            with self.subTest(field=field):
                with self.assertRaisesRegex(ModelSelectionInputError, "five-fold grouped"):
                    resolve_execution_profile(policy, DELIVERY_PROFILE)

    def test_pilot_profile_cannot_verify_delivery_criteria(self):
        profile = resolve_execution_profile(load_selection_policy(DEFAULT_POLICY_PATH), PILOT_PROFILE)
        self.assertFalse(profile["may_verify_delivery_criteria"])


class CrossValidationTests(unittest.TestCase):
    def test_cv_uses_versioned_grouped_strategy_and_seed(self):
        captured = {}

        class FakeSplitter:
            def __init__(self, **kwargs):
                captured.update(kwargs)

            def split(self, _matrix, _labels, _groups):
                yield np.array([0, 1]), np.array([2, 3])

        class FakeTrial:
            params = {"max_depth": 4}

            def __init__(self):
                self.user_attrs = {}

            def set_user_attr(self, name, value):
                self.user_attrs[name] = value

        class FakeStudy:
            def optimize(self, callback, n_trials):
                self.trial_count = n_trials
                trial = FakeTrial()
                self.best_trial = type(
                    "BestTrial",
                    (), {"params": trial.params, "value": callback(trial), "user_attrs": trial.user_attrs},
                )()
                self.trials = [self.best_trial]

        with (
            patch.object(tuning, "StratifiedGroupKFold", FakeSplitter),
            patch.object(tuning.optuna.samplers, "TPESampler", return_value=object()),
            patch.object(tuning.optuna, "create_study", return_value=FakeStudy()),
            patch.object(
                tuning,
                "_objective_rf",
                return_value={
                    "train_macro_f1": 0.6,
                    "validation_macro_f1": 0.5,
                    "class_limitations": ["b"],
                    "per_class_metrics": {
                        "b": {"precision": 0.5, "recall": 0.5, "f1": 0.5, "support": 2}
                    },
                },
            ),
        ):
            result = tuning.tune_hyperparams_cv(
                "rf",
                np.arange(4),
                ["a", "a", "b", "b"],
                ["g1", "g2", "g3", "g4"],
                n_splits=5,
                n_trials=30,
                random_state=42,
            )

        self.assertEqual(captured, {"n_splits": 5, "shuffle": True, "random_state": 42})
        self.assertEqual(result["n_trials"], 30)
        self.assertEqual(result["fold_macro_f1"], [0.5])
        self.assertEqual(result["fold_metrics"][0]["train_macro_f1"], 0.6)
        self.assertEqual(result["trials"][0]["class_limitations"], ["b"])
        self.assertEqual(result["per_class_metrics"]["b"]["support"], 2)


class DeliveryExecutionTests(unittest.TestCase):
    labels = (
        "Checking or savings account",
        "Credit card",
        "Credit reporting or other personal consumer reports",
        "Debt collection",
        "Debt or credit management",
        "Money transfer, virtual currency, or money service",
        "Mortgage",
        "Payday loan, title loan, personal loan, or advance loan",
        "Prepaid card",
        "Student loan",
        "Vehicle loan or lease",
    )

    def _delivery_result(self) -> dict:
        fold = {
            "train_macro_f1": 0.71,
            "validation_macro_f1": 0.69,
            "class_limitations": [],
        }
        return {
            "best_params": {"max_depth": 5},
            "macro_f1_mean": 0.69,
            "train_macro_f1_mean": 0.71,
            "n_trials": 30,
            "n_splits": 5,
            "random_state": 42,
            "per_class_metrics": {
                label: {"precision": 0.7, "recall": 0.7, "f1": 0.7, "support": 1}
                for label in self.labels
            },
            "trials": [
                {
                    "params": {"max_depth": 5},
                    "fold_metrics": [fold.copy() for _ in range(5)],
                    "train_macro_f1_mean": 0.71,
                    "train_macro_f1_std": 0.01,
                    "validation_macro_f1_mean": 0.69,
                    "validation_macro_f1_std": 0.02,
                    "execution_cost_seconds": 1.0,
                    "class_limitations": [],
                }
            ],
        }

    def test_accepts_the_versioned_xgboost_delivery_approval(self):
        validate_delivery_approval(DEFAULT_DELIVERY_APPROVAL_PATH, "xgb")

    def test_rejects_external_approval_and_output_paths(self):
        with TemporaryDirectory() as directory:
            external = Path(directory) / "approval.md"
            external.write_text("synthetic", encoding="utf-8")
            with self.assertRaises(ModelSelectionInputError):
                validate_delivery_approval(external, "xgb")
            with self.assertRaises(ModelSelectionInputError):
                validate_delivery_output_path(Path(directory) / "result.json")

    def test_writes_only_schema_valid_aggregate_delivery_evidence(self):
        policy = load_selection_policy(DEFAULT_POLICY_PATH)
        with TemporaryDirectory() as directory:
            train_input = Path(directory) / "train.parquet"
            output_path = Path(directory) / "result.json"
            train_input.write_bytes(b"synthetic-partition")
            evidence = build_delivery_evidence(
                policy=policy,
                candidate="xgb",
                result=self._delivery_result(),
                train_input=train_input,
            )
            validate_and_write_delivery_evidence(evidence, output_path)
            self.assertTrue(output_path.is_file())
            self.assertNotIn("test_results", output_path.read_text(encoding="utf-8"))


class RecommendationTests(unittest.TestCase):
    def test_prefers_lower_variability_within_macro_f1_tolerance(self):
        result = tuning.recommend_candidate(
            [
                {
                    "name": "a",
                    "macro_f1_mean": 0.7000,
                    "macro_f1_std": 0.03,
                    "train_validation_gap": 0.04,
                    "execution_cost": {"seconds": 10},
                    "class_limitations": [],
                },
                {
                    "name": "b",
                    "macro_f1_mean": 0.6995,
                    "macro_f1_std": 0.01,
                    "train_validation_gap": 0.04,
                    "execution_cost": {"seconds": 20},
                    "class_limitations": [],
                },
            ],
            maximum_gap=0.05,
            macro_f1_tie_tolerance=0.001,
        )
        self.assertEqual(result["status"], "recommended_for_validation")
        self.assertEqual(result["candidate"], "b")

    def test_rejects_candidates_without_approved_gap(self):
        result = tuning.recommend_candidate(
            [
                {
                    "name": "unsafe",
                    "macro_f1_mean": 0.9,
                    "macro_f1_std": 0.01,
                    "train_validation_gap": 0.05,
                    "execution_cost": {"seconds": 1},
                    "class_limitations": [],
                }
            ],
            maximum_gap=0.05,
            macro_f1_tie_tolerance=0.001,
        )
        self.assertEqual(result["status"], "no_selection_approved")
        self.assertIsNone(result["candidate"])


if __name__ == "__main__":
    unittest.main()
