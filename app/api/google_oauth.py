from typing import Dict

from fastapi import APIRouter, HTTPException, status

from app.dependencies import GetDbDeps
from app.schemas.auth import TokenResponse
from app.services.oauth_service import OAuthService


router = APIRouter(prefix="/auth/google", tags=["Google OAuth"])


@router.get("")
async def google_login(db: GetDbDeps) -> Dict:
    """Initiate Google OAuth login."""
    oauth_service = OAuthService(db)
    
    try:
        return await oauth_service.initiate_google_login()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/callback", response_model=TokenResponse)
async def google_callback(code: str, db: GetDbDeps) -> Dict:
    """Handle Google OAuth callback."""
    oauth_service = OAuthService(db)
    
    try:
        return await oauth_service.handle_google_callback(code)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
