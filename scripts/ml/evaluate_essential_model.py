"""Generate aggregate essential-delivery diagnostics without loading test data."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import joblib
import polars as pl
from sklearn.metrics import confusion_matrix

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ml.train_baseline import CLASSES
from src.ml.evaluation import evaluate, save_report_json
from src.ml.visualization import plot_confusion_matrix, plot_feature_importance

DEFAULT_VALIDATION = ROOT / "data" / "processed" / "cfpb_baseline_en" / "validation.parquet"
DEFAULT_MODEL = ROOT / "models" / "cfpb_baseline.pkl"
DEFAULT_REPORT = ROOT / "reports" / "validation" / "cfpb_essential_evaluation.json"
DEFAULT_MANIFEST = ROOT / "reports" / "validation" / "cfpb_essential_model_manifest.json"
DEFAULT_FIGURES = ROOT / "reports" / "validation" / "figures"


def artifact_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frequent_confusions(y_true: list[str], y_pred: list[str], limit: int = 10) -> list[dict]:
    pairs = Counter((actual, predicted) for actual, predicted in zip(y_true, y_pred) if actual != predicted)
    return [
        {"actual": actual, "predicted": predicted, "count": count}
        for (actual, predicted), count in pairs.most_common(limit)
    ]


def evaluate_validation(
    validation_path: Path,
    model_path: Path,
    report_path: Path,
    manifest_path: Path,
    figures_dir: Path,
) -> dict:
    """Load only validation and create safe aggregate evidence."""
    artifact = joblib.load(model_path)
    vectorizer = artifact["vectorizer"]
    model = artifact["model"]
    validation = pl.read_parquet(validation_path)
    texts = validation["complaint_what_happened"].to_list()
    labels = validation["product_canonical"].to_list()
    predicted = model.predict(vectorizer.transform(texts)).tolist()

    report = evaluate(labels, predicted, CLASSES)
    confusion_path = figures_dir / "cfpb_baseline_validation_confusion_matrix.png"
    importance_path = figures_dir / "cfpb_baseline_validation_feature_importance.png"
    plot_confusion_matrix(labels, predicted, CLASSES, confusion_path, "Baseline validation confusion matrix")
    importances = abs(model.coef_).mean(axis=0).tolist()
    plot_feature_importance(importances, vectorizer.feature_names, importance_path, "Mean absolute TF-IDF coefficient")

    matrix = confusion_matrix(labels, predicted, labels=CLASSES).tolist()
    report_data = {
        "split": "validation",
        "size": len(labels),
        "metrics": report.to_dict(),
        "per_class_metrics": report.per_class_metrics,
        "weak_classes": report.weak_classes,
        "frequent_confusions": frequent_confusions(labels, predicted),
        "confusion_matrix_labels": CLASSES,
        "confusion_matrix": matrix,
        "figures": [str(confusion_path.relative_to(ROOT)), str(importance_path.relative_to(ROOT))],
        "privacy": "Aggregate metrics only; no narratives, identifiers, or per-row predictions are stored.",
        "test_partition_used": False,
    }
    save_report_json(report_data, report_path)
    manifest = {
        "artifact_path": str(model_path.relative_to(ROOT)),
        "artifact_sha256": artifact_sha256(model_path),
        "model": artifact["config"]["model"],
        "random_state": artifact["config"]["random_state"],
        "classes": CLASSES,
        "validation_path": str(validation_path.relative_to(ROOT)),
        "validation_size": len(labels),
        "test_partition_used": False,
    }
    save_report_json(manifest, manifest_path)
    return report_data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation-input", default=str(DEFAULT_VALIDATION))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--figures-dir", default=str(DEFAULT_FIGURES))
    args = parser.parse_args()
    result = evaluate_validation(
        Path(args.validation_input), Path(args.model), Path(args.report), Path(args.manifest), Path(args.figures_dir)
    )
    print(f"Validation macro F1: {result['metrics']['macro_f1']:.4f}")
    print(f"Validation accuracy: {result['metrics']['accuracy']:.4f}")
    print("Protected test partition not loaded.")


if __name__ == "__main__":
    main()
