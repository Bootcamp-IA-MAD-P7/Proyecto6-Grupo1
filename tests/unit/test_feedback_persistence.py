"""Synthetic tests for governed local feedback persistence."""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import get_args
from uuid import UUID

from app.api.schemas.feedback import FeedbackValidationError, FeedbackRecord, validate_feedback_payload
from app.api.services.feedback_repository import FeedbackRepositoryError, LocalFeedbackRepository


CANONICAL_CLASS = get_args(FeedbackRecord.model_fields["suggested_class"].annotation)[0]


def feedback_payload() -> dict[str, object]:
    created_at = datetime(2026, 7, 29, tzinfo=timezone.utc)
    return {
        "feedback_id": UUID("00000000-0000-0000-0000-000000000001"),
        "prediction_id": UUID("00000000-0000-0000-0000-000000000002"),
        "model_version": "baseline-1",
        "taxonomy_version": "1.0",
        "suggested_class": CANONICAL_CLASS,
        "reviewed_class": CANONICAL_CLASS,
        "decision": "confirmed",
        "purpose": "human_review_quality_assurance",
        "created_at": created_at,
        "expires_at": created_at + timedelta(days=30),
    }


class FeedbackPersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        self.allowed_root = project_root / "data" / "local" / "feedback"
        self.allowed_root.mkdir(parents=True, exist_ok=True)
        self.temporary_directory = tempfile.TemporaryDirectory(dir=self.allowed_root)
        self.repository = LocalFeedbackRepository(Path(self.temporary_directory.name))

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_records_a_conforming_synthetic_feedback_item(self) -> None:
        feedback = validate_feedback_payload(feedback_payload())

        self.repository.record_feedback(feedback)

        connection = sqlite3.connect(self.repository.database_path)
        try:
            count = connection.execute("SELECT COUNT(*) FROM feedback_records").fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(count, 1)

    def test_rejects_a_noncanonical_class(self) -> None:
        payload = feedback_payload()
        payload["suggested_class"] = "non-canonical-class"

        with self.assertRaises(FeedbackValidationError):
            validate_feedback_payload(payload)

    def test_rejects_a_sensitive_field_without_echoing_its_value(self) -> None:
        payload = feedback_payload()
        payload["free_text"] = ""

        with self.assertRaises(FeedbackValidationError) as context:
            validate_feedback_payload(payload)
        self.assertNotIn("free_text", str(context.exception))

    def test_rejects_a_non_utc_timestamp(self) -> None:
        payload = feedback_payload()
        payload["created_at"] = datetime(2026, 7, 29)

        with self.assertRaises(FeedbackValidationError):
            validate_feedback_payload(payload)

    def test_rejects_a_storage_path_outside_the_controlled_root(self) -> None:
        with tempfile.TemporaryDirectory() as external_directory:
            with self.assertRaises(FeedbackRepositoryError):
                LocalFeedbackRepository(Path(external_directory))

    def test_initialization_is_idempotent_for_the_same_schema(self) -> None:
        self.repository.initialize()
        self.repository.initialize()

        connection = sqlite3.connect(self.repository.database_path)
        try:
            count = connection.execute("SELECT COUNT(*) FROM schema_migrations").fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
