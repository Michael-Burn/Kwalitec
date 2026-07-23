"""Mastery Estimation bounded context — pure educational reasoning engine.

EDU-003.4 implementation of the Mastery Estimation Engine.

Pure Domain-Driven Design only: an engine, an aggregate, value objects,
policies, and specifications. No persistence, Flask, ORM, HTTP APIs,
repositories, serialization, or AI.

``MasteryEstimator`` is the first educational reasoning engine of the
Education OS. It transforms ``student_state.StudentEducationalState``,
``educational_evidence.EducationalEvidence``, and
``knowledge_graph.KnowledgeGraph`` into immutable ``MasteryAssessment``
results. It reasons; it never mutates any of its inputs, orchestrates,
persists, generates recommendations or missions, or invokes AI.

Unlike ``student_state``, ``educational_evidence``, and ``knowledge_graph``
— which deliberately stay isolated from one another — Mastery Estimation
exists specifically to reason across those three bounded contexts. Every
cross-context read happens through explicit, narrow coercions at the
engine boundary (see ``engines/mastery_estimator.py``); this context's own
``SubjectId``/``CompetencyId`` intentionally reuse the same string values
as their counterparts elsewhere for correlation, without claiming the
Python types are interchangeable.
"""

from __future__ import annotations

from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.engines.mastery_estimator import (
    MasteryEstimator,
)
from domain.education.mastery_estimation.enums import (
    AssessmentReasonCode,
    KnowledgeGapKind,
    KnowledgeGapSeverity,
    LearningStabilityBand,
    MasteryBand,
)
from domain.education.mastery_estimation.ids import (
    AssessmentId,
    CompetencyId,
    SubjectId,
)
from domain.education.mastery_estimation.policies.assessment_validation_policy import (  # noqa: E501
    AssessmentValidationPolicy,
)
from domain.education.mastery_estimation.policies.confidence_policy import (
    ConfidencePolicy,
)
from domain.education.mastery_estimation.policies.evidence_weight_policy import (
    EvidenceWeightPolicy,
)
from domain.education.mastery_estimation.policies.mastery_policy import (
    MasteryPolicy,
)
from domain.education.mastery_estimation.policies.prerequisite_influence_policy import (  # noqa: E501
    PrerequisiteInfluencePolicy,
)
from domain.education.mastery_estimation.policies.stability_policy import (
    StabilityPolicy,
)
from domain.education.mastery_estimation.specifications.assessment_confidence_specification import (  # noqa: E501
    AssessmentConfidenceSpecification,
)
from domain.education.mastery_estimation.specifications.knowledge_gap_specification import (  # noqa: E501
    KnowledgeGapSpecification,
)
from domain.education.mastery_estimation.specifications.mastery_assessment_consistency_specification import (  # noqa: E501
    MasteryAssessmentConsistencySpecification,
)
from domain.education.mastery_estimation.value_objects.assessment_reason import (
    AssessmentReason,
)
from domain.education.mastery_estimation.value_objects.assessment_snapshot import (
    AssessmentSnapshot,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.confidence_score import (
    ConfidenceScore,
)
from domain.education.mastery_estimation.value_objects.evidence_contribution import (
    EvidenceContribution,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.mastery_estimation.value_objects.learning_stability import (
    LearningStability,
)
from domain.education.mastery_estimation.value_objects.mastery_confidence import (
    MasteryConfidence,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)
from domain.education.mastery_estimation.value_objects.subject_assessment import (
    SubjectAssessment,
)

__all__ = [
    # Engine
    "MasteryEstimator",
    # Aggregate
    "MasteryAssessment",
    # Value objects
    "MasteryScore",
    "ConfidenceScore",
    "MasteryConfidence",
    "LearningStability",
    "EvidenceContribution",
    "KnowledgeGap",
    "AssessmentReason",
    "CompetencyAssessment",
    "SubjectAssessment",
    "AssessmentSnapshot",
    # Identity
    "AssessmentId",
    "SubjectId",
    "CompetencyId",
    # Enums
    "MasteryBand",
    "LearningStabilityBand",
    "KnowledgeGapKind",
    "KnowledgeGapSeverity",
    "AssessmentReasonCode",
    # Policies
    "EvidenceWeightPolicy",
    "MasteryPolicy",
    "PrerequisiteInfluencePolicy",
    "ConfidencePolicy",
    "StabilityPolicy",
    "AssessmentValidationPolicy",
    # Specifications
    "MasteryAssessmentConsistencySpecification",
    "AssessmentConfidenceSpecification",
    "KnowledgeGapSpecification",
]
