"""Response schemas matching docs/api/openapi.json."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# The 11 canonical classes from config/cfpb_target_contract.json
CanonicalClass = Literal[
    "Checking or savings account",
    "Credit card",
    "Credit reporting or other personal consumer reports",
    "Debt collection",
    "Debt or credit management",
    "Money transfer, virtual currency, or money service",
    "Mortgage",
    "Payday loan, title loan, personal loan, or advance loan",
    "Prepaid card",
    "Student loan",
    "Vehicle loan or lease",
]

ReviewReason = Literal[
    "low_confidence",
    "confidence_unavailable",
    "out_of_domain",
    "language_policy",
    "service_policy",
]


class Alternative(BaseModel):
    """A single alternative class prediction."""

    model_config = ConfigDict(extra="forbid")

    class_label: CanonicalClass
    confidence: float | None = Field(ge=0, le=1, default=None)


class PredictionResponse(BaseModel):
    """Prediction output matching the PredictionResponse contract.

    The response never echoes the complaint narrative or recommends
    an operational queue.
    """

    model_config = ConfigDict(extra="forbid")

    prediction_id: str = Field(description="UUID identifying this prediction")
    predicted_class: CanonicalClass
    alternatives: list[Alternative]
    confidence: float | None = Field(ge=0, le=1, default=None)
    review_required: bool
    review_reasons: list[ReviewReason]
    model_version: str = Field(min_length=1)
    taxonomy_version: str = Field(min_length=1)
    created_at: datetime
    warnings: list[str]


class ErrorResponse(BaseModel):
    """Safe client-facing error without request content or internal details."""

    model_config = ConfigDict(extra="forbid")

    error_code: str
    message: str
    request_id: str
