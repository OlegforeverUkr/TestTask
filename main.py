"""Main application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api import auth_router, users_router, health_router, google_oauth_router
from app.core.config import settings
from app.core.database import close_db, init_db
from app.utils.middleware import RateLimitMiddleware, SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Authentication Service with Social Login Support",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, calls=settings.rate_limit_per_minute, period=60)

app.include_router(auth_router)
app.include_router(google_oauth_router)
app.include_router(users_router)
app.include_router(health_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
