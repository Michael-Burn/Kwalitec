"""Educational Decision bounded context — pure educational domain model.

IMP-011 implementation of Educational Decision architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask, ORM,
HTTP APIs, repositories, serialization, or DTOs.

This domain decides whether a planned educational intervention should proceed
now. It evaluates readiness for execution. It does not create strategies,
diagnose deficiencies, or orchestrate sessions.
"""

from __future__ import annotations

from domain.education.decision.aggregates.educational_decision import (
    EducationalDecision,
)
from domain.education.decision.entities.decision_reason import (
    DecisionReason,
    DecisionReasonId,
)
from domain.education.decision.entities.decision_references import (
    IntentionReference,
    PriorityReference,
    StrategyReference,
)
from domain.education.decision.entities.execution_constraint import (
    ExecutionConstraint,
    ExecutionConstraintId,
)
from domain.education.decision.entities.readiness_indicator import (
    ReadinessIndicator,
    ReadinessIndicatorId,
)
from domain.education.decision.enums import (
    DecisionOutcome,
    DecisionRevisionKind,
    DecisionStatus,
    ExecutionConstraintKind,
    ReadinessBand,
    ReadinessIndicatorKind,
)
from domain.education.decision.events.decision_made import DecisionMade
from domain.education.decision.events.decision_reconsidered import (
    DecisionReconsidered,
)
from domain.education.decision.policies.decision_policy import DecisionPolicy
from domain.education.decision.policies.readiness_policy import ReadinessPolicy
from domain.education.decision.specifications.decision_is_executable import (
    DecisionIsExecutableSpecification,
)
from domain.education.decision.specifications.intervention_is_ready import (
    InterventionIsReadySpecification,
)
from domain.education.decision.value_objects.decision_confidence import (
    DecisionConfidence,
)
from domain.education.decision.value_objects.readiness_level import ReadinessLevel
from domain.education.foundation.ids import DecisionId

__all__ = [
    # Aggregate
    "EducationalDecision",
    # Entities
    "DecisionReason",
    "DecisionReasonId",
    "ReadinessIndicator",
    "ReadinessIndicatorId",
    "ExecutionConstraint",
    "ExecutionConstraintId",
    "PriorityReference",
    "IntentionReference",
    "StrategyReference",
    # Value objects / identity
    "DecisionConfidence",
    "ReadinessLevel",
    "DecisionId",
    # Enums
    "DecisionStatus",
    "DecisionOutcome",
    "ReadinessBand",
    "ReadinessIndicatorKind",
    "ExecutionConstraintKind",
    "DecisionRevisionKind",
    # Policies
    "DecisionPolicy",
    "ReadinessPolicy",
    # Specifications
    "InterventionIsReadySpecification",
    "DecisionIsExecutableSpecification",
    # Events
    "DecisionMade",
    "DecisionReconsidered",
]
