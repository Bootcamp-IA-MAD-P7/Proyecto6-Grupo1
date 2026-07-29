"""Synthetic tests for the local CFPB model quality gate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import joblib
import numpy as np

from scripts.quality.cfpb_model_quality_gate import (
    ModelQualityGateError,
    validate_model_artifact,
)


ROOT = Path(__file__).resolve().parents[2]
MODELS_ROOT = ROOT / "models"
CANONICAL_LABELS = (
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
)


class SyntheticVectorizer:
    """Minimal test double; it never stores or emits the synthetic input."""

    def transform(self, inputs: list[str]) -> list[int]:
        return list(range(len(inputs)))


class SyntheticModel:
    def __init__(self, classes: tuple[str, ...], probability_columns: int | None = None):
        self.classes_ = np.asarray(classes)
        self._probability_columns = probability_columns or len(classes)

    def predict_proba(self, rows: list[int]) -> np.ndarray:
        return np.full(
            (len(rows), self._probability_columns),
            1 / self._probability_columns,
        )


class CFPBModelQualityGateTests(unittest.TestCase):
    def setUp(self) -> None:
        MODELS_ROOT.mkdir(exist_ok=True)
        self._temporary_directory = tempfile.TemporaryDirectory(dir=MODELS_ROOT)
        self.artifact_path = Path(self._temporary_directory.name) / "synthetic.pkl"

    def tearDown(self) -> None:
        self._temporary_directory.cleanup()

    def _write_artifact(
        self,
        *,
        classes: tuple[str, ...] = CANONICAL_LABELS,
        probability_columns: int | None = None,
        artifact_path: Path | None = None,
    ) -> Path:
        target = artifact_path or self.artifact_path
        joblib.dump(
            {
                "vectorizer": SyntheticVectorizer(),
                "model": SyntheticModel(classes, probability_columns),
            },
            target,
        )
        return target

    def _validate(self, artifact_path: Path, *, features: tuple[str, ...] = ("complaint_what_happened",)):
        return validate_model_artifact(
            artifact_path,
            allowed_root=MODELS_ROOT,
            feature_columns=features,
            allowed_feature_columns=("complaint_what_happened",),
            canonical_labels=CANONICAL_LABELS,
            synthetic_inputs=("synthetic quality gate input",),
        )

    def test_accepts_a_conforming_synthetic_artifact(self) -> None:
        result = self._validate(self._write_artifact())

        self.assertTrue(result["synthetic_inference_valid"])
        self.assertEqual(result["probability_shape"], [1, 11])

    def test_rejects_an_artifact_outside_models(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            outside_path = self._write_artifact(artifact_path=Path(outside) / "synthetic.pkl")

            with self.assertRaisesRegex(ModelQualityGateError, "outside the controlled root"):
                self._validate(outside_path)

    def test_rejects_a_prohibited_feature_contract(self) -> None:
        with self.assertRaisesRegex(ModelQualityGateError, "feature contract"):
            self._validate(self._write_artifact(), features=("company",))

    def test_rejects_noncanonical_model_classes(self) -> None:
        invalid_classes = CANONICAL_LABELS[:-1] + ("Unapproved class",)

        with self.assertRaisesRegex(ModelQualityGateError, "classes do not match"):
            self._validate(self._write_artifact(classes=invalid_classes))

    def test_rejects_an_invalid_probability_shape(self) -> None:
        with self.assertRaisesRegex(ModelQualityGateError, "invalid shape"):
            self._validate(self._write_artifact(probability_columns=10))


if __name__ == "__main__":
    unittest.main()
