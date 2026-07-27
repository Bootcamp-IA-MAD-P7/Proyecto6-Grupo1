"""Abstract predictor interface (port for dependency injection)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class RawPrediction:
    """Result produced by a predictor implementation.

    This is an internal data structure; the service layer converts it
    to a PredictionResponse conforming to the API contract.
    """

    predicted_class: str
    confidence: float | None
    alternatives: list[dict] = field(default_factory=list)
    model_version: str = "unknown"


class PredictorInterface(ABC):
    """Abstract base for prediction implementations.

    Implementations include:
    - BaselinePredictor: loads the trained .pkl artifact.
    - MockPredictor: returns synthetic responses for dev/CI.
    - Future: RAGPredictor or ensemble predictors.
    """

    @abstractmethod
    def predict(self, narrative: str) -> RawPrediction:
        """Produce a classification for the given narrative text."""

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the predictor is ready to serve real predictions."""

    @property
    @abstractmethod
    def model_version(self) -> str:
        """Return the version identifier of the loaded model."""
