"""Application configuration."""
from typing import List
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Sales Platform Auth Service"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG" , False)
    api_v1_prefix: str = os.getenv("API_V1_PREFIX" , "/api/v1")

    # Security
    secret_key: str = Field(
        default=os.getenv("SECRET_KEY" , "your-secret-key-change-in-production"),
        description="Secret key for JWT tokens",
    )
    algorithm: str = os.getenv("ALGORITHM" , "HS256")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES" , 30)
    refresh_token_expire_days: int = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS" , 7)
    
    # Email Settings
    mail_username: str = Field(default=os.getenv("MAIL_USERNAME"), description="Email username")
    mail_password: str = Field(default=os.getenv("MAIL_PASSWORD"), description="Email password")
    mail_from: str = Field(default=os.getenv("MAIL_FROM"), description="Email sender")
    mail_port: int = Field(default=int(os.getenv("MAIL_PORT", "587")), description="Email port")
    mail_server: str = Field(default=os.getenv("MAIL_SERVER"), description="Email server")
    mail_tls: bool = Field(default=True, description="Use TLS for email")
    mail_ssl: bool = Field(default=False, description="Use SSL for email")
    mail_from_name: str = Field(default="Authentication Service", description="Email sender name")
    
    # URLs
    frontend_url: str = Field(default=os.getenv(
        "FRONTEND_URL", "http://localhost:3000"), 
        description="Frontend URL for email links"
    )
    backend_url: str = Field(default=os.getenv(
        "BACKEND_URL", "http://localhost:8000"), 
        description="Backend URL for email links"
    )

    # CORS
    allowed_origins: List[str] = Field(
        default=os.getenv("ALLOWED_ORIGINS" , ["http://localhost:3000", "http://localhost:8000"]),
        description="Allowed CORS origins",
    )

    # Database
    database_url: str = Field(default=os.getenv("DATABASE_URL"), description="PostgreSQL database URL")

    # Redis
    redis_url: str = Field(
        default=os.getenv("REDIS_URL" , "redis://localhost:6379/0"),
        description="Redis URL for session storage",
    )

    ######################### OAuth Providers #########################


    # Google OAuth
    google_client_id: str = Field(default=os.getenv("GOOGLE_CLIENT_ID" , ""), description="Google OAuth client ID")
    google_client_secret: str = Field(default=os.getenv("GOOGLE_CLIENT_SECRET" , ""), description="Google OAuth client secret")
    google_redirect_uri: str = Field(
        default="http://localhost:8000/auth/google/callback",
        description="Google OAuth redirect URI",
    )

    # Facebook OAuth
    facebook_client_id: str = Field(default=os.getenv("FACEBOOK_CLIENT_ID" , ""), description="Facebook OAuth client ID")
    facebook_client_secret: str = Field(
        default=os.getenv("FACEBOOK_CLIENT_SECRET" , ""), description="Facebook OAuth client secret"
    )
    facebook_redirect_uri: str = Field(
        default=os.getenv("FACEBOOK_REDIRECT_URI" , "http://localhost:8000/auth/facebook/callback"),
        description="Facebook OAuth redirect URI",
    )

    # Twitter OAuth
    twitter_client_id: str = Field(default=os.getenv("TWITTER_CLIENT_ID" , ""), description="Twitter OAuth client ID")
    twitter_client_secret: str = Field(
        default=os.getenv("TWITTER_CLIENT_SECRET" , ""), description="Twitter OAuth client secret"
    )
    twitter_redirect_uri: str = Field(
        default=os.getenv("TWITTER_REDIRECT_URI" , "http://localhost:8000/auth/twitter/callback"),
        description="Twitter OAuth redirect URI",
    )

    # Rate Limiting
    rate_limit_enabled: bool = os.getenv("RATE_LIMIT_ENABLED" , True)
    rate_limit_per_minute: int = os.getenv("RATE_LIMIT_PER_MINUTE" , 60)

    # Observability
    enable_metrics: bool = os.getenv("ENABLE_METRICS" , True)
    enable_tracing: bool = os.getenv("ENABLE_TRACING" , False)
    log_level: str = os.getenv("LOG_LEVEL" , "INFO")


settings = Settings()
