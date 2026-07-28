"""Prediction service: orchestrates predictor and builds PredictionResponse."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.api.predictors.base import PredictorInterface
from app.api.schemas.response import (
    Alternative,
    PredictionResponse,
    ReviewReason,
)


class PredictionService:
    """Orchestrates the prediction flow.

    Calls the injected predictor, assigns metadata, and builds a
    contract-compliant PredictionResponse.
    """

    def __init__(
        self,
        predictor: PredictorInterface,
        taxonomy_version: str = "1.0",
    ) -> None:
        self.predictor = predictor
        self.taxonomy_version = taxonomy_version

    def predict(
        self,
        narrative: str,
        client_request_id: str | None = None,
    ) -> PredictionResponse:
        """Run prediction and build the API response.

        The narrative is passed to the predictor for vectorization only.
        It is never stored, logged, or included in the response.
        """
        raw = self.predictor.predict(narrative)

        # Determine review state
        review_reasons: list[ReviewReason] = []
        review_required = False

        if raw.confidence is None:
            review_required = True
            review_reasons.append("confidence_unavailable")
        elif raw.confidence < 0.5:
            review_required = True
            review_reasons.append("low_confidence")

        # Build warnings
        warnings: list[str] = []
        if not self.predictor.is_available():
            warnings.append(
                "Prediction generated in mock mode. "
                "No trained model is loaded."
            )
            review_required = True
            if "service_policy" not in review_reasons:
                review_reasons.append("service_policy")

        # Build alternatives
        alternatives = [
            Alternative(
                class_label=alt["class_label"],
                confidence=alt.get("confidence"),
            )
            for alt in raw.alternatives
        ]

        return PredictionResponse(
            prediction_id=str(uuid.uuid4()),
            predicted_class=raw.predicted_class,
            alternatives=alternatives,
            confidence=raw.confidence,
            review_required=review_required,
            review_reasons=review_reasons,
            model_version=raw.model_version,
            taxonomy_version=self.taxonomy_version,
            created_at=datetime.now(timezone.utc),
            warnings=warnings,
        )
