"""Health and Readiness Probes."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, Field

from app import __version__
from app.core.config import Settings, get_settings

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Liveness probe response schema."""

    status: str = Field(default="ok", description="Service liveness state (ok, degraded)")
    service: str = Field(default="cybersage-api", description="Service identifier")
    version: str = Field(description="Service semantic version")
    environment: str = Field(description="Running environment name")
    timestamp: datetime = Field(description="UTC timestamp of the probe")


class SubsystemDetail(BaseModel):
    """Subsystem state breakdown."""

    status: str = Field(
        description="Subsystem status: ready, planned, standby, unconfigured, or degraded"
    )
    phase: str = Field(description="Roadmap phase where full subsystem functionality is delivered")
    description: str = Field(description="Transparent explanation of current operational status")


class ReadinessResponse(BaseModel):
    """Honest readiness probe response schema."""

    status: str = Field(
        default="ready", description="Overall API readiness state: ready, degraded, or not_ready"
    )
    service: str = Field(default="cybersage-api", description="Service identifier")
    version: str = Field(description="Service semantic version")
    subsystems: dict[str, SubsystemDetail] = Field(
        description="Transparent breakdown of all core and planned subsystems"
    )
    checks: dict[str, str] = Field(
        description="Flat status mapping for backward-compatible monitoring tools"
    )
    timestamp: datetime = Field(description="UTC timestamp of the probe")


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Returns whether the FastAPI application process is alive and receiving traffic.",
)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Return 200 OK if service process is healthy."""
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
    summary="Readiness Probe",
    description=(
        "Verifies that required API subsystems are operational. "
        "Unimplemented scanners, AI orchestration, and sandboxing are transparently "
        "reported as 'planned' rather than prematurely claiming readiness."
    ),
)
async def readiness_check(
    response: Response,
    settings: Settings = Depends(get_settings),
) -> ReadinessResponse:
    """Return honest readiness diagnostics without false claims."""
    is_config_ready = settings.is_configured

    subsystems: dict[str, SubsystemDetail] = {
        "api_core": SubsystemDetail(
            status="ready",
            phase="Phase 1",
            description="FastAPI routing, middleware, and request validation active.",
        ),
        "configuration": SubsystemDetail(
            status="ready" if is_config_ready else "unconfigured",
            phase="Phase 1",
            description="Environment settings loaded and validated.",
        ),
        "scanners": SubsystemDetail(
            status="planned",
            phase="Phase 2",
            description="Semgrep (SAST), OSV-Scanner (SCA), and Gitleaks (Secrets) pipeline planned.",
        ),
        "ai_orchestration": SubsystemDetail(
            status="planned",
            phase="Phase 3",
            description="LangGraph stateful workflow coordinator and explainer agent planned.",
        ),
        "verification_sandbox": SubsystemDetail(
            status="planned",
            phase="Phase 4",
            description="Disposable container verification sandbox planned.",
        ),
    }

    checks: dict[str, str] = {name: detail.status for name, detail in subsystems.items()}

    # If configuration is not ready, the API cannot accept operational traffic
    if not is_config_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        overall_status = "not_ready"
    else:
        overall_status = "ready"

    return ReadinessResponse(
        status=overall_status,
        service="cybersage-api",
        version=__version__,
        subsystems=subsystems,
        checks=checks,
        timestamp=datetime.now(UTC),
    )
