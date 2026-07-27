"""Train and evaluate a CFPB multiclass baseline (TF-IDF + LogisticRegression)."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import joblib
import polars as pl
from sklearn.linear_model import LogisticRegression

from src.ml.evaluation import evaluate, save_report_json
from src.ml.vectorizer import VectorizerConfig

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "processed" / "cfpb_training.parquet"
DEFAULT_MODEL_DIR = ROOT / "models"
DEFAULT_REPORT = ROOT / "reports" / "validation" / "cfpb_baseline_metrics.json"
RANDOM_STATE = 42
CLASSES = [
    "Checking or savings account",
    "Credit card",
    "Credit reporting or other personal consumer reports",
    "Debt collection",
    "Debt or credit management",
    "Money transfer, virtual currency, or money service",
    "Mortgage",
    "Payday loan, title loan, personal loan, or advance loan",
    "Prepaid card",
    "Student loan",
    "Vehicle loan or lease",
]


def load_data(input_path: Path) -> pl.DataFrame:
    return pl.read_parquet(input_path)


def temporal_split(df: pl.DataFrame, val_frac: float = 0.15, test_frac: float = 0.15):
    dates = df["date_received"].sort()
    total = len(dates)
    train_cut = dates[int(total * (1 - test_frac - val_frac))]
    val_cut = dates[int(total * (1 - test_frac))]
    train = df.filter(pl.col("date_received") < train_cut)
    val = df.filter(
        (pl.col("date_received") >= train_cut)
        & (pl.col("date_received") < val_cut)
    )
    test = df.filter(pl.col("date_received") >= val_cut)
    return train, val, test


def train_pipeline(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    model_dir = Path(args.model_dir)
    report_path = Path(args.report)

    config = {
        "max_features": args.max_features,
        "min_df": args.min_df,
        "max_df": args.max_df,
        "ngram_range": tuple(int(x) for x in args.ngram_range.split(",")),
        "sublinear_tf": args.sublinear_tf,
        "model": "LogisticRegression",
        "solver": "lbfgs",
        "C": args.C,
        "class_weight": "balanced",
        "max_iter": 1000,
        "random_state": RANDOM_STATE,
    }
    print(f"Config: {json.dumps(config)}")

    print(f"Loading {input_path}...")
    df = load_data(input_path)
    print(f"Total rows: {len(df):,}")

    print("Splitting temporally...")
    train, val, test = temporal_split(df)

    train_texts = train["complaint_what_happened"].to_list()
    train_labels = train["product_canonical"].to_list()
    val_texts = val["complaint_what_happened"].to_list()
    val_labels = val["product_canonical"].to_list()
    test_texts = test["complaint_what_happened"].to_list()
    test_labels = test["product_canonical"].to_list()

    print(f"Train: {len(train):,}  Val: {len(val):,}  Test (protected): {len(test):,}")

    print("Vectorizing with TF-IDF...")
    t0 = time.time()
    vc = VectorizerConfig(config)
    X_train = vc.fit_transform(train_texts)
    X_val = vc.transform(val_texts)
    print(f"Vectorization done in {time.time() - t0:.1f}s. Shape: {X_train.shape}")

    print("Training LogisticRegression...")
    t0 = time.time()
    model = LogisticRegression(
        solver="lbfgs",
        C=config["C"],
        class_weight="balanced",
        max_iter=1000,
        random_state=RANDOM_STATE,
    )
    model.fit(X_train, train_labels)
    print(f"Training done in {time.time() - t0:.1f}s")

    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "cfpb_baseline.joblib"
    joblib.dump({"vectorizer": vc, "model": model, "config": config}, model_path)
    print(f"Model saved to {model_path}")

    print("\n--- Validation Metrics ---")
    val_pred = model.predict(X_val)
    train_pred = model.predict(X_train)

    ev = evaluate(
        val_labels, val_pred, CLASSES,
        y_train_true=train_labels, y_train_pred=train_pred,
    )
    for cls in CLASSES:
        cr = ev.per_class_metrics.get(cls, {})
        print(f"  {cls:<55} F1: {cr.get('f1-score', 0):.4f}  support: {cr.get('support', 0)}")

    print(f"Train macro F1: {ev.train_macro_f1:.4f}")
    print(f"Gap: {ev.gap_macro_f1:.4f}  {'PASS' if ev.gap_within_threshold else 'FAIL'}")

    report_data: dict = {
        "config": vc.get_config() | {"model": "LogisticRegression", "solver": "lbfgs", "C": config["C"], "class_weight": "balanced", "max_iter": 1000, "random_state": RANDOM_STATE},
        "train": {"size": len(train), "macro_f1": ev.train_macro_f1},
        "validation": ev.to_dict(),
        "test_protected": {"size": len(test)},
        "weak_classes": ev.weak_classes,
        "per_class_metrics": ev.per_class_metrics,
        "class_distribution": {
            row["product_canonical"]: row["len"]
            for row in (
                train.group_by("product_canonical")
                .len()
                .sort("product_canonical")
                .iter_rows(named=True)
            )
        },
    }

    if args.evaluate_test:
        print("\n--- Test (protected) Metrics [ONE-SHOT] ---")
        X_test = vc.transform(test_texts)
        test_pred = model.predict(X_test)
        tev = evaluate(test_labels, test_pred, CLASSES)
        report_data["test"] = tev.to_dict()
        report_data["test_per_class_metrics"] = tev.per_class_metrics
        report_data["test_weak_classes"] = tev.weak_classes
        print(f"Test macro F1: {tev.macro_f1:.4f}  accuracy: {tev.accuracy:.4f}")

    save_report_json(report_data, report_path)
    print(f"\nReport saved to {report_path}")


def evaluate_test(args: argparse.Namespace) -> None:
    model_dir = Path(args.model_dir)
    report_path = Path(args.report)
    input_path = Path(args.input)
    model_path = model_dir / "cfpb_baseline.joblib"

    print(f"Loading model from {model_path}...")
    artifact = joblib.load(model_path)
    vc = artifact["vectorizer"]
    model = artifact["model"]

    print(f"Loading data from {input_path}...")
    df = load_data(input_path)
    _, _, test = temporal_split(df)
    test_texts = test["complaint_what_happened"].to_list()
    test_labels = test["product_canonical"].to_list()
    print(f"Test size: {len(test):,}")

    X_test = vc.transform(test_texts)
    test_pred = model.predict(X_test)
    tev = evaluate(test_labels, test_pred, CLASSES)
    print(f"Test macro F1: {tev.macro_f1:.4f}  accuracy: {tev.accuracy:.4f}")

    if report_path.exists():
        with open(report_path) as f:
            report_data = json.load(f)
    else:
        report_data = {}

    report_data["test"] = tev.to_dict()
    report_data["test_per_class_metrics"] = tev.per_class_metrics
    report_data["test_weak_classes"] = tev.weak_classes
    save_report_json(report_data, report_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--model-dir", default=str(DEFAULT_MODEL_DIR))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--C", type=float, default=1.0)
    parser.add_argument("--max-features", type=int, default=10000)
    parser.add_argument("--min-df", type=int, default=1)
    parser.add_argument("--max-df", type=float, default=1.0)
    parser.add_argument("--ngram-range", type=str, default="1,1")
    parser.add_argument("--sublinear-tf", action="store_true")
    parser.add_argument("--evaluate-test", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    args = parser.parse_args()

    if args.test_only:
        evaluate_test(args)
    else:
        train_pipeline(args)


if __name__ == "__main__":
    main()
