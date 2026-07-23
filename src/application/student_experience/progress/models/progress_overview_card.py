"""ProgressOverviewCard — current trajectory and growth highlights."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.progress.enums import TrajectoryLabel
from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class ProgressOverviewCard:
    """Immutable progress overview — never raw Education OS objects."""

    trajectory: TrajectoryLabel
    trajectory_message: str
    weekly_growth_message: str
    monthly_growth_message: str
    strongest_subject: str | None
    most_improved_competency: str | None
    learning_momentum_message: str
    has_overview_data: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.trajectory, TrajectoryLabel):
            raise JourneyInvariantViolation(
                "trajectory must be a TrajectoryLabel",
                invariant="ProgressOverviewCard.trajectory.type",
            )
        for name in (
            "trajectory_message",
            "weekly_growth_message",
            "monthly_growth_message",
            "learning_momentum_message",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise JourneyInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ProgressOverviewCard.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self,
            "strongest_subject",
            (self.strongest_subject or "").strip() or None,
        )
        object.__setattr__(
            self,
            "most_improved_competency",
            (self.most_improved_competency or "").strip() or None,
        )
