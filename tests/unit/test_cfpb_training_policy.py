"""Synthetic tests for the CFPB training-policy fingerprint gate."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.data.cfpb_training_policy import TrainingPolicyError, validate_reference_inputs


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_policy(path: Path, source: Path, contract: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "reference": {
                    "source_sha256": sha256(source),
                    "contract_sha256": sha256(contract),
                }
            }
        ),
        encoding="utf-8",
    )


class CFPBTrainingPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.source = self.root / "source.zip"
        self.contract = self.root / "contract.json"
        self.policy = self.root / "policy.json"
        self.source.write_bytes(b"synthetic-source")
        self.contract.write_text('{"synthetic": true}', encoding="utf-8")
        write_policy(self.policy, self.source, self.contract)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_matching_fingerprints_allow_preparation(self) -> None:
        policy = validate_reference_inputs(
            source_path=self.source,
            contract_path=self.contract,
            policy_path=self.policy,
        )
        self.assertIn("reference", policy)

    def test_changed_source_fails_without_exposing_content(self) -> None:
        self.source.write_bytes(b"synthetic-source-changed")
        with self.assertRaisesRegex(TrainingPolicyError, "does not match") as error:
            validate_reference_inputs(
                source_path=self.source,
                contract_path=self.contract,
                policy_path=self.policy,
            )
        self.assertNotIn("synthetic-source-changed", str(error.exception))

    def test_changed_contract_fails_before_preparation(self) -> None:
        self.contract.write_text('{"synthetic": false}', encoding="utf-8")
        with self.assertRaisesRegex(TrainingPolicyError, "does not match"):
            validate_reference_inputs(
                source_path=self.source,
                contract_path=self.contract,
                policy_path=self.policy,
            )

    def test_missing_input_fails_closed(self) -> None:
        with self.assertRaisesRegex(TrainingPolicyError, "unavailable"):
            validate_reference_inputs(
                source_path=self.root / "missing.zip",
                contract_path=self.contract,
                policy_path=self.policy,
            )

    def test_versioned_policy_defines_baseline_quality_gates(self) -> None:
        policy = json.loads(
            (ROOT / "config" / "cfpb_training_policy.json").read_text(encoding="utf-8")
        )
        self.assertEqual(policy["language"]["baseline"], "en")
        self.assertEqual(policy["split"]["min_class_support_per_split"], 100)
        self.assertTrue(policy["split"]["test_protected"])
        self.assertEqual(policy["baseline"]["primary_metric"], "macro_f1")
        self.assertEqual(policy["baseline"]["class_weight"], "balanced")
        self.assertEqual(policy["baseline"]["max_train_validation_macro_f1_gap"], 0.05)


if __name__ == "__main__":
    unittest.main()
