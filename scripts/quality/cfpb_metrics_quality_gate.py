"""Privacy-safe contract checks for aggregated CFPB evaluation metrics."""

from __future__ import annotations

from collections.abc import Mapping
from math import isfinite
from typing import Any


class MetricsQualityGateError(RuntimeError):
    """Raised when an aggregated metrics report is not eligible evidence."""


def _metric_value(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise MetricsQualityGateError(f"Metric field '{field}' is invalid.")
    return float(value)


def _require_mapping(report: Mapping[str, Any], field: str) -> Mapping[str, Any]:
    value = report.get(field)
    if not isinstance(value, Mapping):
        raise MetricsQualityGateError(f"Metrics report is missing '{field}'.")
    return value


def validate_metrics_report(
    report: Mapping[str, Any],
    *,
    quality_gates: Mapping[str, Any],
    selection_partition: str,
) -> dict[str, Any]:
    """Validate aggregate evidence without recalculating or selecting a model.

    ``selection_partition`` makes any attempted use of protected test evidence
    explicit. A report may retain a protected test section for post-selection
    evaluation, but the gate never accepts it as the selection basis.
    """
    metrics_policy = _require_mapping(quality_gates, "metrics")
    model_policy = _require_mapping(quality_gates, "model")
    evaluation_partition = metrics_policy.get("evaluation_partition")
    if selection_partition != evaluation_partition:
        raise MetricsQualityGateError("Protected test data cannot select or promote a model.")

    required_report_fields = metrics_policy.get("required_report_fields")
    required_validation_fields = metrics_policy.get("required_validation_fields")
    required_per_class_fields = metrics_policy.get("required_per_class_fields")
    expected_class_count = model_policy.get("expected_class_count")
    maximum_gap = metrics_policy.get("max_train_validation_macro_f1_gap_exclusive")
    if not all(
        isinstance(value, list)
        for value in (required_report_fields, required_validation_fields, required_per_class_fields)
    ) or not isinstance(expected_class_count, int) or not isinstance(maximum_gap, (int, float)):
        raise MetricsQualityGateError("Quality-gate policy is invalid.")

    for field in required_report_fields:
        if field not in report:
            raise MetricsQualityGateError(f"Metrics report is missing '{field}'.")

    train = _require_mapping(report, "train")
    validation = _require_mapping(report, "validation")
    _metric_value(train.get("macro_f1"), "train.macro_f1")
    for field in required_validation_fields:
        value = _metric_value(validation.get(field), f"validation.{field}")
        if not 0.0 <= value <= 1.0:
            raise MetricsQualityGateError(f"Metric field 'validation.{field}' is outside its valid range.")

    per_class_metrics = _require_mapping(report, "per_class_metrics")
    if len(per_class_metrics) != expected_class_count:
        raise MetricsQualityGateError("Metrics report does not contain the canonical class count.")
    for metrics in per_class_metrics.values():
        if not isinstance(metrics, Mapping):
            raise MetricsQualityGateError("Per-class metrics are invalid.")
        for field in required_per_class_fields:
            _metric_value(metrics.get(field), f"per_class_metrics.{field}")

    gap = _metric_value(report.get("gap_macro_f1"), "gap_macro_f1")
    if gap >= float(maximum_gap):
        raise MetricsQualityGateError("Train-validation macro F1 gap does not satisfy the policy.")
    if report.get("gap_within_threshold") is not True:
        raise MetricsQualityGateError("Metrics report does not confirm the approved gap status.")

    return {
        "evaluation_partition": selection_partition,
        "canonical_class_count": expected_class_count,
        "gap_within_threshold": True,
        "protected_test_used_for_selection": False,
    }
