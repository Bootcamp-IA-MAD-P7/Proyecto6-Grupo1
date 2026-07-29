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
DELIVERY_PROFILE = "delivery"
PILOT_PROFILE = "pilot"


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


def resolve_execution_profile(policy: dict, profile_name: str) -> dict:
    """Return a governed profile and reject weakened delivery budgets."""
    if profile_name == PILOT_PROFILE:
        pilot = policy["pilot"]
        return {
            "name": PILOT_PROFILE,
            "n_splits": pilot["n_splits"],
            "n_trials": pilot["max_trials_per_candidate"],
            "may_verify_delivery_criteria": False,
        }

    if profile_name != DELIVERY_PROFILE:
        raise ModelSelectionInputError("PG-11 execution profile must be pilot or delivery.")

    cross_validation = policy["cross_validation"]
    optimization = policy["optimization"]
    if cross_validation != {
        "strategy": "StratifiedGroupKFold",
        "group_column": "narrative_hash",
        "n_splits": 5,
        "shuffle": True,
        "random_state": 42,
        "temporal_holdout_boundary_preserved": True,
    }:
        raise ModelSelectionInputError(
            "PG-11 delivery requires the versioned five-fold grouped strategy."
        )
    if optimization["max_trials_per_candidate"] < 30:
        raise ModelSelectionInputError(
            "PG-11 delivery cannot use a reduced tuning budget as MED evidence."
        )

    return {
        "name": DELIVERY_PROFILE,
        "n_splits": cross_validation["n_splits"],
        "n_trials": optimization["max_trials_per_candidate"],
        "may_verify_delivery_criteria": True,
    }


def apply_pilot_limit(frame: pl.DataFrame, pilot_policy: dict) -> pl.DataFrame:
    """Return the approved deterministic feasibility sample."""
    maximum_rows = pilot_policy["maximum_training_rows"]
    if maximum_rows <= 0:
        raise ModelSelectionInputError("Pilot maximum_training_rows must be positive.")
    return frame.sample(
        n=min(frame.height, maximum_rows),
        seed=pilot_policy["sampling_seed"],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the approved training partition for PG-11 model selection."
    )
    parser.add_argument("--train-input", type=Path, default=DEFAULT_TRAIN_INPUT)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--candidate", choices=("rf", "xgb", "lgbm"), default="xgb")
    parser.add_argument(
        "--profile",
        choices=(PILOT_PROFILE, DELIVERY_PROFILE),
        default=PILOT_PROFILE,
        help="Use the feasibility pilot or the governed delivery profile.",
    )
    parser.add_argument(
        "--pilot",
        action="store_true",
        help="Deprecated alias for --profile pilot.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run the approved CV search; omitted by default to prevent accidental training.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.pilot and args.profile != PILOT_PROFILE:
        raise ModelSelectionInputError("--pilot cannot be combined with --profile delivery.")
    frame = load_selection_training_partition(args.train_input)
    policy = load_selection_policy(args.policy)
    profile = resolve_execution_profile(policy, args.profile)
    print(f"PG-11 input accepted: {frame.height:,} training rows with grouped leakage control.")
    if profile["name"] == PILOT_PROFILE:
        frame = apply_pilot_limit(frame, policy["pilot"])
        print(f"Pilot limited to {frame.height:,} deterministic training rows.")
    if not args.execute:
        print("No evaluation executed. Use --execute only after human approval.")
        return
    if profile["name"] == DELIVERY_PROFILE:
        raise ModelSelectionInputError(
            "Full PG-11 delivery requires the recorded human approval from task 3.1."
        )

    vectorizer = VectorizerConfig({"max_features": 8000, "ngram_range": [1, 2]})
    matrix = vectorizer.fit_transform(frame["complaint_what_happened"].to_list())
    result = tune_hyperparams_cv(
        args.candidate,
        matrix,
        frame["product_canonical"].to_list(),
        frame["narrative_hash"].to_list(),
        n_splits=profile["n_splits"],
        n_trials=profile["n_trials"],
        random_state=policy["cross_validation"]["random_state"],
    )
    result["execution_scope"] = profile["name"]
    result["may_verify_delivery_criteria"] = profile["may_verify_delivery_criteria"]
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
