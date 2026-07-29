"""Prepare only the approved input boundary for fast linear model selection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_TRAIN_INPUT = ROOT / "data" / "processed" / "cfpb_baseline_en" / "train.parquet"
DEFAULT_POLICY_PATH = ROOT / "config" / "cfpb_fast_linear_selection_policy.json"
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
    """Load and validate the versioned fast-linear selection boundary."""
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    candidate = policy.get("candidate", {})
    data_scope = policy.get("data_scope", {})
    grouping = policy.get("grouping", {})
    phase_a = policy.get("phase_a_tuning", {})
    phase_b = policy.get("phase_b_full_cv", {})
    selection = policy.get("selection", {})

    if candidate.get("family") != "LogisticRegression":
        raise ModelSelectionInputError("Fast PG-11 accepts only LogisticRegression.")
    if data_scope.get("eligible_partition") != "train" or (
        data_scope.get("validation_allowed_for_selection") is not False
        or data_scope.get("protected_test_allowed_for_selection") is not False
    ):
        raise ModelSelectionInputError("PG-11 policy must keep validation and test reserved.")
    if grouping != {
        "strategy": "StratifiedGroupKFold",
        "group_column": "narrative_hash",
        "shuffle": True,
        "random_state": 42,
        "temporal_holdout_boundary_preserved": True,
    }:
        raise ModelSelectionInputError("Fast PG-11 policy must preserve grouped folds and seed 42.")
    if phase_a.get("n_splits") != 3 or phase_a.get("max_trials") != 30:
        raise ModelSelectionInputError("Fast PG-11 search must use three folds and 30 trials.")
    if phase_a.get("maximum_training_rows", 0) > 50_000:
        raise ModelSelectionInputError("Fast PG-11 search may use at most 50,000 rows.")
    if (
        phase_b.get("input_scope") != "full_train"
        or phase_b.get("n_splits") != 5
        or phase_b.get("parameters_source") != "phase_a_frozen"
        or phase_b.get("retuning_allowed") is not False
    ):
        raise ModelSelectionInputError("Fast PG-11 full CV must use frozen phase-A parameters.")
    if selection.get("champion_declared_automatically") is not False:
        raise ModelSelectionInputError("Fast PG-11 must not declare a Champion automatically.")
    return policy


def phase_settings(policy: dict, phase: str) -> dict:
    """Expose phase settings without loading reserved partitions or training."""
    if phase == "search":
        return policy["phase_a_tuning"]
    if phase == "full_cv":
        return policy["phase_b_full_cv"]
    raise ModelSelectionInputError("Fast PG-11 phase must be search or full_cv.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the approved train boundary for fast linear PG-11 selection."
    )
    parser.add_argument("--train-input", type=Path, default=DEFAULT_TRAIN_INPUT)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument(
        "--candidate",
        choices=("LogisticRegression",),
        default="LogisticRegression",
    )
    parser.add_argument(
        "--phase",
        choices=("search", "full_cv"),
        default="search",
        help="Prepare phase A search or phase B full cross-validation.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Reserved for a later approved execution task; omitted prevents training.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = load_selection_training_partition(args.train_input)
    policy = load_selection_policy(args.policy)
    settings = phase_settings(policy, args.phase)
    print(f"PG-11 input accepted: {frame.height:,} training rows with grouped leakage control.")
    print(f"Fast linear phase prepared: {args.phase}.")
    if not args.execute:
        print("No evaluation executed. Use --execute only after human approval.")
        return
    del settings
    raise ModelSelectionInputError(
        "Fast linear execution is not implemented by the input-boundary task."
    )


if __name__ == "__main__":
    main()
