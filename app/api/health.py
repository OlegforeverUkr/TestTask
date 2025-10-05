from fastapi import APIRouter
from app.core.config import settings


router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Sales Platform Authentication Service",
        "version": settings.app_version,
        "docs": "/docs",
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }