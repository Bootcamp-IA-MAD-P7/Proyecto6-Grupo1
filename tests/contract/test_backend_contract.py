"""Contract tests: validate backend responses against docs/api/openapi.json.

These tests verify that the running service produces responses conforming
to the OpenAPI contract. All test data is synthetic — no CFPB narratives.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import joblib
import polars as pl
from fastapi.testclient import TestClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from app.api.config import get_settings
from app.api.main import create_app
from app.api.predictors.baseline import BaselinePredictor
from app.api.predictors.mock import MockPredictor
from app.api.services.prediction_service import PredictionService

ROOT = Path(__file__).resolve().parents[2]
OPENAPI = json.loads((ROOT / "docs" / "api" / "openapi.json").read_text(encoding="utf-8"))
TARGET = json.loads(
    (ROOT / "config" / "cfpb_target_contract.json").read_text(encoding="utf-8")
)

CANONICAL_CLASSES = set(TARGET["target"]["canonical_labels"])

# Synthetic test narratives (never real CFPB data)
VALID_NARRATIVE = "I noticed a duplicate charge on my account statement last week."
WHITESPACE_NARRATIVE = "   "
SYNTHETIC_FIXTURE = ROOT / "tests" / "fixtures" / "synthetic_baseline_data.csv"


def _create_test_client() -> TestClient:
    """Create a TestClient with MockPredictor wired in."""
    app = create_app()
    settings = get_settings()
    app.state.prediction_service = PredictionService(
        predictor=MockPredictor(),
        taxonomy_version=settings.taxonomy_version,
    )
    app.state.settings = settings
    return TestClient(app, raise_server_exceptions=False)


class PredictionResponseContractTests(unittest.TestCase):
    """Verify POST /api/v1/predictions responses match PredictionResponse schema."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = _create_test_client()

    def _get_prediction(self, narrative: str = VALID_NARRATIVE) -> dict:
        r = self.client.post(
            "/api/v1/predictions", json={"narrative": narrative}
        )
        self.assertEqual(r.status_code, 200)
        return r.json()

    def test_response_contains_all_required_fields(self) -> None:
        """R-002: Response has every field required by PredictionResponse."""
        schema = OPENAPI["components"]["schemas"]["PredictionResponse"]
        required_fields = set(schema["required"])
        data = self._get_prediction()
        self.assertTrue(
            required_fields.issubset(data.keys()),
            f"Missing fields: {required_fields - set(data.keys())}",
        )

    def test_predicted_class_is_canonical(self) -> None:
        """R-002: predicted_class belongs to CanonicalClass enum."""
        data = self._get_prediction()
        self.assertIn(data["predicted_class"], CANONICAL_CLASSES)

    def test_prediction_id_is_uuid_format(self) -> None:
        """R-002: prediction_id is a valid UUID string."""
        import uuid

        data = self._get_prediction()
        # Should not raise ValueError
        uuid.UUID(data["prediction_id"])

    def test_alternatives_have_valid_labels(self) -> None:
        """R-002: All alternatives have class_label from canonical classes."""
        data = self._get_prediction()
        for alt in data["alternatives"]:
            self.assertIn(alt["class_label"], CANONICAL_CLASSES)
            # Confidence is number or null
            if alt["confidence"] is not None:
                self.assertIsInstance(alt["confidence"], (int, float))
                self.assertGreaterEqual(alt["confidence"], 0)
                self.assertLessEqual(alt["confidence"], 1)

    def test_confidence_is_number_or_null(self) -> None:
        """R-002: confidence conforms to NullableConfidence."""
        data = self._get_prediction()
        conf = data["confidence"]
        if conf is not None:
            self.assertIsInstance(conf, (int, float))
            self.assertGreaterEqual(conf, 0)
            self.assertLessEqual(conf, 1)

    def test_review_required_is_boolean(self) -> None:
        """R-002: review_required is a boolean."""
        data = self._get_prediction()
        self.assertIsInstance(data["review_required"], bool)

    def test_review_reasons_are_valid_enum(self) -> None:
        """R-002: review_reasons values are from the contract enum."""
        valid_reasons = {
            "low_confidence",
            "confidence_unavailable",
            "out_of_domain",
            "language_policy",
            "service_policy",
        }
        data = self._get_prediction()
        for reason in data["review_reasons"]:
            self.assertIn(reason, valid_reasons)

    def test_model_version_is_non_empty_string(self) -> None:
        """R-002: model_version is a non-empty string."""
        data = self._get_prediction()
        self.assertIsInstance(data["model_version"], str)
        self.assertGreater(len(data["model_version"]), 0)

    def test_taxonomy_version_is_non_empty_string(self) -> None:
        """R-002: taxonomy_version is a non-empty string."""
        data = self._get_prediction()
        self.assertIsInstance(data["taxonomy_version"], str)
        self.assertGreater(len(data["taxonomy_version"]), 0)

    def test_created_at_is_iso_datetime(self) -> None:
        """R-002: created_at is an ISO 8601 datetime string."""
        from datetime import datetime

        data = self._get_prediction()
        # Should parse without error
        datetime.fromisoformat(data["created_at"])

    def test_warnings_is_list_of_strings(self) -> None:
        """R-002: warnings is an array of strings."""
        data = self._get_prediction()
        self.assertIsInstance(data["warnings"], list)
        for w in data["warnings"]:
            self.assertIsInstance(w, str)

    def test_response_does_not_echo_narrative(self) -> None:
        """R-002: Response body never contains the submitted narrative."""
        narrative = "This is a unique synthetic test narrative for echo check xyz123"
        data = self._get_prediction(narrative)
        response_str = json.dumps(data)
        self.assertNotIn(narrative, response_str)

    def test_mock_response_identified_correctly(self) -> None:
        """R-004: Mock mode sets model_version='mock-v0' and review_required=True."""
        data = self._get_prediction()
        self.assertEqual(data["model_version"], "mock-v0")
        self.assertTrue(data["review_required"])
        self.assertIn("confidence_unavailable", data["review_reasons"])


