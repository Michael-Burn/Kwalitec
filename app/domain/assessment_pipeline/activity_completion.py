"""Activity completion — structured completion of one learning activity."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any


def _freeze_metadata(metadata: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(metadata or {}))


@dataclass(frozen=True)
class ActivityCompletion:
    """Immutable completion record for a discrete learning activity."""

    completion_id: str
    twin_id: str
    student_id: str
    activity_id: str
    activity_kind: str
    completed_at: datetime
    event_id: str = ""
    mission_id: str = ""
    step_id: str = ""
    concept_ids: tuple[str, ...] = ()
    outcome_achieved: bool = True
    score: float | None = None
    duration_seconds: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.completion_id or "").strip():
            raise ValueError("completion_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.activity_id or "").strip():
            raise ValueError("activity_id is required")
        when = self.completed_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "completed_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "concept_ids", tuple(self.concept_ids or ()))
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))
