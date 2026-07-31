"""State transition model for the educational runtime engine."""

from __future__ import annotations

from enum import StrEnum


class EnrolmentStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"


class PlanInstanceStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class MissionStatus(StrEnum):
    GENERATED = "generated"
    ACCEPTED = "accepted"  # SR-002a: Mission Accepted ≡ Study Session start
    DEFERRED = "deferred"  # SR-002a: ILE-004 honest deferral
    COMPLETED = "completed"


class JourneyStage(StrEnum):
    """Student journey stage relative to the published syllabus."""

    NOT_STARTED = "not_started"
    LEARNING = "learning"
    SYLLABUS_COMPLETE = "syllabus_complete"
    REVISION = "revision"


_ENROLMENT_TRANSITIONS: dict[EnrolmentStatus, frozenset[EnrolmentStatus]] = {
    EnrolmentStatus.ACTIVE: frozenset(
        {EnrolmentStatus.COMPLETED, EnrolmentStatus.WITHDRAWN}
    ),
    EnrolmentStatus.COMPLETED: frozenset(),
    EnrolmentStatus.WITHDRAWN: frozenset(),
}

_PLAN_TRANSITIONS: dict[PlanInstanceStatus, frozenset[PlanInstanceStatus]] = {
    PlanInstanceStatus.ACTIVE: frozenset(
        {PlanInstanceStatus.PAUSED, PlanInstanceStatus.COMPLETED}
    ),
    PlanInstanceStatus.PAUSED: frozenset(
        {PlanInstanceStatus.ACTIVE, PlanInstanceStatus.COMPLETED}
    ),
    PlanInstanceStatus.COMPLETED: frozenset(),
}

_MISSION_TRANSITIONS: dict[MissionStatus, frozenset[MissionStatus]] = {
    MissionStatus.GENERATED: frozenset(
        {
            MissionStatus.ACCEPTED,
            MissionStatus.DEFERRED,
            MissionStatus.COMPLETED,  # pilot / rollback Mark-complete path
        }
    ),
    MissionStatus.ACCEPTED: frozenset(
        {MissionStatus.COMPLETED, MissionStatus.DEFERRED}
    ),
    MissionStatus.DEFERRED: frozenset(
        {MissionStatus.ACCEPTED, MissionStatus.COMPLETED}
    ),
    MissionStatus.COMPLETED: frozenset(),
}


class IllegalRuntimeTransition(ValueError):  # noqa: N818
    """Raised when a runtime state transition is not allowed."""


def assert_enrolment_transition(
    current: EnrolmentStatus | str,
    target: EnrolmentStatus | str,
) -> None:
    _assert_transition(
        EnrolmentStatus(current),
        EnrolmentStatus(target),
        _ENROLMENT_TRANSITIONS,
        "enrolment",
    )


def assert_plan_transition(
    current: PlanInstanceStatus | str,
    target: PlanInstanceStatus | str,
) -> None:
    _assert_transition(
        PlanInstanceStatus(current),
        PlanInstanceStatus(target),
        _PLAN_TRANSITIONS,
        "study_plan_instance",
    )


def assert_mission_transition(
    current: MissionStatus | str,
    target: MissionStatus | str,
) -> None:
    _assert_transition(
        MissionStatus(current),
        MissionStatus(target),
        _MISSION_TRANSITIONS,
        "mission_instance",
    )


def next_journey_stage(
    *,
    completed_topic_count: int,
    total_topic_count: int,
) -> JourneyStage:
    """Resolve journey stage from derived completion counts."""
    if total_topic_count <= 0:
        return JourneyStage.NOT_STARTED
    if completed_topic_count <= 0:
        return JourneyStage.NOT_STARTED
    if completed_topic_count >= total_topic_count:
        return JourneyStage.SYLLABUS_COMPLETE
    return JourneyStage.LEARNING


def _assert_transition(
    current: StrEnum,
    target: StrEnum,
    table: dict,
    label: str,
) -> None:
    if current == target:
        return
    allowed = table.get(current, frozenset())
    if target not in allowed:
        raise IllegalRuntimeTransition(
            f"illegal {label} transition {current.value} → {target.value}"
        )
