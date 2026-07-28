"""Health endpoint route."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.api.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def get_health(request: Request) -> HealthResponse:
    """Return non-sensitive service health status.

    Reports 'ok' when the baseline predictor is loaded,
    'degraded' when operating in mock mode.
    """
    service = request.app.state.prediction_service
    settings = request.app.state.settings

    status = "ok" if service.predictor.is_available() else "degraded"

    return HealthResponse(
        status=status,
        service_version=settings.service_version,
    )
