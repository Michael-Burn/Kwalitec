"""Assessment domain exceptions."""

from __future__ import annotations

from domain.assessment.exceptions.errors import (
    AssessmentDomainError,
    AssessmentInvariantViolation,
    DuplicateQuestionReferenceError,
    InvalidAssessmentStateTransition,
    InvalidConfidenceRangeError,
    InvalidObservationPayloadError,
    MissingLearningObjectiveError,
)

__all__ = [
    "AssessmentDomainError",
    "AssessmentInvariantViolation",
    "DuplicateQuestionReferenceError",
    "InvalidAssessmentStateTransition",
    "InvalidConfidenceRangeError",
    "InvalidObservationPayloadError",
    "MissingLearningObjectiveError",
]
