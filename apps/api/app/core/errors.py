"""Centralized Error Handling and Custom Exceptions."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import logger


class CyberSageError(Exception):
    """Base exception for all CyberSage application errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class NotFoundError(CyberSageError):
    """Resource not found error."""

    def __init__(
        self, message: str = "Resource not found", details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class SecurityValidationError(CyberSageError):
    """Security validation or SSRF block error."""

    def __init__(
        self, message: str = "Security validation failed", details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(
            message=message,
            code="SECURITY_VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


def register_error_handlers(app: FastAPI) -> None:
    """Register centralized exception handlers on the FastAPI application."""

    @app.exception_handler(CyberSageError)
    async def cybersage_exception_handler(request: Request, exc: CyberSageError) -> JSONResponse:
        logger.warning(
            "CyberSage error occurred: %s (code=%s, status=%d, path=%s)",
            exc.message,
            exc.code,
            exc.status_code,
            request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                    "path": request.url.path,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.info("Request validation failed for path: %s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request parameters or payload",
                    "details": exc.errors(),
                    "path": request.url.path,
                }
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": exc.detail,
                    "path": request.url.path,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "Unhandled server exception on %s: %s",
            request.url.path,
            str(exc),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred.",
                    "path": request.url.path,
                }
            },
        )
