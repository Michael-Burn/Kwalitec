"""ReflectionCard — post-session reflection prompts for the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class ReflectionCard:
    """Immutable reflection composition — prompts only, never AI generation."""

    available: bool
    reflection_prompt: str
    confidence_reminder: str
    notes_placeholder: str
    prior_reflection_count: int
    summary: str

    def __post_init__(self) -> None:
        for name in (
            "reflection_prompt",
            "confidence_reminder",
            "notes_placeholder",
            "summary",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ReflectionCard.{name}.required",
                )
            object.__setattr__(self, name, value)
        if isinstance(self.prior_reflection_count, bool) or not isinstance(
            self.prior_reflection_count, int
        ):
            raise WorkspaceInvariantViolation(
                "prior_reflection_count must be an integer",
                invariant="ReflectionCard.prior_reflection_count.type",
            )
        if self.prior_reflection_count < 0:
            raise WorkspaceInvariantViolation(
                "prior_reflection_count must be >= 0",
                invariant="ReflectionCard.prior_reflection_count.range",
            )
