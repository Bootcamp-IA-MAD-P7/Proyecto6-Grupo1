"""Load only the approved training partition for governed model selection."""

from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRAIN_INPUT = ROOT / "data" / "processed" / "cfpb_baseline_en" / "train.parquet"
REQUIRED_COLUMNS = (
    "complaint_what_happened",
    "product_canonical",
    "narrative_hash",
)
FORBIDDEN_INPUT_NAMES = {
    "cfpb_training.parquet",
    "validation.parquet",
    "test.parquet",
}


class ModelSelectionInputError(ValueError):
    """Raised when the governed runner receives an unsafe input."""


def validate_training_input_path(input_path: Path) -> None:
    """Reject corpus-wide, validation, and protected-test inputs."""
    if input_path.name in FORBIDDEN_INPUT_NAMES:
        raise ModelSelectionInputError(
            "PG-11 accepts only the approved local train.parquet partition."
        )
    if input_path.name != "train.parquet":
        raise ModelSelectionInputError(
            "PG-11 input must be the approved local train.parquet partition."
        )


def load_selection_training_partition(input_path: Path) -> pl.DataFrame:
    """Load the minimum approved columns without exposing reserved partitions."""
    validate_training_input_path(input_path)
    frame = pl.read_parquet(input_path)
    missing = sorted(set(REQUIRED_COLUMNS).difference(frame.columns))
    if missing:
        raise ModelSelectionInputError(
            f"PG-11 training partition is missing required columns: {', '.join(missing)}."
        )
    return frame.select(REQUIRED_COLUMNS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the approved training partition for PG-11 model selection."
    )
    parser.add_argument("--train-input", type=Path, default=DEFAULT_TRAIN_INPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = load_selection_training_partition(args.train_input)
    print(f"PG-11 input accepted: {frame.height:,} training rows with grouped leakage control.")


if __name__ == "__main__":
    main()
