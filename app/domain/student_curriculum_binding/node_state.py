"""Mutable curriculum node educational state (EI-004).

Stores learner-facing slots only. Does not compute mastery, forgetting,
recommendations, or any curriculum mutation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class CompletionStatus(StrEnum):
    """Learner completion disposition for a curriculum node."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class RevisionStatus(StrEnum):
    """Revision disposition slot (no forgetting-curve engine in EI-004)."""

    NOT_DUE = "not_due"
    DUE = "due"
    OVERDUE = "overdue"


_REVISION_RANK = {
    RevisionStatus.NOT_DUE.value: 0,
    RevisionStatus.DUE.value: 1,
    RevisionStatus.OVERDUE.value: 2,
}


@dataclass(frozen=True)
class NodeStateSnapshot:
    """Immutable view of one node's educational state."""

    node_stable_id: str
    node_kind: str
    mastery: float = 0.0
    confidence: float = 0.0
    revision_status: str = RevisionStatus.NOT_DUE.value
    attempts: int = 0
    total_study_time_minutes: int = 0
    last_interaction_at: datetime | None = None
    completion_status: str = CompletionStatus.NOT_STARTED.value
    evidence_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "node_stable_id": self.node_stable_id,
            "node_kind": self.node_kind,
            "mastery": self.mastery,
            "confidence": self.confidence,
            "revision_status": self.revision_status,
            "attempts": self.attempts,
            "total_study_time_minutes": self.total_study_time_minutes,
            "last_interaction_at": (
                self.last_interaction_at.isoformat()
                if self.last_interaction_at is not None
                else None
            ),
            "completion_status": self.completion_status,
            "evidence_count": self.evidence_count,
        }


def initial_node_state(node_stable_id: str, node_kind: str) -> NodeStateSnapshot:
    """Factory for the default educational state of a newly bound node."""
    return NodeStateSnapshot(
        node_stable_id=node_stable_id,
        node_kind=node_kind,
        mastery=0.0,
        confidence=0.0,
        revision_status=RevisionStatus.NOT_DUE.value,
        attempts=0,
        total_study_time_minutes=0,
        last_interaction_at=None,
        completion_status=CompletionStatus.NOT_STARTED.value,
        evidence_count=0,
    )


def worst_revision_status(statuses: list[str]) -> str:
    """Deterministic worst-case revision status across children."""
    if not statuses:
        return RevisionStatus.NOT_DUE.value
    return max(statuses, key=lambda s: _REVISION_RANK.get(s, 0))


def derive_completion_status(
    *,
    completed_count: int,
    in_progress_count: int,
    total_count: int,
) -> str:
    """Derive aggregate completion from child counts."""
    if total_count <= 0:
        return CompletionStatus.NOT_STARTED.value
    if completed_count >= total_count:
        return CompletionStatus.COMPLETED.value
    if completed_count > 0 or in_progress_count > 0:
        return CompletionStatus.IN_PROGRESS.value
    return CompletionStatus.NOT_STARTED.value
