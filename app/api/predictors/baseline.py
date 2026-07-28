"""Baseline predictor: loads the trained TF-IDF + LogisticRegression artifact."""

from __future__ import annotations

import logging
from pathlib import Path

import joblib
import numpy as np

from app.api.predictors.base import PredictorInterface, RawPrediction

logger = logging.getLogger(__name__)


class BaselinePredictor(PredictorInterface):
    """Loads models/cfpb_baseline.pkl and produces real predictions.

    The artifact is a joblib dict with keys: vectorizer, model, config.
    """

    def __init__(self, model_path: Path) -> None:
        """Load the artifact from the given path.

        Raises:
            FileNotFoundError: If the artifact file does not exist.
            Exception: If the artifact cannot be loaded or is malformed.
        """
        if not model_path.exists():
            raise FileNotFoundError(f"Model artifact not found: {model_path}")

        artifact = joblib.load(model_path)

        if not isinstance(artifact, dict):
            raise ValueError("Artifact is not a dict with vectorizer/model/config.")

        self._vectorizer = artifact["vectorizer"]
        self._model = artifact["model"]
        self._config = artifact.get("config", {})
        self._classes: list[str] = list(self._model.classes_)
        self._model_version = self._build_version_string()

        logger.info(
            "BaselinePredictor loaded: %d classes, version=%s",
            len(self._classes),
            self._model_version,
        )

    def _build_version_string(self) -> str:
        """Build a version identifier from the model config."""
        c_val = self._config.get("C", "?")
        max_feat = self._config.get("max_features", "?")
        return f"baseline-lr-C{c_val}-f{max_feat}"

    def predict(self, narrative: str) -> RawPrediction:
        """Vectorize the narrative and predict using the trained model."""
        # Vectorize (do not log the narrative content)
        X = self._vectorizer.transform([narrative])

        # Get probabilities
        probas = self._model.predict_proba(X)[0]

        # Sort by confidence descending
        sorted_indices = np.argsort(probas)[::-1]
        top_idx = sorted_indices[0]

        predicted_class = self._classes[top_idx]
        confidence = float(probas[top_idx])

        # Build alternatives (all classes sorted by probability)
        alternatives = [
            {
                "class_label": self._classes[idx],
                "confidence": float(probas[idx]),
            }
            for idx in sorted_indices[1:]  # Exclude the top prediction
        ]

        return RawPrediction(
            predicted_class=predicted_class,
            confidence=confidence,
            alternatives=alternatives,
            model_version=self._model_version,
        )

    def is_available(self) -> bool:
        """Baseline predictor is always available once loaded."""
        return True

    @property
    def model_version(self) -> str:
        """Return the baseline model version identifier."""
        return self._model_version
