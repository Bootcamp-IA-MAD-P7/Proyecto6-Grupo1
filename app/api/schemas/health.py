"""Health response schema matching docs/api/openapi.json."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Non-sensitive service health status."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "degraded"]
    service_version: str
