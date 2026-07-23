"""Assessment reason — structured explanation metadata for an assessment.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Assessment Explanation Metadata
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.enums import AssessmentReasonCode
from domain.education.mastery_estimation.ids import CompetencyId, SubjectId


@dataclass(frozen=True, slots=True)
class AssessmentReason(EducationalValueObject):
    """Immutable, structured explanation fact attached to an assessment.

    Reasons are structured domain information — a machine-readable code
    plus optional scoping identities and an optional numeric detail — never
    natural language explanation text.
    """

    reason_code: AssessmentReasonCode
    subject_id: SubjectId | None = None
    competency_id: CompetencyId | None = None
    detail: float | None = None

    def _validate(self) -> None:
        if not isinstance(self.reason_code, AssessmentReasonCode):
            raise EducationalInvariantViolation(
                "reason_code must be an AssessmentReasonCode",
                invariant="AssessmentReason.reason_code.type",
            )
        if self.subject_id is not None and not isinstance(
            self.subject_id, SubjectId
        ):
            raise EducationalInvariantViolation(
                "subject_id must be a SubjectId when provided",
                invariant="AssessmentReason.subject_id.type",
            )
        if self.competency_id is not None and not isinstance(
            self.competency_id, CompetencyId
        ):
            raise EducationalInvariantViolation(
                "competency_id must be a CompetencyId when provided",
                invariant="AssessmentReason.competency_id.type",
            )
        if self.detail is not None:
            if isinstance(self.detail, bool) or not isinstance(
                self.detail, int | float
            ):
                raise EducationalInvariantViolation(
                    "detail must be a real number when provided",
                    invariant="AssessmentReason.detail.type",
                )
            object.__setattr__(self, "detail", round(float(self.detail), 4))
