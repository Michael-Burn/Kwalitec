"""Adapter diagnostics — operational health of infrastructure adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class AdapterHealth:
    """Health snapshot for one adapter."""

    adapter_id: str
    available: bool
    version: str
    checked_at: datetime
    details: dict[str, Any] = field(default_factory=dict)


class AdapterDiagnostics:
    """Collect and report adapter operational health."""

    def __init__(self) -> None:
        self._reports: dict[str, AdapterHealth] = {}
        self._call_counts: dict[str, int] = {}
        self._error_counts: dict[str, int] = {}

    def record_health(
        self,
        adapter_id: str,
        *,
        available: bool,
        version: str = "1.0.0",
        details: dict[str, Any] | None = None,
    ) -> AdapterHealth:
        """Record a health observation."""
        report = AdapterHealth(
            adapter_id=adapter_id,
            available=available,
            version=version,
            checked_at=datetime.now(tz=UTC),
            details=dict(details or {}),
        )
        self._reports[adapter_id] = report
        return report

    def record_call(self, adapter_id: str, *, error: bool = False) -> None:
        """Increment operational call / error counters."""
        self._call_counts[adapter_id] = self._call_counts.get(adapter_id, 0) + 1
        if error:
            self._error_counts[adapter_id] = (
                self._error_counts.get(adapter_id, 0) + 1
            )

    def health(self, adapter_id: str) -> AdapterHealth | None:
        """Return the latest health report for an adapter."""
        return self._reports.get(adapter_id)

    def all_health(self) -> tuple[AdapterHealth, ...]:
        """Return all recorded health reports."""
        return tuple(self._reports.values())

    def metrics(self) -> dict[str, Any]:
        """Operational adapter metrics (not educational)."""
        return {
            "adapters": sorted(self._reports),
            "call_counts": dict(self._call_counts),
            "error_counts": dict(self._error_counts),
            "available": {
                k: v.available for k, v in self._reports.items()
            },
        }
