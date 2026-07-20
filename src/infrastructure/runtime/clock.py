"""Clock adapter for production runtime (INF-006)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.ports.clock import Clock


class SystemClock(Clock):
    """Provide timezone-aware UTC wall-clock timestamps."""

    def now(self) -> datetime:
        return datetime.now(tz=UTC)

