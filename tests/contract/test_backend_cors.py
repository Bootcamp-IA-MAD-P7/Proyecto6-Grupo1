"""Contract tests for the deliberately narrow local CORS policy."""

from __future__ import annotations

import unittest

from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.api.config import Settings
from app.api.main import create_app


class BackendCorsContractTests(unittest.TestCase):
    """Verify local origins are opt-in and never credentialed or wildcarded."""

    def test_default_configuration_does_not_grant_cross_origin_access(self) -> None:
        app = create_app(Settings())

        with TestClient(app) as client:
            response = client.options(
                "/api/v1/predictions",
                headers={
                    "Origin": "http://127.0.0.1:4173",
                    "Access-Control-Request-Method": "POST",
                },
            )

        self.assertNotIn("access-control-allow-origin", response.headers)

    def test_explicit_local_origin_is_granted_without_credentials(self) -> None:
        origin = "http://127.0.0.1:4173"
        app = create_app(Settings(cors_allowed_origins=origin))

        with TestClient(app) as client:
            response = client.options(
                "/api/v1/predictions",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "authorization,content-type",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["access-control-allow-origin"], origin)
        allowed_headers = response.headers["access-control-allow-headers"].lower()
        self.assertIn("authorization", allowed_headers)
        self.assertIn("content-type", allowed_headers)
        self.assertNotIn("access-control-allow-credentials", response.headers)

    def test_wildcard_and_non_local_origins_are_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            Settings(cors_allowed_origins="*")

        with self.assertRaises(ValidationError):
            Settings(cors_allowed_origins="https://claimvox.example")

    def test_api_responses_include_local_security_headers(self) -> None:
        app = create_app(Settings())

        with TestClient(app) as client:
            response = client.get("/api/v1/health")

        self.assertEqual(response.headers["cache-control"], "no-store")
        self.assertEqual(response.headers["referrer-policy"], "no-referrer")
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")
        self.assertEqual(response.headers["x-frame-options"], "DENY")


if __name__ == "__main__":
    unittest.main()
