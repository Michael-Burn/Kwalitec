"""Process-scoped Founder Validation telemetry (FV-001).

Records observational lifecycle outcomes for product metrics. Does not
mutate educational state or invent recommendations.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class LifecycleOutcomeEvent:
    """One observed LP-001 / VP-001 lifecycle outcome."""

    kind: str
    succeeded: bool
    student_id: int | None
    operation_type: str | None
    duration_ms: float | None
    decision_refresh_ms: float | None
    failure_cause: str | None
    skipped: bool
    timestamp: str
    correlation_id: str | None = None


class FounderValidationTelemetry:
    """Thread-safe observational store for FV-001 product metrics."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: list[LifecycleOutcomeEvent] = []
        self._system_failures: int = 0

    def record_lifecycle_outcome(
        self,
        *,
        kind: str,
        succeeded: bool,
        student_id: int | None = None,
        operation_type: str | None = None,
        duration_ms: float | None = None,
        decision_refresh_ms: float | None = None,
        failure_cause: str | None = None,
        skipped: bool = False,
        correlation_id: str | None = None,
        timestamp: str | None = None,
    ) -> LifecycleOutcomeEvent:
        """Append one lifecycle observation."""
        event = LifecycleOutcomeEvent(
            kind=kind,
            succeeded=succeeded,
            student_id=student_id,
            operation_type=operation_type,
            duration_ms=duration_ms,
            decision_refresh_ms=decision_refresh_ms,
            failure_cause=failure_cause,
            skipped=skipped,
            timestamp=timestamp or _utc_now_iso(),
            correlation_id=correlation_id,
        )
        with self._lock:
            self._events.append(event)
        logger.info(
            "fv001_lifecycle kind=%s succeeded=%s skipped=%s student_id=%s "
            "operation_type=%s decision_refresh_ms=%s",
            kind,
            succeeded,
            skipped,
            student_id,
            operation_type,
            decision_refresh_ms,
        )
        return event

    def record_system_failure(
        self,
        *,
        kind: str,
        student_id: int | None = None,
        cause: str | None = None,
        correlation_id: str | None = None,
    ) -> LifecycleOutcomeEvent:
        """Record an unexpected fail-open exception during validation paths."""
        with self._lock:
            self._system_failures += 1
        return self.record_lifecycle_outcome(
            kind=kind,
            succeeded=False,
            student_id=student_id,
            failure_cause=cause,
            correlation_id=correlation_id,
        )

    def snapshot(self) -> dict[str, Any]:
        """Return a JSON-serialisable process snapshot."""
        with self._lock:
            events = list(self._events)
            failures = self._system_failures

        def _count(kind: str, *, succeeded: bool | None = None) -> int:
            total = 0
            for event in events:
                if event.kind != kind or event.skipped:
                    continue
                if succeeded is None or event.succeeded is succeeded:
                    total += 1
            return total

        refresh_samples = [
            float(e.decision_refresh_ms)
            for e in events
            if e.decision_refresh_ms is not None and e.succeeded
        ]
        return {
            "event_count": len(events),
            "system_failures": failures,
            "onboard_attempted": _count("onboard"),
            "onboard_succeeded": _count("onboard", succeeded=True),
            "evidence_attempted": _count("evidence"),
            "evidence_succeeded": _count("evidence", succeeded=True),
            "decision_refresh_samples_ms": refresh_samples,
            "computed_at": _utc_now_iso(),
        }

    def clear(self) -> None:
        """Reset process-local state (tests only)."""
        with self._lock:
            self._events.clear()
            self._system_failures = 0


DEFAULT_FV_TELEMETRY = FounderValidationTelemetry()


def decision_refresh_ms_from_result(result: Any) -> float | None:
    """Sum educational_decisions stage durations from a LifecycleResult."""
    stages = getattr(result, "stages", None) or ()
    total = 0.0
    found = False
    for stage in stages:
        name = getattr(getattr(stage, "stage", None), "value", None) or getattr(
            stage, "stage", None
        )
        if str(name) != "educational_decisions":
            continue
        duration = getattr(stage, "duration_ms", None)
        if duration is None:
            continue
        total += float(duration)
        found = True
    return total if found else None


def total_duration_ms_from_result(result: Any) -> float | None:
    """Sum all stage durations from a LifecycleResult."""
    stages = getattr(result, "stages", None) or ()
    if not stages:
        return None
    return float(sum(float(getattr(s, "duration_ms", 0.0) or 0.0) for s in stages))
