"""Application Configuration and Environment Settings."""

from functools import lru_cache
from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

KNOWN_INSECURE_SECRETS: frozenset[str] = frozenset(
    {
        "",
        "secret",
        "password",
        "changeme",
        "change_this_to_a_secure_random_string_min_32_chars",
        "default-development-secret-key-change-in-production-min32chars",
        "dev-insecure-secret-key-local-only-not-for-production-min32chars",
    }
)


class Settings(BaseSettings):
    """CyberSage AI Typed Settings with Production Hardening."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Core Application
    APP_ENV: str = Field(
        default="development", description="Environment: development, staging, production, test"
    )
    DEBUG: bool = Field(default=True, description="Enable debug mode")
    PROJECT_NAME: str = Field(default="CyberSage AI", description="Platform display name")
    API_V1_STR: str = Field(default="/api/v1", description="API Version 1 prefix")
    HOST: str = Field(default="0.0.0.0", description="API Server Bind Host")
    PORT: int = Field(default=8000, description="API Server Bind Port")
    SECRET_KEY: str = Field(
        default="dev-insecure-secret-key-local-only-not-for-production-min32chars",
        description="Application secret key (must be explicitly set in production)",
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

    # Initial Scanner MVP Tooling (Phase 2)
    SEMGREP_RULES_CONFIG: str = Field(
        default="p/default", description="Semgrep rule configuration pack"
    )
    OSV_SCANNER_ENABLED: bool = Field(
        default=True, description="Enable OSV-Scanner for dependency CVE resolution"
    )
    GITLEAKS_ENABLED: bool = Field(
        default=True, description="Enable Gitleaks for exposed credential detection"
    )

    # AI Configuration (Phase 3+)
    LLM_PROVIDER: str = Field(default="openai", description="Configured LLM provider")
    LLM_MODEL: str = Field(default="gpt-4o-mini", description="LLM model identifier")
    LLM_API_KEY: str = Field(default="", description="Provider API key")
    LLM_TEMPERATURE: float = Field(default=0.1, description="LLM sampling temperature")

    # Sandboxing & Security Boundaries (Phase 4+)
    SANDBOX_EXECUTION_TIMEOUT_SECONDS: int = Field(
        default=60, description="Max execution time for sandbox verification"
    )
    SANDBOX_MAX_MEMORY_MB: int = Field(
        default=1024, description="Max memory allocation for sandbox"
    )
    SANDBOX_ALLOW_NETWORK: bool = Field(
        default=False, description="Allow external network access in sandbox"
    )

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        """Enforce strict security validation for production and staging environments."""
        is_prod = self.APP_ENV.lower() in ("production", "staging")

        if is_prod:
            normalized_key = self.SECRET_KEY.strip()
            if not normalized_key:
                raise ValueError("SECRET_KEY must be provided in production/staging environments.")

            if normalized_key in KNOWN_INSECURE_SECRETS:
                raise ValueError(
                    "SECRET_KEY cannot be a known default or placeholder value in production/staging."
                )

            if len(normalized_key) < 32:
                raise ValueError(
                    f"SECRET_KEY length must be at least 32 characters in production (got {len(normalized_key)})."
                )

            # In production, debug mode must not be enabled by default
            if self.DEBUG:
                raise ValueError("DEBUG must be set to False in production environments.")

        return self

    @property
    def is_production(self) -> bool:
        """Return True if running in production or staging."""
        return self.APP_ENV.lower() in ("production", "staging")

    @property
    def is_configured(self) -> bool:
        """Check if application core settings are properly configured."""
        return bool(self.SECRET_KEY and self.SECRET_KEY.strip())

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a trimmed list."""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    def safe_summary(self) -> dict[str, Any]:
        """Return non-sensitive configuration dictionary for diagnostic logging."""
        return {
            "APP_ENV": self.APP_ENV,
            "DEBUG": self.DEBUG,
            "PROJECT_NAME": self.PROJECT_NAME,
            "API_V1_STR": self.API_V1_STR,
            "HOST": self.HOST,
            "PORT": self.PORT,
            "CORS_ORIGINS": self.cors_origins_list,
            "DATABASE_URL_SCHEME": self.DATABASE_URL.split("://")[0]
            if "://" in self.DATABASE_URL
            else "unknown",
            "REDIS_URL_SCHEME": self.REDIS_URL.split("://")[0]
            if "://" in self.REDIS_URL
            else "unknown",
            "SEMGREP_RULES_CONFIG": self.SEMGREP_RULES_CONFIG,
            "OSV_SCANNER_ENABLED": self.OSV_SCANNER_ENABLED,
            "GITLEAKS_ENABLED": self.GITLEAKS_ENABLED,
            "LLM_PROVIDER": self.LLM_PROVIDER,
            "LLM_MODEL": self.LLM_MODEL,
            "LLM_API_KEY_SET": bool(self.LLM_API_KEY.strip()),
            "SANDBOX_EXECUTION_TIMEOUT_SECONDS": self.SANDBOX_EXECUTION_TIMEOUT_SECONDS,
            "SANDBOX_MAX_MEMORY_MB": self.SANDBOX_MAX_MEMORY_MB,
            "SANDBOX_ALLOW_NETWORK": self.SANDBOX_ALLOW_NETWORK,
        }


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
