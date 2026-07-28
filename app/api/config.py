"""Application configuration from environment variables."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from pydantic import field_validator
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
    cors_allowed_origins: str = ""
    max_narrative_characters: int = 5000
    prediction_rate_limit_per_minute: int = 20

    model_config = {"env_prefix": "APP_"}

    @field_validator("cors_allowed_origins")
    @classmethod
    def validate_cors_allowed_origins(cls, raw_origins: str) -> str:
        """Accept only explicit local origins for the browser development path."""
        origins = tuple(
            origin.strip().rstrip("/")
            for origin in raw_origins.split(",")
            if origin.strip()
        )

        for origin in origins:
            parsed = urlparse(origin)
            if origin == "*" or parsed.scheme not in {"http", "https"}:
                raise ValueError("CORS origins must be explicit http(s) origins")
            if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
                raise ValueError("CORS origins must be local development origins")
            if parsed.path or parsed.params or parsed.query or parsed.fragment:
                raise ValueError("CORS origins must not include a path or query")

        return ",".join(origins)

    @field_validator("max_narrative_characters")
    @classmethod
    def validate_max_narrative_characters(cls, value: int) -> int:
        """Keep the local policy within the published request contract."""
        if not 1 <= value <= 5000:
            raise ValueError("max narrative characters must be between 1 and 5000")
        return value

    @field_validator("prediction_rate_limit_per_minute")
    @classmethod
    def validate_prediction_rate_limit(cls, value: int) -> int:
        """Require a positive, intentionally bounded local frequency limit."""
        if not 1 <= value <= 600:
            raise ValueError("prediction rate limit must be between 1 and 600")
        return value

    @property
    def local_cors_origins(self) -> tuple[str, ...]:
        """Return the validated local origins as a middleware-ready tuple."""
        return tuple(
            origin for origin in self.cors_allowed_origins.split(",") if origin
        )


def get_settings() -> Settings:
    """Return the application settings instance."""
    return Settings()
