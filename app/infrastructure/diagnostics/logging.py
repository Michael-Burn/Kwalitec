"""Structured logging helpers — operational fields only."""

from __future__ import annotations

import logging
from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext


class StructuredLogger:
    """Emit structured operational log records with correlation fields."""

    def __init__(
        self,
        name: str = "kwalitec.v2.infrastructure",
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or logging.getLogger(name)
        self._records: list[dict[str, Any]] = []

    @property
    def records(self) -> tuple[dict[str, Any], ...]:
        """Captured records (test / diagnostics aid)."""
        return tuple(self._records)

    def clear(self) -> None:
        """Clear captured records."""
        self._records.clear()

    def _emit(self, level: int, message: str, **fields: Any) -> dict[str, Any]:
        ids = CorrelationContext.current()
        record = {
            "level": logging.getLevelName(level),
            "message": message,
            "correlation_id": ids.correlation_id,
            "causation_id": ids.causation_id,
            **fields,
        }
        self._records.append(record)
        self._logger.log(level, message, extra={"v2_fields": fields})
        return record

    def info(self, message: str, **fields: Any) -> dict[str, Any]:
        """Log an informational operational event."""
        return self._emit(logging.INFO, message, **fields)

    def warning(self, message: str, **fields: Any) -> dict[str, Any]:
        """Log a warning."""
        return self._emit(logging.WARNING, message, **fields)

    def error(self, message: str, **fields: Any) -> dict[str, Any]:
        """Log an error."""
        return self._emit(logging.ERROR, message, **fields)

    def debug(self, message: str, **fields: Any) -> dict[str, Any]:
        """Log a debug record."""
        return self._emit(logging.DEBUG, message, **fields)
