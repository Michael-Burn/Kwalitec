"""Assessment domain exceptions.

Architecture Source
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md
    knowledge/product/AP-002/EDUCATIONAL_MODEL.md
Concept
    Assessment Domain Errors
"""

from __future__ import annotations

from domain.education.foundation.errors import (
    EducationalDomainError,
    EducationalInvariantViolation,
)


class AssessmentDomainError(EducationalDomainError):
    """Base error for Assessment Engine domain rule failures."""


class AssessmentInvariantViolation(  # noqa: N818
    EducationalInvariantViolation, AssessmentDomainError
):
    """Raised when an assessment invariant is breached."""

    def __init__(self, message: str, *, invariant: str | None = None) -> None:
        EducationalInvariantViolation.__init__(self, message, invariant=invariant)


class InvalidAssessmentStateTransition(AssessmentDomainError):  # noqa: N818
    """Raised when a session lifecycle transition is unlawful."""

    def __init__(
        self,
        message: str,
        *,
        from_status: str | None = None,
        to_status: str | None = None,
    ) -> None:
        super().__init__(message)
        self.from_status = from_status
        self.to_status = to_status


class DuplicateQuestionReferenceError(AssessmentDomainError):
    """Raised when an instrument or session contains duplicate question ids."""


class InvalidObservationPayloadError(AssessmentDomainError):
    """Raised when an observation payload violates educational evidence rules."""


class MissingLearningObjectiveError(AssessmentDomainError):
    """Raised when a required learning objective reference is absent."""


class InvalidConfidenceRangeError(AssessmentDomainError):
    """Raised when a confidence value falls outside the lawful range."""
