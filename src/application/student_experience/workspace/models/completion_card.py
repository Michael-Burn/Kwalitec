"""CompletionCard — post-session completion projection for the workspace."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class CompletionCard:
    """Immutable completion projection — next session, milestone, readiness impact."""

    available: bool
    next_session_preview: str
    next_session_date: date | None
    upcoming_milestone: str
    readiness_impact_summary: str
    summary: str

    def __post_init__(self) -> None:
        for name in (
            "next_session_preview",
            "upcoming_milestone",
            "readiness_impact_summary",
            "summary",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"CompletionCard.{name}.required",
                )
            object.__setattr__(self, name, value)
        if self.next_session_date is not None and not isinstance(
            self.next_session_date, date
        ):
            raise WorkspaceInvariantViolation(
                "next_session_date must be a date when provided",
                invariant="CompletionCard.next_session_date.type",
            )
