"""Static packaging boundaries that do not require a Docker daemon."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PackagingSecurityTests(unittest.TestCase):
    def test_compose_requires_external_secrets(self) -> None:
        compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")

        for required_name in (
            "POSTGRES_PASSWORD",
            "CLAIMVOX_DB_APP_PASSWORD",
            "APP_JWT_SECRET",
            "APP_DEMO_USERNAME",
            "APP_DEMO_PASSWORD",
        ):
            self.assertIn(f"${{{required_name}:?", compose)

        for prohibited_value in (
            "claimvox_secret",
            "claimvox_admin_secret",
            "claimvox2026",
            "change-this-in-production",
        ):
            self.assertNotIn(prohibited_value, compose)

    def test_postgres_runtime_repository_contains_no_ddl(self) -> None:
        repository = (
            ROOT / "app" / "api" / "services" / "postgres_feedback_repository.py"
        ).read_text(encoding="utf-8")
        for ddl in ("CREATE TABLE", "CREATE USER", "CREATE ROLE", "DROP TABLE"):
            self.assertNotIn(ddl, repository.upper())

    def test_deploy_health_failure_is_blocking(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "deploy.yml").read_text(
            encoding="utf-8"
        )
        self.assertNotIn('|| echo "Health check failed"', workflow)
        self.assertIn("exit 1", workflow)

    def test_deploy_materializes_runtime_env_from_github_secrets(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "deploy.yml").read_text(
            encoding="utf-8"
        )

        for required_name in (
            "POSTGRES_PASSWORD",
            "CLAIMVOX_DB_APP_PASSWORD",
            "APP_JWT_SECRET",
            "APP_DEMO_USERNAME",
            "APP_DEMO_PASSWORD",
        ):
            self.assertIn(f"secrets.{required_name}", workflow)
            self.assertIn(f"{required_name}=${{{required_name}}}", workflow)

        for prohibited_value in (
            "claimvox_secret",
            "claimvox_admin_secret",
            "claimvox2026",
            "change-this-in-production",
        ):
            self.assertNotIn(prohibited_value, workflow)


if __name__ == "__main__":
    unittest.main()
