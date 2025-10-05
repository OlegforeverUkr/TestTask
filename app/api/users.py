"""User endpoints - only HTTP handling."""
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.dependencies import GetCurrentActiveUser, GetDbDeps
from app.schemas.user import User as UserSchema
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserSchema)
async def get_current_user(current_user: GetCurrentActiveUser):
    """Get current user profile."""
    return UserSchema.model_validate(current_user)


@router.get("/profile", response_model=UserSchema)
async def get_profile(current_user: GetCurrentActiveUser):
    """Get user profile (alias for /me)."""
    return UserSchema.model_validate(current_user)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user_by_id(user_id: str, db: GetDbDeps):
    """Get user by ID."""
    user_service = UserService(db)
    try:
        user = await user_service.get_user_by_id(UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserSchema.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
