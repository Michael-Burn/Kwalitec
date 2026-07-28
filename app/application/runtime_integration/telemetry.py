"""Fallback / adoption telemetry for Runtime Integration (RI-001).

Process-scoped observational store. Never mutates educational state.
Aggregation methods support RI-005 readiness measurement.
"""

from __future__ import annotations

import logging
import threading
from datetime import UTC, datetime

from app.application.runtime_integration.dto import (
    AdoptionEvent,
    FallbackEvent,
    FallbackReason,
    IntegrationSurface,
    TelemetrySnapshot,
)

logger = logging.getLogger(__name__)


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class RuntimeIntegrationTelemetry:
    """Record and aggregate preferred-authority vs fallback usage."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._fallbacks: list[FallbackEvent] = []
        self._adoptions: list[AdoptionEvent] = []

    def record_fallback(
        self,
        *,
        student_id: int,
        subject: str | None,
        reason: FallbackReason,
        surface: IntegrationSurface,
        missing_prerequisite: str | None = None,
        instance_id: str | None = None,
        timestamp: str | None = None,
    ) -> FallbackEvent:
        event = FallbackEvent(
            student_id=student_id,
            subject=subject,
            reason=reason,
            timestamp=timestamp or _utc_now_iso(),
            missing_prerequisite=missing_prerequisite,
            surface=surface,
            instance_id=instance_id,
        )
        with self._lock:
            self._fallbacks.append(event)
        logger.info(
            "ri001_runtime_a_fallback student_id=%s subject=%s reason=%s "
            "surface=%s missing=%s instance_id=%s",
            student_id,
            subject,
            reason.value,
            surface.value,
            missing_prerequisite,
            instance_id,
        )
        return event

    def record_educational_intelligence(
        self,
        *,
        student_id: int,
        subject: str | None,
        surface: IntegrationSurface,
        instance_id: str,
        decision_id: str,
        timestamp: str | None = None,
    ) -> AdoptionEvent:
        event = AdoptionEvent(
            student_id=student_id,
            subject=subject,
            timestamp=timestamp or _utc_now_iso(),
            surface=surface,
            instance_id=instance_id,
            decision_id=decision_id,
        )
        with self._lock:
            self._adoptions.append(event)
        logger.info(
            "ri001_educational_intelligence student_id=%s subject=%s "
            "surface=%s instance_id=%s decision_id=%s",
            student_id,
            subject,
            surface.value,
            instance_id,
            decision_id,
        )
        return event

    def snapshot(self) -> TelemetrySnapshot:
        with self._lock:
            fallbacks = list(self._fallbacks)
            adoptions = list(self._adoptions)

        by_reason: dict[str, int] = {}
        for event in fallbacks:
            key = event.reason.value
            by_reason[key] = by_reason.get(key, 0) + 1

        return TelemetrySnapshot(
            total_requests=len(fallbacks) + len(adoptions),
            educational_intelligence_count=len(adoptions),
            fallback_count=len(fallbacks),
            migrated_users=frozenset(e.student_id for e in adoptions),
            fallback_users=frozenset(e.student_id for e in fallbacks),
            fallback_by_reason=by_reason,
        )

    def fallback_rate(self) -> float:
        return self.snapshot().fallback_rate

    def migrated_user_count(self) -> int:
        return len(self.snapshot().migrated_users)

    def educational_intelligence_adoption_pct(self) -> float:
        return self.snapshot().educational_intelligence_adoption_pct

    def reset(self) -> None:
        """Clear process-scoped counters (tests only)."""
        with self._lock:
            self._fallbacks.clear()
            self._adoptions.clear()


# Shared process default for production wiring / RI-005 aggregation.
DEFAULT_TELEMETRY = RuntimeIntegrationTelemetry()
