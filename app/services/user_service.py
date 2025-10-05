from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User


class UserService:
    """User service - contains all business logic for user operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID - business logic."""
        return await self.user_repo.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email - business logic."""
        return await self.user_repo.get_by_email(email)

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users - business logic."""
        return await self.user_repo.get_active_users(skip, limit)

    async def create_user(self, user_data: UserCreate) -> User:
        """Create new user - business logic."""
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        return await self.user_repo.create(user_data)

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        """Update user - business logic."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        return await self.user_repo.update(user_id, user_data)

    async def deactivate_user(self, user_id: UUID) -> bool:
        """Deactivate user - business logic."""
        return await self.user_repo.update(user_id, {"is_active": False}) is not None