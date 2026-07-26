"""Adaptive Study Planner consumer package (EP-001.2).

Projects EP-001.1 CanonicalLearnerState into planning inputs / daily study
plan outputs. Extends Runtime A PlanningService — does not replace it or
duplicate learner-state models.
"""

from __future__ import annotations

from app.infrastructure.adapters.adaptive_study_planner.consumer import (
    CanonicalPlannerConsumer,
    build_canonical_planner_consumer,
)
from app.infrastructure.adapters.adaptive_study_planner.contracts import (
    PLANNER_CONSUMER_VERSION,
    REASON_INVALID_STUDENT_ID,
    REASON_NO_ACTIVE_PLAN,
    REASON_STATE_UNAVAILABLE,
    REASON_TWIN_FLAG_OFF,
    SOURCE_SERVICE_ADAPTIVE_STUDY_PLANNER,
    AdaptivePlannerInputs,
    DailyStudyPlanProjection,
    MissionSlot,
    RecommendedWorkload,
    RevisionPriority,
    TopicPlanRow,
)
from app.infrastructure.adapters.adaptive_study_planner.daily_plan import (
    DailyStudyPlanAssembler,
    build_daily_study_plan_assembler,
)

__all__ = [
    "PLANNER_CONSUMER_VERSION",
    "REASON_INVALID_STUDENT_ID",
    "REASON_NO_ACTIVE_PLAN",
    "REASON_STATE_UNAVAILABLE",
    "REASON_TWIN_FLAG_OFF",
    "SOURCE_SERVICE_ADAPTIVE_STUDY_PLANNER",
    "AdaptivePlannerInputs",
    "CanonicalPlannerConsumer",
    "DailyStudyPlanAssembler",
    "DailyStudyPlanProjection",
    "MissionSlot",
    "RecommendedWorkload",
    "RevisionPriority",
    "TopicPlanRow",
    "build_canonical_planner_consumer",
    "build_daily_study_plan_assembler",
]
