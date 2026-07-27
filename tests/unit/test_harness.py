"""Tests for the role-aware agentic harness entry point."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from scripts.harness import (
    ROOT,
    HarnessError,
    build_harness_pack,
    build_openspec_harness_pack,
    doctor_report,
    openspec_context_source,
    resolve_jira_tracking,
)


def openspec_runner(
    arguments: tuple[str, ...],
    *,
    remaining: int = 1,
    state: str = "ready",
    valid: bool = True,
    complete: bool = True,
) -> dict[str, Any]:
    if arguments[0] == "validate":
        return {"items": [{"name": "test-change", "valid": valid}]}
    if arguments[0] == "status":
        return {
            "changeName": "test-change",
            "schemaName": "spec-driven",
            "isComplete": complete,
            "artifacts": [
                {"id": "proposal", "status": "done"},
                {"id": "tasks", "status": "done"},
            ],
        }
    if arguments[:2] == ("instructions", "apply"):
        return {
            "state": state,
            "missingArtifacts": ["tasks"] if state == "blocked" else [],
            "progress": {
                "total": 2,
                "complete": 2 - remaining,
                "remaining": remaining,
            },
            "tasks": [
                {"id": "1", "description": "A test task", "done": remaining == 0}
            ],
            "contextFiles": {},
        }
    raise AssertionError(f"Unexpected OpenSpec invocation: {arguments}")


class HarnessTests(unittest.TestCase):
    def test_recovers_openspec_path_from_windows_encoding_mismatch(self) -> None:
        malformed = (
            r"C:\Users\migue\Documents\Proyecto ClasificaciÃ³n Multiclase"
            r"\openspec\changes\test-change\proposal.md"
        )

        self.assertEqual(
            openspec_context_source(malformed),
            "openspec/changes/test-change/proposal.md",
        )

    def test_rejects_external_openspec_context_path(self) -> None:
        with self.assertRaisesRegex(HarnessError, "outside the repository"):
            openspec_context_source(r"C:\outside\proposal.md")

        with self.assertRaisesRegex(HarnessError, "outside the repository"):
            openspec_context_source("/outside/openspec/changes/test/proposal.md")

    def test_doctor_confirms_real_local_openspec(self) -> None:
        ok, lines = doctor_report()

        self.assertTrue(ok, "\n".join(lines))
        self.assertTrue(any("OpenSpec 1.6.0" in line for line in lines))
        self.assertTrue(any("strict validation" in line for line in lines))

    def test_cli_runs_review_from_repository_root(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/harness.py",
                "review",
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
            "exports/ai-handoffs/harness-review-data-analyst-001-cfpb-target-contract-T-004.md",
            result.stdout,
        )

    def test_builds_start_pack_for_real_data_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch("scripts.harness.task_state", return_value="[~]"):
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
        self.assertIn("docs/project_management/delivery_levels.md", content)
        self.assertIn("ESS-02", content)
        self.assertIn("Jira work item PG-2", content)
        self.assertNotIn("gho_", content)
        self.assertNotIn("ATLAS_TOKEN", content)

    def test_rejects_wrong_jira_key_for_legacy_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "mapped to PG-2"):
                build_harness_pack(
                    "start",
                    "data-analyst",
                    "001",
                    "T-004",
                    output_directory=Path(directory),
                    jira="PG-4",
                )

    def test_validates_jira_tracking(self) -> None:
        self.assertEqual(
            resolve_jira_tracking("PG-12", None, required=True),
            ("PG-12", None),
        )
        self.assertEqual(
            resolve_jira_tracking(None, "bootstrap", required=True),
            (None, "bootstrap"),
        )

        invalid_values = ("pg-12", "PG-0", "PG-", "OTHER-12")
        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaisesRegex(HarnessError, "format PG-N"):
                    resolve_jira_tracking(value, None, required=True)

        with self.assertRaisesRegex(HarnessError, "cannot be combined"):
            resolve_jira_tracking("PG-12", "bootstrap", required=True)

        with self.assertRaisesRegex(HarnessError, "requires --jira"):
            resolve_jira_tracking(None, None, required=True)

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
            with patch("scripts.harness.task_state", return_value="[~]"):
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

    def test_builds_pack_from_openspec_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = build_openspec_harness_pack(
                "start",
                "architect",
                "test-change",
                output_directory=Path(directory),
                runner=openspec_runner,
                jira="PG-12",
            )
            content = output.read_text(encoding="utf-8")

        self.assertEqual(
            output.name,
            "harness-start-architect-openspec-test-change.md",
        )
        self.assertIn("Work only on OpenSpec change test-change", content)
        self.assertIn('"planningComplete": true', content)
        self.assertIn('"remaining": 1', content)
        self.assertIn("ai-specs/agents/architect.md", content)
        self.assertIn("openspec/config.yaml", content)
        self.assertIn("Jira work item: [PG-12]", content)

    def test_builds_openspec_pack_with_controlled_jira_exception(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = build_openspec_harness_pack(
                "start",
                "architect",
                "test-change",
                output_directory=Path(directory),
                runner=openspec_runner,
                jira_exception="bootstrap",
            )
            content = output.read_text(encoding="utf-8")

        self.assertIn("Jira exception: `bootstrap`", content)

    def test_openspec_pack_requires_jira_tracking(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "requires --jira"):
                build_openspec_harness_pack(
                    "start",
                    "architect",
                    "test-change",
                    output_directory=Path(directory),
                    runner=openspec_runner,
                )

    def test_rejects_invalid_openspec_change(self) -> None:
        def invalid_runner(arguments: tuple[str, ...]) -> dict[str, Any]:
            return openspec_runner(arguments, valid=False)

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "strict validation"):
                build_openspec_harness_pack(
                    "start",
                    "architect",
                    "test-change",
                    output_directory=Path(directory),
                    runner=invalid_runner,
                    jira="PG-12",
                )

    def test_rejects_incomplete_openspec_planning(self) -> None:
        def incomplete_runner(arguments: tuple[str, ...]) -> dict[str, Any]:
            return openspec_runner(arguments, complete=False)

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "planning artifacts"):
                build_openspec_harness_pack(
                    "start",
                    "architect",
                    "test-change",
                    output_directory=Path(directory),
                    runner=incomplete_runner,
                    jira="PG-12",
                )

    def test_rejects_blocked_openspec_change(self) -> None:
        def blocked_runner(arguments: tuple[str, ...]) -> dict[str, Any]:
            return openspec_runner(arguments, state="blocked")

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "blocked by tasks"):
                build_openspec_harness_pack(
                    "start",
                    "architect",
                    "test-change",
                    output_directory=Path(directory),
                    runner=blocked_runner,
                    jira="PG-12",
                )

    def test_prepare_pr_rejects_unfinished_openspec_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(HarnessError, "unfinished tasks"):
                build_openspec_harness_pack(
                    "prepare-pr",
                    "architect",
                    "test-change",
                    output_directory=Path(directory),
                    runner=openspec_runner,
                    jira="PG-12",
                )

    def test_prepare_pr_accepts_completed_openspec_tasks(self) -> None:
        def completed_runner(arguments: tuple[str, ...]) -> dict[str, Any]:
            return openspec_runner(arguments, remaining=0)

        with tempfile.TemporaryDirectory() as directory:
            output = build_openspec_harness_pack(
                "prepare-pr",
                "architect",
                "test-change",
                output_directory=Path(directory),
                runner=completed_runner,
                jira="PG-12",
            )
            self.assertTrue(output.is_file())


if __name__ == "__main__":
    unittest.main()
