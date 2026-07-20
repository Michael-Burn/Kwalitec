"""StudyPlan — deterministic study plan projection from missions and constraints.

Architecture Source
    SESSION_ASSEMBLY_MODEL.md
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Study Plan
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import PriorityId
from domain.mission_generation.ids import MissionSpecificationId
from domain.study_planning.enums import PlanningHorizonBand
from domain.study_planning.ids import StudyPlanId
from domain.study_planning.study_calendar import StudyCalendar
from domain.study_planning.study_schedule import StudySchedule
from domain.study_planning.study_session import StudySession


@dataclass(frozen=True, slots=True)
class ReviewWindow(EducationalValueObject):
    """Scheduled spaced-review opportunity after mission work completes."""

    mission_id: MissionSpecificationId
    day_index: int
    duration_minutes: int
    offset_from_completion: int
    sequence: int

    def _validate(self) -> None:
        if not isinstance(self.mission_id, MissionSpecificationId):
            raise EducationalInvariantViolation(
                "mission_id must be a MissionSpecificationId",
                invariant="ReviewWindow.mission_id.type",
            )
        if not isinstance(self.day_index, int) or isinstance(self.day_index, bool):
            raise EducationalInvariantViolation(
                "day_index must be an integer",
                invariant="ReviewWindow.day_index.type",
            )
        if self.day_index < 0:
            raise EducationalInvariantViolation(
                "day_index must be non-negative",
                invariant="ReviewWindow.day_index.non_negative",
            )
        if not isinstance(self.duration_minutes, int) or isinstance(
            self.duration_minutes, bool
        ):
            raise EducationalInvariantViolation(
                "duration_minutes must be an integer",
                invariant="ReviewWindow.duration_minutes.type",
            )
        if self.duration_minutes <= 0:
            raise EducationalInvariantViolation(
                "duration_minutes must be positive",
                invariant="ReviewWindow.duration_minutes.positive",
            )
        if not isinstance(self.offset_from_completion, int) or isinstance(
            self.offset_from_completion, bool
        ):
            raise EducationalInvariantViolation(
                "offset_from_completion must be an integer",
                invariant="ReviewWindow.offset_from_completion.type",
            )
        if self.offset_from_completion < 1:
            raise EducationalInvariantViolation(
                "offset_from_completion must be at least 1",
                invariant="ReviewWindow.offset_from_completion.positive",
            )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="ReviewWindow.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="ReviewWindow.sequence.positive",
            )


@dataclass(frozen=True, slots=True)
class RecoveryAllocation(EducationalValueObject):
    """Scheduled recovery time protecting capacity honesty after mission work."""

    mission_id: MissionSpecificationId
    day_index: int
    minutes: int
    rationale: str

    def _validate(self) -> None:
        if not isinstance(self.mission_id, MissionSpecificationId):
            raise EducationalInvariantViolation(
                "mission_id must be a MissionSpecificationId",
                invariant="RecoveryAllocation.mission_id.type",
            )
        if not isinstance(self.day_index, int) or isinstance(self.day_index, bool):
            raise EducationalInvariantViolation(
                "day_index must be an integer",
                invariant="RecoveryAllocation.day_index.type",
            )
        if self.day_index < 0:
            raise EducationalInvariantViolation(
                "day_index must be non-negative",
                invariant="RecoveryAllocation.day_index.non_negative",
            )
        if not isinstance(self.minutes, int) or isinstance(self.minutes, bool):
            raise EducationalInvariantViolation(
                "minutes must be an integer",
                invariant="RecoveryAllocation.minutes.type",
            )
        if self.minutes <= 0:
            raise EducationalInvariantViolation(
                "minutes must be positive",
                invariant="RecoveryAllocation.minutes.positive",
            )
        object.__setattr__(
            self,
            "rationale",
            require_non_empty_text(self.rationale, "rationale"),
        )


@dataclass(frozen=True, slots=True)
class EstimatedCompletion(EducationalValueObject):
    """Deterministic completion estimate for a StudyPlan."""

    work_complete_day_index: int
    plan_complete_day_index: int
    total_work_minutes: int
    total_review_minutes: int
    total_recovery_minutes: int
    session_count: int
    horizon_band: PlanningHorizonBand

    def _validate(self) -> None:
        for name, value in (
            ("work_complete_day_index", self.work_complete_day_index),
            ("plan_complete_day_index", self.plan_complete_day_index),
            ("total_work_minutes", self.total_work_minutes),
            ("total_review_minutes", self.total_review_minutes),
            ("total_recovery_minutes", self.total_recovery_minutes),
            ("session_count", self.session_count),
        ):
            if not isinstance(value, int) or isinstance(value, bool):
                raise EducationalInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"EstimatedCompletion.{name}.type",
                )
            if value < 0:
                raise EducationalInvariantViolation(
                    f"{name} must be non-negative",
                    invariant=f"EstimatedCompletion.{name}.non_negative",
                )
        if self.session_count < 1:
            raise EducationalInvariantViolation(
                "session_count must be positive",
                invariant="EstimatedCompletion.session_count.positive",
            )
        if self.total_work_minutes < 1:
            raise EducationalInvariantViolation(
                "total_work_minutes must be positive",
                invariant="EstimatedCompletion.total_work_minutes.positive",
            )
        if self.plan_complete_day_index < self.work_complete_day_index:
            raise EducationalInvariantViolation(
                "plan completion cannot precede work completion",
                invariant="EstimatedCompletion.plan_after_work",
            )
        if not isinstance(self.horizon_band, PlanningHorizonBand):
            raise EducationalInvariantViolation(
                "horizon_band must be a PlanningHorizonBand",
                invariant="EstimatedCompletion.horizon_band.type",
            )

    @property
    def total_minutes(self) -> int:
        return (
            self.total_work_minutes
            + self.total_review_minutes
            + self.total_recovery_minutes
        )


@dataclass(frozen=True, slots=True)
class StudyPlan(EducationalValueObject):
    """Fully explainable study plan from missions and learner constraints.

    Contains ordered sessions, a daily calendar, estimated completion, review
    windows, and recovery time. Pure educational projection — no persistence,
    AI, or calendar APIs.
    """

    plan_id: StudyPlanId
    student_id: str
    mission_ids: tuple[MissionSpecificationId, ...]
    schedule: StudySchedule
    calendar: StudyCalendar
    estimated_completion: EstimatedCompletion
    review_windows: tuple[ReviewWindow, ...]
    recovery_allocations: tuple[RecoveryAllocation, ...]
    educational_rationale: str
    priority_id: PriorityId

    def _validate(self) -> None:
        if not isinstance(self.plan_id, StudyPlanId):
            raise EducationalInvariantViolation(
                "plan_id must be a StudyPlanId",
                invariant="StudyPlan.plan_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_non_empty_text(self.student_id, "student_id"),
        )
        if not isinstance(self.mission_ids, tuple) or not self.mission_ids:
            raise EducationalInvariantViolation(
                "mission_ids must be a non-empty tuple",
                invariant="StudyPlan.mission_ids.min_one",
            )
        seen: set[str] = set()
        for mission_id in self.mission_ids:
            if not isinstance(mission_id, MissionSpecificationId):
                raise EducationalInvariantViolation(
                    "mission_ids must contain MissionSpecificationId values",
                    invariant="StudyPlan.mission_ids.item_type",
                )
            if mission_id.value in seen:
                raise EducationalInvariantViolation(
                    "mission_ids must be unique",
                    invariant="StudyPlan.mission_ids.unique",
                )
            seen.add(mission_id.value)
        if not isinstance(self.schedule, StudySchedule):
            raise EducationalInvariantViolation(
                "schedule must be a StudySchedule",
                invariant="StudyPlan.schedule.type",
            )
        if not isinstance(self.calendar, StudyCalendar):
            raise EducationalInvariantViolation(
                "calendar must be a StudyCalendar",
                invariant="StudyPlan.calendar.type",
            )
        if not isinstance(self.estimated_completion, EstimatedCompletion):
            raise EducationalInvariantViolation(
                "estimated_completion must be an EstimatedCompletion",
                invariant="StudyPlan.estimated_completion.type",
            )
        if not isinstance(self.review_windows, tuple):
            raise EducationalInvariantViolation(
                "review_windows must be a tuple",
                invariant="StudyPlan.review_windows.type",
            )
        for window in self.review_windows:
            if not isinstance(window, ReviewWindow):
                raise EducationalInvariantViolation(
                    "review_windows must contain ReviewWindow values",
                    invariant="StudyPlan.review_windows.item_type",
                )
        if not isinstance(self.recovery_allocations, tuple):
            raise EducationalInvariantViolation(
                "recovery_allocations must be a tuple",
                invariant="StudyPlan.recovery_allocations.type",
            )
        for allocation in self.recovery_allocations:
            if not isinstance(allocation, RecoveryAllocation):
                raise EducationalInvariantViolation(
                    "recovery_allocations must contain RecoveryAllocation values",
                    invariant="StudyPlan.recovery_allocations.item_type",
                )
        object.__setattr__(
            self,
            "educational_rationale",
            require_non_empty_text(
                self.educational_rationale, "educational_rationale"
            ),
        )
        if len(self.educational_rationale) < 24:
            raise EducationalInvariantViolation(
                "educational rationale must be educationally substantive",
                invariant="StudyPlan.educational_rationale.substantive",
            )
        if not isinstance(self.priority_id, PriorityId):
            raise EducationalInvariantViolation(
                "priority_id must be a PriorityId",
                invariant="StudyPlan.priority_id.type",
            )
        # Schedule and calendar must agree on ordered sessions.
        if self.schedule.sessions != self.calendar.all_sessions():
            raise EducationalInvariantViolation(
                "schedule sessions must match calendar sessions in order",
                invariant="StudyPlan.schedule_calendar.align",
            )
        if self.estimated_completion.session_count != self.schedule.length:
            raise EducationalInvariantViolation(
                "estimated completion session_count must match schedule length",
                invariant="StudyPlan.estimated_completion.session_count",
            )
        if (
            self.estimated_completion.total_work_minutes
            != self.schedule.total_work_minutes()
        ):
            raise EducationalInvariantViolation(
                "estimated work minutes must match schedule work minutes",
                invariant="StudyPlan.estimated_completion.work_minutes",
            )
        if (
            self.estimated_completion.total_review_minutes
            != self.schedule.total_review_minutes()
        ):
            raise EducationalInvariantViolation(
                "estimated review minutes must match schedule review minutes",
                invariant="StudyPlan.estimated_completion.review_minutes",
            )
        if (
            self.estimated_completion.total_recovery_minutes
            != self.schedule.total_recovery_minutes()
        ):
            raise EducationalInvariantViolation(
                "estimated recovery minutes must match schedule recovery minutes",
                invariant="StudyPlan.estimated_completion.recovery_minutes",
            )

    @property
    def ordered_sessions(self) -> tuple[StudySession, ...]:
        return self.schedule.ordered_sessions()

    def session_count(self) -> int:
        return self.schedule.length

    def daily_schedule(self) -> tuple:
        return self.calendar.days
