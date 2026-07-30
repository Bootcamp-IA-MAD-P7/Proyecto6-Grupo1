"""Tests for the CFPB multiclass baseline pipeline."""

from __future__ import annotations

import json
import pickle
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import polars as pl
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from scripts.ml.train_baseline import (
    APPROVED_BASELINE_DEFAULTS,
    evaluate_test,
    load_approved_splits,
    train_pipeline,
)

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
    def test_default_training_policy_matches_evaluated_baseline(self) -> None:
        """The CLI defaults must reproduce the versioned baseline policy."""
        self.assertEqual(APPROVED_BASELINE_DEFAULTS["C"], 0.1)
        self.assertEqual(APPROVED_BASELINE_DEFAULTS["max_features"], 8000)
        self.assertEqual(APPROVED_BASELINE_DEFAULTS["min_df"], 3)
        self.assertEqual(APPROVED_BASELINE_DEFAULTS["max_df"], 0.8)
        self.assertEqual(APPROVED_BASELINE_DEFAULTS["ngram_range"], "1,2")
        self.assertTrue(APPROVED_BASELINE_DEFAULTS["sublinear_tf"])

    def test_approved_partition_paths_are_loaded_without_resplitting(self) -> None:
        """The policy-approved train/validation/test paths are used as supplied."""
        frame = pl.read_csv(FIXTURE_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            paths = []
            for name, rows in (("train", 5), ("validation", 3), ("test", 3)):
                path = tmp_path / f"{name}.parquet"
                frame.head(rows).write_parquet(path)
                paths.append(str(path))

            train, validation, test = load_approved_splits(
                Namespace(
                    input=None,
                    train_input=paths[0],
                    validation_input=paths[1],
                    test_input=paths[2],
                )
            )

            self.assertEqual((len(train), len(validation), len(test)), (5, 3, 3))

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
        self.assertIn("gap_macro_f1", report.get("validation", report))
        self.assertIn("gap_within_threshold", report.get("validation", report))
        self.assertIn("train", report)
        self.assertIn("validation", report)

    def test_training_pipeline_separates_vectorizer_and_model_settings(self) -> None:
        """The approved baseline config must not pass model keys into TF-IDF."""
        fixture = pl.read_csv(FIXTURE_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_path = tmp_path / "synthetic.parquet"
            model_dir = tmp_path / "models"
            report_path = tmp_path / "metrics.json"
            fixture.write_parquet(input_path)

            train_pipeline(
                Namespace(
                    input=str(input_path),
                    model_dir=str(model_dir),
                    report=str(report_path),
                    C=0.1,
                    max_features=100,
                    min_df=1,
                    max_df=1.0,
                    ngram_range="1,2",
                    sublinear_tf=True,
                    evaluate_test=False,
                )
            )

            artifact_path = model_dir / "cfpb_baseline.pkl"
            self.assertTrue(artifact_path.exists())
            artifact = joblib.load(artifact_path)
            self.assertEqual(artifact["config"]["model"], "LogisticRegression")
            self.assertNotIn("model", artifact["vectorizer"].get_config())
            self.assertTrue(report_path.exists())

    def test_test_only_uses_the_approved_test_partition_by_default(self) -> None:
        """Test-only evaluation must not require or re-split the legacy corpus."""
        vectorizer, model, frame = train_on_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            model_dir = tmp_path / "models"
            model_dir.mkdir()
            joblib.dump(
                {"vectorizer": vectorizer, "model": model},
                model_dir / "cfpb_baseline.pkl",
            )
            test_path = tmp_path / "test.parquet"
            report_path = tmp_path / "metrics.json"
            frame.write_parquet(test_path)

            evaluate_test(
                Namespace(
                    input=None,
                    test_input=str(test_path),
                    model_dir=str(model_dir),
                    report=str(report_path),
                )
            )

            self.assertTrue(report_path.exists())


if __name__ == "__main__":
    unittest.main()
