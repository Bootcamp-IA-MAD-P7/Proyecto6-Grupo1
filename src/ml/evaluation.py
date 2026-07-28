"""Evaluation metrics and report generation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass
class EvaluationReport:
    config: dict | None = None
    train_size: int = 0
    train_macro_f1: float = 0.0
    split: str = "validation"
    size: int = 0
    accuracy: float = 0.0
    macro_f1: float = 0.0
    weighted_f1: float = 0.0
    precision_macro: float = 0.0
    recall_macro: float = 0.0
    roc_auc: float | None = None
    gap_macro_f1: float | None = None
    gap_within_threshold: bool | None = None
    weak_classes: list[dict] = field(default_factory=list)
    per_class_metrics: dict[str, dict] = field(default_factory=dict)
    class_distribution: dict[str, int] | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        base: dict[str, Any] = {
            "size": self.size,
            "accuracy": round(self.accuracy, 4),
            "macro_f1": round(self.macro_f1, 4),
            "weighted_f1": round(self.weighted_f1, 4),
            "precision_macro": round(self.precision_macro, 4),
            "recall_macro": round(self.recall_macro, 4),
        }
        if self.roc_auc is not None:
            base["roc_auc"] = round(self.roc_auc, 4)
        if self.gap_macro_f1 is not None:
            base["gap_macro_f1"] = round(self.gap_macro_f1, 4)
            base["gap_within_threshold"] = self.gap_within_threshold
        return base


def evaluate(
    y_true: list[str],
    y_pred: list[str],
    classes: list[str],
    weak_threshold: float = 0.5,
    *,
    y_train_true: list[str] | None = None,
    y_train_pred: list[str] | None = None,
    y_pred_proba: list[list[float]] | None = None,
) -> EvaluationReport:
    """Compute all metrics and return an EvaluationReport."""
    report = EvaluationReport()
    report.size = len(y_true)
    report.accuracy = accuracy_score(y_true, y_pred)
    report.macro_f1 = f1_score(y_true, y_pred, average="macro")
    report.weighted_f1 = f1_score(y_true, y_pred, average="weighted")
    report.precision_macro = precision_score(y_true, y_pred, average="macro")
    report.recall_macro = recall_score(y_true, y_pred, average="macro")
    if y_pred_proba is not None:
        try:
            report.roc_auc = roc_auc_score(y_true, y_pred_proba, multi_class="ovr", average="macro", labels=classes)
        except Exception:
            report.roc_auc = None

    sk_report = classification_report(
        y_true, y_pred, labels=classes, output_dict=True, zero_division=0
    )

    weak = []
    per_class = {}
    for cls in classes:
        cr = sk_report.get(cls, {})
        f1_val = cr.get("f1-score", 0.0)
        support = cr.get("support", 0)
        per_class[cls] = {
            k: round(v, 4) if isinstance(v, (int, float)) and not isinstance(v, bool) else v
            for k, v in cr.items()
        }
        if f1_val < weak_threshold:
            weak.append({"class": cls, "f1": round(f1_val, 4), "support": support})

    report.per_class_metrics = per_class
    report.weak_classes = weak

    if y_train_true is not None and y_train_pred is not None:
        train_f1 = f1_score(y_train_true, y_train_pred, average="macro")
        report.train_macro_f1 = round(train_f1, 4)
        gap = abs(train_f1 - report.macro_f1)
        report.gap_macro_f1 = round(gap, 4)
        report.gap_within_threshold = gap < 0.05

    return report


def save_report_json(report_data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
