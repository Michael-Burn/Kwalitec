"""Educational Priority bounded context — pure educational domain model.

IMP-008 implementation of Educational Priority architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask, ORM,
HTTP APIs, repositories, serialization, or DTOs.

This domain determines the instructional ordering of educational work. It
answers only: what should the tutor address first? It does not diagnose,
explain, or choose teaching strategies. Severity (learner condition) is never
conflated with priority (instructional ordering).
"""

from __future__ import annotations

from domain.education.foundation.ids import PriorityId
from domain.education.priority.aggregates.educational_priority import (
    EducationalPriority,
)
from domain.education.priority.entities.priority_constraint import (
    PriorityConstraint,
    PriorityConstraintId,
)
from domain.education.priority.entities.priority_factor import (
    PriorityFactor,
    PriorityFactorId,
)
from domain.education.priority.entities.priority_references import (
    DiagnosisReference,
    HypothesisReference,
)
from domain.education.priority.entities.priority_scope import (
    PriorityScope,
    PriorityScopeId,
)
from domain.education.priority.enums import (
    InstructionalImpactLevel,
    PriorityConstraintKind,
    PriorityFactorKind,
    PriorityRevisionKind,
    PriorityScopeKind,
    PriorityScoreBand,
    PriorityStatus,
    UrgencyLevel,
)
from domain.education.priority.events.priority_assigned import PriorityAssigned
from domain.education.priority.events.priority_revised import PriorityRevised
from domain.education.priority.policies.priority_calculation_policy import (
    PriorityCalculationPolicy,
)
from domain.education.priority.policies.priority_validation_policy import (
    PriorityValidationPolicy,
)
from domain.education.priority.specifications.priority_is_actionable import (
    PriorityIsActionableSpecification,
)
from domain.education.priority.specifications.priority_is_stable import (
    PriorityIsStableSpecification,
)
from domain.education.priority.value_objects.instructional_impact import (
    InstructionalImpact,
)
from domain.education.priority.value_objects.priority_score import PriorityScore
from domain.education.priority.value_objects.urgency import Urgency

__all__ = [
    # Aggregate
    "EducationalPriority",
    # Entities
    "PriorityFactor",
    "PriorityFactorId",
    "PriorityScope",
    "PriorityScopeId",
    "PriorityConstraint",
    "PriorityConstraintId",
    "DiagnosisReference",
    "HypothesisReference",
    # Value objects / identity
    "PriorityScore",
    "Urgency",
    "InstructionalImpact",
    "PriorityId",
    # Enums
    "PriorityStatus",
    "PriorityFactorKind",
    "PriorityScoreBand",
    "UrgencyLevel",
    "InstructionalImpactLevel",
    "PriorityScopeKind",
    "PriorityConstraintKind",
    "PriorityRevisionKind",
    # Policies
    "PriorityValidationPolicy",
    "PriorityCalculationPolicy",
    # Specifications
    "PriorityIsActionableSpecification",
    "PriorityIsStableSpecification",
    # Events
    "PriorityAssigned",
    "PriorityRevised",
]
