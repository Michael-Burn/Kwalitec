"""Activity projection — one focused learning activity in the session.

Presentation only. Question content and sequencing arrive from ports.
Evidence recording remains invisible and owned by the educational kernel.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ActivityPhase(StrEnum):
    """Presentation phase of a learning activity."""

    READY = "ready"
    ANSWERING = "answering"
    EXPLAINED = "explained"
    COMPLETED = "completed"


# Internal engine terms must never appear in learner-facing activity copy.
FORBIDDEN_ACTIVITY_TERMS: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "adaptive decision",
    "learning orchestrator",
    "mission engine",
    "curriculum graph",
    "evidence spine",
    "mastery score",
)


@dataclass(frozen=True)
class ActivityProjection:
    """Domain projection for a single Learning Activity surface.

    Displays question, context, supporting material, optional hints,
    answer area guidance, progress, and next action — nothing else.
    """

    activity_id: str
    session_id: str
    question: str = ""
    context: str = ""
    supporting_material: str = ""
    hints: tuple[str, ...] = ()
    answer_prompt: str = "Your answer"
    explanation: str = ""
    phase: ActivityPhase = ActivityPhase.READY
    activity_index: int = 1
    activities_total: int = 1
    next_action_label: str = "Continue"
    topic_title: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        activity_id: str,
        session_id: str,
        *,
        question: str = "",
        context: str = "",
        supporting_material: str = "",
        hints: list[str] | tuple[str, ...] | None = None,
        answer_prompt: str = "Your answer",
        explanation: str = "",
        phase: ActivityPhase | str = ActivityPhase.READY,
        activity_index: int = 1,
        activities_total: int = 1,
        next_action_label: str = "Continue",
        topic_title: str = "",
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
    ) -> ActivityProjection:
        """Build an activity projection from opaque port facts."""
        if activity_index < 1:
            raise ValueError("activity_index must be >= 1")
        if activities_total < 1:
            raise ValueError("activities_total must be >= 1")
        if activity_index > activities_total:
            raise ValueError("activity_index cannot exceed activities_total")
        cleaned_hints = tuple(
            h.strip() for h in (hints or ()) if isinstance(h, str) and h.strip()
        )
        return cls(
            activity_id=_require_non_empty(activity_id, "activity_id"),
            session_id=_require_non_empty(session_id, "session_id"),
            question=(question or "").strip(),
            context=(context or "").strip(),
            supporting_material=(supporting_material or "").strip(),
            hints=cleaned_hints,
            answer_prompt=(answer_prompt or "Your answer").strip() or "Your answer",
            explanation=(explanation or "").strip(),
            phase=_resolve_phase(phase),
            activity_index=int(activity_index),
            activities_total=int(activities_total),
            next_action_label=(next_action_label or "Continue").strip() or "Continue",
            topic_title=(topic_title or "").strip(),
            metadata=tuple(metadata or ()),
        )

    @property
    def has_hints(self) -> bool:
        """True when supporting hints are available."""
        return bool(self.hints)

    @property
    def has_explanation(self) -> bool:
        """True when an explanation is present."""
        return bool(self.explanation)

    @property
    def is_final_activity(self) -> bool:
        """True when this is the last activity in the session sequence."""
        return self.activity_index >= self.activities_total


def is_student_safe_copy(text: str) -> bool:
    """True when ``text`` contains no forbidden internal terms."""
    lowered = (text or "").lower()
    return not any(term in lowered for term in FORBIDDEN_ACTIVITY_TERMS)


def _resolve_phase(value: ActivityPhase | str) -> ActivityPhase:
    if isinstance(value, ActivityPhase):
        return value
    return ActivityPhase(str(value).strip().lower())


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
