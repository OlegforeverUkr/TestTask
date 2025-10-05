"""Authentication schemas."""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.validators import validate_password


class UserLogin(BaseModel):
    """User login schema."""

    email: EmailStr
    password: str = Field(..., max_length=72, description="Password must be at most 72 characters")

    @field_validator("password", mode="before")
    def validate_password(cls, v: str) -> str:
        """Validate password complexity."""
        try:
            validate_password(v)
        except ValueError as e:
            raise ValueError(str(e))
        return v


class UserRegister(BaseModel):
    """User registration schema."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Password must be 8-72 characters")
    full_name: Optional[str] = None

    @field_validator("password", mode="before")
    def validate_password(cls, v: str) -> str:
        """Validate password complexity."""
        try:
            validate_password(v)
        except ValueError as e:
            raise ValueError(str(e))
        return v


class Token(BaseModel):
    """Token schema."""

    access_token: str
    token_type: str = "bearer"


class TokenResponse(BaseModel):
    """Token response with user info."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""

    refresh_token: str


class RegistrationResponse(BaseModel):
    """Registration response schema."""

    message: str
    email: str
    verification_required: bool

