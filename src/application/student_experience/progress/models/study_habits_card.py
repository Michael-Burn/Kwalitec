"""StudyHabitsCard — deterministic learning habit projection."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.progress.enums import StudyTimeBand, WeekdayLabel
from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class StudyHabitsCard:
    """Immutable study habits projection — never AI-inferred."""

    preferred_study_time: StudyTimeBand
    preferred_study_time_message: str
    average_session_duration_minutes: float
    most_productive_weekday: WeekdayLabel
    most_productive_weekday_message: str
    completion_reliability_percent: float
    completion_reliability_message: str
    mission_completion_quality_message: str
    has_habits_data: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.preferred_study_time, StudyTimeBand):
            raise JourneyInvariantViolation(
                "preferred_study_time must be a StudyTimeBand",
                invariant="StudyHabitsCard.preferred_study_time.type",
            )
        if not isinstance(self.most_productive_weekday, WeekdayLabel):
            raise JourneyInvariantViolation(
                "most_productive_weekday must be a WeekdayLabel",
                invariant="StudyHabitsCard.most_productive_weekday.type",
            )
        for name in (
            "preferred_study_time_message",
            "most_productive_weekday_message",
            "completion_reliability_message",
            "mission_completion_quality_message",
        ):
            message = (getattr(self, name) or "").strip()
            if not message:
                raise JourneyInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"StudyHabitsCard.{name}.required",
                )
            object.__setattr__(self, name, message)
        if isinstance(self.average_session_duration_minutes, bool) or not isinstance(
            self.average_session_duration_minutes, int | float
        ):
            raise JourneyInvariantViolation(
                "average_session_duration_minutes must be a real number",
                invariant="StudyHabitsCard.average_session_duration_minutes.type",
            )
        avg = round(float(self.average_session_duration_minutes), 2)
        if avg < 0.0:
            raise JourneyInvariantViolation(
                "average_session_duration_minutes must be >= 0",
                invariant="StudyHabitsCard.average_session_duration_minutes.range",
            )
        object.__setattr__(self, "average_session_duration_minutes", avg)
        if isinstance(self.completion_reliability_percent, bool) or not isinstance(
            self.completion_reliability_percent, int | float
        ):
            raise JourneyInvariantViolation(
                "completion_reliability_percent must be a real number",
                invariant="StudyHabitsCard.completion_reliability_percent.type",
            )
        rate = round(float(self.completion_reliability_percent), 2)
        if rate < 0.0 or rate > 100.0:
            raise JourneyInvariantViolation(
                "completion_reliability_percent must be in [0, 100]",
                invariant="StudyHabitsCard.completion_reliability_percent.range",
            )
        object.__setattr__(self, "completion_reliability_percent", rate)
