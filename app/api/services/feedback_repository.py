"""Isolated local persistence for already validated feedback records."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.api.schemas.feedback import FeedbackRecord


class FeedbackRepositoryError(RuntimeError):
    """Safe repository error that never includes record content."""


class LocalFeedbackRepository:
    """Persist minimised feedback only below the policy-controlled root."""

    _SCHEMA_VERSION = "1"
    _DATABASE_NAME = "feedback.sqlite3"

    def __init__(self, storage_directory: Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[3]
        policy_path = project_root / "config" / "claimvox_feedback_persistence_policy.json"
        try:
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            configured_root = policy["storage"]["allowed_root"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
            raise FeedbackRepositoryError("Feedback storage policy is unavailable.") from error

        self._allowed_root = (project_root / configured_root).resolve()
        requested_directory = storage_directory or self._allowed_root
        self._storage_directory = Path(requested_directory).resolve()
        try:
            self._storage_directory.relative_to(self._allowed_root)
        except ValueError as error:
            raise FeedbackRepositoryError("Feedback storage path is not allowed.") from error

        self._database_path = self._storage_directory / self._DATABASE_NAME

    @property
    def database_path(self) -> Path:
        """Return the controlled local database path without opening it."""
        return self._database_path

    def initialize(self) -> None:
        """Create the versioned local schema idempotently."""
        self._storage_directory.mkdir(parents=True, exist_ok=True)
        try:
            connection = sqlite3.connect(self._database_path)
            try:
                connection.execute("PRAGMA foreign_keys = ON")
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        version TEXT PRIMARY KEY
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS feedback_records (
                        feedback_id TEXT PRIMARY KEY,
                        prediction_id TEXT NOT NULL,
                        model_version TEXT NOT NULL,
                        taxonomy_version TEXT NOT NULL,
                        suggested_class TEXT NOT NULL,
                        reviewed_class TEXT,
                        decision TEXT NOT NULL,
                        purpose TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        expires_at TEXT NOT NULL
                    )
                    """
                )
                connection.execute(
                    "INSERT OR IGNORE INTO schema_migrations(version) VALUES (?)",
                    (self._SCHEMA_VERSION,),
                )
                connection.commit()
            finally:
                connection.close()
        except sqlite3.Error as error:
            raise FeedbackRepositoryError("Feedback storage is unavailable.") from error

    def record_feedback(self, feedback: FeedbackRecord) -> None:
        """Store an already validated minimum feedback record locally."""
        self.initialize()
        try:
            connection = sqlite3.connect(self._database_path)
            try:
                connection.execute(
                    """
                    INSERT INTO feedback_records (
                        feedback_id, prediction_id, model_version, taxonomy_version,
                        suggested_class, reviewed_class, decision, purpose,
                        created_at, expires_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(feedback.feedback_id),
                        str(feedback.prediction_id),
                        feedback.model_version,
                        feedback.taxonomy_version,
                        feedback.suggested_class,
                        feedback.reviewed_class,
                        feedback.decision,
                        feedback.purpose,
                        feedback.created_at.isoformat(),
                        feedback.expires_at.isoformat(),
                    ),
                )
                connection.commit()
            finally:
                connection.close()
        except sqlite3.Error as error:
            raise FeedbackRepositoryError("Feedback record could not be stored.") from error

    def purge_expired_feedback(self, as_of: datetime) -> int:
        """Remove only expired records and return their aggregate count."""
        if as_of.tzinfo is None or as_of.utcoffset() != timedelta(0):
            raise FeedbackRepositoryError("Purge time must be UTC.")

        self.initialize()
        try:
            connection = sqlite3.connect(self._database_path)
            try:
                cursor = connection.execute(
                    "DELETE FROM feedback_records WHERE expires_at <= ?",
                    (as_of.astimezone(timezone.utc).isoformat(),),
                )
                connection.commit()
                return cursor.rowcount
            finally:
                connection.close()
        except sqlite3.Error as error:
            raise FeedbackRepositoryError("Expired feedback could not be purged.") from error

    def list_feedback_summary(self) -> tuple[dict[str, str | int], ...]:
        """Return aggregate counts without identifiers or individual records."""
        self.initialize()
        try:
            connection = sqlite3.connect(self._database_path)
            try:
                rows = connection.execute(
                    """
                    SELECT model_version, suggested_class, decision, COUNT(*)
                    FROM feedback_records
                    GROUP BY model_version, suggested_class, decision
                    ORDER BY model_version, suggested_class, decision
                    """
                ).fetchall()
            finally:
                connection.close()
        except sqlite3.Error as error:
            raise FeedbackRepositoryError("Feedback summary is unavailable.") from error

        return tuple(
            {
                "model_version": model_version,
                "suggested_class": suggested_class,
                "decision": decision,
                "count": count,
            }
            for model_version, suggested_class, decision, count in rows
        )
