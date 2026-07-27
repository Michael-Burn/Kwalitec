"""Evidence dimension packaging for assessment observations.

Architecture Source
    knowledge/product/AP-002/SCORING_MODEL.md
    knowledge/product/AP-002/EVIDENCE_MODEL.md
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.assessment.enums import AttemptOutcome
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.levels import ConfidenceLevel, EvidenceStrength
from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)


@dataclass(frozen=True, slots=True)
class EvidenceDimensions(EducationalValueObject):
    """Structured evidence dimensions extracted from a response.

    These are observational facts / packaging — not Twin mastery writes.
    """

    correctness: AttemptOutcome | None = None
    confidence: ConfidenceLevel | None = None
    response_time_ms: int | None = None
    hints_used: int = 0
    retries: int = 0
    misconception_tags: tuple[str, ...] = ()
    evidence_strength: EvidenceStrength | None = None

    def _validate(self) -> None:
        if self.correctness is not None and not isinstance(
            self.correctness, AttemptOutcome
        ):
            raise AssessmentInvariantViolation(
                "correctness must be an AttemptOutcome when provided",
                invariant="EvidenceDimensions.correctness.type",
            )
        if self.confidence is not None and not isinstance(
            self.confidence, ConfidenceLevel
        ):
            raise AssessmentInvariantViolation(
                "confidence must be a ConfidenceLevel when provided",
                invariant="EvidenceDimensions.confidence.type",
            )
        if self.response_time_ms is not None and (
            not isinstance(self.response_time_ms, int)
            or isinstance(self.response_time_ms, bool)
            or self.response_time_ms < 0
        ):
            raise AssessmentInvariantViolation(
                "response_time_ms must be a non-negative integer",
                invariant="EvidenceDimensions.response_time_ms.range",
            )
        if (
            not isinstance(self.hints_used, int)
            or isinstance(self.hints_used, bool)
            or self.hints_used < 0
        ):
            raise AssessmentInvariantViolation(
                "hints_used must be a non-negative integer",
                invariant="EvidenceDimensions.hints_used.range",
            )
        if (
            not isinstance(self.retries, int)
            or isinstance(self.retries, bool)
            or self.retries < 0
        ):
            raise AssessmentInvariantViolation(
                "retries must be a non-negative integer",
                invariant="EvidenceDimensions.retries.range",
            )
        cleaned: list[str] = []
        for tag in self.misconception_tags or ():
            cleaned.append(require_non_empty_text(str(tag), "misconception_tag"))
        object.__setattr__(self, "misconception_tags", tuple(cleaned))
        if self.evidence_strength is not None and not isinstance(
            self.evidence_strength, EvidenceStrength
        ):
            raise AssessmentInvariantViolation(
                "evidence_strength must be an EvidenceStrength when provided",
                invariant="EvidenceDimensions.evidence_strength.type",
            )
