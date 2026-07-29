"""Synthetic contract tests for fast linear phase-A evidence."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "reports" / "validation" / "cfpb_fast_linear_search.schema.json"


def valid_evidence() -> dict:
    return {
        "schema_version": "1.0",
        "execution_phase": "search",
        "candidate_family": "LogisticRegression",
        "train_partition_fingerprint": "synthetic-train-fingerprint",
        "group_column": "narrative_hash",
        "random_state": 42,
        "sample": {
            "grouped": True,
            "maximum_rows": 20000,
            "rows_used": 100,
            "sampling_seed": 42,
        },
        "cross_validation": {
            "strategy": "StratifiedGroupKFold",
            "n_splits": 3,
            "shuffle": True,
            "random_state": 42,
        },
        "optimization": {
            "primary_metric": "macro_f1",
            "max_trials": 10,
            "trials_completed": 2,
            "sampler_seed": 42,
        },
        "metrics": {"macro_f1_mean": 0.5, "macro_f1_std": 0.01},
        "frozen_parameters": {"C": 1.0, "max_iter": 100},
        "execution_cost": {"elapsed_seconds": 1.0},
        "class_limitations": [
            {"class_name": "Synthetic class", "limitation_code": "low_support"}
        ],
        "decision_boundary": {
            "validation_used_for_selection": False,
            "test_used_for_selection": False,
            "champion_declared": False,
            "contains_prohibited_content": False,
        },
    }


class FastLinearSearchSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_accepts_aggregated_search_evidence(self):
        self.assertEqual(list(self.validator.iter_errors(valid_evidence())), [])

    def test_rejects_invalid_phase_budget(self):
        evidence = copy.deepcopy(valid_evidence())
        evidence["optimization"]["max_trials"] = 11
        self.assertNotEqual(list(self.validator.iter_errors(evidence)), [])

    def test_rejects_reserved_partitions_and_champion(self):
        for key in ("validation_used_for_selection", "test_used_for_selection", "champion_declared"):
            evidence = copy.deepcopy(valid_evidence())
            evidence["decision_boundary"][key] = True
            self.assertNotEqual(list(self.validator.iter_errors(evidence)), [])

    def test_rejects_unstructured_or_sensitive_content_fields(self):
        evidence = copy.deepcopy(valid_evidence())
        evidence["narrative"] = "synthetic text is not allowed here"
        self.assertNotEqual(list(self.validator.iter_errors(evidence)), [])


if __name__ == "__main__":
    unittest.main()
