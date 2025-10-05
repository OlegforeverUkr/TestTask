from typing import Dict

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.dependencies import GetDbDeps
from app.core.config import settings
from app.schemas.auth import (
    RefreshTokenRequest, 
    TokenResponse, 
    UserLogin, 
    UserRegister, 
    RegistrationResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: GetDbDeps) -> RegistrationResponse:
    """Register a new user with email and password."""
    auth_service = AuthService(db)
    
    try:
        return await auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: GetDbDeps) -> Dict:
    """Login with email and password."""
    auth_service = AuthService(db)
    
    try:
        return await auth_service.authenticate_user(credentials)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest, db: GetDbDeps) -> Dict:
    """Refresh access token using refresh token."""
    auth_service = AuthService(db)
    
    try:
        return await auth_service.refresh_user_token(refresh_data.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.get("/verify-email")
async def verify_email(token: str, db: GetDbDeps) -> RedirectResponse:
    """Verify user email and redirect to frontend."""
    auth_service = AuthService(db)
    
    try:
        token_data = await auth_service.verify_email(token)
        
        redirect_url = f"{settings.frontend_url}/auth/verify-success"
        redirect_url += f"?access_token={token_data['access_token']}"
        redirect_url += f"&refresh_token={token_data['refresh_token']}"
        redirect_url += f"&user_id={token_data['user']['id']}"
        
        return RedirectResponse(url=redirect_url, status_code=302)
        
    except ValueError as e:
        error_url = f"{settings.frontend_url}/auth/verify-error"
        error_url += f"?error={str(e)}"
        return RedirectResponse(url=error_url, status_code=302)
