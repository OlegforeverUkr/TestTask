from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.health import router as health_router
from app.api.google_oauth import router as google_oauth_router

__all__ = ["auth_router", "users_router", "health_router", "google_oauth_router"]