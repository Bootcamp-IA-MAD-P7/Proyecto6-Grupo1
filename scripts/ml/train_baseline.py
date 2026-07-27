"""Train and evaluate a CFPB multiclass baseline (TF-IDF + LogisticRegression)."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import joblib
import polars as pl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)

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


def evaluate_and_report(
    y_true: list,
    y_pred: list,
    class_distribution: dict | None = None,
) -> tuple[dict, list]:
    macro_f1 = f1_score(y_true, y_pred, average="macro")
    weighted_f1 = f1_score(y_true, y_pred, average="weighted")
    accuracy = accuracy_score(y_true, y_pred)
    precision_macro = precision_score(y_true, y_pred, average="macro")
    recall_macro = recall_score(y_true, y_pred, average="macro")

    report = classification_report(
        y_true, y_pred, labels=CLASSES, output_dict=True, zero_division=0
    )

    weak_classes = []
    for cls in CLASSES:
        cls_report = report.get(cls, {})
        f1_val = cls_report.get("f1-score", 0)
        support = cls_report.get("support", 0)
        print(f"  {cls:<55} F1: {f1_val:.4f}  support: {support}")
        if f1_val < 0.5:
            weak_classes.append({"class": cls, "f1": round(f1_val, 4), "support": support})

    metrics = {
        "size": len(y_true),
        "accuracy": round(accuracy, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "precision_macro": round(precision_macro, 4),
        "recall_macro": round(recall_macro, 4),
    }
    per_class = {
        cls: {
            k: round(v, 4) if isinstance(v, float) else v
            for k, v in report.get(cls, {}).items()
        }
        for cls in CLASSES
    }
    return metrics, per_class, weak_classes


def train_pipeline(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    model_dir = Path(args.model_dir)
    report_path = Path(args.report)
    ngram = tuple(int(x) for x in args.ngram_range.split(","))

    config = {
        "vectorizer": "TfidfVectorizer",
        "max_features": args.max_features,
        "min_df": args.min_df,
        "max_df": args.max_df,
        "ngram_range": ngram,
        "sublinear_tf": args.sublinear_tf,
        "stop_words": "english",
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
    vectorizer = TfidfVectorizer(
        max_features=config["max_features"],
        stop_words=config["stop_words"],
        min_df=config["min_df"],
        max_df=config["max_df"],
        ngram_range=config["ngram_range"],
        sublinear_tf=config["sublinear_tf"],
    )
    X_train = vectorizer.fit_transform(train_texts)
    X_val = vectorizer.transform(val_texts)
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
    model_path = model_dir / "cfpb_baseline.pkl"
    joblib.dump({"vectorizer": vectorizer, "model": model, "config": config}, model_path)
    print(f"Model saved to {model_path}")

    print("\n--- Validation Metrics ---")
    val_pred = model.predict(X_val)
    train_pred = model.predict(X_train)

    train_macro_f1 = f1_score(train_labels, train_pred, average="macro")
    val_metrics, val_per_class, val_weak = evaluate_and_report(val_labels, val_pred)

    gap = abs(train_macro_f1 - val_metrics["macro_f1"])
    print(f"Train macro F1: {train_macro_f1:.4f}")
    print(f"Gap: {gap:.4f}  {'PASS' if gap < 0.05 else 'FAIL'}")

    report_data = {
        "config": config,
        "train": {"size": len(train), "macro_f1": round(train_macro_f1, 4)},
        "validation": val_metrics,
        "test_protected": {"size": len(test)},
        "gap_macro_f1": round(gap, 4),
        "gap_within_threshold": gap < 0.05,
        "weak_classes": val_weak,
        "per_class_metrics": val_per_class,
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
        X_test = vectorizer.transform(test_texts)
        test_pred = model.predict(X_test)
        test_metrics, test_per_class, test_weak = evaluate_and_report(
            test_labels, test_pred
        )
        report_data["test"] = test_metrics
        report_data["test_per_class_metrics"] = test_per_class
        report_data["test_weak_classes"] = test_weak

        print(f"\nTest  macro F1: {test_metrics['macro_f1']:.4f}")
        print(f"Test  accuracy: {test_metrics['accuracy']:.4f}")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    print(f"\nReport saved to {report_path}")


def evaluate_test(args: argparse.Namespace) -> None:
    model_dir = Path(args.model_dir)
    report_path = Path(args.report)
    input_path = Path(args.input)
    model_path = model_dir / "cfpb_baseline.pkl"

    print(f"Loading model from {model_path}...")
    artifact = joblib.load(model_path)
    vectorizer = artifact["vectorizer"]
    model = artifact["model"]

    print(f"Loading data from {input_path}...")
    df = load_data(input_path)
    _, _, test = temporal_split(df)
    test_texts = test["complaint_what_happened"].to_list()
    test_labels = test["product_canonical"].to_list()
    print(f"Test size: {len(test):,}")

    print("Vectorizing test...")
    X_test = vectorizer.transform(test_texts)

    print("\n--- Test (protected) Metrics [ONE-SHOT] ---")
    test_pred = model.predict(X_test)
    test_metrics, test_per_class, test_weak = evaluate_and_report(
        test_labels, test_pred
    )

    print(f"\nTest  macro F1: {test_metrics['macro_f1']:.4f}")
    print(f"Test  accuracy: {test_metrics['accuracy']:.4f}")

    if report_path.exists():
        with open(report_path) as f:
            report_data = json.load(f)
    else:
        print(f"Report not found at {report_path}, creating new one")
        report_data = {}

    report_data["test"] = test_metrics
    report_data["test_per_class_metrics"] = test_per_class
    report_data["test_weak_classes"] = test_weak
    report_data["evaluated_on_test"] = True

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    print(f"Report updated at {report_path}")


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
