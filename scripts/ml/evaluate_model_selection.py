"""Load only the approved training partition for governed model selection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ml.tuning import tune_hyperparams_cv
from src.ml.vectorizer import VectorizerConfig

DEFAULT_TRAIN_INPUT = ROOT / "data" / "processed" / "cfpb_baseline_en" / "train.parquet"
DEFAULT_POLICY_PATH = ROOT / "config" / "cfpb_model_selection_policy.json"
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


def load_selection_policy(policy_path: Path) -> dict:
    """Load the versioned PG-11 constraints before an explicit execution."""
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    if policy["data_scope"] != {
        "eligible_partition": "train",
        "reserved_confirmation_partition": "validation",
        "protected_partition": "test",
        "protected_test_allowed_for_selection": False,
    }:
        raise ModelSelectionInputError("PG-11 policy must keep validation and test reserved.")
    return policy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the approved training partition for PG-11 model selection."
    )
    parser.add_argument("--train-input", type=Path, default=DEFAULT_TRAIN_INPUT)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--candidate", choices=("rf", "xgb", "lgbm"), default="xgb")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run the approved CV search; omitted by default to prevent accidental training.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = load_selection_training_partition(args.train_input)
    policy = load_selection_policy(args.policy)
    print(f"PG-11 input accepted: {frame.height:,} training rows with grouped leakage control.")
    if not args.execute:
        print("No evaluation executed. Use --execute only after human approval.")
        return

    vectorizer = VectorizerConfig({"max_features": 8000, "ngram_range": [1, 2]})
    matrix = vectorizer.fit_transform(frame["complaint_what_happened"].to_list())
    cv_policy = policy["cross_validation"]
    optimization = policy["optimization"]
    result = tune_hyperparams_cv(
        args.candidate,
        matrix,
        frame["product_canonical"].to_list(),
        frame["narrative_hash"].to_list(),
        n_splits=cv_policy["n_splits"],
        n_trials=optimization["max_trials_per_candidate"],
        random_state=cv_policy["random_state"],
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
