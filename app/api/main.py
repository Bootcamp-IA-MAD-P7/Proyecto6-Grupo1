"""FastAPI application factory for the prediction service."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.config import Settings, get_settings
from app.api.errors import register_exception_handlers
from app.api.predictors.baseline import BaselinePredictor
from app.api.predictors.mock import MockPredictor
from app.api.routes.health import router as health_router
from app.api.routes.predictions import router as predictions_router
from app.api.security import LocalRateLimiter
from app.api.services.prediction_service import PredictionService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Load model at startup, clean up at shutdown."""
    settings: Settings = app.state.bootstrap_settings

    # Attempt to load the baseline artifact
    try:
        predictor = BaselinePredictor(model_path=settings.model_path)
        logger.info(
            "Baseline predictor loaded successfully (version: %s)",
            predictor.model_version,
        )
    except Exception as exc:
        logger.warning(
            "Could not load baseline artifact from %s: %s. Starting in mock mode.",
            settings.model_path,
            type(exc).__name__,
        )
        predictor = MockPredictor()

    # Wire the prediction service
    app.state.prediction_service = PredictionService(
        predictor=predictor,
        taxonomy_version=settings.taxonomy_version,
    )
    app.state.settings = settings

    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and return the FastAPI application."""
    settings = settings or get_settings()

    app = FastAPI(
        title="Complaint Routing Prediction Service",
        version=settings.service_version,
        description=(
            "Backend service for CFPB complaint classification. "
            "Serves predictions from the trained baseline model."
        ),
        lifespan=lifespan,
    )
    app.state.bootstrap_settings = settings
    app.state.rate_limiter = LocalRateLimiter(settings.prediction_rate_limit_per_minute)

    @app.middleware("http")
    async def add_local_api_security_headers(request, call_next):
        """Apply non-deployment-specific response protections to API replies."""
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    if settings.local_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(settings.local_cors_origins),
            allow_credentials=False,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Content-Type"],
        )

    # Register routes
    app.include_router(predictions_router, prefix="/api/v1")
    app.include_router(health_router, prefix="/api/v1")

    # Register error handlers
    register_exception_handlers(app)

    return app


app = create_app()
