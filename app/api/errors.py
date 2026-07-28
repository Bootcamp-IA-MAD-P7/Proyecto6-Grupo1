"""Exception handlers that map errors to safe ErrorResponse format."""

from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.schemas.response import ErrorResponse


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the app."""

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> ErrorResponse:
        """Handle Pydantic/FastAPI validation errors without leaking details."""
        from fastapi.responses import JSONResponse

        body = ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="The request body does not conform to the expected schema.",
            request_id=str(uuid.uuid4()),
        )
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> ErrorResponse:
        """Handle HTTP exceptions with safe error responses."""
        from fastapi.responses import JSONResponse

        error_codes = {
            400: "BAD_REQUEST",
            422: "VALIDATION_ERROR",
            404: "NOT_FOUND",
            429: "RATE_LIMITED",
            503: "SERVICE_UNAVAILABLE",
        }

        body = ErrorResponse(
            error_code=error_codes.get(exc.status_code, "INTERNAL_ERROR"),
            message=str(exc.detail) if exc.detail else "An error occurred.",
            request_id=str(uuid.uuid4()),
        )
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> ErrorResponse:
        """Catch-all handler. Never exposes stack trace or internal state."""
        from fastapi.responses import JSONResponse

        body = ErrorResponse(
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred.",
            request_id=str(uuid.uuid4()),
        )
        return JSONResponse(status_code=500, content=body.model_dump())
