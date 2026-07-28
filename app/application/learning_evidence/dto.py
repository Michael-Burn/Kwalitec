"""DTOs for Learning Evidence Engine services (EI-005)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.domain.learning_evidence.evidence_event import EvidenceEvent
from app.domain.learning_evidence.summary import EvidenceCountSummary


@dataclass(frozen=True)
class RecordEvidenceResult:
    """Outcome of appending one evidence event."""

    event: EvidenceEvent
    created: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "event": self.event.to_dict(),
            "created": self.created,
        }


@dataclass(frozen=True)
class EvidenceHistoryView:
    """Chronological evidence history for a query scope."""

    instance_id: str | None
    student_id: int | None
    node_stable_id: str | None
    evidence_type: str | None
    events: tuple[EvidenceEvent, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "student_id": self.student_id,
            "node_stable_id": self.node_stable_id,
            "evidence_type": self.evidence_type,
            "events": [e.to_dict() for e in self.events],
            "count": len(self.events),
        }


@dataclass(frozen=True)
class EvidenceSummaryView:
    """Evidence count summary for a Student Curriculum Instance."""

    instance_id: str
    node_stable_id: str | None
    summary: EvidenceCountSummary

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "node_stable_id": self.node_stable_id,
            "summary": self.summary.to_dict(),
        }


def format_dt(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()
