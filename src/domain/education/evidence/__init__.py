"""Evidence bounded context — pure educational domain model.

IMP-004 implementation of the Educational Evidence architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask,
SQLAlchemy, APIs, repositories, serialization, or DTOs.

This domain records educational observations only. It does not diagnose,
recommend, or prioritise.
"""

from __future__ import annotations

from domain.education.evidence.aggregates.evidence_record import EvidenceRecord
from domain.education.evidence.entities.evidence_context import (
    EvidenceContext,
    EvidenceContextId,
)
from domain.education.evidence.entities.evidence_item import (
    EvidenceItem,
    EvidenceItemId,
)
from domain.education.evidence.entities.evidence_source import (
    EvidenceSource,
    EvidenceSourceId,
)
from domain.education.evidence.enums import (
    EvidenceItemKind,
    EvidenceRecordStatus,
    EvidenceSourceKind,
    EvidenceStrengthLevel,
)
from domain.education.evidence.events.evidence_recorded import EvidenceRecorded
from domain.education.evidence.events.evidence_updated import EvidenceUpdated
from domain.education.evidence.policies.evidence_consistency_policy import (
    EvidenceConsistencyPolicy,
)
from domain.education.evidence.policies.evidence_validation_policy import (
    EvidenceValidationPolicy,
)
from domain.education.evidence.specifications.evidence_is_consistent import (
    EvidenceIsConsistentSpecification,
)
from domain.education.evidence.specifications.evidence_is_sufficient import (
    EvidenceIsSufficientSpecification,
)
from domain.education.evidence.value_objects.confidence_measure import ConfidenceMeasure
from domain.education.evidence.value_objects.evidence_strength import EvidenceStrength
from domain.education.evidence.value_objects.evidence_timestamp import EvidenceTimestamp

__all__ = [
    # Aggregate
    "EvidenceRecord",
    # Entities
    "EvidenceItem",
    "EvidenceItemId",
    "EvidenceSource",
    "EvidenceSourceId",
    "EvidenceContext",
    "EvidenceContextId",
    # Value objects
    "EvidenceStrength",
    "EvidenceTimestamp",
    "ConfidenceMeasure",
    # Enums
    "EvidenceItemKind",
    "EvidenceSourceKind",
    "EvidenceRecordStatus",
    "EvidenceStrengthLevel",
    # Policies
    "EvidenceValidationPolicy",
    "EvidenceConsistencyPolicy",
    # Specifications
    "EvidenceIsSufficientSpecification",
    "EvidenceIsConsistentSpecification",
    # Events
    "EvidenceRecorded",
    "EvidenceUpdated",
]
