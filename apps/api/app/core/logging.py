"""Structured Logging Setup for CyberSage AI."""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """Formats log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Include custom attributes if present
        for key, value in record.__dict__.items():
            if key not in (
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
            ):
                log_entry[key] = value

        return json.dumps(log_entry)


def setup_logging(debug: bool = False, json_output: bool = False) -> logging.Logger:
    """Configure and return root logger for CyberSage AI."""
    logger = logging.getLogger("cybersage")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG if debug else logging.INFO)

        if json_output:
            handler.setFormatter(JSONFormatter())
        else:
            handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )

        logger.addHandler(handler)

    return logger


logger = setup_logging()
