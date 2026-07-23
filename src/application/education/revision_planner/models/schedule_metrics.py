"""ScheduleMetrics and WorkloadDistribution — schedule analytics value objects."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.revision_planner.errors import ScheduleInvariantViolation


@dataclass(frozen=True, slots=True)
class ScheduleMetrics:
    """Aggregate quantitative metrics for a StudySchedule."""

    total_days: int
    study_days: int
    rest_days: int
    total_sessions: int
    active_sessions: int
    completed_sessions: int
    cancelled_sessions: int
    total_allocated_minutes: int
    total_available_minutes: int
    scheduled_mission_count: int
    completed_mission_count: int
    average_daily_minutes: float
    peak_daily_minutes: int

    def __post_init__(self) -> None:
        for name in (
            "total_days",
            "study_days",
            "rest_days",
            "total_sessions",
            "active_sessions",
            "completed_sessions",
            "cancelled_sessions",
            "total_allocated_minutes",
            "total_available_minutes",
            "scheduled_mission_count",
            "completed_mission_count",
            "peak_daily_minutes",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ScheduleInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"ScheduleMetrics.{name}.type",
                )
            if value < 0:
                raise ScheduleInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ScheduleMetrics.{name}.non_negative",
                )
        if isinstance(self.average_daily_minutes, bool) or not isinstance(
            self.average_daily_minutes, int | float
        ):
            raise ScheduleInvariantViolation(
                "average_daily_minutes must be a real number",
                invariant="ScheduleMetrics.average_daily_minutes.type",
            )
        if self.average_daily_minutes < 0.0:
            raise ScheduleInvariantViolation(
                "average_daily_minutes must be >= 0",
                invariant="ScheduleMetrics.average_daily_minutes.non_negative",
            )
        object.__setattr__(
            self, "average_daily_minutes", round(float(self.average_daily_minutes), 4)
        )

    @property
    def utilisation_ratio(self) -> float:
        if self.total_available_minutes <= 0:
            return 0.0
        return round(
            self.total_allocated_minutes / self.total_available_minutes, 4
        )


@dataclass(frozen=True, slots=True)
class DayWorkload:
    """Per-day workload entry within a WorkloadDistribution."""

    day_iso: str
    allocated_minutes: int
    available_minutes: int

    def __post_init__(self) -> None:
        day_iso = (self.day_iso or "").strip()
        if not day_iso:
            raise ScheduleInvariantViolation(
                "day_iso must be a non-empty string",
                invariant="DayWorkload.day_iso.required",
            )
        object.__setattr__(self, "day_iso", day_iso)
        for name, value in (
            ("allocated_minutes", self.allocated_minutes),
            ("available_minutes", self.available_minutes),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ScheduleInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"DayWorkload.{name}.type",
                )
            if value < 0:
                raise ScheduleInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"DayWorkload.{name}.non_negative",
                )


@dataclass(frozen=True, slots=True)
class WorkloadDistribution:
    """Immutable distribution of allocated minutes across study days."""

    daily: tuple[DayWorkload, ...] = ()
    weekly_totals: tuple[int, ...] = ()
    max_day_minutes: int = 0
    min_day_minutes: int = 0
    variance: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "daily", tuple(self.daily))
        for entry in self.daily:
            if not isinstance(entry, DayWorkload):
                raise ScheduleInvariantViolation(
                    "daily must contain DayWorkload values",
                    invariant="WorkloadDistribution.daily.type",
                )
        object.__setattr__(self, "weekly_totals", tuple(self.weekly_totals))
        for total in self.weekly_totals:
            if isinstance(total, bool) or not isinstance(total, int):
                raise ScheduleInvariantViolation(
                    "weekly_totals must contain integers",
                    invariant="WorkloadDistribution.weekly_totals.type",
                )
            if total < 0:
                raise ScheduleInvariantViolation(
                    "weekly_totals must be >= 0",
                    invariant="WorkloadDistribution.weekly_totals.non_negative",
                )
        for name in ("max_day_minutes", "min_day_minutes"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ScheduleInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"WorkloadDistribution.{name}.type",
                )
            if value < 0:
                raise ScheduleInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"WorkloadDistribution.{name}.non_negative",
                )
        if isinstance(self.variance, bool) or not isinstance(
            self.variance, int | float
        ):
            raise ScheduleInvariantViolation(
                "variance must be a real number",
                invariant="WorkloadDistribution.variance.type",
            )
        if self.variance < 0.0:
            raise ScheduleInvariantViolation(
                "variance must be >= 0",
                invariant="WorkloadDistribution.variance.non_negative",
            )
        object.__setattr__(self, "variance", round(float(self.variance), 4))
