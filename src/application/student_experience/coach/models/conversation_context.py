"""ConversationContext — deterministic coaching conversation scaffolding."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.coach.errors import CoachInvariantViolation
from application.student_experience.coach.ids import ConversationId
from application.student_experience.coach.models.suggested_questions import (
    SuggestedQuestions,
)


@dataclass(frozen=True, slots=True)
class ConversationContext:
    """Immutable conversation scaffolding for the AI Learning Coach.

    Holds deterministic opening copy and suggested questions. Downstream
    LLM adapters (outside this package) may consume this context — this
    package never invokes them.
    """

    conversation_id: ConversationId
    student_id: str
    composed_at: datetime
    opening_message: str
    focus_summary: str
    suggested_questions: SuggestedQuestions
    context_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.conversation_id, ConversationId):
            raise CoachInvariantViolation(
                "conversation_id must be a ConversationId",
                invariant="ConversationContext.conversation_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise CoachInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ConversationContext.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.composed_at, datetime):
            raise CoachInvariantViolation(
                "composed_at must be a datetime",
                invariant="ConversationContext.composed_at.type",
            )
        for name in ("opening_message", "focus_summary", "context_digest"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ConversationContext.{name}.required",
                )
            object.__setattr__(self, name, value)
        if not isinstance(self.suggested_questions, SuggestedQuestions):
            raise CoachInvariantViolation(
                "suggested_questions must be a SuggestedQuestions",
                invariant="ConversationContext.suggested_questions.type",
            )
