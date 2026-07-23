"""Subject state — supplied study posture for one subject.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Subject State
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state.enums import SubjectStatus
from domain.education.student_state.ids import SubjectId


@dataclass(frozen=True, slots=True)
class SubjectState(EducationalValueObject):
    """Immutable, supplied study posture for a subject.

    SubjectState records what it is given. It does not compute coverage,
    diagnose weakness, or infer status from evidence.
    """

    subject_id: SubjectId
    status: SubjectStatus
    coverage_ratio: float | None = None
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.subject_id, SubjectId):
            raise EducationalInvariantViolation(
                "subject_id must be a SubjectId",
                invariant="SubjectState.subject_id.type",
            )
        if not isinstance(self.status, SubjectStatus):
            raise EducationalInvariantViolation(
                "status must be a SubjectStatus",
                invariant="SubjectState.status.type",
            )
        if self.coverage_ratio is not None:
            if isinstance(self.coverage_ratio, bool) or not isinstance(
                self.coverage_ratio, int | float
            ):
                raise EducationalInvariantViolation(
                    "coverage_ratio must be a real number when provided",
                    invariant="SubjectState.coverage_ratio.type",
                )
            if self.coverage_ratio < 0.0 or self.coverage_ratio > 1.0:
                raise EducationalInvariantViolation(
                    "coverage_ratio must be between 0.0 and 1.0 inclusive",
                    invariant="SubjectState.coverage_ratio.range",
                )
            object.__setattr__(self, "coverage_ratio", float(self.coverage_ratio))
        if self.label is not None:
            object.__setattr__(
                self, "label", require_non_empty_text(self.label, "label")
            )

    def with_status(self, status: SubjectStatus) -> SubjectState:
        return SubjectState(
            subject_id=self.subject_id,
            status=status,
            coverage_ratio=self.coverage_ratio,
            label=self.label,
        )

    def with_coverage_ratio(self, coverage_ratio: float | None) -> SubjectState:
        return SubjectState(
            subject_id=self.subject_id,
            status=self.status,
            coverage_ratio=coverage_ratio,
            label=self.label,
        )

    def __str__(self) -> str:
        return f"{self.subject_id.value}:{self.status.value}"
