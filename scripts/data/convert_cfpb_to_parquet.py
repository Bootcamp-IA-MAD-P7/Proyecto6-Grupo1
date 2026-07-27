"""Build a local CFPB training dataset without versioning complaint narratives."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
from typing import Any

import polars as pl


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT_PATH = ROOT / "config" / "cfpb_target_contract.json"
DEFAULT_RAW_PATH = ROOT / "data" / "raw" / "complaints.csv.zip"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "cfpb_training.parquet"
DEFAULT_MANIFEST_PATH = ROOT / "reports" / "validation" / "cfpb_training_dataset_manifest.json"

SOURCE_COLUMNS = {
    "complaint_id": "Complaint ID",
    "date_received": "Date received",
    "narrative": "Consumer complaint narrative",
    "product": "Product",
}
REQUIRED_SOURCE_COLUMNS = list(SOURCE_COLUMNS.values())
OUTPUT_COLUMNS = [
    "date_received",
    "complaint_what_happened",
    "product_canonical",
    "narrative_hash",
]


class DatasetBuildError(RuntimeError):
    """Raised when a local CFPB source cannot satisfy the target contract."""


def load_contract(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fingerprint_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint_contract(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path: Path) -> str:
    """Return a stable, non-sensitive path label for manifests and tests."""

    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def resolve_csv_source(input_path: Path) -> Path:
    """Return a local CSV, extracting one CSV member from a local ZIP safely."""

    if input_path.suffix.lower() != ".zip":
        return input_path

    with zipfile.ZipFile(input_path) as archive:
        csv_members = [
            member
            for member in archive.infolist()
            if not member.is_dir() and member.filename.lower().endswith(".csv")
        ]
        if len(csv_members) != 1:
            raise DatasetBuildError(
                "Local CFPB ZIP must contain exactly one CSV source file."
            )
        member = csv_members[0]
        destination = input_path.parent / Path(member.filename).name
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        with archive.open(member) as compressed, temporary.open("wb") as extracted:
            shutil.copyfileobj(compressed, extracted, length=1024 * 1024)
        temporary.replace(destination)
    return destination


def build_mapping(contract: dict[str, Any]) -> dict[str, str]:
    mapping = {
        label: label for label in contract["target"]["canonical_labels"]
    }
    mapping.update(contract["target"]["aliases"])
    return mapping


def normalize_narrative(text: str | None) -> str:
    return " ".join((text or "").lower().split())


def narrative_hash(text: str | None) -> str:
    return hashlib.sha256(normalize_narrative(text).encode("utf-8")).hexdigest()


def hash_batch(series: pl.Series) -> pl.Series:
    return series.map_elements(narrative_hash, return_dtype=pl.Utf8)


def non_empty(column: str) -> pl.Expr:
    return pl.col(column).is_not_null() & pl.col(column).str.strip_chars().ne("")


def count_rows(frame: pl.LazyFrame) -> int:
    return int(frame.select(pl.len()).collect(engine="streaming").item())


def class_counts(frame: pl.LazyFrame) -> dict[str, int]:
    rows = (
        frame.group_by("product_canonical")
        .len()
        .collect(engine="streaming")
        .sort("product_canonical")
    )
    return dict(zip(rows["product_canonical"].to_list(), rows["len"].to_list(), strict=True))


def build_training_dataset(
    *,
    input_path: Path,
    output_path: Path,
    manifest_path: Path,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    """Create a local corpus and a safe aggregate manifest from a CFPB CSV or ZIP."""

    if not input_path.is_file():
        raise DatasetBuildError(f"Local CFPB source does not exist: {input_path}")

    contract = load_contract(contract_path)
    mapping = build_mapping(contract)
    excluded_labels = set(contract["target"]["excluded_source_labels"])
    columns = SOURCE_COLUMNS
    date_column = columns["date_received"]
    narrative_column = columns["narrative"]
    product_column = columns["product"]

    csv_source = resolve_csv_source(input_path)
    source = pl.scan_csv(
        csv_source,
        infer_schema_length=10_000,
        null_values=["", "NA", "N/A"],
        truncate_ragged_lines=True,
    ).select(REQUIRED_SOURCE_COLUMNS)

    parsed_date = pl.col(date_column).str.strptime(pl.Date, format="%Y-%m-%d", strict=False)
    date_min = pl.lit(contract["source"]["date_received_min"]).str.strptime(pl.Date, "%Y-%m-%d")
    date_max = pl.lit(contract["source"]["date_received_max_exclusive"]).str.strptime(pl.Date, "%Y-%m-%d")
    in_window = parsed_date.is_between(date_min, date_max, closed="left")
    eligible = in_window & non_empty(narrative_column) & non_empty(product_column)
    mapped_product = pl.col(product_column).replace_strict(mapping, default=None)
    is_ambiguous = pl.col(product_column).is_in(excluded_labels)
    is_unknown = eligible & mapped_product.is_null() & ~is_ambiguous

    population = source.select(
        pl.len().alias("source"),
        in_window.sum().alias("in_window"),
        eligible.sum().alias("eligible_required_fields"),
        (eligible & is_ambiguous).sum().alias("excluded_ambiguous_labels"),
        is_unknown.sum().alias("unknown_labels"),
    ).collect(engine="streaming")
    population_counts = population.row(0, named=True)
    unknown_rows = int(population_counts["unknown_labels"] or 0)
    if unknown_rows:
        raise DatasetBuildError(
            f"Contract rejected {unknown_rows} row(s) with unknown source labels."
        )

    canonical = (
        source.filter(eligible & ~is_ambiguous)
        .with_columns(
            parsed_date.alias("date_received"),
            mapped_product.alias("product_canonical"),
            pl.col(narrative_column)
            .map_batches(hash_batch, return_dtype=pl.Utf8, is_elementwise=True)
            .alias("narrative_hash"),
        )
        .select(
            pl.col("date_received"),
            pl.col(narrative_column).alias("complaint_what_happened"),
            pl.col("product_canonical"),
            pl.col("narrative_hash"),
        )
    )
    staging_path = ROOT / "data" / "interim" / "cfpb_training_candidates.parquet"
    staging_path.parent.mkdir(parents=True, exist_ok=True)
    canonical.select(OUTPUT_COLUMNS).sink_parquet(staging_path)
    staged = pl.scan_parquet(staging_path)
    canonical_rows = count_rows(staged)

    conflict_hashes = (
        staged.group_by("narrative_hash")
        .agg(pl.col("product_canonical").n_unique().alias("target_count"))
        .filter(pl.col("target_count") > 1)
        .select("narrative_hash")
        .collect(engine="streaming")
    )
    conflict_values = conflict_hashes["narrative_hash"].to_list()
    conflicting_groups = len(conflict_values)
    is_conflicting = pl.col("narrative_hash").is_in(conflict_values)
    conflicting_rows = count_rows(staged.filter(is_conflicting))
    training = staged.filter(~is_conflicting)
    output_rows = count_rows(training)

    duplicate_groups = (
        training.group_by("narrative_hash")
        .len()
        .filter(pl.col("len") > 1)
    )
    duplicate_group_count = count_rows(duplicate_groups)
    duplicate_rows = int(
        duplicate_groups.select(pl.col("len").sum()).collect(engine="streaming").item() or 0
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    training.select(OUTPUT_COLUMNS).sink_parquet(output_path)

    manifest = {
        "schema_version": "1.0",
        "source": {
            "filename": input_path.name,
            "sha256": fingerprint_file(input_path),
        },
        "contract": {
            "path": display_path(contract_path),
            "sha256": fingerprint_contract(contract_path),
        },
        "rows": {
            "source": int(population_counts["source"] or 0),
            "in_window": int(population_counts["in_window"] or 0),
            "eligible_required_fields": int(population_counts["eligible_required_fields"] or 0),
            "canonical_before_conflicts": canonical_rows,
            "excluded_ambiguous_labels": int(population_counts["excluded_ambiguous_labels"] or 0),
            "excluded_conflicting_target_rows": conflicting_rows,
            "training_corpus": output_rows,
        },
        "groups": {
            "duplicate_non_conflicting": duplicate_group_count,
            "rows_in_duplicate_non_conflicting_groups": duplicate_rows,
            "conflicting_target": conflicting_groups,
        },
        "classes": class_counts(training),
        "output": {
            "path": display_path(output_path),
            "columns": OUTPUT_COLUMNS,
            "contains_narratives": True,
            "tracked_by_git": False,
        },
        "open_gates_before_training": contract["open_gates_before_training"],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a local CFPB training dataset and aggregate manifest."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_RAW_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = build_training_dataset(
        input_path=args.input,
        output_path=args.output,
        manifest_path=args.manifest,
        contract_path=args.contract,
    )
    print(
        "Built local CFPB training dataset: "
        f"{manifest['rows']['training_corpus']:,} rows, "
        f"{len(manifest['classes'])} canonical classes."
    )


if __name__ == "__main__":
    main()
