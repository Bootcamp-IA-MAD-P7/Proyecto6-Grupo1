"""Tests for the ensemble model wrappers (RF, XGBoost)."""

from __future__ import annotations

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


def _load_fixture():
    df = pl.read_csv(FIXTURE_PATH)
    texts = df["complaint_what_happened"].to_list()
    labels = df["product_canonical"].to_list()
    vc = VectorizerConfig({"max_features": 100, "ngram_range": [1, 1]})
    X = vc.fit_transform(texts)
    return X, labels, df


class EnsembleModelTests(unittest.TestCase):
    def test_rf_output_shape(self):
        X, labels, _df = _load_fixture()
        model = train_rf(X, labels)
        preds = model.predict(X)
        self.assertEqual(len(preds), len(_df))

    def test_xgb_output_shape(self):
        X, labels, _df = _load_fixture()
        model = train_xgb(X, labels)
        preds = model.predict(X)
        self.assertEqual(len(preds), len(_df))

    def test_rf_all_classes_in_model(self):
        X, labels, _ = _load_fixture()
        model = train_rf(X, labels)
        for cls in CLASSES:
            self.assertIn(cls, model.classes_)

    def test_xgb_all_classes_in_model(self):
        X, labels, _ = _load_fixture()
        model = train_xgb(X, labels)
        for cls in CLASSES:
            self.assertIn(cls, model.classes_)

    def test_rf_predictions_are_from_contract(self):
        X, labels, _ = _load_fixture()
        model = train_rf(X, labels)
        preds = model.predict(X)
        for p in preds:
            self.assertIn(p, CLASSES)

    def test_xgb_predictions_are_from_contract(self):
        X, labels, _ = _load_fixture()
        model = train_xgb(X, labels)
        preds = model.predict(X)
        for p in preds:
            self.assertIn(p, CLASSES)

    def test_rf_reproducibility_same_seed(self):
        X, labels, _ = _load_fixture()

        def run():
            m = train_rf(X, labels)
            return m.predict(X).tolist()

        p1 = run()
        p2 = run()
        self.assertEqual(p1, p2)

    def test_xgb_reproducibility_same_seed(self):
        X, labels, _ = _load_fixture()

        def run():
            m = train_xgb(X, labels)
            return m.predict(X).tolist()

        p1 = run()
        p2 = run()
        self.assertEqual(p1, p2)

    def test_evaluation_returns_metrics(self):
        X, labels, _ = _load_fixture()
        model = train_rf(X, labels)
        preds = model.predict(X)
        ev = evaluate(labels, preds, CLASSES)
        self.assertGreater(ev.macro_f1, 0)
        self.assertGreater(ev.accuracy, 0)
        self.assertGreater(len(ev.per_class_metrics), 0)


if __name__ == "__main__":
    unittest.main()