class ValidationErrorContractTests(unittest.TestCase):
    """Verify error responses conform to ErrorResponse schema."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = _create_test_client()

    def _assert_error_response(self, data: dict) -> None:
        """Verify data conforms to ErrorResponse schema."""
        required = {"error_code", "message", "request_id"}
        self.assertTrue(
            required.issubset(data.keys()),
            f"ErrorResponse missing: {required - set(data.keys())}",
        )
        self.assertIsInstance(data["error_code"], str)
        self.assertIsInstance(data["message"], str)
        self.assertIsInstance(data["request_id"], str)

    def test_whitespace_narrative_returns_422(self) -> None:
        """R-006: Whitespace-only narrative produces 422 ErrorResponse."""
        r = self.client.post(
            "/api/v1/predictions", json={"narrative": WHITESPACE_NARRATIVE}
        )
        self.assertEqual(r.status_code, 422)
        self._assert_error_response(r.json())

    def test_missing_narrative_returns_422(self) -> None:
        """R-006: Missing narrative field produces 422 ErrorResponse."""
        r = self.client.post("/api/v1/predictions", json={})
        self.assertEqual(r.status_code, 422)
        self._assert_error_response(r.json())

    def test_extra_field_returns_422(self) -> None:
        """R-006: Extra fields rejected (additionalProperties: false)."""
        r = self.client.post(
            "/api/v1/predictions",
            json={"narrative": "valid text", "extra_field": "bad"},
        )
        self.assertEqual(r.status_code, 422)
        self._assert_error_response(r.json())

    def test_client_request_id_too_long_returns_422(self) -> None:
        """R-006: client_request_id over 100 chars produces 422."""
        r = self.client.post(
            "/api/v1/predictions",
            json={"narrative": "valid text", "client_request_id": "x" * 101},
        )
        self.assertEqual(r.status_code, 422)
        self._assert_error_response(r.json())

    def test_narrative_over_contract_limit_returns_422_without_echo(self) -> None:
        """R-006: narratives over 5,000 characters are safely rejected."""
        narrative = "sensitive-oversized-input-" + ("x" * 5000)
        r = self.client.post("/api/v1/predictions", json={"narrative": narrative})
        self.assertEqual(r.status_code, 422)
        self._assert_error_response(r.json())
        self.assertNotIn(narrative, json.dumps(r.json()))

    def test_error_does_not_leak_narrative(self) -> None:
        """R-006: Error responses never contain the submitted narrative."""
        narrative = "sensitive unique narrative content abc789"
        r = self.client.post(
            "/api/v1/predictions",
            json={"narrative": narrative, "extra_field": "trigger_error"},
        )
        response_str = json.dumps(r.json())
        self.assertNotIn(narrative, response_str)

    def test_error_does_not_leak_internal_state(self) -> None:
        """R-006: Error messages don't contain paths or stack traces."""
        r = self.client.post("/api/v1/predictions", json={})
        data = r.json()
        # Should not contain file paths or traceback markers
        self.assertNotIn("Traceback", data["message"])
        self.assertNotIn(".py", data["message"])
        self.assertNotIn("\\", data["message"])


