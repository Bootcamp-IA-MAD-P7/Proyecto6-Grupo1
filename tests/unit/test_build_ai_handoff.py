"""Tests for task-scoped AI handoff generation."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.documentation.build_ai_handoff import HandoffError, build_handoff


class BuildAIHandoffTests(unittest.TestCase):
    def test_builds_pack_for_existing_spec_and_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = build_handoff(
                "001",
                "T-004",
                ["reports/validation/cfpb_viability.md"],
                Path(directory),
            )
            content = output.read_text(encoding="utf-8")

        self.assertIn("AGENTS.md", content)
        self.assertIn(".specify/intent.md", content)
        self.assertIn("docs/project_management/delivery_levels.md", content)
        self.assertIn("ESS-01", content)
        self.assertIn("EXP-04", content)
        self.assertIn("specs/001-cfpb-target-contract/spec.md", content)
        self.assertIn("config/cfpb_target_contract.json", content)
        self.assertIn("reports/validation/cfpb_viability.md", content)
        self.assertIn("Work only on T-004", content)

    def test_includes_referenced_openapi_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = build_handoff("003", "T-006", output_directory=Path(directory))
            content = output.read_text(encoding="utf-8")

        self.assertIn("docs/api/openapi.json", content)
        self.assertIn("specs/003-complaint-routing-experience/spec.md", content)

    def test_rejects_unknown_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HandoffError, "does not exist"):
                build_handoff("001", "T-999", output_directory=Path(directory))

    def test_rejects_untracked_or_outside_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(HandoffError):
                build_handoff(
                    "001",
                    "T-004",
                    ["../outside.md"],
                    Path(directory),
                )

    def test_rejects_non_documental_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HandoffError, "format is not allowed"):
                build_handoff(
                    "001",
                    "T-004",
                    ["scripts/data/cfpb_viability.py"],
                    Path(directory),
                )

    def test_rejects_data_and_notebook_areas(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HandoffError, "area is not allowed"):
                build_handoff(
                    "001",
                    "T-004",
                    ["data/README.md"],
                    Path(directory),
                )

    def test_rejects_unsafe_output_filename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HandoffError, "safe Markdown filename"):
                build_handoff(
                    "001",
                    "T-004",
                    output_directory=Path(directory),
                    output_filename="../outside.md",
                )


if __name__ == "__main__":
    unittest.main()
