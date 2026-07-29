"""Local use case for explicit, privacy-minimised human feedback."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from app.api.schemas.feedback import (
    FeedbackCreateRequest,
    FeedbackRecord,
    FeedbackSummaryItem,
    FeedbackSummaryResponse,
)
from app.api.services.feedback_repository import LocalFeedbackRepository


class FeedbackServiceError(RuntimeError):
    """Safe feedback use-case error without submitted content."""


class FeedbackService:
    """Create validated feedback records after an explicit human action."""

    def __init__(self, repository: LocalFeedbackRepository) -> None:
        self._repository = repository
        self._retention_days = self._load_retention_days()

    @staticmethod
    def _load_retention_days() -> int:
        project_root = Path(__file__).resolve().parents[3]
        policy_path = project_root / "config" / "claimvox_feedback_persistence_policy.json"
        try:
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            retention_days = policy["retention"]["default_days"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
            raise FeedbackServiceError("Feedback retention policy is unavailable.") from error

        if not isinstance(retention_days, int) or retention_days <= 0:
            raise FeedbackServiceError("Feedback retention policy is invalid.")
        return retention_days

    def create_feedback(
        self,
        request: FeedbackCreateRequest,
        *,
        created_at: datetime | None = None,
    ) -> None:
        """Persist approved metadata without affecting the prediction path."""
        timestamp = created_at or datetime.now(timezone.utc)
        if timestamp.tzinfo is None or timestamp.utcoffset() != timedelta(0):
            raise FeedbackServiceError("Feedback creation time must be UTC.")

        record = FeedbackRecord(
            feedback_id=uuid4(),
            prediction_id=request.prediction_id,
            model_version=request.model_version,
            taxonomy_version=request.taxonomy_version,
            suggested_class=request.suggested_class,
            reviewed_class=request.reviewed_class,
            decision=request.decision,
            purpose=request.purpose,
            created_at=timestamp.astimezone(timezone.utc),
            expires_at=timestamp.astimezone(timezone.utc)
            + timedelta(days=self._retention_days),
        )
        self._repository.record_feedback(record)

    def get_summary(
        self,
        *,
        as_of: datetime | None = None,
    ) -> FeedbackSummaryResponse:
        """Purge expired records and return privacy-minimised aggregates only."""
        timestamp = as_of or datetime.now(timezone.utc)
        if timestamp.tzinfo is None or timestamp.utcoffset() != timedelta(0):
            raise FeedbackServiceError("Feedback summary time must be UTC.")

        self._repository.purge_expired_feedback(timestamp.astimezone(timezone.utc))
        items = [
            FeedbackSummaryItem.model_validate(item)
            for item in self._repository.list_feedback_summary()
        ]
        return FeedbackSummaryResponse(items=items)
