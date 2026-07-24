"""Convert CFPB CSV to Parquet applying the target contract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "config" / "cfpb_target_contract.json"
RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"

CSV_COLUMNS = {
    "complaint_id": "Complaint ID",
    "date_received": "Date received",
    "narrative": "Consumer complaint narrative",
    "product": "Product",
}
KEEP_COLUMNS = list(CSV_COLUMNS.values())
WRITE_COLUMNS = [
    ("Complaint ID", pl.Utf8),
    ("Date received", pl.Utf8),
    ("Consumer complaint narrative", pl.Utf8),
    ("Product", pl.Utf8),
    ("product_canonical", pl.Utf8),
    ("narrative_hash", pl.Utf8),
]


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def build_mapping(contract: dict) -> dict:
    mapping = {}
    for label in contract["target"]["canonical_labels"]:
        mapping[label] = label
    for alias, canonical in contract["target"]["aliases"].items():
        mapping[alias] = canonical
    return mapping


def normalize_narrative(text: str | None) -> str:
    if text is None:
        return ""
    return " ".join(text.lower().split())


def narrative_hash(text: str | None) -> str:
    return hashlib.sha256(normalize_narrative(text).encode("utf-8")).hexdigest()


def hash_batch(series: pl.Series) -> pl.Series:
    return series.map_elements(narrative_hash, return_dtype=pl.Utf8)


def main() -> None:
    contract = load_contract()
    mapping = build_mapping(contract)
    excluded = set(contract["target"]["excluded_source_labels"])
    date_min = contract["source"]["date_received_min"]
    date_max = contract["source"]["date_received_max_exclusive"]
    unknown_policy = contract["target"]["unknown_label_policy"]

    csv_files = list(RAW_DIR.glob("*.csv")) + list(RAW_DIR.glob("*.csv.zip"))
    if not csv_files:
        print("No CSV found in data/raw/")
        return
    source = csv_files[0]

    print(f"Reading {source.name}...")
    lazy = pl.scan_csv(
        source,
        infer_schema_length=10000,
        null_values=["", "NA", "N/A"],
        truncate_ragged_lines=True,
    ).select(KEEP_COLUMNS)

    col = CSV_COLUMNS
    date_col = col["date_received"]
    narrative_col = col["narrative"]
    product_col = col["product"]

    print("Filtering window and non-empty...")
    df = lazy.filter(
        pl.col(date_col).str.strptime(pl.Date, format="%Y-%m-%d", strict=False).is_between(
            pl.lit(date_min).str.strptime(pl.Date, "%Y-%m-%d"),
            pl.lit(date_max).str.strptime(pl.Date, "%Y-%m-%d"),
            closed="left",
        ),
    ).filter(
        pl.col(narrative_col).is_not_null(),
        pl.col(product_col).is_not_null(),
    )

    print("Mapping target...")
    map_expr = pl.col(product_col).replace_strict(mapping, default=None)

    df = df.with_columns(map_expr.alias("product_canonical"))

    if unknown_policy == "fail":
        unknown = df.filter(pl.col("product_canonical").is_null() & ~pl.col(product_col).is_in(excluded))
        unknown_count = unknown.select(pl.len()).collect().item()
        if unknown_count > 0:
            labels = unknown.select(pl.col(product_col).unique()).collect().to_series().to_list()
            raise ValueError(f"Unknown labels ({unknown_count} rows): {labels}")

    print("Excluding ambiguous labels...")
    excluded_count = df.filter(pl.col(product_col).is_in(excluded)).select(pl.len()).collect().item()
    df = df.filter(
        pl.col("product_canonical").is_not_null(),
    )

    print("Computing narrative hashes...")
    df = df.with_columns(
        pl.col(narrative_col).map_batches(
            hash_batch, return_dtype=pl.Utf8, is_elementwise=True
        ).alias("narrative_hash")
    )

    total = df.select(pl.len()).collect().item()
    print(f"Total rows after filtering: {total:,}")
    print(f"Excluded ambiguous: {excluded_count:,}")

    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    out_path = INTERIM_DIR / "cfpb.parquet"
    df.sink_parquet(out_path)
    print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
