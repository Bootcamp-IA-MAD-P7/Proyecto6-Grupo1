"""FastAPI application factory for the prediction service."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.config import Settings, get_settings
from app.api.errors import register_exception_handlers
from app.api.predictors.baseline import BaselinePredictor
from app.api.predictors.mock import MockPredictor
from app.api.routes.health import router as health_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.auth import router as auth_router
from app.api.schemas.feedback import (
    FeedbackCreateRequest,
    FeedbackSummaryResponse,
)
from app.api.security import LocalRateLimiter
from app.api.services.feedback_repository import FeedbackRepositoryError, LocalFeedbackRepository
from app.api.services.feedback_service import FeedbackService, FeedbackServiceError
from app.api.services.postgres_feedback_repository import PostgresFeedbackRepository
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

    # Wire database repository (PostgreSQL when configured, local SQLite otherwise)
    if settings.database_url:
        try:
            pg_repo = PostgresFeedbackRepository(settings.database_url)
            app.state.postgres_repository = pg_repo
            logger.info("PostgreSQL repository connected for feedback persistence.")
        except Exception as exc:
            logger.warning(
                "Could not connect to PostgreSQL: %s. Feedback uses local SQLite only.",
                type(exc).__name__,
            )
            app.state.postgres_repository = None
    else:
        app.state.postgres_repository = None

    yield

    # Cleanup
    if app.state.postgres_repository:
        app.state.postgres_repository.close()


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

    @app.post(
        "/api/v1/feedback",
        status_code=status.HTTP_201_CREATED,
    )
    def create_local_feedback(request: FeedbackCreateRequest) -> dict[str, str]:
        """Persist one explicit local review without changing a prediction."""
        try:
            FeedbackService(LocalFeedbackRepository()).create_feedback(request)
        except (FeedbackRepositoryError, FeedbackServiceError) as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Local feedback is unavailable.",
            ) from error
        return {"status": "recorded"}

    @app.get(
        "/api/v1/feedback/summary",
        response_model=FeedbackSummaryResponse,
    )
    def get_local_feedback_summary() -> FeedbackSummaryResponse:
        """Read aggregate-only feedback without exposing individual records."""
        try:
            summary = FeedbackService(LocalFeedbackRepository()).get_summary()
        except (FeedbackRepositoryError, FeedbackServiceError, ValueError) as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Local feedback is unavailable.",
            ) from error
        return summary

    # Register routes
    app.include_router(predictions_router, prefix="/api/v1")
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")

    # Register error handlers
    register_exception_handlers(app)

    return app


app = create_app()
