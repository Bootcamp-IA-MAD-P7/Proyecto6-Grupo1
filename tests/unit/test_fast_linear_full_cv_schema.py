"""Synthetic contract tests for fast linear phase-B evidence."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "reports" / "validation" / "cfpb_fast_linear_full_cv.schema.json"
CLASSES = (
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


def valid_evidence() -> dict:
    return {
        "schema_version": "1.0",
        "execution_phase": "full_cv",
        "candidate_family": "LogisticRegression",
        "train_partition_fingerprint": "synthetic-train-fingerprint",
        "group_column": "narrative_hash",
        "random_state": 42,
        "cross_validation": {
            "strategy": "StratifiedGroupKFold",
            "n_splits": 5,
            "shuffle": True,
            "random_state": 42,
        },
        "frozen_parameters": {"C": 1.0, "max_iter": 100},
        "retuning_performed": False,
        "convergence_warning_count": 0,
        "fold_metrics": [
            {"fold": fold, "train_macro_f1": 0.70, "validation_macro_f1": 0.67}
            for fold in range(1, 6)
        ],
        "metrics": {
            "macro_f1_mean": 0.67,
            "macro_f1_std": 0.01,
            "train_fold_macro_f1_gap": 0.03,
        },
        "per_class_metrics": {
            class_name: {"precision": 0.5, "recall": 0.5, "f1": 0.5}
            for class_name in CLASSES
        },
        "execution_cost": {"elapsed_seconds": 1.0},
        "decision_boundary": {
            "validation_used_for_selection": False,
            "test_used_for_selection": False,
            "champion_declared": False,
            "contains_prohibited_content": False,
        },
    }


class FastLinearFullCvSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_accepts_complete_aggregated_evidence(self):
        self.assertEqual(list(self.validator.iter_errors(valid_evidence())), [])

    def test_rejects_incomplete_class_coverage_and_gap_at_threshold(self):
        evidence = copy.deepcopy(valid_evidence())
        evidence["per_class_metrics"].pop("Credit card")
        self.assertNotEqual(list(self.validator.iter_errors(evidence)), [])
        evidence = valid_evidence()
        evidence["metrics"]["train_fold_macro_f1_gap"] = 0.05
        self.assertNotEqual(list(self.validator.iter_errors(evidence)), [])

    def test_rejects_retuning_reserved_partitions_and_champion(self):
        for path, value in (
            (("retuning_performed",), True),
            (("convergence_warning_count",), 1),
            (("decision_boundary", "validation_used_for_selection"), True),
            (("decision_boundary", "test_used_for_selection"), True),
            (("decision_boundary", "champion_declared"), True),
        ):
            evidence = copy.deepcopy(valid_evidence())
            target = evidence
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            self.assertNotEqual(list(self.validator.iter_errors(evidence)), [])

    def test_rejects_unaggregated_content(self):
        evidence = copy.deepcopy(valid_evidence())
        evidence["raw_narrative"] = "synthetic text is not allowed here"
        self.assertNotEqual(list(self.validator.iter_errors(evidence)), [])


if __name__ == "__main__":
    unittest.main()
