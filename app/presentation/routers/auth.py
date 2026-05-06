"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import authenticate_admin, create_access_token
from app.core.settings import Settings, get_settings
from app.presentation.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    if not authenticate_admin(payload.username, payload.password, settings):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    return TokenResponse(access_token=create_access_token(payload.username, settings))
