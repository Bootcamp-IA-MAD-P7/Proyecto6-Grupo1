"""Synthetic tests for language filtering and temporal group-isolated splits."""

from __future__ import annotations

from datetime import date
import unittest

import polars as pl

from scripts.data.cfpb_training_preparation import (
    TrainingPreparationError,
    apply_english_policy,
    assign_temporal_group_splits,
    detect_language,
    validate_temporal_group_split,
)


def synthetic_frame() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "date_received": [
                date(2024, 1, 1),
                date(2024, 1, 2),
                date(2024, 1, 3),
                date(2024, 1, 4),
                date(2024, 1, 5),
                date(2024, 1, 6),
            ],
            "complaint_what_happened": [
                "This synthetic complaint is written in English.",
                "This synthetic complaint is written in English.",
                "This is another English synthetic statement.",
                "Esta reclamación sintética está escrita en español.",
                "Synthetic English text for another class.",
                "Synthetic English text for another class.",
            ],
            "product_canonical": [
                "Credit card",
                "Credit card",
                "Mortgage",
                "Mortgage",
                "Credit card",
                "Credit card",
            ],
            "narrative_hash": ["a", "a", "b", "c", "d", "d"],
        }
    )


class CFPBTrainingPreparationTests(unittest.TestCase):
    def test_language_detection_is_deterministic_for_synthetic_english(self) -> None:
        text = "This synthetic complaint describes a billing problem in English."
        self.assertEqual(detect_language(text), "en")
        self.assertEqual(detect_language(text), "en")

    def test_english_policy_excludes_non_english_without_returning_text(self) -> None:
        english, summary = apply_english_policy(synthetic_frame())
        self.assertEqual(summary["input_rows"], 6)
        self.assertEqual(summary["english_rows"], 5)
        self.assertEqual(summary["excluded_non_english_or_unclassified"], 1)
        self.assertNotIn("language", english.columns)

    def test_temporal_split_keeps_duplicate_group_together(self) -> None:
        frame = synthetic_frame().filter(pl.col("narrative_hash") != "c")
        split = assign_temporal_group_splits(
            frame,
            {"train": 0.7, "validation": 0.15, "test": 0.15},
        )
        grouped = split.group_by("narrative_hash").agg(pl.col("split").n_unique().alias("n"))
        self.assertEqual(grouped.filter(pl.col("n") > 1).height, 0)

    def test_split_validation_rejects_cross_partition_group(self) -> None:
        frame = synthetic_frame().with_columns(
            pl.Series("split", ["train", "validation", "validation", "test", "test", "test"])
        )
        with self.assertRaisesRegex(TrainingPreparationError, "cross"):
            validate_temporal_group_split(frame, min_class_support=1)

    def test_split_validation_requires_explicit_positive_support(self) -> None:
        frame = synthetic_frame().with_columns(pl.lit("train").alias("split"))
        with self.assertRaisesRegex(TrainingPreparationError, "at least one"):
            validate_temporal_group_split(frame, min_class_support=0)

    def test_temporal_split_is_reproducible_and_valid(self) -> None:
        frame = pl.DataFrame(
            {
                "date_received": [date(2024, 1, day) for day in range(1, 11)],
                "complaint_what_happened": [f"synthetic English {day}" for day in range(1, 11)],
                "product_canonical": ["Credit card"] * 10,
                "narrative_hash": [f"group-{day}" for day in range(1, 11)],
            }
        )
        proportions = {"train": 0.7, "validation": 0.15, "test": 0.15}
        first = assign_temporal_group_splits(frame, proportions)
        second = assign_temporal_group_splits(frame, proportions)
        self.assertEqual(first.to_dicts(), second.to_dicts())
        evidence = validate_temporal_group_split(
            first,
            min_class_support=1,
            expected_classes={"Credit card"},
        )
        self.assertEqual(evidence["rows_by_split"], {"train": 7, "validation": 1, "test": 2})


if __name__ == "__main__":
    unittest.main()
