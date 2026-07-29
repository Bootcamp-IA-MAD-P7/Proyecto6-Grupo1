"""Synthetic tests for the explicit local feedback flow."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import get_args
from unittest.mock import patch
from uuid import UUID

from fastapi.testclient import TestClient

from app.api.config import Settings
from app.api.main import create_app
from app.api.schemas.feedback import FeedbackCreateRequest, FeedbackRecord
from app.api.services.feedback_repository import LocalFeedbackRepository


CANONICAL_CLASS = get_args(FeedbackCreateRequest.model_fields["suggested_class"].annotation)[0]


def feedback_request() -> dict[str, str]:
    return {
        "prediction_id": "00000000-0000-4000-8000-000000000001",
        "model_version": "synthetic-baseline-1",
        "taxonomy_version": "1.0",
        "suggested_class": CANONICAL_CLASS,
        "decision": "confirmed",
        "purpose": "human_review_quality_assurance",
    }


class FeedbackOperationalFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        allowed_root = project_root / "data" / "local" / "feedback"
        allowed_root.mkdir(parents=True, exist_ok=True)
        self.temporary_directory = tempfile.TemporaryDirectory(dir=allowed_root)
        self.repository = LocalFeedbackRepository(Path(self.temporary_directory.name))
        self.app = create_app(Settings())
        self.prediction_service_before_feedback = object()
        self.app.state.prediction_service = self.prediction_service_before_feedback

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _client(self) -> TestClient:
        return TestClient(self.app, raise_server_exceptions=False)

    def test_creates_conforming_feedback_without_altering_prediction_service(self) -> None:
        with patch("app.api.main.LocalFeedbackRepository", return_value=self.repository):
            response = self._client().post("/api/v1/feedback", json=feedback_request())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"status": "recorded"})
        self.assertIs(self.app.state.prediction_service, self.prediction_service_before_feedback)

    def test_rejects_sensitive_extra_field_without_echoing_its_value(self) -> None:
        secret = "synthetic-sensitive-value-must-not-appear"
        request = feedback_request() | {"free_text": secret}

        with patch("app.api.main.LocalFeedbackRepository", return_value=self.repository):
            response = self._client().post("/api/v1/feedback", json=request)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error_code"], "VALIDATION_ERROR")
        self.assertNotIn(secret, json.dumps(response.json()))

    def test_summary_purges_expired_feedback_and_returns_aggregates_only(self) -> None:
        created_at = datetime(2026, 7, 1, tzinfo=timezone.utc)
        self.repository.record_feedback(
            FeedbackRecord(
                feedback_id=UUID("00000000-0000-4000-8000-000000000010"),
                prediction_id=UUID("00000000-0000-4000-8000-000000000011"),
                model_version="expired-model",
                taxonomy_version="1.0",
                suggested_class=CANONICAL_CLASS,
                decision="confirmed",
                purpose="human_review_quality_assurance",
                created_at=created_at,
                expires_at=created_at + timedelta(days=1),
            )
        )
        self.repository.record_feedback(
            FeedbackRecord(
                feedback_id=UUID("00000000-0000-4000-8000-000000000012"),
                prediction_id=UUID("00000000-0000-4000-8000-000000000013"),
                model_version="current-model",
                taxonomy_version="1.0",
                suggested_class=CANONICAL_CLASS,
                decision="confirmed",
                purpose="future_retraining_candidate",
                created_at=created_at,
                expires_at=datetime(2099, 1, 1, tzinfo=timezone.utc),
            )
        )

        with patch("app.api.main.LocalFeedbackRepository", return_value=self.repository):
            response = self._client().get("/api/v1/feedback/summary")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "items": [
                    {
                        "model_version": "current-model",
                        "suggested_class": CANONICAL_CLASS,
                        "decision": "confirmed",
                        "count": 1,
                    }
                ]
            },
        )
        serialized = json.dumps(response.json())
        self.assertNotIn("feedback_id", serialized)
        self.assertNotIn("prediction_id", serialized)
        self.assertNotIn("expired-model", serialized)


if __name__ == "__main__":
    unittest.main()
