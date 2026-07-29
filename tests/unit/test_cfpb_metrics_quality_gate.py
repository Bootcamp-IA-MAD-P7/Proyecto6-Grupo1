"""Synthetic tests for the CFPB aggregate metrics quality gate."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.quality.cfpb_metrics_quality_gate import (
    MetricsQualityGateError,
    validate_metrics_report,
)


ROOT = Path(__file__).resolve().parents[2]
QUALITY_GATES = json.loads((ROOT / "config" / "cfpb_quality_gates.json").read_text(encoding="utf-8"))


def conforming_report() -> dict[str, object]:
    per_class = {
        f"class-{index}": {
            "precision": 0.6,
            "recall": 0.6,
            "f1-score": 0.6,
            "support": 10,
        }
        for index in range(11)
    }
    return {
        "train": {"macro_f1": 0.64},
        "validation": {
            "accuracy": 0.8,
            "macro_f1": 0.6,
            "weighted_f1": 0.8,
            "precision_macro": 0.6,
            "recall_macro": 0.6,
        },
        "per_class_metrics": per_class,
        "gap_macro_f1": 0.04,
        "gap_within_threshold": True,
    }


class CFPBMetricsQualityGateTests(unittest.TestCase):
    def test_accepts_conforming_aggregate_report(self) -> None:
        evidence = validate_metrics_report(
            conforming_report(),
            quality_gates=QUALITY_GATES,
            selection_partition="validation",
        )

        self.assertEqual(evidence["canonical_class_count"], 11)
        self.assertTrue(evidence["gap_within_threshold"])
        self.assertNotIn("narrative", evidence)

    def test_rejects_report_with_a_missing_validation_field(self) -> None:
        report = conforming_report()
        del report["validation"]["accuracy"]

        with self.assertRaisesRegex(MetricsQualityGateError, "validation.accuracy"):
            validate_metrics_report(report, quality_gates=QUALITY_GATES, selection_partition="validation")

    def test_rejects_class_without_a_required_metric(self) -> None:
        report = conforming_report()
        del report["per_class_metrics"]["class-0"]["recall"]

        with self.assertRaisesRegex(MetricsQualityGateError, "per_class_metrics.recall"):
            validate_metrics_report(report, quality_gates=QUALITY_GATES, selection_partition="validation")

    def test_rejects_gap_equal_to_the_exclusive_threshold(self) -> None:
        report = conforming_report()
        report["gap_macro_f1"] = 0.05
        report["gap_within_threshold"] = False

        with self.assertRaisesRegex(MetricsQualityGateError, "gap"):
            validate_metrics_report(report, quality_gates=QUALITY_GATES, selection_partition="validation")

    def test_rejects_protected_test_as_selection_partition(self) -> None:
        with self.assertRaisesRegex(MetricsQualityGateError, "Protected test"):
            validate_metrics_report(
                conforming_report(),
                quality_gates=QUALITY_GATES,
                selection_partition="test_protected",
            )


if __name__ == "__main__":
    unittest.main()
