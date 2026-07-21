"""LearningSessionOutcome — immutable facts from a completed study session.

Records what happened. Never diagnoses, recommends, or modifies educational
state. Values are observational copies forwarded from presentation / runtime
inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class CompletionStatus(StrEnum):
    """Observed session-completion posture (fact vocabulary only)."""

    COMPLETED = "completed"
    INCOMPLETE = "incomplete"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class LearningSessionOutcome:
    """Immutable observational outcome of one study session sitting.

    Attributes:
        student_id: Learner identity supplied by the caller.
        mission_id: Mission identity supplied by the caller.
        session_id: Runtime session identity when available.
        session_started: When the session started (caller-supplied).
        session_completed: When the session completed (caller-supplied).
        actual_duration_seconds: Observed duration in whole seconds, or None.
        completion_status: Observed completion posture.
        confidence: Student-reported confidence key or label (verbatim).
        difficulty: Student-reported difficulty key or label (verbatim).
        weak_concept: Student-noted weak concept text (verbatim).
        student_notes: Student notes text (verbatim).
        reflection_summary: Reflection summary text (verbatim / joined lines).
        mission_title: Display title copied from session / reflection inputs.
    """

    student_id: str
    mission_id: str
    session_id: str
    session_started: datetime | None
    session_completed: datetime | None
    actual_duration_seconds: int | None
    completion_status: CompletionStatus
    confidence: str
    difficulty: str
    weak_concept: str
    student_notes: str
    reflection_summary: str
    mission_title: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", _text(self.student_id))
        object.__setattr__(self, "mission_id", _text(self.mission_id))
        object.__setattr__(self, "session_id", _text(self.session_id))
        object.__setattr__(self, "confidence", _text(self.confidence))
        object.__setattr__(self, "difficulty", _text(self.difficulty))
        object.__setattr__(self, "weak_concept", _text(self.weak_concept))
        object.__setattr__(self, "student_notes", _text(self.student_notes))
        object.__setattr__(
            self, "reflection_summary", _text(self.reflection_summary)
        )
        object.__setattr__(self, "mission_title", _text(self.mission_title))

        if not isinstance(self.completion_status, CompletionStatus):
            raise ValueError("completion_status must be a CompletionStatus")

        if self.actual_duration_seconds is not None:
            if isinstance(self.actual_duration_seconds, bool) or not isinstance(
                self.actual_duration_seconds, int
            ):
                raise ValueError("actual_duration_seconds must be an int or None")
            if self.actual_duration_seconds < 0:
                raise ValueError("actual_duration_seconds must be >= 0")

        if (
            self.session_started is not None
            and self.session_completed is not None
            and self.session_completed < self.session_started
        ):
            raise ValueError(
                "session_completed must not precede session_started"
            )


def _text(value: str | None) -> str:
    if value is None:
        return ""
    return str(value).strip()
