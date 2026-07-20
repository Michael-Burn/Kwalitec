"""Application events for Digital Twin coordination."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.events.base import ApplicationEvent, utc_now


@dataclass(frozen=True, slots=True)
class DigitalTwinUpdatedApplicationEvent(ApplicationEvent):
    """Emitted after a Twin update has been coordinated and committed."""

    twin_id: str
    student_id: str
    update_kind: str

    @classmethod
    def create(
        cls,
        *,
        twin_id: str,
        student_id: str,
        update_kind: str,
        occurred_at: datetime | None = None,
    ) -> DigitalTwinUpdatedApplicationEvent:
        return cls(
            occurred_at=occurred_at or utc_now(),
            twin_id=twin_id,
            student_id=student_id,
            update_kind=update_kind,
        )
