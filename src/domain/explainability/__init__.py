"""Educational Explainability Engine — deterministic decision explanations.

EDU-005: Convert MissionSpecification, StudyPlan, ProgressReport, and
RecommendationSpecification into an EducationalExplanation that answers the
four-question explainability contract (what we know, what we estimate, why,
what next) with a DecisionTrace and EvidenceReferences.

The explanation is part of the educational model — not UI chrome.

Pure domain logic only. No AI, no prompting, no randomness, no persistence,
Flask, ORM, HTTP, or DTOs. Educational decisions are narrated, never modified.
"""

from __future__ import annotations

from domain.explainability.decision_trace import DecisionTrace, TraceStep
from domain.explainability.educational_explanation import EducationalExplanation
from domain.explainability.enums import (
    DecisionStage,
    EvidenceSourceKind,
    ExplanationSectionKind,
)
from domain.explainability.evidence_reference import EvidenceReference
from domain.explainability.explanation_builder import ExplanationBuilder
from domain.explainability.explanation_section import ExplanationSection
from domain.explainability.ids import (
    DecisionTraceId,
    EducationalExplanationId,
    EvidenceReferenceId,
    ExplanationSectionId,
)

__all__ = [
    # Aggregate
    "EducationalExplanation",
    "ExplanationSection",
    "DecisionTrace",
    "TraceStep",
    "EvidenceReference",
    # Identities
    "EducationalExplanationId",
    "ExplanationSectionId",
    "DecisionTraceId",
    "EvidenceReferenceId",
    # Enums
    "ExplanationSectionKind",
    "DecisionStage",
    "EvidenceSourceKind",
    # Builder
    "ExplanationBuilder",
]
