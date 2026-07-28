"""Train the frozen essential baseline using train and validation only."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import joblib
import polars as pl
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ml.evaluate_essential_model import evaluate_validation
from scripts.ml.train_baseline import APPROVED_BASELINE_DEFAULTS, CLASSES
from src.ml.evaluation import evaluate, save_report_json
from src.ml.vectorizer import VectorizerConfig

DEFAULT_SPLITS = ROOT / "data" / "processed" / "cfpb_baseline_en"


def train_essential_baseline(
    train_path: Path,
    validation_path: Path,
    model_path: Path,
    report_path: Path,
    manifest_path: Path,
    figures_dir: Path,
) -> dict:
    """Train solely from train and generate validation-only diagnostics."""
    train = pl.read_parquet(train_path)
    validation = pl.read_parquet(validation_path)
    config = {
        "max_features": APPROVED_BASELINE_DEFAULTS["max_features"],
        "min_df": APPROVED_BASELINE_DEFAULTS["min_df"],
        "max_df": APPROVED_BASELINE_DEFAULTS["max_df"],
        "ngram_range": tuple(int(value) for value in APPROVED_BASELINE_DEFAULTS["ngram_range"].split(",")),
        "sublinear_tf": APPROVED_BASELINE_DEFAULTS["sublinear_tf"],
        "model": "LogisticRegression",
        "solver": "lbfgs",
        "C": APPROVED_BASELINE_DEFAULTS["C"],
        "class_weight": "balanced",
        "max_iter": 1000,
        "random_state": 42,
    }
    vectorizer = VectorizerConfig({key: config[key] for key in ("max_features", "min_df", "max_df", "ngram_range", "sublinear_tf")})
    train_texts = train["complaint_what_happened"].to_list()
    train_labels = train["product_canonical"].to_list()
    validation_texts = validation["complaint_what_happened"].to_list()
    validation_labels = validation["product_canonical"].to_list()

    started = time.monotonic()
    train_matrix = vectorizer.fit_transform(train_texts)
    validation_matrix = vectorizer.transform(validation_texts)
    model = LogisticRegression(
        solver=config["solver"], C=config["C"], class_weight=config["class_weight"],
        max_iter=config["max_iter"], random_state=config["random_state"],
    )
    model.fit(train_matrix, train_labels)
    train_predicted = model.predict(train_matrix)
    validation_predicted = model.predict(validation_matrix)
    metrics = evaluate(
        validation_labels, validation_predicted.tolist(), CLASSES,
        y_train_true=train_labels, y_train_pred=train_predicted.tolist(),
    )
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"vectorizer": vectorizer, "model": model, "config": config}, model_path)
    diagnostic = evaluate_validation(validation_path, model_path, report_path, manifest_path, figures_dir)
    diagnostic["training"] = {
        "size": len(train), "macro_f1": metrics.train_macro_f1,
        "gap_macro_f1": metrics.gap_macro_f1,
        "gap_within_threshold": metrics.gap_within_threshold,
        "elapsed_seconds": round(time.monotonic() - started, 1),
    }
    diagnostic["configuration"] = config
    diagnostic["test_partition_used"] = False
    save_report_json(diagnostic, report_path)
    return diagnostic


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-input", default=str(DEFAULT_SPLITS / "train.parquet"))
    parser.add_argument("--validation-input", default=str(DEFAULT_SPLITS / "validation.parquet"))
    parser.add_argument("--model", default=str(ROOT / "models" / "cfpb_essential_baseline.pkl"))
    parser.add_argument("--report", default=str(ROOT / "reports" / "validation" / "cfpb_essential_evaluation.json"))
    parser.add_argument("--manifest", default=str(ROOT / "reports" / "validation" / "cfpb_essential_model_manifest.json"))
    parser.add_argument("--figures-dir", default=str(ROOT / "reports" / "validation" / "figures"))
    args = parser.parse_args()
    result = train_essential_baseline(
        Path(args.train_input), Path(args.validation_input), Path(args.model),
        Path(args.report), Path(args.manifest), Path(args.figures_dir),
    )
    print(json.dumps(result["training"], ensure_ascii=False))
    print("Protected test partition not loaded.")


if __name__ == "__main__":
    main()
