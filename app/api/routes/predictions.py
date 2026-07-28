"""Prediction endpoint route."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.api.schemas.request import PredictionRequest
from app.api.schemas.response import PredictionResponse

router = APIRouter()


@router.post("/predictions", response_model=PredictionResponse)
async def create_prediction(
    body: PredictionRequest,
    request: Request,
) -> PredictionResponse:
    """Classify one complaint narrative.

    Accepts a PredictionRequest and returns a PredictionResponse using
    the loaded predictor (baseline model or mock fallback).
    """
    service = request.app.state.prediction_service
    return service.predict(
        narrative=body.narrative,
        client_request_id=body.client_request_id,
    )
