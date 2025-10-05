"""User database models."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    profile_picture: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    verification_token_expires: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    social_accounts: Mapped[List["SocialAccount"]] = relationship(
        "SocialAccount", back_populates="user", cascade="all, delete-orphan"
    )


    def __repr__(self) -> str:
        """String representation."""
        return f"<User {self.email}>"


class SocialAccount(BaseModel):
    """Social account model for OAuth providers."""

    __tablename__ = "social_accounts"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    access_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="social_accounts")


    def __repr__(self) -> str:
        """String representation."""
        return f"<SocialAccount {self.provider}:{self.provider_user_id}>"

