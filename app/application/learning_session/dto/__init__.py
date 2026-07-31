"""Immutable DTOs for the Learning Session Runtime."""

from __future__ import annotations

from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.completion_result import CompletionResult
from app.application.learning_session.dto.evidence_package import (
    EvidenceDisposition,
    EvidenceLifecycleState,
    EvidenceValidationResult,
    SessionEvidencePackage,
)
from app.application.learning_session.dto.evidence_summary import EvidenceSummary
from app.application.learning_session.dto.finish_review import (
    FinishReview,
    FinishReviewVerdict,
)
from app.application.learning_session.dto.learning_session_plan import (
    LearningSessionPlan,
)
from app.application.learning_session.dto.reflection_summary import ReflectionSummary
from app.application.learning_session.dto.runtime_snapshot import RuntimeSnapshot

__all__ = [
    "CandidateObservation",
    "CompletionResult",
    "EvidenceDisposition",
    "EvidenceLifecycleState",
    "EvidenceSummary",
    "EvidenceValidationResult",
    "FinishReview",
    "FinishReviewVerdict",
    "LearningSessionPlan",
    "ReflectionSummary",
    "RuntimeEvidenceType",
    "RuntimeSnapshot",
    "SessionEvidencePackage",
]
