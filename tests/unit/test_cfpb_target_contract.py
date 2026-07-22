"""Invariants for the versioned CFPB target contract."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "config" / "cfpb_target_contract.json"


class CFPBTargetContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def test_contract_has_eleven_unique_canonical_labels(self) -> None:
        labels = self.contract["target"]["canonical_labels"]
        self.assertEqual(len(labels), 11)
        self.assertEqual(len(labels), len(set(labels)))

    def test_aliases_only_point_to_canonical_labels(self) -> None:
        target = self.contract["target"]
        canonical = set(target["canonical_labels"])
        self.assertTrue(set(target["aliases"].values()).issubset(canonical))
        self.assertTrue(set(target["aliases"]).isdisjoint(canonical))

    def test_contract_covers_all_fourteen_observed_labels(self) -> None:
        target = self.contract["target"]
        covered = (
            set(target["canonical_labels"])
            | set(target["aliases"])
            | set(target["excluded_source_labels"])
        )
        self.assertEqual(len(covered), 14)

    def test_ambiguous_historical_label_is_excluded(self) -> None:
        target = self.contract["target"]
        self.assertIn("Credit card or prepaid card", target["excluded_source_labels"])
        self.assertNotIn("Credit card or prepaid card", target["aliases"])

    def test_unknown_labels_fail_explicitly(self) -> None:
        self.assertEqual(self.contract["target"]["unknown_label_policy"], "fail")

    def test_narrative_is_the_only_allowed_feature(self) -> None:
        features = self.contract["features"]
        self.assertEqual(features["allowed"], ["complaint_what_happened"])
        self.assertTrue(set(features["allowed"]).isdisjoint(features["forbidden"]))
        self.assertIn(features["target_source"], features["forbidden"])
        self.assertIn(features["target_derived"], features["forbidden"])

    def test_duplicate_groups_cannot_cross_splits(self) -> None:
        duplicates = self.contract["duplicates"]
        self.assertTrue(duplicates["prevent_group_cross_split"])
        self.assertEqual(duplicates["conflicting_target_policy"], "exclude_and_report")

    def test_contract_forbids_persisting_narratives(self) -> None:
        privacy = self.contract["privacy"]
        persistence_flags = [
            value for key, value in privacy.items() if key.startswith("persist_narratives")
        ]
        self.assertTrue(persistence_flags)
        self.assertFalse(any(persistence_flags))


if __name__ == "__main__":
    unittest.main()
