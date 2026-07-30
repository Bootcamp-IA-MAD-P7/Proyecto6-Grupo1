"""Simple JWT authentication for the prediction service.

Uses a demo user from environment variables. This is NOT production-grade
auth — it demonstrates the flow for the bootcamp presentation.
No passwords are stored in code.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field

# Secret key for signing tokens (from env, fallback for dev only)
SECRET_KEY = os.environ.get("APP_JWT_SECRET", "dev-secret-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = int(os.environ.get("APP_TOKEN_EXPIRE_HOURS", "24"))

# Demo credentials (multiple users for presentation)
DEMO_USERS = {
    "admin": {"password": "claimvox2026", "role": "admin", "name": "Admin"},
    "ana@example.com": {"password": "prueba", "role": "user", "name": "Ana García"},
    "carlos@example.com": {"password": "prueba", "role": "admin", "name": "Carlos López"},
}

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
    """Validate credentials against demo users.

    In production this would check a database with hashed passwords.
    """
    user = DEMO_USERS.get(username)
    if not user:
        return False
    return user["password"] == password


def get_user_role(username: str) -> str:
    """Return the role for a given username."""
    user = DEMO_USERS.get(username)
    return user["role"] if user else "user"


def get_user_name(username: str) -> str:
    """Return the display name for a given username."""
    user = DEMO_USERS.get(username)
    return user["name"] if user else username
