"""Synthetic contract tests for the local CFPB training dataset builder."""

from __future__ import annotations

import csv
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import polars as pl

from scripts.data.convert_cfpb_to_parquet import (
    DatasetBuildError,
    OUTPUT_COLUMNS,
    build_training_dataset,
)


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "config" / "cfpb_target_contract.json"
FIELDNAMES = [
    "Complaint ID",
    "Date received",
    "Consumer complaint narrative",
    "Product",
]


def synthetic_row(
    complaint_id: str,
    received: str,
    narrative: str,
    product: str,
) -> dict[str, str]:
    return {
        "Complaint ID": complaint_id,
        "Date received": received,
        "Consumer complaint narrative": narrative,
        "Product": product,
    }


def write_synthetic_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as source:
        writer = csv.DictWriter(source, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


class CFPBTrainingDatasetTests(unittest.TestCase):
    def build(self, rows: list[dict[str, str]]) -> tuple[dict, pl.DataFrame]:
        self.tempdir = tempfile.TemporaryDirectory()
        root = Path(self.tempdir.name)
        source = root / "synthetic.csv"
        output = root / "training.parquet"
        manifest_path = root / "manifest.json"
        write_synthetic_csv(source, rows)
        manifest = build_training_dataset(
            input_path=source,
            output_path=output,
            manifest_path=manifest_path,
            contract_path=CONTRACT_PATH,
        )
        self.assertEqual(manifest, json.loads(manifest_path.read_text(encoding="utf-8")))
        return manifest, pl.read_parquet(output)

    def tearDown(self) -> None:
        tempdir = getattr(self, "tempdir", None)
        if tempdir is not None:
            tempdir.cleanup()

    def test_filters_maps_aliases_and_keeps_only_authorized_columns(self) -> None:
        manifest, corpus = self.build(
            [
                synthetic_row("syn-001", "2024-01-10", "synthetic alpha", "Credit card"),
                synthetic_row(
                    "syn-002",
                    "2024-01-11",
                    "synthetic beta",
                    "Credit reporting, credit repair services, or other personal consumer reports",
                ),
                synthetic_row("syn-003", "2024-01-12", "synthetic gamma", "Credit card or prepaid card"),
                synthetic_row("syn-004", "2023-01-01", "outside window", "Mortgage"),
                synthetic_row("syn-005", "2024-01-13", "   ", "Mortgage"),
            ]
        )

        self.assertEqual(corpus.columns, OUTPUT_COLUMNS)
        self.assertNotIn("Complaint ID", corpus.columns)
        self.assertNotIn("Product", corpus.columns)
        self.assertEqual(corpus.height, 2)
        self.assertEqual(
            set(corpus["product_canonical"].to_list()),
            {"Credit card", "Credit reporting or other personal consumer reports"},
        )
        self.assertEqual(manifest["rows"]["excluded_ambiguous_labels"], 1)
        self.assertEqual(manifest["rows"]["training_corpus"], 2)

    def test_unknown_source_label_fails_without_exposing_synthetic_narrative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "synthetic.csv"
            write_synthetic_csv(
                source,
                [synthetic_row("syn-unknown", "2024-01-10", "synthetic private text", "Unknown product")],
            )
            with self.assertRaisesRegex(DatasetBuildError, "unknown source labels") as error:
                build_training_dataset(
                    input_path=source,
                    output_path=root / "training.parquet",
                    manifest_path=root / "manifest.json",
                    contract_path=CONTRACT_PATH,
                )
        self.assertNotIn("synthetic private text", str(error.exception))

    def test_excludes_conflicting_groups_and_preserves_non_conflicting_duplicates(self) -> None:
        manifest, corpus = self.build(
            [
                synthetic_row("syn-101", "2024-01-10", "same conflict", "Credit card"),
                synthetic_row("syn-102", "2024-01-11", " same   conflict ", "Mortgage"),
                synthetic_row("syn-103", "2024-01-12", "same accepted", "Student loan"),
                synthetic_row("syn-104", "2024-01-13", "same accepted", "Student loan"),
            ]
        )

        self.assertEqual(corpus.height, 2)
        self.assertEqual(corpus["product_canonical"].unique().to_list(), ["Student loan"])
        self.assertEqual(manifest["groups"]["conflicting_target"], 1)
        self.assertEqual(manifest["rows"]["excluded_conflicting_target_rows"], 2)
        self.assertEqual(manifest["groups"]["duplicate_non_conflicting"], 1)
        self.assertEqual(manifest["groups"]["rows_in_duplicate_non_conflicting_groups"], 2)

    def test_manifest_is_aggregate_and_repeatable(self) -> None:
        rows = [
            synthetic_row("syn-201", "2024-01-10", "synthetic repeatable", "Vehicle loan or lease"),
            synthetic_row("syn-202", "2024-01-11", "synthetic repeatable", "Vehicle loan or lease"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "synthetic.csv"
            output = root / "training.parquet"
            manifest_path = root / "manifest.json"
            write_synthetic_csv(source, rows)
            first = build_training_dataset(
                input_path=source,
                output_path=output,
                manifest_path=manifest_path,
                contract_path=CONTRACT_PATH,
            )
            second = build_training_dataset(
                input_path=source,
                output_path=output,
                manifest_path=manifest_path,
                contract_path=CONTRACT_PATH,
            )

        self.assertEqual(first, second)
        serialized = json.dumps(first)
        self.assertNotIn("synthetic repeatable", serialized)
        self.assertNotIn("syn-201", serialized)
        self.assertTrue(first["output"]["contains_narratives"])
        self.assertFalse(first["output"]["tracked_by_git"])

    def test_missing_source_fails_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(DatasetBuildError, "does not exist"):
                build_training_dataset(
                    input_path=root / "missing.csv",
                    output_path=root / "training.parquet",
                    manifest_path=root / "manifest.json",
                    contract_path=CONTRACT_PATH,
                )

    def test_accepts_a_local_zip_with_one_synthetic_csv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            csv_source = root / "fixture.csv"
            archive = root / "fixture.zip"
            write_synthetic_csv(
                csv_source,
                [synthetic_row("syn-zip", "2024-01-10", "synthetic zip text", "Mortgage")],
            )
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as compressed:
                compressed.write(csv_source, arcname="complaints.csv")

            manifest = build_training_dataset(
                input_path=archive,
                output_path=root / "training.parquet",
                manifest_path=root / "manifest.json",
                contract_path=CONTRACT_PATH,
            )

        self.assertEqual(manifest["rows"]["training_corpus"], 1)


if __name__ == "__main__":
    unittest.main()
