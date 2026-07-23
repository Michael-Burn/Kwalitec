"""Specification: confidence is only ever eroded by observed contradiction.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Assessment Confidence Specification
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.value_objects.mastery_confidence import (
    MasteryConfidence,
)

_TOLERANCE = 1e-6


class AssessmentConfidenceSpecification:
    """Contradictory evidence must reduce confidence, never corrupt it.

    A confidence posture is well-formed when: its magnitude is always
    within ``[0.0, 1.0]`` (already enforced by the value object itself);
    zero evidence always yields zero confidence, never an arbitrary
    positive figure; and a fully contradictory evidence set (a
    ``contradiction_ratio`` of ``1.0``, perfectly balanced conflicting
    evidence) can never receive a *maximal* confidence score — some
    erosion must always be visible.
    """

    @staticmethod
    def is_satisfied_by(confidence: MasteryConfidence) -> bool:
        if confidence.evidence_count == 0:
            return confidence.score.magnitude <= _TOLERANCE
        if confidence.contradiction_ratio >= 1.0 - _TOLERANCE:
            return confidence.score.magnitude < 1.0 - _TOLERANCE
        return True

    @staticmethod
    def assert_satisfied_by(confidence: MasteryConfidence) -> None:
        if not AssessmentConfidenceSpecification.is_satisfied_by(confidence):
            raise EducationalInvariantViolation(
                "confidence must be zero with no evidence, and eroded by "
                "full contradiction — never undefined or maximal despite "
                "conflicting evidence",
                invariant="AssessmentConfidenceSpecification.contradiction_erosion",
            )
