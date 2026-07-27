"""Application configuration from environment variables."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Backend service settings.

    All values can be overridden via environment variables prefixed with APP_.
    Example: APP_MODEL_PATH=/custom/path/model.pkl
    """

    model_path: Path = ROOT_DIR / "models" / "cfpb_baseline.pkl"
    service_version: str = "0.1.0"
    taxonomy_version: str = "1.0"
    debug: bool = False

    model_config = {"env_prefix": "APP_"}


def get_settings() -> Settings:
    """Return the application settings instance."""
    return Settings()
