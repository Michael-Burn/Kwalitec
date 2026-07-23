"""Educational Evidence bounded context — the Educational Evidence Engine.

EDU-003.2 implementation of the Educational Evidence Engine.

Pure Domain-Driven Design only: an aggregate, value objects, policies, and
specifications. No persistence, Flask, ORM, HTTP APIs, repositories,
serialization, or DTOs, and no AI.

This engine transforms every meaningful student interaction into
deterministic educational evidence. Educational evidence is the only
mechanism through which ``StudentEducationalState`` and
``EducationalDigitalTwin`` may evolve — but this milestone deliberately
does not wire evidence into either of those aggregates, into the
Recommendation or Mastery Engines, or into persistence. Those integrations
belong to later milestones.

This context is intentionally isolated from every other education bounded
context, including the unrelated, pre-existing
``domain.education.evidence`` (IMP-004 ``EvidenceRecord``) package, which
serves a different pipeline and is left untouched.
"""

from __future__ import annotations

from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)
from domain.education.educational_evidence.enums import (
    EvidenceSourceKind,
    EvidenceType,
    EvidenceWeightBand,
    LearningEnvironmentKind,
)
from domain.education.educational_evidence.ids import (
    CheckpointId,
    CompetencyId,
    EvidenceId,
    MissionId,
    SubjectId,
)
from domain.education.educational_evidence.policies.evidence_normalisation_policy import (  # noqa: E501
    EvidenceNormalisationPolicy,
)
from domain.education.educational_evidence.policies.evidence_validation_policy import (
    EvidenceValidationPolicy,
)
from domain.education.educational_evidence.specifications.evidence_belongs_to_student import (  # noqa: E501
    EvidenceBelongsToStudentSpecification,
)
from domain.education.educational_evidence.specifications.evidence_is_consistent import (  # noqa: E501
    EvidenceIsConsistentSpecification,
)
from domain.education.educational_evidence.specifications.normalised_evidence import (
    NormalisedEvidenceSpecification,
)
from domain.education.educational_evidence.value_objects.evidence_context import (
    EvidenceContext,
)
from domain.education.educational_evidence.value_objects.evidence_metadata import (
    EvidenceMetadata,
)
from domain.education.educational_evidence.value_objects.evidence_snapshot import (
    EvidenceSnapshot,
)
from domain.education.educational_evidence.value_objects.evidence_source import (
    EvidenceSource,
)
from domain.education.educational_evidence.value_objects.evidence_timestamp import (
    EvidenceTimestamp,
)
from domain.education.educational_evidence.value_objects.evidence_weight import (
    EvidenceWeight,
)
from domain.education.educational_evidence.value_objects.learning_context import (
    LearningContext,
)
from domain.education.educational_evidence.value_objects.learning_environment import (
    LearningEnvironment,
)

__all__ = [
    # Aggregate
    "EducationalEvidence",
    # Value objects
    "EvidenceSource",
    "EvidenceWeight",
    "EvidenceContext",
    "EvidenceMetadata",
    "LearningContext",
    "LearningEnvironment",
    "EvidenceTimestamp",
    "EvidenceSnapshot",
    # Identity
    "EvidenceId",
    "SubjectId",
    "CompetencyId",
    "MissionId",
    "CheckpointId",
    # Enums
    "EvidenceType",
    "EvidenceSourceKind",
    "LearningEnvironmentKind",
    "EvidenceWeightBand",
    # Policies
    "EvidenceValidationPolicy",
    "EvidenceNormalisationPolicy",
    # Specifications
    "EvidenceIsConsistentSpecification",
    "EvidenceBelongsToStudentSpecification",
    "NormalisedEvidenceSpecification",
]
