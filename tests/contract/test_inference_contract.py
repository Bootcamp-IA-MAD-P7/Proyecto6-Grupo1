"""Contract checks for the local ClaimVox prediction API."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OPENAPI = json.loads((ROOT / "docs/api/openapi.json").read_text(encoding="utf-8"))
TARGET = json.loads(
    (ROOT / "config/cfpb_target_contract.json").read_text(encoding="utf-8")
)


class InferenceContractTests(unittest.TestCase):
    def test_contract_is_openapi_31_and_locally_implemented(self) -> None:
        self.assertEqual(OPENAPI["openapi"], "3.1.0")
        prediction = OPENAPI["paths"]["/v1/predictions"]["post"]
        self.assertEqual(prediction["x-implementation-status"], "local-implemented")

    def test_api_classes_equal_the_target_contract(self) -> None:
        api_labels = OPENAPI["components"]["schemas"]["CanonicalClass"]["enum"]
        target_labels = TARGET["target"]["canonical_labels"]
        self.assertEqual(set(api_labels), set(target_labels))
        self.assertEqual(len(api_labels), 11)

    def test_request_has_narrative_as_only_model_input(self) -> None:
        prediction = OPENAPI["paths"]["/v1/predictions"]["post"]
        handling = prediction["x-data-handling"]
        request = OPENAPI["components"]["schemas"]["PredictionRequest"]
        self.assertEqual(handling["model_inputs"], ["narrative"])
        self.assertEqual(request["required"], ["narrative"])
        self.assertFalse(request["additionalProperties"])
        self.assertEqual(set(request["properties"]), {"narrative", "client_request_id"})
        self.assertEqual(request["properties"]["narrative"]["pattern"], r"\S")

    def test_response_does_not_echo_narrative_or_route(self) -> None:
        response = OPENAPI["components"]["schemas"]["PredictionResponse"]
        forbidden = {"narrative", "queue", "department", "feedback"}
        self.assertTrue(forbidden.isdisjoint(response["properties"]))
        self.assertFalse(response["additionalProperties"])

    def test_nullable_confidence_and_review_are_explicit(self) -> None:
        confidence = OPENAPI["components"]["schemas"]["NullableConfidence"]
        types = {option["type"] for option in confidence["oneOf"]}
        response = OPENAPI["components"]["schemas"]["PredictionResponse"]
        self.assertEqual(types, {"number", "null"})
        self.assertIn("review_required", response["required"])
        self.assertIn("confidence_unavailable", response["properties"]["review_reasons"]["items"]["enum"])
        self.assertTrue(
            any(
                rule.get("then", {}).get("properties", {}).get("review_required")
                == {"const": True}
                for rule in response["allOf"]
            )
        )

    def test_privacy_and_operational_errors_are_declared(self) -> None:
        prediction = OPENAPI["paths"]["/v1/predictions"]["post"]
        handling = prediction["x-data-handling"]
        self.assertEqual(handling["request_body_logging"], "prohibited")
        self.assertEqual(handling["narrative_persistence"], "none-by-default")
        self.assertTrue({"400", "422", "429", "503"}.issubset(prediction["responses"]))

    def test_feedback_endpoints_are_local_and_privacy_minimised(self) -> None:
        creation = OPENAPI["paths"]["/v1/feedback"]["post"]
        summary = OPENAPI["paths"]["/v1/feedback/summary"]["get"]
        request = OPENAPI["components"]["schemas"]["FeedbackCreateRequest"]
        summary_item = OPENAPI["components"]["schemas"]["FeedbackSummaryItem"]

        self.assertEqual(creation["x-implementation-status"], "local-implemented")
        self.assertEqual(summary["x-implementation-status"], "local-implemented")
        self.assertEqual(creation["x-data-handling"]["operation_scope"], "local-only")
        self.assertEqual(summary["x-data-handling"]["operation_scope"], "local-only")
        self.assertFalse(request["additionalProperties"])
        self.assertTrue(
            {"narrative", "identity", "free_text", "audio", "transcription", "probabilities"}
            .isdisjoint(request["properties"])
        )
        self.assertEqual(
            set(summary_item["properties"]),
            {"model_version", "suggested_class", "decision", "count"},
        )


if __name__ == "__main__":
    unittest.main()
