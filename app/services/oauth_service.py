from typing import Dict, Optional

import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.core.config import settings
from app.models.user import SocialAccount
from app.repositories.user_repository import UserRepository
from app.repositories.social_account_repository import SocialAccountRepository
from app.schemas.user import UserCreate, UserOAuthCreate
from app.core.security import create_access_token, create_refresh_token


class OAuthService:
    """OAuth service - contains all business logic for social login."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.social_repo = SocialAccountRepository(db)


    async def initiate_google_login(self) -> Dict:
        """Initiate Google OAuth login."""
        
        client = AsyncOAuth2Client(
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            redirect_uri=settings.google_redirect_uri,
        )
        
        authorization_url, state = client.create_authorization_url(
            "https://accounts.google.com/o/oauth2/v2/auth",
            scope=["openid", "email", "profile"]
        )
        
        return {
            "authorization_url": authorization_url,
            "state": state,
        }


    async def handle_google_callback(self, code: str) -> Dict:
        """Handle Google OAuth callback."""
        token = await self._exchange_google_code(code)
        
        user_info = await self._get_google_user_info(token["access_token"])
        
        user = await self._create_or_update_google_user(
            user_info, token["access_token"], token.get("refresh_token")
        )
        
        return self._generate_token_response(user)


    async def handle_facebook_callback(self, code: str) -> Dict:
        """Handle Facebook OAuth callback"""
        token = await self._exchange_facebook_code(code)
        user_info = await self._get_facebook_user_info(token["access_token"])
        
        user = await self._create_or_update_facebook_user(user_info, token["access_token"])
        return await self._generate_token_response(user)


    async def handle_twitter_callback(self, code: str) -> Dict:
        """Handle Twitter OAuth callback."""
        token = await self._exchange_twitter_code(code)
        user_info = await self._get_twitter_user_info(token["access_token"])
        
        user = await self._create_or_update_twitter_user(
            user_info, token["access_token"], token.get("refresh_token")
        )
        return await self._generate_token_response(user)


    async def _create_or_update_google_user(
        self, user_info: Dict, access_token: str, refresh_token: Optional[str] = None
    ):
        """Create or update Google user."""
        result = await self.db.execute(
            select(SocialAccount)
            .options(selectinload(SocialAccount.user))
            .where(
                SocialAccount.provider == "google",
                SocialAccount.provider_user_id == user_info["id"]
            )
        )
        social_account = result.scalar_one_or_none()
        
        if social_account:
            await self.social_repo.update(social_account.id, {
                "access_token": access_token,
                "refresh_token": refresh_token,
            })
            if not social_account.user.is_verified or not social_account.user.is_active:
                await self.user_repo.update(social_account.user.id, {
                    "is_verified": True,
                    "is_active": True,
                })
            return social_account.user
        else:
            user = await self.user_repo.get_by_email(user_info["email"])
            
            if not user:
                user = await self.user_repo.create(
                    UserOAuthCreate(
                        email=user_info["email"],
                        full_name=user_info.get("name"),
                        profile_picture=user_info.get("picture"),
                    )
                )
                await self.user_repo.update(user.id, {
                    "is_verified": True,
                    "is_active": True,
                })
            else:
                if not user.is_verified or not user.is_active:
                    await self.user_repo.update(user.id, {
                        "is_verified": True,
                        "is_active": True,
                    })
            
            await self.social_repo.create({
                "user_id": str(user.id),
                "provider": "google",
                "provider_user_id": user_info["id"],
                "access_token": access_token,
                "refresh_token": refresh_token,
            })
            
            return user

    async def _create_or_update_facebook_user(self, user_info: Dict, access_token: str):
        """Create or update Facebook user."""
        pass


    async def _create_or_update_twitter_user(
        self, user_info: Dict, access_token: str, refresh_token: Optional[str] = None
    ):
        """Create or update Twitter user."""
        pass


    def _generate_token_response(self, user) -> Dict:
        """Generate token response."""
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


    async def _exchange_google_code(self, code: str) -> Dict:
        """Exchange Google authorization code for token."""
        
        client = AsyncOAuth2Client(
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            redirect_uri=settings.google_redirect_uri,
        )
        
        token = await client.fetch_token(
            "https://oauth2.googleapis.com/token",
            code=code,
            scope="openid email profile"
        )
        return token


    async def _get_google_user_info(self, access_token: str) -> Dict:
        """Get user info from Google."""
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()


    async def _exchange_facebook_code(self, code: str) -> Dict:
        """Exchange Facebook authorization code for token."""
        pass

    async def _get_facebook_user_info(self, access_token: str) -> Dict:
        """Get user info from Facebook."""
        pass

    async def _exchange_twitter_code(self, code: str) -> Dict:
        """Exchange Twitter authorization code for token."""
        pass

    async def _get_twitter_user_info(self, access_token: str) -> Dict:
        """Get user info from Twitter."""
        pass