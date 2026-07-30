"""Authentication routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.api.auth import (
    LoginRequest,
    TOKEN_EXPIRE_HOURS,
    TokenResponse,
    authenticate_user,
    create_access_token,
    get_user_name,
    get_user_role,
)

router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
async def login(body: LoginRequest) -> TokenResponse:
    """Authenticate and return a JWT token.

    The token must be sent as Bearer token in subsequent requests.
    """
    if not authenticate_user(body.username, body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(body.username)

    return TokenResponse(
        access_token=token,
        expires_in=TOKEN_EXPIRE_HOURS * 3600,
        role=get_user_role(body.username),
        name=get_user_name(body.username),
    )
