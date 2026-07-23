"""Regression tests for repository presentation and structure quality gates."""

from __future__ import annotations

import unittest

from scripts.quality import check_repository


class RepositoryQualityTests(unittest.TestCase):
    def test_accepts_jira_key_or_controlled_exception(self) -> None:
        jira = "## Tracking\n\n- Jira: `PG-12`.\n"
        bootstrap = "## Tracking\n\n- Jira exception: `bootstrap`.\n"

        self.assertTrue(check_repository.proposal_has_jira_tracking(jira))
        self.assertTrue(check_repository.proposal_has_jira_tracking(bootstrap))
        self.assertFalse(
            check_repository.proposal_has_jira_tracking(
                "## Tracking\n\n- Jira: `OTHER-12`.\n"
            )
        )
        self.assertFalse(
            check_repository.proposal_has_jira_tracking(
                "## Tracking\n\n- Jira exception: `convenience`.\n"
            )
        )

    def test_readme_delivery_ids_cannot_wrap(self) -> None:
        errors: list[str] = []

        check_repository.check_readme_delivery_ids(errors)

        self.assertEqual([], errors)

    def test_documentation_svgs_are_accessible_and_valid(self) -> None:
        errors: list[str] = []

        check_repository.check_svg_assets(errors)

        self.assertEqual([], errors)

    def test_delivery_states_and_chart_are_synchronized(self) -> None:
        errors: list[str] = []

        check_repository.check_delivery_state_consistency(errors)

        self.assertEqual([], errors)

    def test_only_data_stages_keep_placeholders(self) -> None:
        errors: list[str] = []

        check_repository.check_tracked_files(
            check_repository.tracked_files(),
            errors,
        )

        placeholder_errors = [
            error for error in errors if error.startswith("Placeholder file")
        ]
        self.assertEqual([], placeholder_errors)


if __name__ == "__main__":
    unittest.main()
