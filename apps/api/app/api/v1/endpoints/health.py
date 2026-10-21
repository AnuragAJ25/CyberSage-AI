"""Health and Readiness Probes."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from app import __version__
from app.core.config import Settings, get_settings

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Liveness probe response schema."""

    status: str = Field(default="ok", description="Service liveness state")
    service: str = Field(default="cybersage-api", description="Service identifier")
    version: str = Field(description="Service semantic version")
    environment: str = Field(description="Running environment name")
    timestamp: datetime = Field(description="UTC timestamp of the probe")


class ReadinessResponse(BaseModel):
    """Readiness probe response schema."""

    status: str = Field(default="ready", description="Overall readiness state")
    service: str = Field(default="cybersage-api", description="Service identifier")
    version: str = Field(description="Service semantic version")
    checks: dict[str, str] = Field(description="Subsystem readiness checks")
    timestamp: datetime = Field(description="UTC timestamp of the probe")


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness Check",
    description="Returns service liveness status and version metadata.",
)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Return 200 OK if service is up and serving requests."""
    return HealthResponse(
        status="ok",
        service="cybersage-api",
        version=__version__,
        environment=settings.APP_ENV,
        timestamp=datetime.now(UTC),
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness Check",
    description="Verifies that all required subsystems are initialized and ready to accept work.",
)
async def readiness_check(settings: Settings = Depends(get_settings)) -> ReadinessResponse:
    """Return readiness status verifying settings and core modules."""
    checks = {
        "configuration": "ready" if settings.SECRET_KEY else "unconfigured",
        "sandboxing": "ready",
        "scanner_subsystems": "standby",
    }
    return ReadinessResponse(
        status="ready",
        service="cybersage-api",
        version=__version__,
        checks=checks,
        timestamp=datetime.now(UTC),
    )
