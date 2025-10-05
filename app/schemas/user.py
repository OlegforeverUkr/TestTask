"""User schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user with password."""

    password: str = Field(..., min_length=8, max_length=72, description="Password must be 8-72 characters")


class UserOAuthCreate(UserBase):
    """Schema for creating a user via OAuth (no password required)."""
    
    email: EmailStr
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    full_name: Optional[str] = None
    profile_picture: Optional[str] = None


class User(UserBase):
    """User response schema."""

    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserInDB(User):
    """User schema with hashed password (for internal use)."""

    hashed_password: Optional[str] = None

