"""Application Configuration and Environment Settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """CyberSage AI Typed Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Core Application
    APP_ENV: str = Field(
        default="development", description="Environment: development, staging, production"
    )
    DEBUG: bool = Field(default=True, description="Enable debug mode")
    PROJECT_NAME: str = Field(default="CyberSage AI", description="Platform display name")
    API_V1_STR: str = Field(default="/api/v1", description="API Version 1 prefix")
    HOST: str = Field(default="0.0.0.0", description="API Server Bind Host")
    PORT: int = Field(default=8000, description="API Server Bind Port")
    SECRET_KEY: str = Field(
        default="default-development-secret-key-change-in-production-min32chars",
        description="Application secret key",
    )

    # CORS
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        description="Comma-separated allowed CORS origins",
    )

    # Persistence & Queues (Phase 2+)
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./cybersage.db",
        description="Database connection string",
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string",
    )

    # AI Configuration (Phase 3+)
    LLM_PROVIDER: str = Field(default="openai", description="Configured LLM provider")
    LLM_MODEL: str = Field(default="gpt-4o-mini", description="LLM model identifier")
    LLM_API_KEY: str = Field(default="", description="Provider API key")
    LLM_TEMPERATURE: float = Field(default=0.1, description="LLM sampling temperature")

    # Sandboxing & Security Boundaries
    SANDBOX_EXECUTION_TIMEOUT_SECONDS: int = Field(
        default=60, description="Max execution time for sandbox verification"
    )
    SANDBOX_MAX_MEMORY_MB: int = Field(
        default=1024, description="Max memory allocation for sandbox"
    )
    SANDBOX_ALLOW_NETWORK: bool = Field(
        default=False, description="Allow external network access in sandbox"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a trimmed list."""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
