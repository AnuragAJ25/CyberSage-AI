"""Tests for Service Root, Health, and Readiness Probes."""

import pytest
from httpx import AsyncClient

from app import __version__


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
async def test_readiness_check_endpoint(async_client: AsyncClient) -> None:
    """Verify that /api/v1/ready returns ready status and subsystem checks."""
    response = await async_client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["service"] == "cybersage-api"
    assert data["version"] == __version__
    assert "checks" in data
    assert data["checks"]["configuration"] == "ready"
    assert data["checks"]["sandboxing"] == "ready"
