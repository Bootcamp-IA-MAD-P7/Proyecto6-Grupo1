"""Tests for the CFPB multiclass baseline pipeline."""

from __future__ import annotations

import json
import pickle
import tempfile
import unittest
from pathlib import Path

import polars as pl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "synthetic_baseline_data.csv"
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
RANDOM_STATE = 42


def train_on_fixture() -> tuple:
    df = pl.read_csv(FIXTURE_PATH)
    texts = df["complaint_what_happened"].to_list()
    labels = df["product_canonical"].to_list()
    vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
    X = vectorizer.fit_transform(texts)
    model = LogisticRegression(
        solver="lbfgs", class_weight="balanced", max_iter=1000, random_state=RANDOM_STATE
    )
    model.fit(X, labels)
    return vectorizer, model, df


class CFPBBaselineTests(unittest.TestCase):
    def test_output_shape(self) -> None:
        vectorizer, model, df = train_on_fixture()
        texts = df["complaint_what_happened"].to_list()
        X = vectorizer.transform(texts)
        probs = model.predict_proba(X)
        preds = model.predict(X)
        self.assertEqual(probs.shape, (len(df), 11))
        self.assertEqual(len(preds), len(df))

    def test_all_eleven_classes_predicted(self) -> None:
        vectorizer, model, df = train_on_fixture()
        texts = df["complaint_what_happened"].to_list()
        X = vectorizer.transform(texts)
        preds = model.predict(X)
        pred_classes = set(preds)
        for cls in CLASSES:
            self.assertIn(cls, model.classes_)
        self.assertTrue(pred_classes.issubset(set(CLASSES)))

    def test_reproducibility_same_seed(self) -> None:
        df = pl.read_csv(FIXTURE_PATH)
        texts = df["complaint_what_happened"].to_list()
        labels = df["product_canonical"].to_list()

        def run() -> float:
            v = TfidfVectorizer(max_features=100, stop_words="english")
            m = LogisticRegression(
                solver="lbfgs", class_weight="balanced", max_iter=1000, random_state=RANDOM_STATE
            )
            X = v.fit_transform(texts)
            m.fit(X, labels)
            from sklearn.metrics import f1_score
            return f1_score(labels, m.predict(X), average="macro")

        f1_1 = run()
        f1_2 = run()
        self.assertAlmostEqual(f1_1, f1_2)

    def test_model_serialization(self) -> None:
        vectorizer, model, df = train_on_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "model.pkl"
            with open(path, "wb") as f:
                pickle.dump({"vectorizer": vectorizer, "model": model}, f)
            self.assertTrue(path.exists())
            with open(path, "rb") as f:
                loaded = pickle.load(f)
            self.assertIn("vectorizer", loaded)
            self.assertIn("model", loaded)
            texts = df["complaint_what_happened"].to_list()
            X = loaded["vectorizer"].transform(texts)
            preds = loaded["model"].predict(X)
            self.assertEqual(len(preds), len(df))

    def test_metrics_report_no_narratives(self) -> None:
        report_path = ROOT / "reports" / "validation" / "cfpb_baseline_metrics.json"
        self.assertTrue(report_path.exists())
        with open(report_path, encoding="utf-8") as f:
            report = json.load(f)
        report_str = json.dumps(report)
        self.assertNotIn("I had an issue", report_str)
        self.assertNotIn("complaint_what_happened", report_str)
        self.assertIn("macro_f1", report_str)
        self.assertIn("per_class_metrics", report_str)
        self.assertIn("weak_classes", report_str)

    def test_gap_recorded_in_report(self) -> None:
        report_path = ROOT / "reports" / "validation" / "cfpb_baseline_metrics.json"
        self.assertTrue(report_path.exists())
        with open(report_path, encoding="utf-8") as f:
            report = json.load(f)
        self.assertIn("gap_macro_f1", report)
        self.assertIn("gap_within_threshold", report)
        self.assertIn("train", report)
        self.assertIn("validation", report)


if __name__ == "__main__":
    unittest.main()
