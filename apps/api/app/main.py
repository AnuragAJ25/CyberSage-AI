"""CyberSage AI - FastAPI Application Entry Point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.core.logging import logger, setup_logging


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Lifespan event handler for application startup and shutdown."""
    settings = get_settings()
    setup_logging(debug=settings.DEBUG)
    logger.info(
        "Starting %s v%s in %s mode (Debug=%s)",
        settings.PROJECT_NAME,
        __version__,
        settings.APP_ENV,
        settings.DEBUG,
    )
    yield
    logger.info("Shutting down %s", settings.PROJECT_NAME)


def create_application() -> FastAPI:
    """Instantiate and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-Assisted Cybersecurity Detection, Analysis, and Remediation Platform",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS Middleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Centralized Error Handlers
    register_error_handlers(app)

    # Include Versioned API Routes
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

    @app.get("/", tags=["Root"], summary="API Root Metadata")
    async def root() -> dict[str, str]:
        """Root endpoint returning service identity and navigation links."""
        return {
            "name": settings.PROJECT_NAME,
            "version": __version__,
            "status": "operational",
            "docs": "/docs",
            "health": f"{settings.API_V1_STR}/health",
            "ready": f"{settings.API_V1_STR}/ready",
        }

    return app


app = create_application()
