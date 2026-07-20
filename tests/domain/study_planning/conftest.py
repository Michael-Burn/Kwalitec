"""Shared factories for Study Planning domain tests."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    LearningTrajectory,
    TrajectoryPoint,
    TrajectoryPointKind,
)
from domain.education.priority import (
    EducationalPriority,
    PriorityScoreBand,
    UrgencyLevel,
)
from domain.mission_generation import MissionSpecification
from domain.study_planning import (
    AvailabilityWindow,
    LearnerAvailability,
    StudyPlan,
    StudyPlanner,
)
from tests.domain.mission_generation.conftest import (
    generate_mission,
    make_aligned_priority,
)


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_availability(
    *,
    student_id: str = "student-ada",
    day_count: int = 10,
    minutes_per_day: int = 60,
) -> LearnerAvailability:
    windows = tuple(
        AvailabilityWindow(day_index=day, available_minutes=minutes_per_day)
        for day in range(day_count)
    )
    return LearnerAvailability(student_id=student_id, windows=windows)


def make_planning_priority(
    *,
    priority_id: str = "prio-001",
    student_id: str = "student-ada",
    score_band: PriorityScoreBand = PriorityScoreBand.HIGH,
    urgency_level: UrgencyLevel = UrgencyLevel.ELEVATED,
) -> EducationalPriority:
    return make_aligned_priority(
        priority_id=priority_id,
        student_id=student_id,
        score_band=score_band,
        urgency_level=urgency_level,
    )


def make_trajectory(
    *,
    with_intervention: bool = False,
) -> LearningTrajectory:
    points = [
        TrajectoryPoint(
            sequence=1,
            kind=TrajectoryPointKind.CREATED,
            label="twin-created",
        )
    ]
    if with_intervention:
        points.append(
            TrajectoryPoint(
                sequence=2,
                kind=TrajectoryPointKind.INTERVENTION,
                label="recent-scaffold",
            )
        )
    return LearningTrajectory.of(*points)


def plan_study(
    *,
    missions: tuple[MissionSpecification, ...] | None = None,
    availability: LearnerAvailability | None = None,
    trajectory: LearningTrajectory | None = None,
    priority: EducationalPriority | None = None,
    with_secondaries: bool = True,
) -> StudyPlan:
    missions = missions or (generate_mission(with_secondaries=with_secondaries),)
    availability = availability or make_availability()
    trajectory = trajectory or make_trajectory()
    priority = priority or make_planning_priority()
    return StudyPlanner.plan(missions, availability, trajectory, priority)
