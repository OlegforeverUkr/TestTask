from uuid import UUID
from typing import Dict
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token

from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLogin, UserRegister
from app.schemas.user import UserCreate
from app.core.security import (
    create_access_token, 
    create_refresh_token, 
    create_verification_token,
)
from app.services.email_service import get_email_service
from app.core.config import settings


class AuthService:
    """Authentication service - contains all business logic for auth."""


    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)


    async def register_user(self, user_data: UserRegister) -> Dict:
        """Register a new user - business logic."""
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        user = await self.user_repo.create(
            UserCreate(
                email=user_data.email,
                password=user_data.password,
                full_name=user_data.full_name,
            )
        )

        verification_token = create_verification_token(str(user.id))
        token_expires = datetime.now() + timedelta(hours=24)
        
        await self.user_repo.update(user.id, {
            "verification_token": verification_token,
            "verification_token_expires": token_expires,
            "is_active": False
        })

        verification_url = f"{settings.backend_url}/auth/verify-email?token={verification_token}"
        email_service = get_email_service()
        email_sent = await email_service.send_verification_email(
            email=user.email,
            verification_url=verification_url,
            user_name=user.full_name
        )

        if not email_sent:
            # Якщо емейл не відправлений, то повертаємо помилку, або в проді робимо вже логіку через RabbitMQ
            pass

        return {
            "message": "Registration successful. Please check your email to verify your account.",
            "email": user.email,
            "verification_required": True
        }


    async def authenticate_user(self, credentials: UserLogin) -> Dict:
        """Authenticate user - business logic."""
        user = await self.user_repo.authenticate(
            credentials.email, credentials.password
        )
        if not user:
            raise ValueError("Incorrect email or password")

        return self._generate_token_response(user)


    async def refresh_user_token(self, refresh_token: str) -> Dict:
        """Refresh user token - business logic."""
        payload = decode_token(refresh_token)
        if payload is None or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid refresh token")

        user = await self.user_repo.get_by_id(UUID(user_id))
        if not user:
            raise ValueError("User not found")

        return self._generate_token_response(user)


    async def verify_email(self, verification_token: str) -> Dict:
        """Verify user email - business logic."""
        user = await self.user_repo.get_by_field("verification_token", verification_token)
        if not user:
            raise ValueError("Invalid verification token")

        if user.verification_token_expires and user.verification_token_expires < datetime.now():
            raise ValueError("Verification token has expired")

        if user.is_verified:
            raise ValueError("Email already verified")

        await self.user_repo.update(user.id, {
            "is_verified": True,
            "is_active": True,
            "verification_token": None,
            "verification_token_expires": None
        })

        return self._generate_token_response(user)


    def _generate_token_response(self, user) -> Dict:
        """Generate token response - business logic for token creation."""
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
            },
        }
