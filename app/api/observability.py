"""Privacy-preserving technical events for the local prediction API."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from app.api.predictors.base import PredictorInterface
from app.api.schemas.response import PredictionResponse

event_logger = logging.getLogger("claimvox.api.events")


def emit_prediction_completed(
    *,
    elapsed_seconds: float,
    predictor: PredictorInterface,
    response: PredictionResponse,
) -> None:
    """Emit an aggregate technical event without request or user information."""
    event = {
        "event": "prediction_completed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "duration_ms_rounded": int(round(elapsed_seconds * 100) * 10),
        "status_code": 200,
        "predictor_mode": "real" if predictor.is_available() else "mock",
        "model_version": response.model_version,
        "human_review_required": response.review_required,
    }
    event_logger.info("%s", json.dumps(event, sort_keys=True))
