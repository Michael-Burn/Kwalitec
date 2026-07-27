"""Immutable assessment events — educational evidence before Twin reasoning.

Assessment events record learner activity. They do not infer educational state.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any


class AssessmentEventType(StrEnum):
    """Canonical learner-activity event types for AP-001."""

    QUESTION_ATTEMPT = "question_attempt"
    QUIZ_SUBMISSION = "quiz_submission"
    MISSION_STEP_COMPLETION = "mission_step_completion"
    MISSION_COMPLETION = "mission_completion"
    REVISION_SESSION = "revision_session"
    WORKED_EXAMPLE_COMPLETION = "worked_example_completion"
    FORMULA_RECALL = "formula_recall"
    REFLECTION_SUBMISSION = "reflection_submission"
    STUDY_SESSION_COMPLETION = "study_session_completion"


def _freeze_metadata(metadata: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(metadata or {}))


@dataclass(frozen=True)
class AssessmentEvent:
    """One immutable learner-activity event.

    Append-only educational evidence. Never mutated after creation.
    """

    event_id: str
    event_type: AssessmentEventType
    twin_id: str
    student_id: str
    occurred_at: datetime
    activity_id: str = ""
    curriculum_entity_id: str = ""
    curriculum_entity_kind: str = ""
    concept_ids: tuple[str, ...] = ()
    mission_id: str = ""
    step_id: str = ""
    source: str = ""
    score: float | None = None
    correct: bool | None = None
    duration_seconds: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.event_id or "").strip():
            raise ValueError("event_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.student_id or "").strip():
            raise ValueError("student_id is required")
        event_type = (
            self.event_type
            if isinstance(self.event_type, AssessmentEventType)
            else AssessmentEventType(str(self.event_type))
        )
        object.__setattr__(self, "event_type", event_type)
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "concept_ids", tuple(self.concept_ids or ()))
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))
        if self.score is not None:
            object.__setattr__(self, "score", float(self.score))
        if self.duration_seconds is not None:
            object.__setattr__(self, "duration_seconds", int(self.duration_seconds))

    @classmethod
    def create(
        cls,
        *,
        event_id: str,
        event_type: AssessmentEventType | str,
        twin_id: str,
        student_id: str,
        occurred_at: datetime | None = None,
        activity_id: str = "",
        curriculum_entity_id: str = "",
        curriculum_entity_kind: str = "",
        concept_ids: tuple[str, ...] | list[str] | None = None,
        mission_id: str = "",
        step_id: str = "",
        source: str = "",
        score: float | None = None,
        correct: bool | None = None,
        duration_seconds: int | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> AssessmentEvent:
        """Factory for a new immutable assessment event."""
        when = occurred_at or datetime.now(UTC).replace(tzinfo=None)
        return cls(
            event_id=event_id,
            event_type=(
                event_type
                if isinstance(event_type, AssessmentEventType)
                else AssessmentEventType(event_type)
            ),
            twin_id=twin_id,
            student_id=student_id,
            occurred_at=when,
            activity_id=activity_id or "",
            curriculum_entity_id=curriculum_entity_id or "",
            curriculum_entity_kind=curriculum_entity_kind or "",
            concept_ids=tuple(concept_ids or ()),
            mission_id=mission_id or "",
            step_id=step_id or "",
            source=source or "",
            score=score,
            correct=correct,
            duration_seconds=duration_seconds,
            metadata=_freeze_metadata(metadata),
        )
