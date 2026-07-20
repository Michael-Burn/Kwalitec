"""Study Planning Engine — deterministic Educational OS study plans.

EDU-002: Generate StudyPlans from MissionSpecifications, Learner Availability,
Learning Trajectory, and Educational Priority.

Pure domain logic only. No AI, no prompting, no randomness, no persistence,
Flask, ORM, HTTP, calendar APIs, or DTOs.
"""

from __future__ import annotations

from domain.study_planning.enums import PlanningHorizonBand, SessionKind
from domain.study_planning.ids import StudyPlanId, StudySessionId
from domain.study_planning.learner_availability import (
    AvailabilityWindow,
    LearnerAvailability,
)
from domain.study_planning.study_calendar import StudyCalendar
from domain.study_planning.study_day import StudyDay
from domain.study_planning.study_plan import (
    EstimatedCompletion,
    RecoveryAllocation,
    ReviewWindow,
    StudyPlan,
)
from domain.study_planning.study_planner import (
    StudyPlanner,
    max_session_minutes,
    recovery_minutes_for,
    review_offsets_for,
)
from domain.study_planning.study_schedule import StudySchedule
from domain.study_planning.study_session import StudySession

__all__ = [
    # Aggregate / plan
    "StudyPlan",
    "EstimatedCompletion",
    "ReviewWindow",
    "RecoveryAllocation",
    # Schedule structures
    "StudySession",
    "StudyDay",
    "StudyCalendar",
    "StudySchedule",
    # Constraints
    "LearnerAvailability",
    "AvailabilityWindow",
    # Identities
    "StudyPlanId",
    "StudySessionId",
    # Enums
    "SessionKind",
    "PlanningHorizonBand",
    # Planner
    "StudyPlanner",
    "recovery_minutes_for",
    "review_offsets_for",
    "max_session_minutes",
]
