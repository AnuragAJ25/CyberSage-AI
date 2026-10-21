"""Tests for Service Root, Health, Readiness Probes, and Configuration Hardening."""

import pytest
from httpx import ASGITransport, AsyncClient

from app import __version__
from app.core.config import Settings, get_settings
from app.main import create_application


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient) -> None:
    """Verify that root endpoint returns operational metadata."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "CyberSage AI"
    assert data["version"] == __version__
    assert data["status"] == "operational"
    assert data["health"] == "/api/v1/health"
    assert data["ready"] == "/api/v1/ready"


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient) -> None:
    """Verify that /api/v1/health returns liveness status ok and metadata."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "cybersage-api"
    assert data["version"] == __version__
    assert "environment" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_readiness_check_endpoint_honest_states(async_client: AsyncClient) -> None:
    """Verify that /api/v1/ready honestly reports planned subsystems rather than claiming false readiness."""
    response = await async_client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["service"] == "cybersage-api"
    assert data["version"] == __version__

    # Verify flat checks mapping
    checks = data["checks"]
    assert checks["api_core"] == "ready"
    assert checks["configuration"] == "ready"
    assert checks["scanners"] == "planned"
    assert checks["ai_orchestration"] == "planned"
    assert checks["verification_sandbox"] == "planned"

    # Verify detailed subsystem breakdown
    subsystems = data["subsystems"]
    assert subsystems["scanners"]["status"] == "planned"
    assert subsystems["scanners"]["phase"] == "Phase 2"
    assert "Semgrep" in subsystems["scanners"]["description"]
    assert "OSV-Scanner" in subsystems["scanners"]["description"]

    assert subsystems["ai_orchestration"]["status"] == "planned"
    assert subsystems["ai_orchestration"]["phase"] == "Phase 3"

    assert subsystems["verification_sandbox"]["status"] == "planned"
    assert subsystems["verification_sandbox"]["phase"] == "Phase 4"


@pytest.mark.asyncio
async def test_readiness_check_unconfigured_fallback() -> None:
    """Verify that /api/v1/ready returns 503 when configuration is unconfigured."""
    unconfigured_settings = Settings(
        APP_ENV="development",
        SECRET_KEY="",
    )

    app = create_application()
    app.dependency_overrides[get_settings] = lambda: unconfigured_settings

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/ready")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not_ready"
        assert data["checks"]["configuration"] == "unconfigured"


def test_production_secret_validation_rejects_weak_secrets() -> None:
    """Verify that Settings raises ValueError when insecure secrets are provided in production."""
    # Placeholder key in production
    with pytest.raises(ValueError, match="cannot be a known default or placeholder"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            SECRET_KEY="change_this_to_a_secure_random_string_min_32_chars",
        )

    # Empty key in production
    with pytest.raises(ValueError, match="SECRET_KEY must be provided"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            SECRET_KEY="",
        )

    # Short key in production (< 32 chars)
    with pytest.raises(ValueError, match="must be at least 32 characters"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            SECRET_KEY="short-secret-key-too-short",
        )

    # Debug=True in production
    with pytest.raises(ValueError, match="DEBUG must be set to False"):
        Settings(
            APP_ENV="production",
            DEBUG=True,
            SECRET_KEY="a-sufficiently-long-production-secret-key-at-least-32-chars",
        )


def test_production_secret_validation_accepts_strong_secret() -> None:
    """Verify that Settings accepts strong secrets in production."""
    settings = Settings(
        APP_ENV="production",
        DEBUG=False,
        SECRET_KEY="super-strong-production-secret-key-that-exceeds-32-characters-entropy",
    )
    assert settings.is_production is True
    assert settings.is_configured is True


def test_safe_summary_does_not_leak_raw_secret() -> None:
    """Verify that safe_summary masks sensitive secret keys."""
    raw_secret = "my-secret-key-12345678901234567890123456"
    settings = Settings(APP_ENV="development", SECRET_KEY=raw_secret)
    summary = settings.safe_summary()
    assert "SECRET_KEY" not in summary
    assert raw_secret not in str(summary)
