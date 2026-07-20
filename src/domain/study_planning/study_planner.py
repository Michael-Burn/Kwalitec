"""StudyPlanner — deterministic StudyPlan from missions and learner constraints.

Architecture Source
    SESSION_ASSEMBLY_MODEL.md
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Study Planning

Rules
    No AI. No prompting. No randomness. No calendar APIs.
    Same educational inputs always yield the same StudyPlan.
"""

from __future__ import annotations

from domain.education.digital_twin.enums import TrajectoryPointKind
from domain.education.digital_twin.value_objects.learning_trajectory import (
    LearningTrajectory,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import PriorityId
from domain.education.priority.aggregates.educational_priority import (
    EducationalPriority,
)
from domain.education.priority.enums import PriorityScoreBand, PriorityStatus
from domain.mission_generation.enums import (
    MissionDurationBand,
    MissionPriorityBand,
)
from domain.mission_generation.ids import MissionTaskId
from domain.mission_generation.mission_specification import MissionSpecification
from domain.study_planning.enums import SessionKind
from domain.study_planning.ids import StudyPlanId, StudySessionId
from domain.study_planning.learner_availability import LearnerAvailability
from domain.study_planning.study_calendar import StudyCalendar
from domain.study_planning.study_day import StudyDay
from domain.study_planning.study_plan import (
    EstimatedCompletion,
    RecoveryAllocation,
    ReviewWindow,
    StudyPlan,
)
from domain.study_planning.study_schedule import StudySchedule
from domain.study_planning.study_session import StudySession

# Capacity honesty: no single sitting may exceed this instructional ceiling.
_MAX_SESSION_MINUTES = 45
_MIN_SESSION_MINUTES = 5

_RECOVERY_BY_DURATION: dict[MissionDurationBand, int] = {
    MissionDurationBand.SHORT: 0,
    MissionDurationBand.MEDIUM: 5,
    MissionDurationBand.LONG: 10,
}

_TRAJECTORY_RECOVERY_BONUS = 3

_REVIEW_OFFSETS_BY_PRIORITY: dict[PriorityScoreBand, tuple[int, ...]] = {
    PriorityScoreBand.CRITICAL: (1, 3),
    PriorityScoreBand.HIGH: (1, 3),
    PriorityScoreBand.MEDIUM: (2, 4),
    PriorityScoreBand.LOW: (3, 6),
    PriorityScoreBand.NEGLIGIBLE: (3, 6),
}

_MISSION_PRIORITY_ORDER: dict[MissionPriorityBand, int] = {
    MissionPriorityBand.CRITICAL: 5,
    MissionPriorityBand.HIGH: 4,
    MissionPriorityBand.MEDIUM: 3,
    MissionPriorityBand.LOW: 2,
    MissionPriorityBand.NEGLIGIBLE: 1,
}


class StudyPlanner:
    """Pure domain service that generates StudyPlans.

    Planning is fully deterministic and explainable from MissionSpecifications,
    LearnerAvailability, LearningTrajectory, and EducationalPriority.
    """

    @classmethod
    def plan(
        cls,
        missions: tuple[MissionSpecification, ...] | list[MissionSpecification],
        availability: LearnerAvailability,
        trajectory: LearningTrajectory,
        priority: EducationalPriority,
    ) -> StudyPlan:
        """Generate a StudyPlan from missions and learner constraints.

        Args:
            missions: One or more MissionSpecifications to schedule.
            availability: Relative-day capacity constraints.
            trajectory: Learner memory spine influencing recovery density.
            priority: Governing EducationalPriority for review aggressiveness
                and plan identity.

        Returns:
            Immutable StudyPlan with ordered sessions, daily calendar,
            estimated completion, review windows, and recovery allocations.

        Raises:
            EducationalInvariantViolation: When inputs are inconsistent or
                capacity is insufficient.
        """
        mission_tuple = tuple(missions)
        cls._assert_inputs(mission_tuple, availability, trajectory, priority)

        ordered_missions = cls._order_missions(mission_tuple)
        remaining_capacity = {
            window.day_index: window.available_minutes
            for window in availability.windows
        }
        day_order = [window.day_index for window in availability.windows]

        sessions: list[StudySession] = []
        review_windows: list[ReviewWindow] = []
        recovery_allocations: list[RecoveryAllocation] = []
        sequence_index = 1
        work_complete_by_mission: dict[str, int] = {}
        trajectory_bonus = cls._trajectory_recovery_bonus(trajectory)

        # Phase 1 — priority-ordered work sessions (capacity-honest).
        for mission in ordered_missions:
            sequence_index, work_day = cls._schedule_mission_work(
                mission=mission,
                remaining_capacity=remaining_capacity,
                day_order=day_order,
                sessions=sessions,
                sequence_index=sequence_index,
            )
            work_complete_by_mission[mission.mission_id.value] = work_day

        work_complete_day = max(work_complete_by_mission.values())

        # Phase 2 — recovery after each mission's work completes.
        for mission in ordered_missions:
            recovery_minutes = cls._recovery_minutes(mission, trajectory_bonus)
            if recovery_minutes <= 0:
                continue
            last_day = sessions[-1].day_index if sessions else 0
            preferred = max(
                work_complete_by_mission[mission.mission_id.value],
                last_day,
            )
            sequence_index, recovery_day = cls._schedule_recovery(
                mission=mission,
                recovery_minutes=recovery_minutes,
                remaining_capacity=remaining_capacity,
                day_order=day_order,
                sessions=sessions,
                sequence_index=sequence_index,
                preferred_day=preferred,
                not_before=last_day,
            )
            recovery_allocations.append(
                RecoveryAllocation(
                    mission_id=mission.mission_id,
                    day_index=recovery_day,
                    minutes=recovery_minutes,
                    rationale=cls._recovery_rationale(
                        mission, recovery_minutes, trajectory_bonus
                    ),
                )
            )

        # Phase 3 — spaced review windows after work completion.
        for mission in ordered_missions:
            mission_reviews = cls._plan_review_windows(
                mission=mission,
                priority=priority,
                work_complete_day=work_complete_by_mission[mission.mission_id.value],
            )
            for window in mission_reviews:
                last_day = sessions[-1].day_index if sessions else 0
                preferred = max(window.day_index, last_day)
                adjusted = ReviewWindow(
                    mission_id=window.mission_id,
                    day_index=preferred,
                    duration_minutes=window.duration_minutes,
                    offset_from_completion=window.offset_from_completion,
                    sequence=window.sequence,
                )
                sequence_index, scheduled_day = cls._schedule_review(
                    mission=mission,
                    window=adjusted,
                    remaining_capacity=remaining_capacity,
                    day_order=day_order,
                    sessions=sessions,
                    sequence_index=sequence_index,
                    not_before=last_day,
                )
                review_windows.append(
                    ReviewWindow(
                        mission_id=window.mission_id,
                        day_index=scheduled_day,
                        duration_minutes=window.duration_minutes,
                        offset_from_completion=window.offset_from_completion,
                        sequence=window.sequence,
                    )
                )

        if not sessions:
            raise EducationalInvariantViolation(
                "planner produced no sessions",
                invariant="StudyPlanner.sessions.empty",
            )

        schedule = StudySchedule.of(*sessions)
        calendar = cls._build_calendar(availability, sessions)
        estimated = EstimatedCompletion(
            work_complete_day_index=work_complete_day,
            plan_complete_day_index=calendar.last_session_day_index(),
            total_work_minutes=schedule.total_work_minutes(),
            total_review_minutes=schedule.total_review_minutes(),
            total_recovery_minutes=schedule.total_recovery_minutes(),
            session_count=schedule.length,
            horizon_band=calendar.horizon_band(),
        )
        plan_id = cls._plan_id(ordered_missions, availability, priority.priority_id)
        rationale = cls._build_rationale(
            missions=ordered_missions,
            availability=availability,
            trajectory=trajectory,
            priority=priority,
            schedule=schedule,
            estimated=estimated,
            recovery_allocations=tuple(recovery_allocations),
            review_windows=tuple(review_windows),
        )

        return StudyPlan(
            plan_id=plan_id,
            student_id=availability.student_id,
            mission_ids=tuple(m.mission_id for m in ordered_missions),
            schedule=schedule,
            calendar=calendar,
            estimated_completion=estimated,
            review_windows=tuple(review_windows),
            recovery_allocations=tuple(recovery_allocations),
            educational_rationale=rationale,
            priority_id=priority.priority_id,
        )

    @classmethod
    def plan_one(
        cls,
        mission: MissionSpecification,
        availability: LearnerAvailability,
        trajectory: LearningTrajectory,
        priority: EducationalPriority,
    ) -> StudyPlan:
        """Convenience wrapper to plan a single MissionSpecification."""
        return cls.plan((mission,), availability, trajectory, priority)

    # --- validation ---------------------------------------------------------

    @staticmethod
    def _assert_inputs(
        missions: tuple[MissionSpecification, ...],
        availability: LearnerAvailability,
        trajectory: LearningTrajectory,
        priority: EducationalPriority,
    ) -> None:
        if not missions:
            raise EducationalInvariantViolation(
                "at least one MissionSpecification is required",
                invariant="StudyPlanner.missions.min_one",
            )
        for mission in missions:
            if not isinstance(mission, MissionSpecification):
                raise EducationalInvariantViolation(
                    "missions must contain MissionSpecification values",
                    invariant="StudyPlanner.missions.item_type",
                )
        if not isinstance(availability, LearnerAvailability):
            raise EducationalInvariantViolation(
                "availability must be a LearnerAvailability",
                invariant="StudyPlanner.availability.type",
            )
        if not isinstance(trajectory, LearningTrajectory):
            raise EducationalInvariantViolation(
                "trajectory must be a LearningTrajectory",
                invariant="StudyPlanner.trajectory.type",
            )
        if not isinstance(priority, EducationalPriority):
            raise EducationalInvariantViolation(
                "priority must be an EducationalPriority",
                invariant="StudyPlanner.priority.type",
            )

        student_ids = {availability.student_id, priority.student_id}
        student_ids.update(mission.student_id for mission in missions)
        if len(student_ids) != 1:
            raise EducationalInvariantViolation(
                "missions, availability, and priority must share student_id",
                invariant="StudyPlanner.student_alignment",
            )

        if priority.status not in {
            PriorityStatus.ASSIGNED,
            PriorityStatus.REVISED,
            PriorityStatus.STABILISED,
        }:
            raise EducationalInvariantViolation(
                "priority must be assigned, revised, or stabilised",
                invariant="StudyPlanner.priority.status",
            )

        mission_ids = [m.mission_id.value for m in missions]
        if len(mission_ids) != len(set(mission_ids)):
            raise EducationalInvariantViolation(
                "missions must declare unique mission identities",
                invariant="StudyPlanner.missions.unique",
            )

        total_work = sum(m.duration.planned_minutes for m in missions)
        # Reviews and recovery need headroom beyond raw work minutes.
        if availability.total_available_minutes() < total_work:
            raise EducationalInvariantViolation(
                "learner availability is insufficient for mission work minutes",
                invariant="StudyPlanner.availability.insufficient",
            )

    # --- ordering -----------------------------------------------------------

    @staticmethod
    def _order_missions(
        missions: tuple[MissionSpecification, ...],
    ) -> tuple[MissionSpecification, ...]:
        return tuple(
            sorted(
                missions,
                key=lambda m: (
                    -_MISSION_PRIORITY_ORDER[m.priority.band],
                    m.mission_id.value,
                ),
            )
        )

    # --- recovery / review catalogues ---------------------------------------

    @staticmethod
    def _trajectory_recovery_bonus(trajectory: LearningTrajectory) -> int:
        last = trajectory.last()
        if last is not None and last.kind is TrajectoryPointKind.INTERVENTION:
            return _TRAJECTORY_RECOVERY_BONUS
        return 0

    @staticmethod
    def _recovery_minutes(
        mission: MissionSpecification,
        trajectory_bonus: int,
    ) -> int:
        base = _RECOVERY_BY_DURATION[mission.duration.band]
        return base + trajectory_bonus

    @staticmethod
    def _recovery_rationale(
        mission: MissionSpecification,
        recovery_minutes: int,
        trajectory_bonus: int,
    ) -> str:
        parts = [
            f"{recovery_minutes} minutes recovery after "
            f"{mission.duration.band.value} mission "
            f"({mission.duration.planned_minutes} work minutes)"
        ]
        if trajectory_bonus:
            parts.append(
                f"including +{trajectory_bonus} for recent intervention trajectory"
            )
        return "; ".join(parts)

    @staticmethod
    def _review_minutes(mission: MissionSpecification) -> int:
        # Integer arithmetic: clamp between 5 and 15.
        raw = mission.duration.planned_minutes // 4
        if raw < 5:
            return 5
        if raw > 15:
            return 15
        return raw

    @classmethod
    def _plan_review_windows(
        cls,
        mission: MissionSpecification,
        priority: EducationalPriority,
        work_complete_day: int,
    ) -> tuple[ReviewWindow, ...]:
        offsets = _REVIEW_OFFSETS_BY_PRIORITY[priority.score.band]
        duration = cls._review_minutes(mission)
        windows: list[ReviewWindow] = []
        for sequence, offset in enumerate(offsets, start=1):
            windows.append(
                ReviewWindow(
                    mission_id=mission.mission_id,
                    day_index=work_complete_day + offset,
                    duration_minutes=duration,
                    offset_from_completion=offset,
                    sequence=sequence,
                )
            )
        return tuple(windows)

    # --- capacity scheduling ------------------------------------------------

    @classmethod
    def _schedule_mission_work(
        cls,
        *,
        mission: MissionSpecification,
        remaining_capacity: dict[int, int],
        day_order: list[int],
        sessions: list[StudySession],
        sequence_index: int,
    ) -> tuple[int, int]:
        remaining = mission.duration.planned_minutes
        task_cursor = cls._TaskCursor(mission)
        last_work_day = -1

        while remaining > 0:
            day_index = cls._next_day_with_capacity(
                remaining_capacity, day_order, minimum=1
            )
            if day_index is None:
                raise EducationalInvariantViolation(
                    "insufficient availability to schedule remaining mission work",
                    invariant="StudyPlanner.work.capacity_exhausted",
                )
            chunk = min(
                remaining,
                remaining_capacity[day_index],
                _MAX_SESSION_MINUTES,
            )
            if chunk < _MIN_SESSION_MINUTES and remaining >= _MIN_SESSION_MINUTES:
                # Skip tiny leftover capacity; try later days first.
                later = cls._next_day_with_capacity(
                    remaining_capacity,
                    day_order,
                    minimum=_MIN_SESSION_MINUTES,
                    after_day=day_index,
                )
                if later is not None:
                    day_index = later
                    chunk = min(
                        remaining,
                        remaining_capacity[day_index],
                        _MAX_SESSION_MINUTES,
                    )
                elif remaining_capacity[day_index] > 0:
                    chunk = min(remaining, remaining_capacity[day_index])
                else:
                    raise EducationalInvariantViolation(
                        "insufficient availability to schedule remaining mission work",
                        invariant="StudyPlanner.work.capacity_exhausted",
                    )

            claimed_tasks = task_cursor.claim(chunk)
            sessions.append(
                StudySession(
                    session_id=StudySessionId(
                        f"sess-{mission.mission_id.value}-w"
                        f"{sequence_index:02d}-d{day_index}"
                    ),
                    sequence_index=sequence_index,
                    day_index=day_index,
                    kind=SessionKind.WORK,
                    mission_id=mission.mission_id,
                    allocated_minutes=chunk,
                    label=(
                        f"Work on {mission.objective.statement[:60]}"
                        if len(mission.objective.statement) > 60
                        else f"Work on {mission.objective.statement}"
                    ),
                    mission_task_ids=claimed_tasks,
                )
            )
            remaining_capacity[day_index] -= chunk
            remaining -= chunk
            last_work_day = day_index
            sequence_index += 1

        return sequence_index, last_work_day

    @classmethod
    def _schedule_recovery(
        cls,
        *,
        mission: MissionSpecification,
        recovery_minutes: int,
        remaining_capacity: dict[int, int],
        day_order: list[int],
        sessions: list[StudySession],
        sequence_index: int,
        preferred_day: int,
        not_before: int = 0,
    ) -> tuple[int, int]:
        day_index = cls._find_day_for_minutes(
            remaining_capacity,
            day_order,
            recovery_minutes,
            preferred_day=preferred_day,
            not_before=not_before,
        )
        if day_index is None:
            raise EducationalInvariantViolation(
                "insufficient availability to schedule recovery time",
                invariant="StudyPlanner.recovery.capacity_exhausted",
            )
        sessions.append(
            StudySession(
                session_id=StudySessionId(
                    f"sess-{mission.mission_id.value}-r"
                    f"{sequence_index:02d}-d{day_index}"
                ),
                sequence_index=sequence_index,
                day_index=day_index,
                kind=SessionKind.RECOVERY,
                mission_id=mission.mission_id,
                allocated_minutes=recovery_minutes,
                label=f"Recovery after mission {mission.mission_id.value}",
            )
        )
        remaining_capacity[day_index] -= recovery_minutes
        return sequence_index + 1, day_index

    @classmethod
    def _schedule_review(
        cls,
        *,
        mission: MissionSpecification,
        window: ReviewWindow,
        remaining_capacity: dict[int, int],
        day_order: list[int],
        sessions: list[StudySession],
        sequence_index: int,
        not_before: int = 0,
    ) -> tuple[int, int]:
        day_index = cls._find_day_for_minutes(
            remaining_capacity,
            day_order,
            window.duration_minutes,
            preferred_day=window.day_index,
            not_before=max(not_before, window.day_index),
        )
        if day_index is None:
            raise EducationalInvariantViolation(
                "insufficient availability to schedule review window",
                invariant="StudyPlanner.review.capacity_exhausted",
            )
        sessions.append(
            StudySession(
                session_id=StudySessionId(
                    f"sess-{mission.mission_id.value}-v"
                    f"{window.sequence:02d}-d{day_index}"
                ),
                sequence_index=sequence_index,
                day_index=day_index,
                kind=SessionKind.REVIEW,
                mission_id=mission.mission_id,
                allocated_minutes=window.duration_minutes,
                label=(
                    f"Review window {window.sequence} for mission "
                    f"{mission.mission_id.value}"
                ),
            )
        )
        remaining_capacity[day_index] -= window.duration_minutes
        return sequence_index + 1, day_index

    @staticmethod
    def _next_day_with_capacity(
        remaining_capacity: dict[int, int],
        day_order: list[int],
        *,
        minimum: int,
        after_day: int | None = None,
    ) -> int | None:
        for day_index in day_order:
            if after_day is not None and day_index <= after_day:
                continue
            if remaining_capacity.get(day_index, 0) >= minimum:
                return day_index
        return None

    @staticmethod
    def _find_day_for_minutes(
        remaining_capacity: dict[int, int],
        day_order: list[int],
        minutes: int,
        *,
        preferred_day: int,
        not_before: int | None = None,
    ) -> int | None:
        floor = preferred_day if not_before is None else not_before
        # Prefer exact preferred day, then the next available day at/after floor.
        if (
            preferred_day in remaining_capacity
            and remaining_capacity[preferred_day] >= minutes
            and preferred_day >= floor
        ):
            return preferred_day
        for day_index in day_order:
            if day_index < floor:
                continue
            if remaining_capacity.get(day_index, 0) >= minutes:
                return day_index
        return None

    # --- calendar / identity / rationale ------------------------------------

    @staticmethod
    def _build_calendar(
        availability: LearnerAvailability,
        sessions: list[StudySession],
    ) -> StudyCalendar:
        by_day: dict[int, list[StudySession]] = {
            window.day_index: [] for window in availability.windows
        }
        for session in sessions:
            if session.day_index not in by_day:
                by_day[session.day_index] = []
            by_day[session.day_index].append(session)

        days: list[StudyDay] = []
        for window in availability.windows:
            days.append(
                StudyDay(
                    day_index=window.day_index,
                    available_minutes=window.available_minutes,
                    sessions=tuple(by_day.get(window.day_index, ())),
                )
            )
        # Include any overflow days created only if sessions land outside
        # declared windows (should not happen with capacity checks).
        known = {window.day_index for window in availability.windows}
        for day_index in sorted(by_day):
            if day_index in known:
                continue
            allocated = sum(s.allocated_minutes for s in by_day[day_index])
            days.append(
                StudyDay(
                    day_index=day_index,
                    available_minutes=max(allocated, 1),
                    sessions=tuple(by_day[day_index]),
                )
            )
        return StudyCalendar.of(*days)

    @staticmethod
    def _plan_id(
        missions: tuple[MissionSpecification, ...],
        availability: LearnerAvailability,
        priority_id: PriorityId,
    ) -> StudyPlanId:
        mission_part = "_".join(m.mission_id.value for m in missions)
        return StudyPlanId(
            f"plan-{priority_id.value}-{mission_part}-{availability.fingerprint()}"
        )

    @classmethod
    def _build_rationale(
        cls,
        *,
        missions: tuple[MissionSpecification, ...],
        availability: LearnerAvailability,
        trajectory: LearningTrajectory,
        priority: EducationalPriority,
        schedule: StudySchedule,
        estimated: EstimatedCompletion,
        recovery_allocations: tuple[RecoveryAllocation, ...],
        review_windows: tuple[ReviewWindow, ...],
    ) -> str:
        mission_labels = ", ".join(m.mission_id.value for m in missions)
        order = " → ".join(
            f"{m.mission_id.value}({m.priority.band.value})" for m in missions
        )
        last = trajectory.last()
        trajectory_clause = (
            f"Learning trajectory length {trajectory.length()}"
            + (
                f"; last point {last.kind.value}:{last.label}"
                if last is not None
                else "; empty trajectory"
            )
        )
        recovery_total = sum(a.minutes for a in recovery_allocations)
        return (
            f"Study plan schedules missions [{mission_labels}] for student "
            f"{availability.student_id} under priority "
            f"{priority.score.band.value} ({priority.priority_id.value}). "
            f"Mission order by instructional urgency: {order}. "
            f"Allocated {estimated.total_work_minutes} work minutes across "
            f"{len(schedule.work_sessions())} work session(s), "
            f"{estimated.total_review_minutes} review minutes "
            f"({len(review_windows)} window(s)), and {recovery_total} recovery "
            f"minutes. Work completes on relative day "
            f"{estimated.work_complete_day_index}; plan completes on day "
            f"{estimated.plan_complete_day_index} "
            f"({estimated.horizon_band.value} horizon). "
            f"Availability fingerprint {availability.fingerprint()}. "
            f"{trajectory_clause}."
        )

    # --- task cursor --------------------------------------------------------

    class _TaskCursor:
        """Deterministic cursor that claims mission tasks into work sessions."""

        def __init__(self, mission: MissionSpecification) -> None:
            self._tasks = list(mission.sequence.tasks)
            self._index = 0
            self._remaining = (
                self._tasks[0].estimated_minutes if self._tasks else 0
            )

        def claim(self, minutes: int) -> tuple[MissionTaskId, ...]:
            if minutes <= 0:
                raise EducationalInvariantViolation(
                    "claim minutes must be positive",
                    invariant="StudyPlanner.task_cursor.minutes",
                )
            claimed: list[MissionTaskId] = []
            need = minutes
            while need > 0:
                if self._index >= len(self._tasks):
                    raise EducationalInvariantViolation(
                        "task cursor exhausted before session minutes claimed",
                        invariant="StudyPlanner.task_cursor.exhausted",
                    )
                task = self._tasks[self._index]
                if task.task_id not in claimed:
                    claimed.append(task.task_id)
                take = min(need, self._remaining)
                self._remaining -= take
                need -= take
                if self._remaining == 0:
                    self._index += 1
                    if self._index < len(self._tasks):
                        self._remaining = self._tasks[self._index].estimated_minutes
            return tuple(claimed)


def recovery_minutes_for(
    band: MissionDurationBand,
    *,
    trajectory_bonus: int = 0,
) -> int:
    """Return catalogue recovery minutes for a mission duration band."""
    try:
        return _RECOVERY_BY_DURATION[band] + trajectory_bonus
    except KeyError as exc:
        raise EducationalInvariantViolation(
            "unknown mission duration band for recovery catalogue",
            invariant="StudyPlanner.recovery.unknown_band",
        ) from exc


def review_offsets_for(band: PriorityScoreBand) -> tuple[int, ...]:
    """Return catalogue review-day offsets for a priority score band."""
    try:
        return _REVIEW_OFFSETS_BY_PRIORITY[band]
    except KeyError as exc:
        raise EducationalInvariantViolation(
            "unknown priority score band for review offsets",
            invariant="StudyPlanner.review.unknown_band",
        ) from exc


def max_session_minutes() -> int:
    """Return the fixed instructional sitting ceiling in minutes."""
    return _MAX_SESSION_MINUTES
