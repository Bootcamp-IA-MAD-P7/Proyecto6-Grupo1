"""Mock predictor for development and CI environments without model artifact."""

from __future__ import annotations

from app.api.predictors.base import PredictorInterface, RawPrediction

# Default mock class (first canonical label)
_MOCK_CLASS = "Checking or savings account"


class MockPredictor(PredictorInterface):
    """Returns a fixed synthetic prediction clearly identified as mock.

    Used when the baseline artifact is not available (CI, tests, first deploy).
    """

    def predict(self, narrative: str) -> RawPrediction:
        """Return a mock prediction with null confidence."""
        return RawPrediction(
            predicted_class=_MOCK_CLASS,
            confidence=None,
            alternatives=[],
            model_version=self.model_version,
        )

    def is_available(self) -> bool:
        """Mock predictor is never considered a 'real' available model."""
        return False

    @property
    def model_version(self) -> str:
        """Identify this as a mock response."""
        return "mock-v0"
