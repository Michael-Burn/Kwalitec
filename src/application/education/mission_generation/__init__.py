"""Adaptive Mission Generator — PRD-001.

Application-layer capability that transforms an immutable
``RecommendationSet`` into an executable ``MissionPlan``.

Consumes educational decisions. Produces learning work.

Does not estimate mastery, generate recommendations, modify
``StudentEducationalState``, persist, call Flask/SQLAlchemy, or invoke AI.
"""

from __future__ import annotations

from application.education.mission_generation.adaptive_mission_generator import (
    AdaptiveMissionGenerator,
)
from application.education.mission_generation.enums import (
    LearningPace,
    MissionConstraintKind,
    MissionDurationBand,
    MissionObjectiveCode,
    MissionPriorityBand,
    MissionRecurrenceBand,
    MissionStepAction,
    MissionType,
)
from application.education.mission_generation.errors import (
    MissionGenerationError,
    MissionInvariantViolation,
)
from application.education.mission_generation.ids import (
    MissionId,
    MissionPlanId,
    MissionStepId,
)
from application.education.mission_generation.models import (
    Mission,
    MissionConstraint,
    MissionEstimate,
    MissionObjective,
    MissionOrdering,
    MissionPlan,
    MissionSnapshot,
    MissionStep,
    MissionSummary,
)
from application.education.mission_generation.planning_constraints import (
    PlanningConstraints,
)
from application.education.mission_generation.ports import (
    MissionPublisher,
    MissionTemplateProvider,
    StudyConstraintProvider,
)
from application.education.mission_generation.rules import (
    ConstraintRules,
    DurationRules,
    MappingRules,
    MergeRules,
    OrderingRules,
    SplitRules,
)
from application.education.mission_generation.rules.mapping_rules import MissionIntent
from application.education.mission_generation.rules.merge_rules import (
    MergedRecommendationGroup,
)

__all__ = [
    # Generator
    "AdaptiveMissionGenerator",
    # Models
    "Mission",
    "MissionPlan",
    "MissionStep",
    "MissionObjective",
    "MissionConstraint",
    "MissionEstimate",
    "MissionOrdering",
    "MissionSnapshot",
    "MissionSummary",
    # Inputs
    "PlanningConstraints",
    "MissionIntent",
    "MergedRecommendationGroup",
    # Identity
    "MissionPlanId",
    "MissionId",
    "MissionStepId",
    # Enums
    "MissionType",
    "MissionDurationBand",
    "MissionPriorityBand",
    "MissionConstraintKind",
    "MissionStepAction",
    "MissionObjectiveCode",
    "MissionRecurrenceBand",
    "LearningPace",
    # Errors
    "MissionGenerationError",
    "MissionInvariantViolation",
    # Rules
    "MappingRules",
    "DurationRules",
    "MergeRules",
    "SplitRules",
    "OrderingRules",
    "ConstraintRules",
    # Ports
    "MissionPublisher",
    "MissionTemplateProvider",
    "StudyConstraintProvider",
]
