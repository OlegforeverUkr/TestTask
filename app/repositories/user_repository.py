from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOAuthCreate
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)


    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return await self.get_by_field("email", email)


    async def get_active_users(self, skip: int = 0, limit: int = 100):
        """Get active users."""
        result = await self.db.execute(
            select(User)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


    async def create(self, obj_in: Union[UserCreate, UserOAuthCreate]) -> User:
        """Create new user with password handling."""
        create_data = obj_in.model_dump(exclude_unset=True)

        if create_data.get("password"):
            create_data["hashed_password"] = get_password_hash(create_data.pop("password"))
        else:
            create_data["hashed_password"] = None

        db_obj = self.model(**create_data)
        self.db.add(db_obj)

        await self.db.commit()
        await self.db.refresh(db_obj)
        
        return db_obj

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        from app.core.security import verify_password
        
        user = await self.get_by_email(email)
        if not user or not user.is_active:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        return user
