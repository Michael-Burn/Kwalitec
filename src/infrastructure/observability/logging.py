"""Structured JSON logging for operational events."""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any


class JsonLogFormatter(logging.Formatter):
    """Format log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        fields = getattr(record, "structured_fields", None)
        if isinstance(fields, dict):
            payload.update(fields)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=True)


def configure_structured_logging(
    *,
    level: str = "INFO",
    structured: bool = True,
    stream: Any | None = None,
) -> None:
    """Configure the root logger for structured or plain operational logging."""
    root = logging.getLogger()
    root.handlers.clear()
    handler = logging.StreamHandler(stream or sys.stderr)
    if structured:
        handler.setFormatter(JsonLogFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))


class StructuredLogger:
    """Emit structured operational log records with optional captured history."""

    def __init__(
        self,
        name: str = "kwalitec.eos",
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or logging.getLogger(name)
        self._records: list[dict[str, Any]] = []

    @property
    def records(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._records)

    def clear(self) -> None:
        self._records.clear()

    def _emit(self, level: int, message: str, **fields: Any) -> dict[str, Any]:
        record = {"level": logging.getLevelName(level), "message": message, **fields}
        self._records.append(record)
        self._logger.log(level, message, extra={"structured_fields": fields})
        return record

    def info(self, message: str, **fields: Any) -> dict[str, Any]:
        return self._emit(logging.INFO, message, **fields)

    def warning(self, message: str, **fields: Any) -> dict[str, Any]:
        return self._emit(logging.WARNING, message, **fields)

    def error(self, message: str, **fields: Any) -> dict[str, Any]:
        return self._emit(logging.ERROR, message, **fields)

    def debug(self, message: str, **fields: Any) -> dict[str, Any]:
        return self._emit(logging.DEBUG, message, **fields)
