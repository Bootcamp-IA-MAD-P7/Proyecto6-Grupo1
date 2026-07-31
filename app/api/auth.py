"""Simple JWT authentication for the prediction service.

Uses a demo user from environment variables. This is NOT production-grade
auth — it demonstrates the flow for the bootcamp presentation.
No passwords are stored in code.
"""

from __future__ import annotations

import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field

# The environment supplies a stable key for an intentional demo deployment.
# Local processes without one receive an ephemeral key instead of a repository
# credential; tokens then expire naturally when the process stops.
SECRET_KEY = os.environ.get("APP_JWT_SECRET") or secrets.token_urlsafe(32)
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = int(os.environ.get("APP_TOKEN_EXPIRE_HOURS", "24"))

security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login credentials."""

    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """JWT token response."""

    model_config = ConfigDict(extra="forbid")

    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Token lifetime in seconds")
    role: str = Field(description="User role (user or admin)")
    name: str = Field(description="Display name")


def create_access_token(username: str) -> str:
    """Create a signed JWT token."""
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": username,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify JWT token and return the username.

    Used as a FastAPI dependency on protected routes.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def authenticate_user(username: str, password: str) -> bool:
    """Validate credentials against the optional environment demo user.

    Authentication is unavailable until both values are configured. This is
    deliberately a single-user demonstration boundary, not a production
    identity store.
    """
    configured_username = os.environ.get("APP_DEMO_USERNAME")
    configured_password = os.environ.get("APP_DEMO_PASSWORD")
    if not configured_username or not configured_password:
        return False
    return secrets.compare_digest(username, configured_username) and secrets.compare_digest(
        password, configured_password
    )


def get_user_role(username: str) -> str:
    """Return the role for a given username."""
    if username != os.environ.get("APP_DEMO_USERNAME"):
        return "user"
    role = os.environ.get("APP_DEMO_ROLE", "admin")
    return role if role in {"user", "admin"} else "user"


def get_user_name(username: str) -> str:
    """Return the display name for a given username."""
    if username != os.environ.get("APP_DEMO_USERNAME"):
        return username
    return os.environ.get("APP_DEMO_NAME", "ClaimVox reviewer")