class HealthEndpointContractTests(unittest.TestCase):
    """Verify GET /api/v1/health conforms to HealthResponse schema."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = _create_test_client()

    def test_health_returns_200(self) -> None:
        """R-005: Health endpoint returns 200."""
        r = self.client.get("/api/v1/health")
        self.assertEqual(r.status_code, 200)

    def test_health_conforms_to_schema(self) -> None:
        """R-005: Response matches HealthResponse (status + service_version)."""
        r = self.client.get("/api/v1/health")
        data = r.json()
        self.assertIn("status", data)
        self.assertIn("service_version", data)
        self.assertIn(data["status"], ("ok", "degraded"))
        self.assertIsInstance(data["service_version"], str)

    def test_health_reports_degraded_in_mock_mode(self) -> None:
        """R-005: Health reports 'degraded' when no real model is loaded."""
        r = self.client.get("/api/v1/health")
        data = r.json()
        self.assertEqual(data["status"], "degraded")


class BaselinePredictorContractTests(unittest.TestCase):
    """Verify the real-predictor path with a synthetic serialized artifact."""

    @classmethod
    def setUpClass(cls) -> None:
        fixture = pl.read_csv(SYNTHETIC_FIXTURE)
        vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
        matrix = vectorizer.fit_transform(
            fixture["complaint_what_happened"].to_list()
        )
        model = LogisticRegression(
            solver="lbfgs", class_weight="balanced", max_iter=1000, random_state=42
        )
        model.fit(matrix, fixture["product_canonical"].to_list())

        cls.temp_dir = tempfile.TemporaryDirectory()
        artifact_path = Path(cls.temp_dir.name) / "synthetic_baseline.pkl"
        joblib.dump(
            {
                "vectorizer": vectorizer,
                "model": model,
                "config": {"C": 1.0, "max_features": 100},
            },
            artifact_path,
        )
        predictor = BaselinePredictor(artifact_path)
        app = create_app()
        settings = get_settings()
        app.state.prediction_service = PredictionService(
            predictor=predictor,
            taxonomy_version=settings.taxonomy_version,
        )
        app.state.settings = settings
        cls.client = TestClient(app, raise_server_exceptions=False)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_real_predictor_reports_healthy_and_returns_probabilities(self) -> None:
        narrative = "Synthetic verification input for a credit card billing issue."
        health = self.client.get("/api/v1/health")
        response = self.client.post("/api/v1/predictions", json={"narrative": narrative})

        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "ok")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertNotEqual(body["model_version"], "mock-v0")
        self.assertIsInstance(body["confidence"], float)
        self.assertIn(body["predicted_class"], CANONICAL_CLASSES)
        self.assertNotIn(narrative, json.dumps(body))


if __name__ == "__main__":
    unittest.main()
