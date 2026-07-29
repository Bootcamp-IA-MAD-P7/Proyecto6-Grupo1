"""Prepare only the approved input boundary for fast linear model selection."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import polars as pl
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ml.tuning import tune_logistic_regression_cv
from src.ml.vectorizer import VectorizerConfig

DEFAULT_TRAIN_INPUT = ROOT / "data" / "processed" / "cfpb_baseline_en" / "train.parquet"
DEFAULT_POLICY_PATH = ROOT / "config" / "cfpb_fast_linear_selection_policy.json"
DEFAULT_APPROVAL_PATH = ROOT / "reports" / "validation" / "cfpb_fast_linear_phase_a_approval.md"
DEFAULT_SEARCH_OUTPUT = ROOT / "reports" / "validation" / "cfpb_fast_linear_search.json"
SEARCH_SCHEMA_PATH = ROOT / "reports" / "validation" / "cfpb_fast_linear_search.schema.json"
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
    if phase_a.get("n_splits") != 3 or phase_a.get("max_trials") != 10:
        raise ModelSelectionInputError("Fast PG-11 search must use three folds and 10 trials.")
    if phase_a.get("maximum_training_rows", 0) > 20_000:
        raise ModelSelectionInputError("Fast PG-11 search may use at most 20,000 rows.")
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


def apply_grouped_search_limit(frame: pl.DataFrame, phase_policy: dict) -> pl.DataFrame:
    """Select complete, deterministically ordered groups up to the phase-A limit."""
    maximum_rows = phase_policy["maximum_training_rows"]
    if maximum_rows <= 0:
        raise ModelSelectionInputError("Search maximum_training_rows must be positive.")
    if frame.height <= maximum_rows:
        return frame

    class_rows = {
        row["product_canonical"]: row["rows"]
        for row in frame.group_by("product_canonical").len(name="rows").iter_rows(named=True)
    }
    total_rows = sum(class_rows.values())
    quotas = {
        label: max(1, int(maximum_rows * rows / total_rows))
        for label, rows in class_rows.items()
    }
    remaining = maximum_rows - sum(quotas.values())
    for label in sorted(class_rows, key=lambda item: (-class_rows[item], item)):
        if remaining <= 0:
            break
        quotas[label] += 1
        remaining -= 1

    groups = (
        frame.group_by("product_canonical", "narrative_hash")
        .len(name="group_rows")
        .with_columns(
            pl.col("narrative_hash")
            .hash(seed=phase_policy["sampling_seed"])
            .alias("sort_key")
        )
        .sort(["product_canonical", "sort_key"])
    )
    selected_groups: list[str] = []
    selected_rows = {label: 0 for label in class_rows}
    for group in groups.iter_rows(named=True):
        label = group["product_canonical"]
        if selected_rows[label] + group["group_rows"] <= quotas[label]:
            selected_groups.append(group["narrative_hash"])
            selected_rows[label] += group["group_rows"]
    if not selected_groups:
        raise ModelSelectionInputError("Grouped search sampling did not select any eligible rows.")
    return frame.filter(pl.col("narrative_hash").is_in(selected_groups))


def fingerprint_groups(frame: pl.DataFrame) -> str:
    """Return a non-reversible aggregate fingerprint of selected groups."""
    digest = hashlib.sha256()
    digest.update(str(frame.height).encode("utf-8"))
    for (group,) in frame.select("narrative_hash").unique().sort("narrative_hash").iter_rows():
        digest.update(group.encode("utf-8"))
    return digest.hexdigest()


def validate_controlled_output_path(output_path: Path) -> Path:
    """Keep generated evidence under the versioned validation-report root."""
    controlled_root = (ROOT / "reports" / "validation").resolve()
    resolved = output_path.resolve()
    if not resolved.is_relative_to(controlled_root):
        raise ModelSelectionInputError("Search evidence output must stay under reports/validation.")
    return resolved


def validate_search_evidence(evidence: dict) -> None:
    """Validate aggregate-only phase-A output before it is persisted."""
    schema = json.loads(SEARCH_SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(evidence))
    if errors:
        raise ModelSelectionInputError("Search evidence does not satisfy its aggregate schema.")


def execute_search(frame: pl.DataFrame, policy: dict, output_path: Path) -> dict:
    """Run only approved phase-A tuning and persist its aggregated evidence."""
    phase_policy = phase_settings(policy, "search")
    sample = apply_grouped_search_limit(frame, phase_policy)
    started_at = time.monotonic()
    vectorizer = VectorizerConfig({"max_features": 8000, "ngram_range": [1, 2]})
    matrix = vectorizer.fit_transform(sample["complaint_what_happened"].to_list())
    result = tune_logistic_regression_cv(
        matrix,
        sample["product_canonical"].to_list(),
        sample["narrative_hash"].to_list(),
        n_splits=phase_policy["n_splits"],
        n_trials=phase_policy["max_trials"],
        random_state=policy["grouping"]["random_state"],
    )
    evidence = {
        "schema_version": "1.0",
        "execution_phase": "search",
        "candidate_family": "LogisticRegression",
        "train_partition_fingerprint": fingerprint_groups(sample),
        "group_column": "narrative_hash",
        "random_state": policy["grouping"]["random_state"],
        "sample": {
            "grouped": True,
            "maximum_rows": phase_policy["maximum_training_rows"],
            "rows_used": sample.height,
            "sampling_seed": phase_policy["sampling_seed"],
        },
        "cross_validation": {
            "strategy": policy["grouping"]["strategy"],
            "n_splits": phase_policy["n_splits"],
            "shuffle": policy["grouping"]["shuffle"],
            "random_state": policy["grouping"]["random_state"],
        },
        "optimization": {
            "primary_metric": phase_policy["primary_metric"],
            "max_trials": phase_policy["max_trials"],
            "trials_completed": result["n_trials"],
            "sampler_seed": phase_policy["sampler_seed"],
        },
        "metrics": {
            "macro_f1_mean": result["macro_f1_mean"],
            "macro_f1_std": result["macro_f1_std"],
        },
        "frozen_parameters": result["best_params"],
        "execution_cost": {"elapsed_seconds": time.monotonic() - started_at},
        "class_limitations": result["class_limitations"],
        "decision_boundary": {
            "validation_used_for_selection": False,
            "test_used_for_selection": False,
            "champion_declared": False,
            "contains_prohibited_content": False,
        },
    }
    validate_search_evidence(evidence)
    output_path = validate_controlled_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the approved train boundary for fast linear PG-11 selection."
    )
    parser.add_argument("--train-input", type=Path, default=DEFAULT_TRAIN_INPUT)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    parser.add_argument("--approval", type=Path, default=DEFAULT_APPROVAL_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_SEARCH_OUTPUT)
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
        help="Run only the approved phase-A search; omitted prevents training.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = load_selection_training_partition(args.train_input)
    policy = load_selection_policy(args.policy)
    phase_settings(policy, args.phase)
    print(f"PG-11 input accepted: {frame.height:,} training rows with grouped leakage control.")
    print(f"Fast linear phase prepared: {args.phase}.")
    if not args.execute:
        print("No evaluation executed. Use --execute only after human approval.")
        return
    if args.phase != "search":
        raise ModelSelectionInputError("Fast linear full CV is not implemented by the phase-A task.")
    if not args.approval.is_file():
        raise ModelSelectionInputError("Fast linear phase A requires its versioned approval file.")
    evidence = execute_search(frame, policy, args.output)
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    main()
