"""Competency state — supplied mastery posture for one competency.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Competency State
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state.enums import MasteryBand
from domain.education.student_state.ids import CompetencyId, SubjectId


@dataclass(frozen=True, slots=True)
class CompetencyState(EducationalValueObject):
    """Immutable, supplied mastery posture for a competency.

    CompetencyState records what it is given. It does not estimate mastery
    from evidence, diagnose gaps, or invent educational meaning.
    """

    competency_id: CompetencyId
    subject_id: SubjectId
    band: MasteryBand
    mastery_ratio: float | None = None
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.competency_id, CompetencyId):
            raise EducationalInvariantViolation(
                "competency_id must be a CompetencyId",
                invariant="CompetencyState.competency_id.type",
            )
        if not isinstance(self.subject_id, SubjectId):
            raise EducationalInvariantViolation(
                "subject_id must be a SubjectId",
                invariant="CompetencyState.subject_id.type",
            )
        if not isinstance(self.band, MasteryBand):
            raise EducationalInvariantViolation(
                "band must be a MasteryBand",
                invariant="CompetencyState.band.type",
            )
        if self.mastery_ratio is not None:
            if isinstance(self.mastery_ratio, bool) or not isinstance(
                self.mastery_ratio, int | float
            ):
                raise EducationalInvariantViolation(
                    "mastery_ratio must be a real number when provided",
                    invariant="CompetencyState.mastery_ratio.type",
                )
            if self.mastery_ratio < 0.0 or self.mastery_ratio > 1.0:
                raise EducationalInvariantViolation(
                    "mastery_ratio must be between 0.0 and 1.0 inclusive",
                    invariant="CompetencyState.mastery_ratio.range",
                )
            object.__setattr__(
                self, "mastery_ratio", float(self.mastery_ratio)
            )
        if self.label is not None:
            object.__setattr__(
                self, "label", require_non_empty_text(self.label, "label")
            )

    def with_band(self, band: MasteryBand) -> CompetencyState:
        return CompetencyState(
            competency_id=self.competency_id,
            subject_id=self.subject_id,
            band=band,
            mastery_ratio=self.mastery_ratio,
            label=self.label,
        )

    def with_mastery_ratio(self, mastery_ratio: float | None) -> CompetencyState:
        return CompetencyState(
            competency_id=self.competency_id,
            subject_id=self.subject_id,
            band=self.band,
            mastery_ratio=mastery_ratio,
            label=self.label,
        )

    def __str__(self) -> str:
        return f"{self.competency_id.value}:{self.band.value}"
