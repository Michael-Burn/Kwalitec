"""Tutor explainability — validated provenance → learner-facing narration (AP-002D6).

The Tutor explains.
It never infers.
It never predicts.
It never estimates mastery.
It never creates recommendations independently.

Pipeline:
  EducationalDecisionSet + Twin (+ optional StudyMissionPlan / Graph)
    → ExplanationBuilder
    → TutorExplanation
    → validation
    → factual events
    → STOP
"""

from __future__ import annotations

from app.domain.intelligent_tutor.explainability.context import ExplanationContext
from app.domain.intelligent_tutor.explainability.errors import (
    BrokenConceptReference,
    BrokenLearningObjectiveReference,
    DuplicateExplanationRequest,
    ExplanationError,
    ExplanationRejected,
    IncompleteProvenance,
    InvalidDecisionVersion,
    InvalidExplanationSchema,
    MissingExplanationInput,
    MissingProvenance,
    MissionVersionMismatch,
    TwinVersionMismatch,
    UnknownExplanationSchema,
    UnknownTwinVersion,
    UnsupportedExplanationContract,
)
from app.domain.intelligent_tutor.explainability.events import (
    ExplanationEventKind,
    TutorExplanationGenerated,
    TutorExplanationRequested,
    TutorExplanationUnavailable,
)
from app.domain.intelligent_tutor.explainability.explanation import TutorExplanation
from app.domain.intelligent_tutor.explainability.reference import ExplanationReference
from app.domain.intelligent_tutor.explainability.result import ExplanationResult
from app.domain.intelligent_tutor.explainability.section import (
    KNOWN_EXPLANATION_SECTION_KINDS,
    ConceptExplanation,
    DecisionExplanation,
    EvidenceExplanation,
    ExplanationSection,
    ExplanationSectionKind,
    LearningObjectiveExplanation,
    MissionExplanation,
    parse_section_kind,
)
from app.domain.intelligent_tutor.explainability.version import (
    EXPLANATION_VERSION,
    ExplanationVersion,
)

__all__ = [
    "EXPLANATION_VERSION",
    "KNOWN_EXPLANATION_SECTION_KINDS",
    "BrokenConceptReference",
    "BrokenLearningObjectiveReference",
    "ConceptExplanation",
    "DecisionExplanation",
    "DuplicateExplanationRequest",
    "EvidenceExplanation",
    "ExplanationContext",
    "ExplanationError",
    "ExplanationEventKind",
    "ExplanationReference",
    "ExplanationRejected",
    "ExplanationResult",
    "ExplanationSection",
    "ExplanationSectionKind",
    "ExplanationVersion",
    "IncompleteProvenance",
    "InvalidDecisionVersion",
    "InvalidExplanationSchema",
    "LearningObjectiveExplanation",
    "MissionExplanation",
    "MissingExplanationInput",
    "MissingProvenance",
    "MissionVersionMismatch",
    "TutorExplanation",
    "TutorExplanationGenerated",
    "TutorExplanationRequested",
    "TutorExplanationUnavailable",
    "TwinVersionMismatch",
    "UnknownExplanationSchema",
    "UnknownTwinVersion",
    "UnsupportedExplanationContract",
    "parse_section_kind",
]
