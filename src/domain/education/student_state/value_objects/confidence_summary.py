"""Confidence summary — supplied aggregate confidence posture.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Confidence Summary
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state.ids import SubjectId


@dataclass(frozen=True, slots=True)
class ConfidenceSummary(EducationalValueObject):
    """Immutable, supplied summary of confidence across a student's state.

    ConfidenceSummary stores a supplied confidence posture. It does not
    calibrate psychologically, diagnose false confidence, or infer
    confidence from behaviour.
    """

    overall: ConfidenceLevel
    overall_ratio: float | None = None
    subjects_considered: int = 0
    lowest_confidence_subject_id: SubjectId | None = None

    def _validate(self) -> None:
        if not isinstance(self.overall, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "overall must be a ConfidenceLevel",
                invariant="ConfidenceSummary.overall.type",
            )
        if self.overall_ratio is not None:
            if isinstance(self.overall_ratio, bool) or not isinstance(
                self.overall_ratio, int | float
            ):
                raise EducationalInvariantViolation(
                    "overall_ratio must be a real number when provided",
                    invariant="ConfidenceSummary.overall_ratio.type",
                )
            if self.overall_ratio < 0.0 or self.overall_ratio > 1.0:
                raise EducationalInvariantViolation(
                    "overall_ratio must be between 0.0 and 1.0 inclusive",
                    invariant="ConfidenceSummary.overall_ratio.range",
                )
            object.__setattr__(
                self, "overall_ratio", float(self.overall_ratio)
            )
        if isinstance(self.subjects_considered, bool) or not isinstance(
            self.subjects_considered, int
        ):
            raise EducationalInvariantViolation(
                "subjects_considered must be an integer",
                invariant="ConfidenceSummary.subjects_considered.type",
            )
        if self.subjects_considered < 0:
            raise EducationalInvariantViolation(
                "subjects_considered must be non-negative",
                invariant="ConfidenceSummary.subjects_considered.non_negative",
            )
        if self.lowest_confidence_subject_id is not None and not isinstance(
            self.lowest_confidence_subject_id, SubjectId
        ):
            raise EducationalInvariantViolation(
                "lowest_confidence_subject_id must be a SubjectId when provided",
                invariant="ConfidenceSummary.lowest_confidence_subject_id.type",
            )

    @classmethod
    def unknown(cls) -> ConfidenceSummary:
        return cls(overall=ConfidenceLevel.UNKNOWN)
