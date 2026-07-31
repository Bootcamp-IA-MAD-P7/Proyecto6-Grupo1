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


@router.get("/status")
async def get_status(request: Request) -> dict:
    """Extended status for the admin dashboard."""
    service = request.app.state.prediction_service
    settings = request.app.state.settings
    pg_repo = getattr(request.app.state, "postgres_repository", None)

    return {
        "service_health": "ok" if service.predictor.is_available() else "degraded",
        "service_version": settings.service_version,
        "model_version": service.predictor.model_version,
        "database_connected": pg_repo is not None,
        "database_type": "postgresql" if pg_repo else "none",
    }
