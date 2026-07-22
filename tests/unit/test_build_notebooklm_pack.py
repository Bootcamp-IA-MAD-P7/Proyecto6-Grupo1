"""Tests for the curated NotebookLM source pack."""

from __future__ import annotations

import unittest

from scripts.documentation.build_notebooklm_pack import ROOT, source_paths


class BuildNotebookLMPackTests(unittest.TestCase):
    def test_includes_daily_and_customer_brief(self) -> None:
        relative_paths = {
            path.relative_to(ROOT).as_posix() for path in source_paths("2026-07-22")
        }

        self.assertIn(
            "docs/project_management/dailies/2026-07-22.md", relative_paths
        )
        self.assertIn(
            "docs/notebooklm/briefs/2026-07-22-client-project-status.md",
            relative_paths,
        )

    def test_customer_narrative_is_a_stable_source(self) -> None:
        relative_paths = [
            path.relative_to(ROOT).as_posix() for path in source_paths("2026-07-22")
        ]

        self.assertIn("docs/notebooklm/business_narrative.md", relative_paths)
        self.assertIn("docs/notebooklm/project_facts.md", relative_paths)


if __name__ == "__main__":
    unittest.main()
