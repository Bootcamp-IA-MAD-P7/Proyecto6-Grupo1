"""Tests for the role-aware agentic harness entry point."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.harness import ROOT, HarnessError, build_harness_pack


class HarnessTests(unittest.TestCase):
    def test_cli_runs_from_repository_root(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/harness.py",
                "start",
                "--role",
                "data-analyst",
                "--spec",
                "001",
                "--task",
                "T-004",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn(
            "exports/ai-handoffs/harness-start-data-analyst-001-cfpb-target-contract-T-004.md",
            result.stdout,
        )

    def test_builds_start_pack_for_real_data_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = build_harness_pack(
                "start",
                "data-analyst",
                "001",
                "T-004",
                output_directory=Path(directory),
            )
            content = output.read_text(encoding="utf-8")

        self.assertEqual(
            output.name,
            "harness-start-data-analyst-001-cfpb-target-contract-T-004.md",
        )
        self.assertIn("ai-specs/agents/data-analyst.md", content)
        self.assertIn("ai-specs/skills/start-task/SKILL.md", content)
        self.assertIn("Work only on T-004", content)
        self.assertIn("Human review is required", content)
        self.assertIn("config/cfpb_target_contract.json", content)

    def test_rejects_unknown_role(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "Unknown role"):
                build_harness_pack(
                    "start",
                    "model-wizard",
                    "001",
                    "T-004",
                    output_directory=Path(directory),
                )

    def test_rejects_unknown_action(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "Unknown action"):
                build_harness_pack(
                    "publish",
                    "data-analyst",
                    "001",
                    "T-004",
                    output_directory=Path(directory),
                )

    def test_rejects_blocked_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "blocked"):
                build_harness_pack(
                    "start",
                    "backend-developer",
                    "003",
                    "T-007",
                    output_directory=Path(directory),
                )

    def test_rejects_start_for_completed_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "cannot be started"):
                build_harness_pack(
                    "start",
                    "data-analyst",
                    "001",
                    "T-001",
                    output_directory=Path(directory),
                )

    def test_prepare_pr_requires_completed_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "must be completed"):
                build_harness_pack(
                    "prepare-pr",
                    "data-analyst",
                    "001",
                    "T-004",
                    output_directory=Path(directory),
                )

    def test_builds_prepare_pr_pack_for_completed_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = build_harness_pack(
                "prepare-pr",
                "data-analyst",
                "001",
                "T-001",
                output_directory=Path(directory),
            )
            content = output.read_text(encoding="utf-8")

        self.assertIn("ai-specs/skills/prepare-pr/SKILL.md", content)
        self.assertIn("currently in state [x]", content)


if __name__ == "__main__":
    unittest.main()
