"""Integration tests for the full ensemble pipeline on synthetic data."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import polars as pl

from src.ml.evaluation import evaluate
from src.ml.models import train_rf, train_xgb
from src.ml.vectorizer import VectorizerConfig

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


class EnsemblePipelineTests(unittest.TestCase):
    def _prepare(self):
        df = pl.read_csv(FIXTURE_PATH)
        train = df.head(8)
        val = df.tail(3)
        train_texts = train["complaint_what_happened"].to_list()
        train_labels = train["product_canonical"].to_list()
        val_texts = val["complaint_what_happened"].to_list()
        val_labels = val["product_canonical"].to_list()
        vc = VectorizerConfig({"max_features": 100, "min_df": 1, "max_df": 1.0, "ngram_range": [1, 1]})
        X_train = vc.fit_transform(train_texts)
        X_val = vc.transform(val_texts)
        return X_train, train_labels, X_val, val_labels, vc

    def test_rf_pipeline_predicts_on_val(self):
        X_train, y_train, X_val, y_val, _ = self._prepare()
        model = train_rf(X_train, y_train)
        preds = model.predict(X_val)
        self.assertEqual(len(preds), len(y_val))
        for p in preds:
            self.assertIn(p, CLASSES)

    def test_xgb_pipeline_predicts_on_val(self):
        X_train, y_train, X_val, y_val, _ = self._prepare()
        model = train_xgb(X_train, y_train)
        preds = model.predict(X_val)
        self.assertEqual(len(preds), len(y_val))
        for p in preds:
            self.assertIn(p, CLASSES)

    def test_rf_evaluates_with_report_structure(self):
        X_train, y_train, X_val, y_val, _vc = self._prepare()
        model = train_rf(X_train, y_train)
        preds = model.predict(X_val)
        ev = evaluate(y_val, preds, CLASSES)
        report = ev.to_dict()
        self.assertIn("macro_f1", report)
        self.assertIn("accuracy", report)

    def test_xgb_gap_is_reasonable(self):
        X_train, y_train, X_val, y_val, _ = self._prepare()
        model = train_xgb(X_train, y_train)
        train_pred = model.predict(X_train)
        val_pred = model.predict(X_val)
        ev = evaluate(
            y_val, val_pred, CLASSES,
            y_train_true=y_train, y_train_pred=train_pred,
        )
        if ev.gap_macro_f1 is not None:
            self.assertGreaterEqual(ev.gap_macro_f1, 0)

    def test_serialization_roundtrip(self):
        X_train, y_train, X_val, y_val, vc = self._prepare()
        model = train_rf(X_train, y_train)
        import joblib
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "model.pkl"
            joblib.dump({"vectorizer": vc, "model": model}, path)
            loaded = joblib.load(path)
            preds = loaded["model"].predict(X_val)
            self.assertEqual(len(preds), len(y_val))


if __name__ == "__main__":
    unittest.main()
