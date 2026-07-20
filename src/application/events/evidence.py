"""Application events for evidence coordination."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.events.base import ApplicationEvent, utc_now


@dataclass(frozen=True, slots=True)
class EvidenceRecordedApplicationEvent(ApplicationEvent):
    """Emitted after educational evidence has been recorded via application."""

    evidence_id: str
    student_id: str

    @classmethod
    def create(
        cls,
        *,
        evidence_id: str,
        student_id: str,
        occurred_at: datetime | None = None,
    ) -> EvidenceRecordedApplicationEvent:
        return cls(
            occurred_at=occurred_at or utc_now(),
            evidence_id=evidence_id,
            student_id=student_id,
        )
