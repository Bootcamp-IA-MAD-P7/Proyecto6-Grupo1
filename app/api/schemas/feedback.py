"""Validated, privacy-minimised feedback domain records."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from app.api.schemas.response import CanonicalClass


FeedbackDecision = Literal["confirmed", "corrected", "not_actionable"]
FeedbackPurpose = Literal[
    "human_review_quality_assurance",
    "future_retraining_candidate",
]
PROHIBITED_FEEDBACK_FIELDS = frozenset(
    {
        "narrative",
        "client_request_id",
        "audio",
        "transcription",
        "name",
        "email",
        "account_number",
        "address",
        "ip_address",
        "http_headers",
        "free_text",
    }
)


class FeedbackValidationError(ValueError):
    """A safe validation error that never includes submitted field values."""


class FeedbackRecord(BaseModel):
    """Minimum local record allowed after an explicit human review."""

    model_config = ConfigDict(extra="forbid")

    feedback_id: UUID
    prediction_id: UUID
    model_version: str = Field(min_length=1)
    taxonomy_version: str = Field(min_length=1)
    suggested_class: CanonicalClass
    reviewed_class: CanonicalClass | None = None
    decision: FeedbackDecision
    purpose: FeedbackPurpose
    created_at: datetime
    expires_at: datetime

    @field_validator("model_version", "taxonomy_version")
    @classmethod
    def require_non_blank_version(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Version must not be blank.")
        return value

    @field_validator("created_at", "expires_at")
    @classmethod
    def require_utc_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("Timestamp must be UTC.")
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def require_future_expiry(self) -> "FeedbackRecord":
        if self.expires_at <= self.created_at:
            raise ValueError("Expiry must be after creation.")
        return self


def validate_feedback_payload(payload: Mapping[str, Any]) -> FeedbackRecord:
    """Create a feedback record while keeping validation errors content-free."""
    if PROHIBITED_FEEDBACK_FIELDS.intersection(payload):
        raise FeedbackValidationError("Feedback payload contains prohibited fields.")

    try:
        return FeedbackRecord.model_validate(payload)
    except ValidationError as error:
        raise FeedbackValidationError("Feedback payload is invalid.") from error
