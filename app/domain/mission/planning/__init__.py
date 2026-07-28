"""Mission planning — Twin decisions → study mission plans (AP-002D5).

The Mission Engine answers \"what should the learner do next?\".
It never answers \"what does the learner know?\" — that belongs to Reasoning.
Planning never reasons, never invents mastery, never notifies Tutor.
"""

from __future__ import annotations

from app.domain.mission.planning.activity_type import (
    KNOWN_PLANNING_ACTIVITY_TYPES,
    PlanningActivityType,
    parse_planning_activity_type,
)
from app.domain.mission.planning.batch import PlanningBatch
from app.domain.mission.planning.candidate import MissionCandidateProjection
from app.domain.mission.planning.context import PlanningContext
from app.domain.mission.planning.errors import (
    BrokenConceptReference,
    BrokenLearningObjectiveReference,
    DuplicateMissionRequest,
    IncompleteProvenance,
    InvalidDecisionVersion,
    InvalidPlanningSchema,
    MissingLearnerState,
    MissingProvenance,
    PlanningError,
    PlanningRejected,
    UnknownTwinVersion,
    UnsupportedPlanningContract,
)
from app.domain.mission.planning.events import (
    MissionGenerated,
    MissionPlanningCompleted,
    MissionPlanningSkipped,
    MissionPlanningStarted,
    PlanningEventKind,
)
from app.domain.mission.planning.plan import StudyMissionPlan
from app.domain.mission.planning.reference import PlanningReference
from app.domain.mission.planning.result import PlanningResult
from app.domain.mission.planning.version import PLANNING_VERSION, PlanningVersion

__all__ = [
    "KNOWN_PLANNING_ACTIVITY_TYPES",
    "PLANNING_VERSION",
    "BrokenConceptReference",
    "BrokenLearningObjectiveReference",
    "DuplicateMissionRequest",
    "IncompleteProvenance",
    "InvalidDecisionVersion",
    "InvalidPlanningSchema",
    "MissionCandidateProjection",
    "MissionGenerated",
    "MissionPlanningCompleted",
    "MissionPlanningSkipped",
    "MissionPlanningStarted",
    "MissingLearnerState",
    "MissingProvenance",
    "PlanningActivityType",
    "PlanningBatch",
    "PlanningContext",
    "PlanningError",
    "PlanningEventKind",
    "PlanningReference",
    "PlanningRejected",
    "PlanningResult",
    "PlanningVersion",
    "StudyMissionPlan",
    "UnknownTwinVersion",
    "UnsupportedPlanningContract",
    "parse_planning_activity_type",
]
