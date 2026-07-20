"""Educational Foundation Domain — shared educational primitives.

IMP-001 package for the Educational Operating System.

Pure domain model only: identities, enums, references, and shared bases.
No persistence, Flask, ORM, APIs, UI, AI, or infrastructure.
"""

from __future__ import annotations

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    DependencyKind,
    DiagnosisType,
    EvidenceType,
    LearningDimension,
    ReflectionType,
    RepresentationKind,
    TeachingIntentionType,
    TeachingStrategyType,
    TransferLevel,
    UnderstandingLevel,
)
from domain.education.foundation.errors import (
    EducationalDomainError,
    EducationalInvariantViolation,
)
from domain.education.foundation.ids import (
    ConceptId,
    DecisionId,
    DiagnosisId,
    DigitalTwinId,
    EvidenceId,
    HypothesisId,
    LearningEpisodeId,
    LearningObjectiveId,
    MisconceptionId,
    OrchestratorId,
    PriorityId,
    ReflectionId,
    StudentKnowledgeId,
    TeachingIntentionId,
    TeachingStrategyId,
)
from domain.education.foundation.references import (
    ApplicationContextReference,
    ConceptReference,
    DependencyReference,
    LearningObjectiveReference,
    MisconceptionReference,
    RepresentationReference,
    TransferContextReference,
)
from domain.education.foundation.result import EducationalResult

__all__ = [
    # Bases / errors / result
    "EducationalValueObject",
    "EducationalEntity",
    "EducationalDomainError",
    "EducationalInvariantViolation",
    "EducationalResult",
    "require_identity_value",
    "require_non_empty_text",
    # Identities
    "LearningObjectiveId",
    "ConceptId",
    "LearningEpisodeId",
    "TeachingStrategyId",
    "TeachingIntentionId",
    "DiagnosisId",
    "HypothesisId",
    "PriorityId",
    "DecisionId",
    "OrchestratorId",
    "DigitalTwinId",
    "EvidenceId",
    "ReflectionId",
    "StudentKnowledgeId",
    "MisconceptionId",
    # Enums
    "UnderstandingLevel",
    "LearningDimension",
    "TeachingIntentionType",
    "TeachingStrategyType",
    "DiagnosisType",
    "EvidenceType",
    "ReflectionType",
    "ConfidenceLevel",
    "TransferLevel",
    "RepresentationKind",
    "DependencyKind",
    # References
    "LearningObjectiveReference",
    "ConceptReference",
    "MisconceptionReference",
    "RepresentationReference",
    "DependencyReference",
    "TransferContextReference",
    "ApplicationContextReference",
]
