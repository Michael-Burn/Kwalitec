"""SuggestedQuestions — deterministic coaching question prompts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.coach.enums import SuggestedQuestionKind
from application.student_experience.coach.errors import CoachInvariantViolation


@dataclass(frozen=True, slots=True)
class SuggestedQuestion:
    """One deterministic suggested question for the coach conversation."""

    kind: SuggestedQuestionKind
    prompt: str
    rationale: str
    enabled: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.kind, SuggestedQuestionKind):
            raise CoachInvariantViolation(
                "kind must be a SuggestedQuestionKind",
                invariant="SuggestedQuestion.kind.type",
            )
        for name in ("prompt", "rationale"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"SuggestedQuestion.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class SuggestedQuestions:
    """Immutable collection of suggested coaching questions."""

    questions: tuple[SuggestedQuestion, ...] = ()

    def __post_init__(self) -> None:
        questions = tuple(self.questions or ())
        for question in questions:
            if not isinstance(question, SuggestedQuestion):
                raise CoachInvariantViolation(
                    "questions must contain SuggestedQuestion instances",
                    invariant="SuggestedQuestions.questions.type",
                )
        object.__setattr__(self, "questions", questions)

    @property
    def enabled_count(self) -> int:
        return sum(1 for question in self.questions if question.enabled)

    def by_kind(self, kind: SuggestedQuestionKind) -> SuggestedQuestion | None:
        for question in self.questions:
            if question.kind is kind:
                return question
        return None
