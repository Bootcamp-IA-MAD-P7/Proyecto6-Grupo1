"""Load only the approved training partition for governed model selection."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import polars as pl
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ml.tuning import tune_hyperparams_cv
from src.ml.vectorizer import VectorizerConfig

DEFAULT_TRAIN_INPUT = ROOT / "data" / "processed" / "cfpb_baseline_en" / "train.parquet"
DEFAULT_POLICY_PATH = ROOT / "config" / "cfpb_model_selection_policy.json"
DEFAULT_DELIVERY_APPROVAL_PATH = ROOT / "reports" / "validation" / "cfpb_model_selection_delivery_approval.md"
DEFAULT_DELIVERY_SCHEMA_PATH = ROOT / "reports" / "validation" / "cfpb_model_selection_delivery.schema.json"
DEFAULT_DELIVERY_OUTPUT_PATH = ROOT / "reports" / "validation" / "cfpb_model_selection_delivery_xgb.json"
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


def validate_delivery_approval(approval_path: Path, candidate: str) -> None:
    """Require the reviewed PG-11 approval stored at its controlled location."""
    if approval_path.resolve() != DEFAULT_DELIVERY_APPROVAL_PATH.resolve():
        raise ModelSelectionInputError("PG-11 delivery approval must use the versioned path.")
    if candidate != "xgb" or not approval_path.is_file():
        raise ModelSelectionInputError("PG-11 delivery is approved only for XGBoost.")
    approval = approval_path.read_text(encoding="utf-8")
    required_markers = (
        "Approved environment: Colab",
        "Candidate: `xgb`",
        "five folds",
        "up to 30 trials",
        "Time limit: none",
    )
    if not all(marker in approval for marker in required_markers):
        raise ModelSelectionInputError("PG-11 delivery approval is incomplete.")


def validate_delivery_output_path(output_path: Path) -> None:
    """Keep aggregate delivery evidence inside the versioned validation root."""
    output_root = ROOT / "reports" / "validation"
    if output_path.resolve().parent != output_root.resolve() or output_path.suffix != ".json":
        raise ModelSelectionInputError("PG-11 delivery output must be a JSON file in reports/validation.")


def _file_fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _package_versions() -> dict[str, str]:
    packages = ("polars", "scikit-learn", "xgboost", "optuna")
    versions = {"python": sys.version.split()[0]}
    for package in packages:
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "not-installed"
    return versions


def build_delivery_evidence(
    *, policy: dict, candidate: str, result: dict, train_input: Path
) -> dict:
    """Build aggregate-only delivery evidence from governed CV output."""
    trials = [
        {
            "parameters": trial["params"],
            "fold_metrics": trial["fold_metrics"],
            "train_macro_f1_mean": trial["train_macro_f1_mean"],
            "train_macro_f1_std": trial["train_macro_f1_std"],
            "validation_macro_f1_mean": trial["validation_macro_f1_mean"],
            "validation_macro_f1_std": trial["validation_macro_f1_std"],
            "execution_cost_seconds": trial["execution_cost_seconds"],
            "class_limitations": trial["class_limitations"],
        }
        for trial in result["trials"]
    ]
    return {
        "schema_version": "1.0",
        "policy_version": policy["policy_version"],
        "execution_manifest": {
            "execution_scope": DELIVERY_PROFILE,
            "partition_fingerprint": _file_fingerprint(train_input),
            "package_versions": _package_versions(),
            "random_state": policy["cross_validation"]["random_state"],
        },
        "candidate": {"name": candidate, "parameters": result["best_params"]},
        "cross_validation": {
            "strategy": policy["cross_validation"]["strategy"],
            "group_column": policy["cross_validation"]["group_column"],
            "n_splits": result["n_splits"],
            "random_state": result["random_state"],
        },
        "optimization": {
            "primary_metric": policy["optimization"]["primary_metric"],
            "max_trials": result["n_trials"],
            "sampler_seed": policy["optimization"]["sampler_seed"],
        },
        "trials": trials,
        "per_class_metrics": result["per_class_metrics"],
        "train_validation_macro_f1_gap": abs(
            result["train_macro_f1_mean"] - result["macro_f1_mean"]
        ),
        "confirmation_boundary": {
            "reserved_partition": policy["data_scope"]["reserved_confirmation_partition"],
            "used_for_selection": False,
            "used_for_retuning": False,
            "protected_test_used": False,
            "champion_declared": False,
        },
    }


def validate_and_write_delivery_evidence(evidence: dict, output_path: Path) -> None:
    """Validate aggregate evidence before writing it to the controlled location."""
    schema = json.loads(DEFAULT_DELIVERY_SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(evidence), key=str)
    if errors:
        raise ModelSelectionInputError("PG-11 delivery evidence failed its versioned schema.")
    output_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the approved training partition for PG-11 model selection."
    )
    parser.add_argument("--train-input", type=Path, default=DEFAULT_TRAIN_INPUT)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--candidate", choices=("rf", "xgb", "lgbm"), default="xgb")
    parser.add_argument(
        "--delivery-approval", type=Path, default=DEFAULT_DELIVERY_APPROVAL_PATH
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_DELIVERY_OUTPUT_PATH)
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
    if profile["name"] == DELIVERY_PROFILE:
        validate_delivery_approval(args.delivery_approval, args.candidate)
        validate_delivery_output_path(args.output)
    print(f"PG-11 input accepted: {frame.height:,} training rows with grouped leakage control.")
    if profile["name"] == PILOT_PROFILE:
        frame = apply_pilot_limit(frame, policy["pilot"])
        print(f"Pilot limited to {frame.height:,} deterministic training rows.")
    if not args.execute:
        print("No evaluation executed. Use --execute only after human approval.")
        return
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
    if profile["name"] == DELIVERY_PROFILE:
        evidence = build_delivery_evidence(
            policy=policy,
            candidate=args.candidate,
            result=result,
            train_input=args.train_input,
        )
        validate_and_write_delivery_evidence(evidence, args.output)
        print(f"PG-11 delivery evidence written: {args.output}")
        return
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
