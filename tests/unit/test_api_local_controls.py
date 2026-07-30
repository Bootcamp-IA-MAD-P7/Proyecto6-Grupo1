"""Unit tests for local API limits and privacy-safe technical events."""

from __future__ import annotations

import json
import unittest

from fastapi.testclient import TestClient

from app.api.config import Settings
from app.api.main import create_app
from app.api.observability import emit_prediction_completed
from app.api.predictors.mock import MockPredictor
from app.api.security import LocalRateLimiter
from app.api.services.prediction_service import PredictionService


class LocalRateLimiterTests(unittest.TestCase):
    """The limiter is temporary, bounded and configurable."""

    def test_rejects_requests_above_the_active_window(self) -> None:
        limiter = LocalRateLimiter(requests_per_minute=2, window_seconds=60)

        self.assertTrue(limiter.allow("local-client", now=0))
        self.assertTrue(limiter.allow("local-client", now=1))
        self.assertFalse(limiter.allow("local-client", now=2))
        self.assertTrue(limiter.allow("local-client", now=61))

    def test_uses_separate_temporary_keys(self) -> None:
        limiter = LocalRateLimiter(requests_per_minute=1, window_seconds=60)

        self.assertTrue(limiter.allow("first", now=0))
        self.assertTrue(limiter.allow("second", now=0))


class LocalApiPolicyTests(unittest.TestCase):
    """Verify configurable local policy without using real CFPB text."""

    def _client(self, rate_limit: int = 20) -> TestClient:
        settings = Settings(
            max_narrative_characters=50,
            prediction_rate_limit_per_minute=rate_limit,
        )
        app = create_app(settings)
        app.state.prediction_service = PredictionService(
            predictor=MockPredictor(), taxonomy_version=settings.taxonomy_version
        )
        app.state.settings = settings
        return TestClient(app, raise_server_exceptions=False)

    def _auth_headers(self) -> dict:
        from app.api.auth import create_access_token

        token = create_access_token("test-user")
        return {"Authorization": f"Bearer {token}"}

    def test_lower_configured_length_limit_returns_safe_validation_error(self) -> None:
        client = self._client()
        narrative = "private-synthetic-" + ("x" * 40)

        response = client.post(
            "/api/v1/predictions",
            json={"narrative": narrative},
            headers=self._auth_headers(),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error_code"], "VALIDATION_ERROR")
        self.assertNotIn(narrative, json.dumps(response.json()))

    def test_rate_limit_returns_contractual_safe_error(self) -> None:
        client = self._client(rate_limit=1)
        headers = self._auth_headers()

        first = client.post("/api/v1/predictions", json={"narrative": "synthetic input"}, headers=headers)
        second = client.post("/api/v1/predictions", json={"narrative": "synthetic input"}, headers=headers)

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.json()["error_code"], "RATE_LIMITED")
        self.assertNotIn("synthetic input", json.dumps(second.json()))

    def test_prediction_event_contains_only_approved_technical_fields(self) -> None:
        service = PredictionService(MockPredictor())
        response = service.predict("synthetic input that must never be logged")

        with self.assertLogs("claimvox.api.events", level="INFO") as captured:
            emit_prediction_completed(
                elapsed_seconds=0.123,
                predictor=service.predictor,
                response=response,
            )

        payload = json.loads(captured.output[0].split(":", 2)[-1])
        self.assertEqual(
            set(payload),
            {
                "event",
                "timestamp",
                "duration_ms_rounded",
                "status_code",
                "predictor_mode",
                "model_version",
                "human_review_required",
            },
        )
        serialized = json.dumps(payload)
        for prohibited in (
            "narrative",
            "synthetic input",
            "prediction_id",
            "confidence",
            "alternatives",
            "client_request_id",
            "ip",
            "user",
        ):
            self.assertNotIn(prohibited, serialized)


if __name__ == "__main__":
    unittest.main()
