from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import SocialAccount
from app.repositories.base import BaseRepository


class SocialAccountRepository(BaseRepository[SocialAccount, dict, dict]):
    """Social account repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(SocialAccount, db)


    async def get_by_provider_and_user_id(
        self, provider: str, provider_user_id: str
    ) -> Optional[SocialAccount]:
        """Get social account by provider and provider user ID."""
        result = await self.db.execute(
            select(SocialAccount).where(
                SocialAccount.provider == provider,
                SocialAccount.provider_user_id == provider_user_id
            )
        )
        return result.scalar_one_or_none()


    async def get_by_user_and_provider(
        self, user_id: str, provider: str
    ) -> Optional[SocialAccount]:
        """Get social account by user ID and provider."""
        result = await self.db.execute(
            select(SocialAccount).where(
                SocialAccount.user_id == user_id,
                SocialAccount.provider == provider
            )
        )
        return result.scalar_one_or_none()
