"""Recommendation Engine bounded context — pure educational reasoning engine.

EDU-003.5 implementation of the Recommendation Engine.

Pure Domain-Driven Design only: an engine, an aggregate, value objects,
policies, and specifications. No persistence, Flask, ORM, HTTP APIs,
repositories, serialization, or AI.

``RecommendationEngine`` is the second educational reasoning engine of the
Education OS. It transforms ``student_state.StudentEducationalState``,
``mastery_estimation.MasteryAssessment``,
``educational_evidence.EducationalEvidence``, and
``knowledge_graph.KnowledgeGraph`` into immutable ``RecommendationSet``
results. It decides; it never mutates any of its inputs, orchestrates,
persists, updates the Digital Twin, generates missions, or invokes AI.

Unlike ``student_state``, ``educational_evidence``, and ``knowledge_graph``
— which deliberately stay isolated from one another — Recommendation
Engine exists specifically to reason across those bounded contexts and
Mastery Estimation. Every cross-context read happens through explicit,
narrow coercions at the engine boundary (see
``engines/recommendation_engine.py``); this context's own
``SubjectId``/``CompetencyId`` intentionally reuse the same string values
as their counterparts elsewhere for correlation, without claiming the
Python types are interchangeable.
"""

from __future__ import annotations

from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)
from domain.education.recommendation_engine.engines.recommendation_engine import (
    RecommendationEngine,
)
from domain.education.recommendation_engine.enums import (
    RecommendationCategory,
    RecommendationConstraintKind,
    RecommendationImpactBand,
    RecommendationPriorityBand,
    RecommendationReasonCode,
)
from domain.education.recommendation_engine.ids import (
    CompetencyId,
    RecommendationId,
    RecommendationSetId,
    SubjectId,
)
from domain.education.recommendation_engine.policies.constraint_policy import (
    ConstraintPolicy,
)
from domain.education.recommendation_engine.policies.impact_policy import ImpactPolicy
from domain.education.recommendation_engine.policies.ordering_policy import (
    OrderingPolicy,
)
from domain.education.recommendation_engine.policies.priority_policy import (
    PriorityPolicy,
)
from domain.education.recommendation_engine.policies.recommendation_policy import (
    RecommendationPolicy,
)
from domain.education.recommendation_engine.policies.recommendation_validation_policy import (  # noqa: E501
    RecommendationValidationPolicy,
)
from domain.education.recommendation_engine.specifications.constraint_specification import (  # noqa: E501
    ConstraintSpecification,
)
from domain.education.recommendation_engine.specifications.priority_specification import (  # noqa: E501
    PrioritySpecification,
)
from domain.education.recommendation_engine.specifications.recommendation_consistency_specification import (  # noqa: E501
    RecommendationConsistencySpecification,
)
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)
from domain.education.recommendation_engine.value_objects.recommendation_confidence import (  # noqa: E501
    RecommendationConfidence,
)
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)
from domain.education.recommendation_engine.value_objects.recommendation_explanation import (  # noqa: E501
    RecommendationExplanation,
)
from domain.education.recommendation_engine.value_objects.recommendation_impact import (
    RecommendationImpact,
)
from domain.education.recommendation_engine.value_objects.recommendation_ordering import (  # noqa: E501
    RecommendationOrdering,
)
from domain.education.recommendation_engine.value_objects.recommendation_priority import (  # noqa: E501
    RecommendationPriority,
)
from domain.education.recommendation_engine.value_objects.recommendation_reason import (
    RecommendationReason,
)
from domain.education.recommendation_engine.value_objects.recommendation_snapshot import (  # noqa: E501
    RecommendationSnapshot,
)
from domain.education.recommendation_engine.value_objects.recommendation_target import (
    RecommendationTarget,
)

__all__ = [
    # Engine
    "RecommendationEngine",
    # Aggregate
    "RecommendationSet",
    # Value objects
    "Recommendation",
    "RecommendationPriority",
    "RecommendationImpact",
    "RecommendationConfidence",
    "RecommendationReason",
    "RecommendationConstraint",
    "RecommendationTarget",
    "RecommendationOrdering",
    "RecommendationExplanation",
    "RecommendationSnapshot",
    # Identity
    "RecommendationSetId",
    "RecommendationId",
    "SubjectId",
    "CompetencyId",
    # Enums
    "RecommendationCategory",
    "RecommendationPriorityBand",
    "RecommendationImpactBand",
    "RecommendationReasonCode",
    "RecommendationConstraintKind",
    # Policies
    "RecommendationPolicy",
    "PriorityPolicy",
    "ImpactPolicy",
    "ConstraintPolicy",
    "OrderingPolicy",
    "RecommendationValidationPolicy",
    # Specifications
    "RecommendationConsistencySpecification",
    "PrioritySpecification",
    "ConstraintSpecification",
]
