"""ReflectionPrompts — post-study reflection prompts for coaching."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.coach.enums import ReflectionPromptKind
from application.student_experience.coach.errors import CoachInvariantViolation


@dataclass(frozen=True, slots=True)
class ReflectionPrompt:
    """One deterministic post-study reflection prompt."""

    kind: ReflectionPromptKind
    prompt: str
    detail: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, ReflectionPromptKind):
            raise CoachInvariantViolation(
                "kind must be a ReflectionPromptKind",
                invariant="ReflectionPrompt.kind.type",
            )
        for name in ("prompt", "detail"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ReflectionPrompt.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class ReflectionPrompts:
    """Immutable collection of post-study reflection prompts."""

    available: bool
    prompts: tuple[ReflectionPrompt, ...] = ()
    summary: str = "Reflection prompts will appear after you study."

    def __post_init__(self) -> None:
        prompts = tuple(self.prompts or ())
        for prompt in prompts:
            if not isinstance(prompt, ReflectionPrompt):
                raise CoachInvariantViolation(
                    "prompts must contain ReflectionPrompt instances",
                    invariant="ReflectionPrompts.prompts.type",
                )
        object.__setattr__(self, "prompts", prompts)
        summary = (self.summary or "").strip()
        if not summary:
            raise CoachInvariantViolation(
                "summary must be a non-empty string",
                invariant="ReflectionPrompts.summary.required",
            )
        object.__setattr__(self, "summary", summary)
