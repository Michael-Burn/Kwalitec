"""Planning constraints — caller-supplied scheduling limits and preferences.

These are application inputs. They are not domain state, not
StudentEducationalState fields, and not mastery estimates.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time

from application.education.revision_planner.enums import (
    AbandonmentPolicy,
    SpacingPolicy,
    Weekday,
)
from application.education.revision_planner.errors import ScheduleInvariantViolation

DEFAULT_MAX_DAILY_MINUTES = 120
DEFAULT_MAX_SESSION_MINUTES = 45
DEFAULT_PREFERRED_SESSION_MINUTES = 30
DEFAULT_WEEKLY_WORKLOAD_MINUTES = 600
DEFAULT_MIN_RECOVERY_MINUTES = 0


@dataclass(frozen=True, slots=True)
class PlanningConstraints:
    """Optional scheduling inputs supplied by the application caller.

    Absent values mean "no additional constraint" except where documented
    defaults apply for session sizing.
    """

    available_study_minutes_per_day: int | None = None
    maximum_daily_study_minutes: int = DEFAULT_MAX_DAILY_MINUTES
    preferred_session_minutes: int = DEFAULT_PREFERRED_SESSION_MINUTES
    maximum_session_minutes: int = DEFAULT_MAX_SESSION_MINUTES
    preferred_window_start: time | None = None
    preferred_window_end: time | None = None
    rest_weekdays: tuple[Weekday, ...] = ()
    target_completion_date: date | None = None
    weekly_workload_minutes: int | None = DEFAULT_WEEKLY_WORKLOAD_MINUTES
    spacing_policy: SpacingPolicy = SpacingPolicy.BALANCED
    abandonment_policy: AbandonmentPolicy = (
        AbandonmentPolicy.RESCHEDULE_NEXT_AVAILABLE
    )
    minimum_recovery_minutes_between_sessions: int = DEFAULT_MIN_RECOVERY_MINUTES
    honour_mission_dependencies: bool = True
    honour_mission_priority: bool = True

    def __post_init__(self) -> None:
        if self.available_study_minutes_per_day is not None:
            self._require_positive_int(
                self.available_study_minutes_per_day,
                "available_study_minutes_per_day",
            )
        self._require_positive_int(
            self.maximum_daily_study_minutes, "maximum_daily_study_minutes"
        )
        self._require_positive_int(
            self.preferred_session_minutes, "preferred_session_minutes"
        )
        self._require_positive_int(
            self.maximum_session_minutes, "maximum_session_minutes"
        )
        if self.preferred_session_minutes > self.maximum_session_minutes:
            raise ScheduleInvariantViolation(
                "preferred_session_minutes must be <= maximum_session_minutes",
                invariant="PlanningConstraints.session_minutes.order",
            )
        if (
            self.preferred_window_start is not None
            and self.preferred_window_end is not None
            and self.preferred_window_start >= self.preferred_window_end
        ):
            raise ScheduleInvariantViolation(
                "preferred_window_start must be before preferred_window_end",
                invariant="PlanningConstraints.preferred_window.order",
            )
        rest = tuple(self.rest_weekdays)
        for day in rest:
            if not isinstance(day, Weekday):
                raise ScheduleInvariantViolation(
                    "rest_weekdays must contain Weekday values",
                    invariant="PlanningConstraints.rest_weekdays.type",
                )
        object.__setattr__(self, "rest_weekdays", rest)
        if self.target_completion_date is not None and not isinstance(
            self.target_completion_date, date
        ):
            raise ScheduleInvariantViolation(
                "target_completion_date must be a date when provided",
                invariant="PlanningConstraints.target_completion_date.type",
            )
        if self.weekly_workload_minutes is not None:
            self._require_positive_int(
                self.weekly_workload_minutes, "weekly_workload_minutes"
            )
        if not isinstance(self.spacing_policy, SpacingPolicy):
            raise ScheduleInvariantViolation(
                "spacing_policy must be a SpacingPolicy",
                invariant="PlanningConstraints.spacing_policy.type",
            )
        if not isinstance(self.abandonment_policy, AbandonmentPolicy):
            raise ScheduleInvariantViolation(
                "abandonment_policy must be an AbandonmentPolicy",
                invariant="PlanningConstraints.abandonment_policy.type",
            )
        if isinstance(
            self.minimum_recovery_minutes_between_sessions, bool
        ) or not isinstance(self.minimum_recovery_minutes_between_sessions, int):
            raise ScheduleInvariantViolation(
                "minimum_recovery_minutes_between_sessions must be an integer",
                invariant=(
                    "PlanningConstraints."
                    "minimum_recovery_minutes_between_sessions.type"
                ),
            )
        if self.minimum_recovery_minutes_between_sessions < 0:
            raise ScheduleInvariantViolation(
                "minimum_recovery_minutes_between_sessions must be >= 0",
                invariant=(
                    "PlanningConstraints."
                    "minimum_recovery_minutes_between_sessions.non_negative"
                ),
            )

    @staticmethod
    def _require_positive_int(value: int, name: str) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ScheduleInvariantViolation(
                f"{name} must be an integer",
                invariant=f"PlanningConstraints.{name}.type",
            )
        if value < 1:
            raise ScheduleInvariantViolation(
                f"{name} must be >= 1",
                invariant=f"PlanningConstraints.{name}.positive",
            )

    def effective_daily_cap_minutes(self) -> int:
        """Return the tightest applicable daily study-time cap."""
        caps = [self.maximum_daily_study_minutes]
        if self.available_study_minutes_per_day is not None:
            caps.append(self.available_study_minutes_per_day)
        return min(caps)

    def is_rest_weekday(self, day: date) -> bool:
        return Weekday.from_iso(day.isoweekday()) in self.rest_weekdays
