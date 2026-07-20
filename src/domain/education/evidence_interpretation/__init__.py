"""Evidence Interpretation bounded context — pure educational domain model.

IMP-005 implementation of Evidence Interpretation architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask,
SQLAlchemy, APIs, repositories, serialization, or DTOs.

This domain converts raw educational observations into interpreted educational
patterns. It does not diagnose, recommend, or prioritise.
"""

from __future__ import annotations

from domain.education.evidence_interpretation.aggregates.interpretation import (
    Interpretation,
)
from domain.education.evidence_interpretation.entities.evidence_cluster import (
    EvidenceCluster,
    EvidenceClusterId,
)
from domain.education.evidence_interpretation.entities.interpretation_context import (
    InterpretationContext,
    InterpretationContextId,
)
from domain.education.evidence_interpretation.entities.interpreted_pattern import (
    REPEATED_PATTERN_KINDS,
    InterpretedPattern,
    InterpretedPatternId,
)
from domain.education.evidence_interpretation.enums import (
    EducationalScopeKind,
    InterpretationStatus,
    PatternKind,
)
from domain.education.evidence_interpretation.events.interpretation_created import (
    InterpretationCreated,
)
from domain.education.evidence_interpretation.policies.clustering_policy import (
    ClusteringPolicy,
)
from domain.education.evidence_interpretation.policies.interpretation_validation_policy import (  # noqa: E501
    InterpretationId,
    InterpretationValidationPolicy,
)
from domain.education.evidence_interpretation.specifications.interpretation_is_actionable import (  # noqa: E501
    InterpretationIsActionableSpecification,
)
from domain.education.evidence_interpretation.specifications.interpretation_is_consistent import (  # noqa: E501
    InterpretationIsConsistentSpecification,
)
from domain.education.evidence_interpretation.value_objects.interpretation_confidence import (  # noqa: E501
    InterpretationConfidence,
)
from domain.education.evidence_interpretation.value_objects.interpretation_summary import (  # noqa: E501
    InterpretationSummary,
)

__all__ = [
    # Aggregate
    "Interpretation",
    # Entities
    "InterpretedPattern",
    "InterpretedPatternId",
    "EvidenceCluster",
    "EvidenceClusterId",
    "InterpretationContext",
    "InterpretationContextId",
    # Value objects / identity
    "InterpretationConfidence",
    "InterpretationSummary",
    "InterpretationId",
    "REPEATED_PATTERN_KINDS",
    # Enums
    "PatternKind",
    "InterpretationStatus",
    "EducationalScopeKind",
    # Policies
    "InterpretationValidationPolicy",
    "ClusteringPolicy",
    # Specifications
    "InterpretationIsActionableSpecification",
    "InterpretationIsConsistentSpecification",
    # Events
    "InterpretationCreated",
]
