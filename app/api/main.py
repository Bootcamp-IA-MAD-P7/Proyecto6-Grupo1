"""FastAPI application factory for the prediction service."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api.config import get_settings
from app.api.errors import register_exception_handlers
from app.api.predictors.baseline import BaselinePredictor
from app.api.predictors.mock import MockPredictor
from app.api.routes.health import router as health_router
from app.api.routes.predictions import router as predictions_router
from app.api.services.prediction_service import PredictionService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Load model at startup, clean up at shutdown."""
    settings = get_settings()

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


def create_app() -> FastAPI:
    """Build and return the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Complaint Routing Prediction Service",
        version=settings.service_version,
        description=(
            "Backend service for CFPB complaint classification. "
            "Serves predictions from the trained baseline model."
        ),
        lifespan=lifespan,
    )

    # Register routes
    app.include_router(predictions_router, prefix="/api/v1")
    app.include_router(health_router, prefix="/api/v1")

    # Register error handlers
    register_exception_handlers(app)

    return app


app = create_app()
