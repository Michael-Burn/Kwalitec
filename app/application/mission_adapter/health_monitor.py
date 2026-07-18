"""Health monitoring for Mission Adapter engines and routing.

Observes availability, failures, fallbacks, routing consistency, and
comparison failures. Never alters routing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.application.mission_adapter.dto.routing_decision import RoutingMode


@dataclass
class HealthCounters:
    """Mutable counters for health observation (not a public DTO)."""

    invocations: int = 0
    successes: int = 0
    failures: int = 0
    fallbacks: int = 0
    comparison_runs: int = 0
    comparison_failures: int = 0
    comparison_divergences: int = 0
    routing_inconsistencies: int = 0
    v1_unavailable: int = 0
    v2_unavailable: int = 0
    by_mode: dict[str, int] = field(default_factory=dict)
    by_error: dict[str, int] = field(default_factory=dict)


class HealthMonitor:
    """Observe adapter health without influencing routing decisions."""

    def __init__(self, *, clock=None) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._counters = HealthCounters()
        self._last_event_at: datetime | None = None

    @property
    def counters(self) -> HealthCounters:
        """Current counter snapshot (mutable internal object)."""
        return self._counters

    def reset(self) -> None:
        """Reset all counters (tests / process reset)."""
        self._counters = HealthCounters()
        self._last_event_at = None

    def note_invocation(
        self,
        *,
        mode: RoutingMode,
        success: bool,
        fallback_used: bool = False,
        comparison_executed: bool = False,
        comparison_failed: bool = False,
        comparison_diverged: bool = False,
        error_type: str | None = None,
        v1_unavailable: bool = False,
        v2_unavailable: bool = False,
        routing_inconsistent: bool = False,
    ) -> None:
        """Record one adapter invocation observation."""
        c = self._counters
        c.invocations += 1
        if success:
            c.successes += 1
        else:
            c.failures += 1
        if fallback_used:
            c.fallbacks += 1
        if comparison_executed:
            c.comparison_runs += 1
        if comparison_failed:
            c.comparison_failures += 1
        if comparison_diverged:
            c.comparison_divergences += 1
        if v1_unavailable:
            c.v1_unavailable += 1
        if v2_unavailable:
            c.v2_unavailable += 1
        if routing_inconsistent:
            c.routing_inconsistencies += 1
        key = mode.value
        c.by_mode[key] = c.by_mode.get(key, 0) + 1
        if error_type:
            c.by_error[error_type] = c.by_error.get(error_type, 0) + 1
        self._last_event_at = self._clock()

    def status(
        self,
        *,
        v1_available: bool,
        v2_available: bool,
        routing_mode: RoutingMode,
        migration_phase: str,
    ) -> dict[str, object]:
        """Read-only health status payload (never mutates routing)."""
        c = self._counters
        return {
            "v1_available": v1_available,
            "v2_available": v2_available,
            "routing_mode": routing_mode.value,
            "migration_phase": migration_phase,
            "invocations": c.invocations,
            "successes": c.successes,
            "failures": c.failures,
            "fallback_frequency": (
                c.fallbacks / c.invocations if c.invocations else 0.0
            ),
            "comparison_runs": c.comparison_runs,
            "comparison_failures": c.comparison_failures,
            "comparison_divergences": c.comparison_divergences,
            "routing_inconsistencies": c.routing_inconsistencies,
            "v1_unavailable_count": c.v1_unavailable,
            "v2_unavailable_count": c.v2_unavailable,
            "by_mode": dict(c.by_mode),
            "by_error": dict(c.by_error),
            "last_event_at": (
                self._last_event_at.isoformat() if self._last_event_at else None
            ),
            "healthy": c.failures == 0
            and c.comparison_failures == 0
            and c.routing_inconsistencies == 0,
        }
