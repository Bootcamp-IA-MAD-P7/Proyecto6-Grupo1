"""Direct tests for the intentionally limited environment-only demo auth."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from app.api.auth import authenticate_user, get_user_name, get_user_role


class DemoAuthSecurityTests(unittest.TestCase):
    def test_authentication_is_unavailable_without_environment_credentials(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(authenticate_user("reviewer", "synthetic-password"))

    def test_environment_credentials_and_profile_are_used_without_defaults(self) -> None:
        environment = {
            "APP_DEMO_USERNAME": "synthetic-reviewer",
            "APP_DEMO_PASSWORD": "synthetic-password",
            "APP_DEMO_ROLE": "admin",
            "APP_DEMO_NAME": "Synthetic reviewer",
        }
        with patch.dict(os.environ, environment, clear=True):
            self.assertTrue(authenticate_user("synthetic-reviewer", "synthetic-password"))
            self.assertFalse(authenticate_user("synthetic-reviewer", "wrong"))
            self.assertEqual(get_user_role("synthetic-reviewer"), "admin")
            self.assertEqual(get_user_name("synthetic-reviewer"), "Synthetic reviewer")

    def test_invalid_environment_role_is_reduced_to_user(self) -> None:
        environment = {
            "APP_DEMO_USERNAME": "synthetic-reviewer",
            "APP_DEMO_PASSWORD": "synthetic-password",
            "APP_DEMO_ROLE": "superuser",
        }
        with patch.dict(os.environ, environment, clear=True):
            self.assertEqual(get_user_role("synthetic-reviewer"), "user")


if __name__ == "__main__":
    unittest.main()
