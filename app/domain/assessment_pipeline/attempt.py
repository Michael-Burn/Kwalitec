"""Activity attempt — one discrete try at a learning activity."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any


def _freeze_metadata(metadata: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(metadata or {}))


@dataclass(frozen=True)
class ActivityAttempt:
    """Immutable record of one learner attempt at an activity."""

    attempt_id: str
    twin_id: str
    student_id: str
    activity_id: str
    activity_kind: str
    attempted_at: datetime
    event_id: str = ""
    curriculum_entity_id: str = ""
    concept_ids: tuple[str, ...] = ()
    score: float | None = None
    correct: bool | None = None
    duration_seconds: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.attempt_id or "").strip():
            raise ValueError("attempt_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.activity_id or "").strip():
            raise ValueError("activity_id is required")
        when = self.attempted_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "attempted_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "concept_ids", tuple(self.concept_ids or ()))
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))
