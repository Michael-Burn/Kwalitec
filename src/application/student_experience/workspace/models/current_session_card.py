"""CurrentSessionCard — current study session summary for the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.enums import SessionPresence
from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class CurrentSessionCard:
    """Immutable projection of the student's current study session.

    Composes current mission, remaining duration, objectives preview, and
    estimated completion from existing Education OS artefacts.
    """

    available: bool
    presence: SessionPresence
    session_id: str | None
    mission_id: str | None
    mission_title: str | None
    remaining_duration_minutes: int | None
    remaining_duration_label: str
    objectives_preview: tuple[str, ...]
    estimated_completion_label: str
    summary: str

    def __post_init__(self) -> None:
        if not isinstance(self.presence, SessionPresence):
            raise WorkspaceInvariantViolation(
                "presence must be a SessionPresence",
                invariant="CurrentSessionCard.presence.type",
            )
        object.__setattr__(
            self, "session_id", (self.session_id or "").strip() or None
        )
        object.__setattr__(
            self, "mission_id", (self.mission_id or "").strip() or None
        )
        object.__setattr__(
            self,
            "mission_title",
            (self.mission_title or "").strip() or None,
        )
        object.__setattr__(
            self, "objectives_preview", tuple(self.objectives_preview)
        )
        for name in (
            "remaining_duration_label",
            "estimated_completion_label",
            "summary",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"CurrentSessionCard.{name}.required",
                )
            object.__setattr__(self, name, value)
        if self.remaining_duration_minutes is not None:
            if isinstance(self.remaining_duration_minutes, bool) or not isinstance(
                self.remaining_duration_minutes, int
            ):
                raise WorkspaceInvariantViolation(
                    "remaining_duration_minutes must be an integer when provided",
                    invariant="CurrentSessionCard.remaining_duration_minutes.type",
                )
            if self.remaining_duration_minutes < 0:
                raise WorkspaceInvariantViolation(
                    "remaining_duration_minutes must be >= 0",
                    invariant="CurrentSessionCard.remaining_duration_minutes.range",
                )
