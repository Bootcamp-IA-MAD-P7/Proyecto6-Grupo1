"""PostgreSQL-backed feedback repository for Docker/production environments.

Used when APP_DATABASE_URL is configured. Falls back to LocalFeedbackRepository
(SQLite) when not configured.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

import psycopg2

from app.api.schemas.feedback import FeedbackRecord
from app.api.services.feedback_repository import FeedbackRepositoryError

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS predictions (
    id TEXT PRIMARY KEY,
    predicted_class VARCHAR(100) NOT NULL,
    confidence DOUBLE PRECISION,
    review_required BOOLEAN NOT NULL DEFAULT TRUE,
    model_version VARCHAR(50) NOT NULL,
    taxonomy_version VARCHAR(10) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

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
);

INSERT INTO schema_migrations(version) VALUES ('1') ON CONFLICT DO NOTHING;
"""


class PostgresFeedbackRepository:
    """Persist feedback to PostgreSQL with minimum-privilege connection.

    Mirrors the LocalFeedbackRepository interface but uses PostgreSQL.
    Narratives are NEVER stored.
    """

    def __init__(self, database_url: str) -> None:
        try:
            self._conn = psycopg2.connect(database_url)
            self._conn.autocommit = True
            logger.info("PostgreSQL feedback repository connected.")
        except Exception as exc:
            raise FeedbackRepositoryError(
                "Could not connect to PostgreSQL."
            ) from exc

    def _initialize_schema(self) -> None:
        """Ensure tables exist (idempotent)."""
        with self._conn.cursor() as cur:
            cur.execute(_SCHEMA)

    @property
    def database_path(self) -> Path:
        """Compatibility with interface; returns a placeholder."""
        return Path("/db/postgresql")

    def initialize(self) -> None:
        """No-op; schema created at connect time."""
        pass

    def record_feedback(self, feedback: FeedbackRecord) -> None:
        """Store a validated feedback record."""
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO feedback_records (
                        feedback_id, prediction_id, model_version, taxonomy_version,
                        suggested_class, reviewed_class, decision, purpose,
                        created_at, expires_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (feedback_id) DO NOTHING
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
        except Exception as exc:
            raise FeedbackRepositoryError(
                "Feedback record could not be stored."
            ) from exc

    def save_prediction_metadata(
        self,
        prediction_id: str,
        predicted_class: str,
        confidence: float | None,
        review_required: bool,
        model_version: str,
        taxonomy_version: str,
        created_at: datetime,
    ) -> None:
        """Save prediction metadata. NEVER stores the narrative."""
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO predictions
                        (id, predicted_class, confidence, review_required,
                         model_version, taxonomy_version, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        prediction_id,
                        predicted_class,
                        confidence,
                        review_required,
                        model_version,
                        taxonomy_version,
                        created_at,
                    ),
                )
        except Exception as exc:
            logger.warning("Could not persist prediction metadata: %s", type(exc).__name__)

    def purge_expired_feedback(self, as_of: datetime) -> int:
        """Remove expired records."""
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM feedback_records WHERE expires_at <= %s",
                    (as_of.isoformat(),),
                )
                return cur.rowcount
        except Exception as exc:
            raise FeedbackRepositoryError(
                "Expired feedback could not be purged."
            ) from exc

    def list_feedback_summary(self) -> tuple[dict[str, str | int], ...]:
        """Return aggregate counts without individual records."""
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT model_version, suggested_class, decision, COUNT(*)
                    FROM feedback_records
                    GROUP BY model_version, suggested_class, decision
                    ORDER BY model_version, suggested_class, decision
                    """
                )
                rows = cur.fetchall()
        except Exception as exc:
            raise FeedbackRepositoryError(
                "Feedback summary is unavailable."
            ) from exc

        return tuple(
            {
                "model_version": model_version,
                "suggested_class": suggested_class,
                "decision": decision,
                "count": count,
            }
            for model_version, suggested_class, decision, count in rows
        )

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
