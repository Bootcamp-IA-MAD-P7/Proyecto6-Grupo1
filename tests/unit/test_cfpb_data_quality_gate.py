"""Synthetic tests for the CFPB data quality gate."""

from __future__ import annotations

import unittest

import polars as pl

from scripts.quality.cfpb_data_quality_gate import (
    DataQualityGateError,
    validate_partition_frames,
)


REQUIRED_COLUMNS = {
    "complaint_what_happened",
    "product_canonical",
    "narrative_hash",
}
CANONICAL_LABELS = {"Credit card", "Mortgage"}


def frame(rows: list[dict[str, str | None]]) -> pl.DataFrame:
    return pl.DataFrame(rows)


def validate(partitions: dict[str, pl.DataFrame]) -> dict[str, object]:
    return validate_partition_frames(
        partitions,
        required_columns=REQUIRED_COLUMNS,
        canonical_labels=CANONICAL_LABELS,
        group_key="narrative_hash",
        allowed_columns=REQUIRED_COLUMNS,
    )


class CFPBDataQualityGateTests(unittest.TestCase):
    def test_accepts_conforming_synthetic_partitions(self) -> None:
        evidence = validate(
            {
                "train": frame(
                    [
                        {
                            "complaint_what_happened": "synthetic text one",
                            "product_canonical": "Credit card",
                            "narrative_hash": "group-a",
                        },
                        {
                            "complaint_what_happened": "synthetic text two",
                            "product_canonical": "Mortgage",
                            "narrative_hash": "group-b",
                        },
                    ]
                ),
                "validation": frame(
                    [
                        {
                            "complaint_what_happened": "synthetic text three",
                            "product_canonical": "Credit card",
                            "narrative_hash": "group-c",
                        }
                    ]
                ),
            }
        )

        self.assertEqual(evidence["rows_by_partition"], {"train": 2, "validation": 1})
        self.assertEqual(evidence["cross_partition_groups"], 0)

    def test_rejects_column_outside_contract(self) -> None:
        invalid = frame(
            [
                {
                    "complaint_what_happened": "synthetic text",
                    "product_canonical": "Credit card",
                    "narrative_hash": "group-a",
                    "unexpected_column": "not allowed",
                }
            ]
        )

        with self.assertRaisesRegex(DataQualityGateError, "outside"):
            validate({"train": invalid})

    def test_rejects_non_canonical_label(self) -> None:
        invalid = frame(
            [
                {
                    "complaint_what_happened": "synthetic text",
                    "product_canonical": "Other",
                    "narrative_hash": "group-a",
                }
            ]
        )

        with self.assertRaisesRegex(DataQualityGateError, "canonical"):
            validate({"train": invalid})

    def test_rejects_critical_null(self) -> None:
        invalid = frame(
            [
                {
                    "complaint_what_happened": None,
                    "product_canonical": "Credit card",
                    "narrative_hash": "group-a",
                }
            ]
        )

        with self.assertRaisesRegex(DataQualityGateError, "null"):
            validate({"train": invalid})

    def test_rejects_conflicting_duplicate_target(self) -> None:
        invalid = frame(
            [
                {
                    "complaint_what_happened": "synthetic text one",
                    "product_canonical": "Credit card",
                    "narrative_hash": "group-a",
                },
                {
                    "complaint_what_happened": "synthetic text two",
                    "product_canonical": "Mortgage",
                    "narrative_hash": "group-a",
                },
            ]
        )

        with self.assertRaisesRegex(DataQualityGateError, "conflicting"):
            validate({"train": invalid})

    def test_rejects_group_leakage_between_partitions(self) -> None:
        train = frame(
            [
                {
                    "complaint_what_happened": "synthetic train text",
                    "product_canonical": "Credit card",
                    "narrative_hash": "group-a",
                }
            ]
        )
        validation = frame(
            [
                {
                    "complaint_what_happened": "synthetic validation text",
                    "product_canonical": "Credit card",
                    "narrative_hash": "group-a",
                }
            ]
        )

        with self.assertRaisesRegex(DataQualityGateError, "cross"):
            validate({"train": train, "validation": validation})


if __name__ == "__main__":
    unittest.main()
