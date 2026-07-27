"""Tutor response — complete evidence-backed reply to a student question."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.intelligent_tutor.coaching_message import CoachingMessage
from app.domain.intelligent_tutor.explanation import Explanation
from app.domain.intelligent_tutor.learning_hint import LearningHint


@dataclass(frozen=True)
class TutorResponse:
    """Full Tutor reply after evidence assembly and response generation."""

    response_id: str
    session_id: str
    twin_id: str
    question_id: str
    body: str
    explanation: Explanation
    supporting_evidence_ids: tuple[str, ...]
    suggested_next_action: str
    related_concepts: tuple[str, ...]
    recovery_guidance: str
    reflection_prompt: str
    hints: tuple[LearningHint, ...] = ()
    coaching: tuple[CoachingMessage, ...] = ()
    evidence_summaries: tuple[str, ...] = ()
    context_id: str = ""
    generation_backend: str = "deterministic_placeholder"
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if not (self.response_id or "").strip():
            raise ValueError("response_id is required")
        if not (self.session_id or "").strip():
            raise ValueError("session_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.body or "").strip():
            raise ValueError("response body is required")
        object.__setattr__(
            self,
            "supporting_evidence_ids",
            tuple(self.supporting_evidence_ids or ()),
        )
        object.__setattr__(self, "related_concepts", tuple(self.related_concepts or ()))
        object.__setattr__(self, "hints", tuple(self.hints or ()))
        object.__setattr__(self, "coaching", tuple(self.coaching or ()))
        object.__setattr__(
            self, "evidence_summaries", tuple(self.evidence_summaries or ())
        )
        when = self.created_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )

    def as_student_card(self) -> dict[str, str | list[str]]:
        """Simple projection for student Mission / Home surfaces."""
        return {
            "title": self.explanation.summary,
            "body": self.body,
            "next_action": self.suggested_next_action,
            "reflection": self.reflection_prompt,
            "related_concepts": list(self.related_concepts),
            "evidence_count": str(len(self.supporting_evidence_ids)),
        }
