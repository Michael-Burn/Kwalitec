"""SessionTimerCard — display-only session timing for the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.enums import TimerDisplayState
from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class SessionTimerCard:
    """Immutable timing display projected from existing duration facts.

    Never implements a live timer. Values are caller-supplied projections only.
    """

    available: bool
    display_state: TimerDisplayState
    planned_minutes: int | None
    planned_label: str
    elapsed_minutes: int | None
    elapsed_label: str
    remaining_minutes: int | None
    remaining_label: str
    summary: str

    def __post_init__(self) -> None:
        if not isinstance(self.display_state, TimerDisplayState):
            raise WorkspaceInvariantViolation(
                "display_state must be a TimerDisplayState",
                invariant="SessionTimerCard.display_state.type",
            )
        for name in (
            "planned_label",
            "elapsed_label",
            "remaining_label",
            "summary",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"SessionTimerCard.{name}.required",
                )
            object.__setattr__(self, name, value)
        for name in ("planned_minutes", "elapsed_minutes", "remaining_minutes"):
            value = getattr(self, name)
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, int):
                raise WorkspaceInvariantViolation(
                    f"{name} must be an integer when provided",
                    invariant=f"SessionTimerCard.{name}.type",
                )
            if value < 0:
                raise WorkspaceInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"SessionTimerCard.{name}.range",
                )
