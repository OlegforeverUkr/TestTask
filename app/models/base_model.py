from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class BaseModel(DeclarativeBase):
    """Base class for all models."""
    __abstract__ = True

    id = Column(UUID, primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    def __repr__(self) -> str:
        """String representation."""
        return f"<{self.__class__.__name__} {self.id}>"
