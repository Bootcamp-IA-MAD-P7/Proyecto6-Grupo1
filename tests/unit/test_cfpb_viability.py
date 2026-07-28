from __future__ import annotations

import csv
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/data/cfpb_viability.py"
SPEC = importlib.util.spec_from_file_location("cfpb_viability", MODULE_PATH)
assert SPEC and SPEC.loader
cfpb_viability = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cfpb_viability)


def config() -> dict:
    return {
        "schema_version": "1.0",
        "source": {
            "api_url": "https://example.test/api/",
            "csv_url": "https://example.test/data.zip",
            "documentation_url": "https://example.test/docs",
        },
        "window": {
            "date_received_min": "2023-08-24",
            "date_received_max_exclusive": "2026-07-23",
        },
        "limits": {
            "api_page_size": 100,
            "api_sample_records_per_edge": 2,
            "max_api_response_bytes": 2048,
            "max_scanned_rows": 100,
        },
        "fields": {
            "complaint_id": ["Complaint ID", "complaint_id"],
            "date_received": ["Date received", "date_received"],
            "narrative": ["Consumer complaint narrative", "complaint_what_happened"],
            "target": ["Product", "product"],
        },
        "model_contract": {
            "allowed_inputs": ["complaint_what_happened"],
            "target": "product",
            "forbidden_inputs": ["product"],
        },
        "review_thresholds": {
            "minimum_classes": 3,
            "minimum_eligible_rows": 3,
            "minimum_rows_per_retained_class": 1,
            "majority_share_warning": 0.8,
            "pii_pattern_rate_warning": 0.5,
        },
    }


class CFPBViabilityTests(unittest.TestCase):
    def test_inspection_filters_window_and_never_returns_narratives(self) -> None:
        content = """Complaint ID,Date received,Consumer complaint narrative,Product
1,2023-08-23,Outside window,Mortgage
2,2023-08-24,My card was charged,Credit card
3,2024-01-10,Call me at 202-555-0182,Debt collection
4,2025-04-05,Duplicate text,Mortgage
5,2025-04-05,Duplicate text,Mortgage
6,2026-07-23,Outside exclusive maximum,Credit card
"""
        reader = csv.DictReader(io.StringIO(content))

        report = cfpb_viability.inspect_rows(iter(reader), reader.fieldnames, config())

        self.assertEqual(report["scan"]["eligible_rows"], 4)
        self.assertEqual(report["classes"]["count"], 3)
        self.assertEqual(report["quality"]["duplicate_narratives"], 1)
        self.assertEqual(report["privacy"]["pattern_match_counts"]["phone"], 1)
        self.assertEqual(report["privacy"]["records_with_any_pattern"], 1)
        serialized = json.dumps(report)
        self.assertNotIn("My card was charged", serialized)
        self.assertNotIn("202-555-0182", serialized)
        self.assertNotIn("Duplicate text", serialized)

    def test_missing_values_are_reported_without_becoming_eligible(self) -> None:
        content = """Complaint ID,Date received,Consumer complaint narrative,Product
,2024-01-01,Has no identifier,Mortgage
2,2024-01-01,,Credit card
3,2024-01-01,Has no target,
"""
        reader = csv.DictReader(io.StringIO(content))

        report = cfpb_viability.inspect_rows(iter(reader), reader.fieldnames, config())

        self.assertEqual(report["scan"]["rows_in_window"], 3)
        self.assertEqual(report["scan"]["eligible_rows"], 1)
        self.assertEqual(report["quality"]["missing"]["complaint_id"], 1)
        self.assertEqual(report["quality"]["missing"]["narrative"], 1)
        self.assertEqual(report["quality"]["missing"]["target"], 1)

    def test_contract_rejects_target_as_an_allowed_input(self) -> None:
        invalid = config()
        invalid["model_contract"]["allowed_inputs"] = [
            "complaint_what_happened",
            "product",
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaises(cfpb_viability.ContractError):
                cfpb_viability.load_config(path)

    def test_probe_url_freezes_the_window_and_limits_results(self) -> None:
        url = cfpb_viability.build_probe_url(config())

        self.assertIn("date_received_min=2023-08-24", url)
        self.assertIn("date_received_max=2026-07-23", url)
        self.assertIn("has_narrative=true", url)
        self.assertIn("size=1", url)

    def test_api_timestamp_is_parsed_as_received_date(self) -> None:
        parsed = cfpb_viability.parse_date("2023-08-24T00:00:47.000Z")

        self.assertEqual(parsed.isoformat(), "2023-08-24")

    def test_real_product_aggregation_shape_is_sanitized(self) -> None:
        payload = {
            "aggregations": {
                "product": {
                    "product": {
                        "buckets": [
                            {"key": "Credit card", "doc_count": 10},
                            {"key": "Mortgage", "doc_count": 5},
                        ]
                    }
                }
            }
        }

        buckets = cfpb_viability.extract_product_buckets(payload)

        self.assertEqual(
            buckets,
            [
                {"class": "Credit card", "count": 10},
                {"class": "Mortgage", "count": 5},
            ],
        )

    def test_sample_pagination_uses_page_breakpoint_contract(self) -> None:
        url = cfpb_viability.build_sample_url(
            config(), "created_date_asc", 100, page=2, search_after="123_456"
        )

        self.assertIn("page=2", url)
        self.assertIn("frm=100", url)
        self.assertIn("search_after=123_456", url)

        third_page = cfpb_viability.build_sample_url(
            config(), "created_date_asc", 100, page=3, search_after="789_012"
        )
        self.assertIn("frm=200", third_page)


if __name__ == "__main__":
    unittest.main()
