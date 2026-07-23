"""PrimaryFocus — structured result of determine_primary_focus()."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.home.enums import FocusActionKind
from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class PrimaryFocus:
    """Immutable primary focus decision projected for the home surface."""

    mission_id: str | None
    mission_title: str | None
    estimated_duration_minutes: int | None
    study_objective: str | None
    reason: str
    action_kind: FocusActionKind
    action_label: str
    has_focus: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "mission_id", (self.mission_id or "").strip() or None
        )
        object.__setattr__(
            self, "mission_title", (self.mission_title or "").strip() or None
        )
        object.__setattr__(
            self, "study_objective", (self.study_objective or "").strip() or None
        )
        reason = (self.reason or "").strip()
        if not reason:
            raise HomeInvariantViolation(
                "reason must be a non-empty string",
                invariant="PrimaryFocus.reason.required",
            )
        object.__setattr__(self, "reason", reason)
        if not isinstance(self.action_kind, FocusActionKind):
            raise HomeInvariantViolation(
                "action_kind must be a FocusActionKind",
                invariant="PrimaryFocus.action_kind.type",
            )
        label = (self.action_label or "").strip()
        if not label:
            raise HomeInvariantViolation(
                "action_label must be a non-empty string",
                invariant="PrimaryFocus.action_label.required",
            )
        object.__setattr__(self, "action_label", label)
        if self.estimated_duration_minutes is not None:
            if isinstance(self.estimated_duration_minutes, bool) or not isinstance(
                self.estimated_duration_minutes, int
            ):
                raise HomeInvariantViolation(
                    "estimated_duration_minutes must be an integer when provided",
                    invariant="PrimaryFocus.estimated_duration_minutes.type",
                )
            if self.estimated_duration_minutes < 1:
                raise HomeInvariantViolation(
                    "estimated_duration_minutes must be >= 1 when provided",
                    invariant="PrimaryFocus.estimated_duration_minutes.positive",
                )
