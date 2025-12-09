"""
Application configuration using Pydantic BaseSettings.

All environment variables are loaded from .env file and validated.
This replaces the previous Starlette Config approach for consistency.
"""
import logging
import sys
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger
from app.core.logging import InterceptHandler


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    API_PREFIX: str = "/api"
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "Pookie Backend"
    DEBUG: bool = False

    # Database Configuration (for future use)
    MAX_CONNECTIONS_COUNT: int = 10
    MIN_CONNECTIONS_COUNT: int = 10

    # Security (required for production)
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for session management and token signing. MUST be changed in production."
    )

    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    # Database URL (PostgreSQL connection string for Alembic and tests)
    DATABASE_URL: str

    # CORS Origins (iOS app)
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Environment
    ENVIRONMENT: str = "development"

    # ML Model Configuration
    MODEL_PATH: str = "./ml/model/"
    MODEL_NAME: str = "model.pkl"

    # OpenRouter API Configuration (for chat/LLM features)
    OPENROUTER_API_KEY: str = Field(
        default="",
        description="OpenRouter API key for LLM access (Claude Haiku). Optional - chat will fail gracefully if not set."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Singleton settings instance
settings = Settings()

# Configure logging based on DEBUG mode
LOGGING_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
