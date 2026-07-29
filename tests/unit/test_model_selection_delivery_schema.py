"""Synthetic validation for the governed delivery evidence schema."""

from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "reports" / "validation" / "cfpb_model_selection_delivery.schema.json"


def compliant_delivery_evidence() -> dict:
    fold = {
        "train_macro_f1": 0.71,
        "validation_macro_f1": 0.69,
        "class_limitations": ["Synthetic class"],
    }
    return {
        "schema_version": "1.0",
        "policy_version": "1.0",
        "execution_manifest": {
            "execution_scope": "delivery",
            "partition_fingerprint": "synthetic-partition-fingerprint",
            "package_versions": {"python": "3.11"},
            "random_state": 42,
        },
        "candidate": {"name": "xgb", "parameters": {"max_depth": 5}},
        "cross_validation": {
            "strategy": "StratifiedGroupKFold",
            "group_column": "narrative_hash",
            "n_splits": 5,
            "random_state": 42,
        },
        "optimization": {
            "primary_metric": "macro_f1",
            "max_trials": 30,
            "sampler_seed": 42,
        },
        "trials": [
            {
                "parameters": {"max_depth": 5},
                "fold_metrics": [deepcopy(fold) for _ in range(5)],
                "train_macro_f1_mean": 0.71,
                "train_macro_f1_std": 0.01,
                "validation_macro_f1_mean": 0.69,
                "validation_macro_f1_std": 0.02,
                "execution_cost_seconds": 12.0,
                "class_limitations": ["Synthetic class"],
            }
        ],
        "confirmation_boundary": {
            "reserved_partition": "validation",
            "used_for_selection": False,
            "protected_test_used": False,
            "champion_declared": False,
        },
    }


class GovernedDeliverySchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(schema)

    def test_accepts_aggregate_delivery_evidence(self):
        self.assertEqual(list(self.validator.iter_errors(compliant_delivery_evidence())), [])

    def test_rejects_test_results_and_raw_fields(self):
        evidence = compliant_delivery_evidence()
        evidence["test_results"] = {"macro_f1": 1.0}
        self.assertTrue(list(self.validator.iter_errors(evidence)))

    def test_rejects_incomplete_fold_metrics(self):
        evidence = compliant_delivery_evidence()
        del evidence["trials"][0]["fold_metrics"][0]["train_macro_f1"]
        self.assertTrue(list(self.validator.iter_errors(evidence)))

    def test_rejects_a_confirmation_used_for_selection(self):
        evidence = compliant_delivery_evidence()
        evidence["confirmation_boundary"]["used_for_selection"] = True
        self.assertTrue(list(self.validator.iter_errors(evidence)))


if __name__ == "__main__":
    unittest.main()
