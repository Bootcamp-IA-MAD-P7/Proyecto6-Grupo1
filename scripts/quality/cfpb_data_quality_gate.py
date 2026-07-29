"""Privacy-safe integrity checks for CFPB partition contracts."""

from __future__ import annotations

from collections.abc import Collection, Mapping
from typing import Any

import polars as pl


class DataQualityGateError(RuntimeError):
    """Raised when an aggregate partition contract is not satisfied."""


def validate_partition_frames(
    partitions: Mapping[str, pl.DataFrame],
    *,
    required_columns: Collection[str],
    canonical_labels: Collection[str],
    group_key: str,
    allowed_columns: Collection[str] | None = None,
) -> dict[str, Any]:
    """Validate synthetic or local partitions without returning row contents."""

    if not partitions:
        raise DataQualityGateError("At least one partition is required.")

    required = set(required_columns)
    expected_labels = set(canonical_labels)
    if not required or not expected_labels:
        raise DataQualityGateError("Quality gate contracts must define columns and labels.")

    partition_frames: list[pl.DataFrame] = []
    rows_by_partition: dict[str, int] = {}
    for partition_name, frame in partitions.items():
        if not partition_name:
            raise DataQualityGateError("Partition names must be non-empty.")
        if missing := required.difference(frame.columns):
            raise DataQualityGateError("A partition is missing required contract columns.")
        if allowed_columns is not None and set(frame.columns).difference(allowed_columns):
            raise DataQualityGateError("A partition contains columns outside its contract.")
        if frame.select([pl.col(column).is_null().any() for column in required]).row(0).count(True):
            raise DataQualityGateError("A partition contains null values in critical columns.")
        if frame.filter(~pl.col("product_canonical").is_in(expected_labels)).height:
            raise DataQualityGateError("A partition contains a label outside the canonical contract.")

        rows_by_partition[partition_name] = frame.height
        partition_frames.append(frame.select([group_key, "product_canonical"]).with_columns(
            pl.lit(partition_name).alias("_quality_partition")
        ))

    combined = pl.concat(partition_frames, how="vertical")
    conflicting_targets = (
        combined.group_by(group_key)
        .agg(pl.col("product_canonical").n_unique().alias("_target_count"))
        .filter(pl.col("_target_count") > 1)
    )
    if conflicting_targets.height:
        raise DataQualityGateError("Duplicate groups contain conflicting canonical targets.")

    cross_partition_groups = (
        combined.group_by(group_key)
        .agg(pl.col("_quality_partition").n_unique().alias("_partition_count"))
        .filter(pl.col("_partition_count") > 1)
    )
    if cross_partition_groups.height:
        raise DataQualityGateError("Narrative groups cross local partitions.")

    return {
        "partitions": len(partitions),
        "rows_by_partition": rows_by_partition,
        "canonical_label_count": len(expected_labels),
        "cross_partition_groups": 0,
        "conflicting_duplicate_groups": 0,
    }
