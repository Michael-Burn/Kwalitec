"""Teaching Intention bounded context — pure educational domain model.

IMP-009 implementation of Teaching Intention architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask, ORM,
HTTP APIs, repositories, serialization, or DTOs.

This domain converts Educational Priorities into explicit teaching intentions.
It answers only: what educational change should happen next? It does not
choose teaching strategies, construct learning episodes, or orchestrate
sessions.
"""

from __future__ import annotations

from domain.education.foundation.enums import TeachingIntentionType
from domain.education.foundation.ids import TeachingIntentionId
from domain.education.teaching_intention.aggregates.teaching_intention import (
    TeachingIntention,
)
from domain.education.teaching_intention.entities.intention_constraint import (
    IntentionConstraint,
    IntentionConstraintId,
)
from domain.education.teaching_intention.entities.intention_goal import (
    IntentionGoal,
    IntentionGoalId,
)
from domain.education.teaching_intention.entities.intention_reference import (
    DiagnosisReference,
    HypothesisReference,
    PriorityReference,
)
from domain.education.teaching_intention.entities.intention_scope import (
    IntentionScope,
    IntentionScopeId,
)
from domain.education.teaching_intention.enums import (
    IntentionConstraintKind,
    IntentionRevisionKind,
    IntentionScopeKind,
    IntentionStatus,
    IntentionStrengthLevel,
)
from domain.education.teaching_intention.events.intention_created import (
    TeachingIntentionCreated,
)
from domain.education.teaching_intention.events.intention_revised import (
    TeachingIntentionRevised,
)
from domain.education.teaching_intention.policies.intention_alignment_policy import (
    IntentionAlignmentPolicy,
)
from domain.education.teaching_intention.policies.intention_validation_policy import (
    IntentionValidationPolicy,
)
from domain.education.teaching_intention.specifications.intention_is_actionable import (
    IntentionIsActionableSpecification,
)
from domain.education.teaching_intention.specifications.intention_is_aligned import (
    IntentionIsAlignedSpecification,
)
from domain.education.teaching_intention.value_objects.expected_outcome import (
    ExpectedOutcome,
)
from domain.education.teaching_intention.value_objects.intention_strength import (
    IntentionStrength,
)

__all__ = [
    # Aggregate
    "TeachingIntention",
    # Entities
    "IntentionGoal",
    "IntentionGoalId",
    "IntentionScope",
    "IntentionScopeId",
    "IntentionConstraint",
    "IntentionConstraintId",
    "PriorityReference",
    "DiagnosisReference",
    "HypothesisReference",
    # Value objects / identity
    "IntentionStrength",
    "ExpectedOutcome",
    "TeachingIntentionId",
    "TeachingIntentionType",
    # Enums
    "IntentionStatus",
    "IntentionStrengthLevel",
    "IntentionScopeKind",
    "IntentionConstraintKind",
    "IntentionRevisionKind",
    # Policies
    "IntentionValidationPolicy",
    "IntentionAlignmentPolicy",
    # Specifications
    "IntentionIsActionableSpecification",
    "IntentionIsAlignedSpecification",
    # Events
    "TeachingIntentionCreated",
    "TeachingIntentionRevised",
]
