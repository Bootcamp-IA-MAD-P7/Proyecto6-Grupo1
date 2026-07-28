"""PredictionRequest schema matching docs/api/openapi.json."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    """Incoming prediction request.

    Mirrors the PredictionRequest schema from docs/api/openapi.json.
    """

    model_config = ConfigDict(extra="forbid")

    narrative: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        pattern=r"\S",
        description=(
            "Complaint narrative. Clients must reject whitespace-only values "
            "and warn against unnecessary personal data."
        ),
    )
    client_request_id: str | None = Field(
        default=None,
        max_length=100,
        description="Optional technical correlation identifier; never a model feature.",
    )
