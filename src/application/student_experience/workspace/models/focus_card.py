"""FocusCard — deterministic focus prompts for the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.enums import FocusPromptKind
from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class FocusPrompt:
    """One deterministic focus prompt — never a newly generated recommendation."""

    kind: FocusPromptKind
    title: str
    prompt: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, FocusPromptKind):
            raise WorkspaceInvariantViolation(
                "kind must be a FocusPromptKind",
                invariant="FocusPrompt.kind.type",
            )
        for name in ("title", "prompt"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"FocusPrompt.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class FocusCard:
    """Immutable focus prompts composed from current session state only."""

    prompts: tuple[FocusPrompt, ...]
    primary: FocusPrompt | None
    has_prompts: bool
    summary: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "prompts", tuple(self.prompts))
        for prompt in self.prompts:
            if not isinstance(prompt, FocusPrompt):
                raise WorkspaceInvariantViolation(
                    "prompts must contain FocusPrompt values",
                    invariant="FocusCard.prompts.type",
                )
        if self.primary is not None and not isinstance(self.primary, FocusPrompt):
            raise WorkspaceInvariantViolation(
                "primary must be a FocusPrompt when provided",
                invariant="FocusCard.primary.type",
            )
        summary = (self.summary or "").strip()
        if not summary:
            raise WorkspaceInvariantViolation(
                "summary must be a non-empty string",
                invariant="FocusCard.summary.required",
            )
        object.__setattr__(self, "summary", summary)
