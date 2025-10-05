from abc import ABC
from typing import Generic, TypeVar, Optional, List, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    """Base repository with common CRUD operations."""

    def __init__(self, model: type[ModelType], db: AsyncSession):
        """Initialize repository."""
        self.model = model
        self.db = db


    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """Get entity by ID."""
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()


    async def get_by_field(self, field_name: str, value: Any) -> Optional[ModelType]:
        """Get entity by field value."""
        field = getattr(self.model, field_name)
        result = await self.db.execute(select(self.model).where(field == value))
        return result.scalar_one_or_none()


    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination."""
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()


    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create new entity."""
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        db_obj = self.model(**create_data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj


    async def update(self, id: UUID, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """Update entity."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        result = await self.db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .returning(self.model)
        )
        await self.db.commit()
        return result.scalar_one_or_none()


    async def delete(self, id: UUID) -> bool:
        """Delete entity."""
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.db.commit()
        return result.rowcount > 0


    async def exists(self, id: UUID) -> bool:
        """Check if entity exists."""
        result = await self.db.execute(
            select(self.model.id).where(self.model.id == id)
        )
        return result.scalar_one_or_none() is not None
