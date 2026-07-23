"""TodaysFocusCard — answers \"What should I do right now?\""""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.home.enums import FocusActionKind
from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class TodaysFocusCard:
    """Immutable card answering the student's primary focus question.

    Never exposes domain type names. Carries student-facing labels only.
    """

    headline: str
    mission_title: str | None
    estimated_duration_minutes: int | None
    study_objective: str | None
    reason: str
    primary_action_label: str
    primary_action_kind: FocusActionKind
    mission_id: str | None = None
    has_focus: bool = False

    def __post_init__(self) -> None:
        headline = (self.headline or "").strip()
        if not headline:
            raise HomeInvariantViolation(
                "headline must be a non-empty string",
                invariant="TodaysFocusCard.headline.required",
            )
        object.__setattr__(self, "headline", headline)
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
                invariant="TodaysFocusCard.reason.required",
            )
        object.__setattr__(self, "reason", reason)
        label = (self.primary_action_label or "").strip()
        if not label:
            raise HomeInvariantViolation(
                "primary_action_label must be a non-empty string",
                invariant="TodaysFocusCard.primary_action_label.required",
            )
        object.__setattr__(self, "primary_action_label", label)
        if not isinstance(self.primary_action_kind, FocusActionKind):
            raise HomeInvariantViolation(
                "primary_action_kind must be a FocusActionKind",
                invariant="TodaysFocusCard.primary_action_kind.type",
            )
        if self.estimated_duration_minutes is not None:
            if isinstance(self.estimated_duration_minutes, bool) or not isinstance(
                self.estimated_duration_minutes, int
            ):
                raise HomeInvariantViolation(
                    "estimated_duration_minutes must be an integer when provided",
                    invariant="TodaysFocusCard.estimated_duration_minutes.type",
                )
            if self.estimated_duration_minutes < 1:
                raise HomeInvariantViolation(
                    "estimated_duration_minutes must be >= 1 when provided",
                    invariant="TodaysFocusCard.estimated_duration_minutes.positive",
                )
        object.__setattr__(
            self, "mission_id", (self.mission_id or "").strip() or None
        )
