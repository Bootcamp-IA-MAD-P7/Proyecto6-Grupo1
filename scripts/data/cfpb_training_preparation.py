"""Prepare local CFPB rows for an English, group-isolated temporal baseline."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from concurrent.futures import ProcessPoolExecutor
import json
import os
from pathlib import Path
from typing import Any

import polars as pl
from langdetect import DetectorFactory, LangDetectException, detect

from scripts.data.cfpb_training_policy import (
    DEFAULT_POLICY_PATH,
    load_policy,
    validate_reference_inputs,
)


DetectorFactory.seed = 0

SPLIT_NAMES = ("train", "validation", "test")
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_PATH = ROOT / "data" / "processed" / "cfpb_training.parquet"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed" / "cfpb_baseline_en"
DEFAULT_MANIFEST_PATH = ROOT / "reports" / "validation" / "cfpb_training_preparation_manifest.json"
DEFAULT_CONTRACT_PATH = ROOT / "config" / "cfpb_target_contract.json"


class TrainingPreparationError(RuntimeError):
    """Raised when a local preparation step violates the approved policy."""


def detect_language(text: str | None, max_characters: int = 500) -> str | None:
    """Return a deterministic ISO language code without retaining the text."""

    if not text or not text.strip():
        return None
    try:
        return detect(text[:max_characters])
    except LangDetectException:
        return None


def apply_english_policy(
    frame: pl.DataFrame,
    language_codes: list[str | None] | None = None,
) -> tuple[pl.DataFrame, dict[str, Any]]:
    """Keep English rows and return aggregate-only language counts."""

    required = {"complaint_what_happened", "product_canonical", "narrative_hash"}
    missing = required.difference(frame.columns)
    if missing:
        raise TrainingPreparationError("Local corpus does not contain policy columns.")

    languages = language_codes or [
        detect_language(value) for value in frame["complaint_what_happened"].to_list()
    ]
    if len(languages) != frame.height:
        raise TrainingPreparationError("Language output does not match local corpus rows.")
    labelled = frame.with_columns(pl.Series("language", languages))
    english = labelled.filter(pl.col("language") == "en").drop("language")
    by_class = labelled.group_by("product_canonical").agg(
        pl.len().alias("input_rows"),
        (pl.col("language") == "en").sum().alias("english_rows"),
    )
    summary = {
        "input_rows": frame.height,
        "english_rows": english.height,
        "excluded_non_english_or_unclassified": frame.height - english.height,
        "by_class": {
            row["product_canonical"]: {
                "input_rows": int(row["input_rows"]),
                "english_rows": int(row["english_rows"]),
            }
            for row in by_class.to_dicts()
        },
    }
    return english, summary


def _split_boundaries(total_rows: int, proportions: Mapping[str, float]) -> tuple[int, int]:
    if total_rows <= 0:
        raise TrainingPreparationError("Cannot split an empty local corpus.")
    if set(proportions) != set(SPLIT_NAMES) or abs(sum(proportions.values()) - 1.0) > 1e-9:
        raise TrainingPreparationError("Split proportions must define train, validation and test.")
    return (
        round(total_rows * proportions["train"]),
        round(total_rows * (proportions["train"] + proportions["validation"])),
    )


def assign_temporal_group_splits(
    frame: pl.DataFrame,
    proportions: Mapping[str, float],
) -> pl.DataFrame:
    """Assign full narrative-hash groups to chronological train/validation/test splits."""

    required = {"date_received", "product_canonical", "narrative_hash"}
    if missing := required.difference(frame.columns):
        raise TrainingPreparationError("Local corpus does not contain split-policy columns.")
    if frame["date_received"].null_count():
        raise TrainingPreparationError("Local corpus has missing dates for temporal splitting.")

    train_limit, validation_limit = _split_boundaries(frame.height, proportions)
    groups = (
        frame.group_by("narrative_hash")
        .agg(
            pl.col("date_received").max().alias("group_max_date"),
            pl.len().alias("group_rows"),
        )
        .sort(["group_max_date", "narrative_hash"])
        .with_columns(pl.col("group_rows").cum_sum().alias("cumulative_rows"))
        .with_columns(
            pl.when(pl.col("cumulative_rows") <= train_limit)
            .then(pl.lit("train"))
            .when(pl.col("cumulative_rows") <= validation_limit)
            .then(pl.lit("validation"))
            .otherwise(pl.lit("test"))
            .alias("split")
        )
        .select("narrative_hash", "split")
    )
    return frame.join(groups, on="narrative_hash", how="inner")


def validate_temporal_group_split(
    frame: pl.DataFrame,
    *,
    min_class_support: int,
    expected_classes: set[str] | None = None,
) -> dict[str, object]:
    """Return safe aggregate split evidence or fail on leakage, time or class support."""

    if min_class_support < 1:
        raise TrainingPreparationError("Minimum class support must be at least one row.")
    required = {"date_received", "product_canonical", "narrative_hash", "split"}
    if missing := required.difference(frame.columns):
        raise TrainingPreparationError("Local split does not contain required policy columns.")

    group_splits = frame.group_by("narrative_hash").agg(pl.col("split").n_unique().alias("n"))
    if group_splits.filter(pl.col("n") > 1).height:
        raise TrainingPreparationError("Narrative groups cross local partitions.")

    group_dates = frame.group_by(["split", "narrative_hash"]).agg(
        pl.col("date_received").max().alias("group_max_date")
    )
    date_bounds = (
        group_dates.group_by("split")
        .agg(
            pl.col("group_max_date").min().alias("min_date"),
            pl.col("group_max_date").max().alias("max_date"),
        )
        .sort("min_date")
    )
    ordered = date_bounds["split"].to_list()
    if ordered != [name for name in SPLIT_NAMES if name in ordered]:
        raise TrainingPreparationError("Local partitions are not in chronological order.")

    rows_by_split = frame.group_by("split").len().rename({"len": "rows"})
    bounds = date_bounds.join(rows_by_split, on="split", how="left").sort("min_date")

    support = (
        frame.group_by(["split", "product_canonical"])
        .len()
        .rename({"len": "rows"})
    )
    required_classes = expected_classes or set(frame["product_canonical"].unique().to_list())
    observed = {
        (row["split"], row["product_canonical"]): int(row["rows"])
        for row in support.to_dicts()
    }
    insufficient = [
        (split, label)
        for split in SPLIT_NAMES
        for label in required_classes
        if observed.get((split, label), 0) < min_class_support
    ]
    if insufficient:
        raise TrainingPreparationError("A class does not meet the approved local split support.")

    return {
        "rows_by_split": dict(zip(bounds["split"].to_list(), bounds["rows"].to_list(), strict=True)),
        "date_bounds": {
            row["split"]: {"min": str(row["min_date"]), "max": str(row["max_date"])}
            for row in bounds.to_dicts()
        },
        "class_support": {
            row["split"]: {
                label: count
                for label, count in zip(
                    support.filter(pl.col("split") == row["split"])["product_canonical"].to_list(),
                    support.filter(pl.col("split") == row["split"])["rows"].to_list(),
                    strict=True,
                )
            }
            for row in bounds.to_dicts()
        },
    }


def detect_languages_parallel(texts: list[str], workers: int) -> list[str | None]:
    """Detect language locally in parallel without persisting narratives or detector logs."""

    if workers < 1:
        raise TrainingPreparationError("Language workers must be at least one.")
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(detect_language, texts, chunksize=500))


def prepare_local_baseline_corpus(
    *,
    input_path: Path,
    output_dir: Path,
    manifest_path: Path,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    policy_path: Path = DEFAULT_POLICY_PATH,
    workers: int = 1,
) -> dict[str, Any]:
    """Create local English train/validation/test files and a safe aggregate manifest."""

    policy = validate_reference_inputs(
        source_path=ROOT / "data" / "raw" / "complaints.csv.zip",
        contract_path=contract_path,
        policy_path=policy_path,
    )
    if not input_path.is_file():
        raise TrainingPreparationError("Approved local training corpus is unavailable.")
    frame = pl.read_parquet(input_path)
    language_codes = detect_languages_parallel(
        frame["complaint_what_happened"].to_list(), workers
    )
    english, language_summary = apply_english_policy(frame, language_codes)
    split_policy = policy["split"]
    split = assign_temporal_group_splits(english, split_policy["target_proportions"])
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    split_summary = validate_temporal_group_split(
        split,
        min_class_support=split_policy["min_class_support_per_split"],
        expected_classes=set(contract["target"]["canonical_labels"]),
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    for split_name in SPLIT_NAMES:
        split.filter(pl.col("split") == split_name).drop("split").write_parquet(
            output_dir / f"{split_name}.parquet"
        )
    manifest = {
        "schema_version": "1.0",
        "policy": {
            "path": "config/cfpb_training_policy.json",
            "source_sha256": policy["reference"]["source_sha256"],
            "contract_sha256": policy["reference"]["contract_sha256"],
            "language": policy["language"],
            "split": split_policy,
        },
        "language": language_summary,
        "split": split_summary,
        "output": {
            "contains_narratives": True,
            "tracked_by_git": False,
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare local CFPB English temporal baseline partitions."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = prepare_local_baseline_corpus(
        input_path=args.input,
        output_dir=args.output_dir,
        manifest_path=args.manifest,
        contract_path=args.contract,
        policy_path=args.policy,
        workers=args.workers,
    )
    print(
        "Prepared local CFPB baseline partitions: "
        f"{manifest['language']['english_rows']:,} English rows."
    )


if __name__ == "__main__":
    main()
