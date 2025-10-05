from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import get_db


GetDbDeps = Annotated[AsyncSession, Depends(get_db)]
