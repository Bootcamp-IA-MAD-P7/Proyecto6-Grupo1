"""Prediction endpoint route."""

from __future__ import annotations

from time import perf_counter

from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.auth import verify_token
from app.api.observability import emit_prediction_completed
from app.api.schemas.request import PredictionRequest
from app.api.schemas.response import PredictionResponse

router = APIRouter()


@router.post("/predictions", response_model=PredictionResponse)
async def create_prediction(
    body: PredictionRequest,
    request: Request,
    _user: str = Depends(verify_token),
) -> PredictionResponse:
    """Classify one complaint narrative.

    Accepts a PredictionRequest and returns a PredictionResponse using
    the loaded predictor (baseline model or mock fallback).
    """
    service = request.app.state.prediction_service
    settings = request.app.state.settings

    if len(body.narrative) > settings.max_narrative_characters:
        raise HTTPException(
            status_code=422,
            detail="The narrative exceeds the active local length limit.",
        )

    temporary_client_key = request.client.host if request.client else "local-unknown"
    if not request.app.state.rate_limiter.allow(temporary_client_key):
        raise HTTPException(
            status_code=429,
            detail="Prediction request frequency limit reached. Please retry later.",
        )

    started_at = perf_counter()
    response = service.predict(
        narrative=body.narrative,
        client_request_id=body.client_request_id,
    )
    emit_prediction_completed(
        elapsed_seconds=perf_counter() - started_at,
        predictor=service.predictor,
        response=response,
    )
    return response
