"""Contract tests for the environment-only JWT demonstration boundary."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api.config import Settings
from app.api.main import create_app


class DemoAuthBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.environment = {
            "APP_DEMO_USERNAME": "synthetic-reviewer",
            "APP_DEMO_PASSWORD": "synthetic-password",
            "APP_DEMO_ROLE": "admin",
            "APP_DEMO_NAME": "Synthetic reviewer",
        }

    def _client(self) -> TestClient:
        settings = Settings(model_path="models/missing-contract-artifact.pkl")
        return TestClient(create_app(settings))

    def test_protected_operations_reject_missing_bearer_token(self) -> None:
        with patch.dict(os.environ, self.environment, clear=True), self._client() as client:
            prediction = client.post(
                "/api/v1/predictions",
                json={"narrative": "Synthetic complaint text for contract testing."},
            )
            feedback = client.get("/api/v1/feedback/summary")

        self.assertEqual(prediction.status_code, 401)
        self.assertEqual(feedback.status_code, 401)

    def test_environment_login_issues_a_token_for_protected_operations(self) -> None:
        with patch.dict(os.environ, self.environment, clear=True), self._client() as client:
            login = client.post(
                "/api/v1/auth/login",
                json={
                    "username": self.environment["APP_DEMO_USERNAME"],
                    "password": self.environment["APP_DEMO_PASSWORD"],
                },
            )
            self.assertEqual(login.status_code, 200)
            token = login.json()["access_token"]
            summary = client.get(
                "/api/v1/feedback/summary",
                headers={"Authorization": f"Bearer {token}"},
            )

        self.assertEqual(summary.status_code, 200)
        self.assertEqual(set(summary.json()), {"items"})

    def test_login_rejects_unknown_credentials_without_echoing_password(self) -> None:
        secret = "synthetic-secret-that-must-not-be-echoed"
        with patch.dict(os.environ, self.environment, clear=True), self._client() as client:
            response = client.post(
                "/api/v1/auth/login",
                json={"username": "unknown", "password": secret},
            )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn(secret, response.text)


if __name__ == "__main__":
    unittest.main()
