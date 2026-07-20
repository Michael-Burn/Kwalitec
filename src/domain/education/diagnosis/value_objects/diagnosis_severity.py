"""Diagnosis severity — educational consequence of a named deficiency.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    Diagnosis Severity
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.diagnosis.enums import DiagnosisSeverityLevel
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class DiagnosisSeverity(EducationalValueObject):
    """Immutable qualitative severity of an educational diagnosis.

    Severity names how consequential the deficiency is educationally within
    its scope. It is not a priority decision, numerical score-as-law, or
    teaching strategy selector.
    """

    level: DiagnosisSeverityLevel
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.level, DiagnosisSeverityLevel):
            raise EducationalInvariantViolation(
                "level must be a DiagnosisSeverityLevel",
                invariant="DiagnosisSeverity.level.type",
            )
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "severity rationale must be non-empty when provided",
                    invariant="DiagnosisSeverity.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)

    @classmethod
    def of(
        cls,
        level: DiagnosisSeverityLevel,
        *,
        rationale: str | None = None,
    ) -> DiagnosisSeverity:
        return cls(level=level, rationale=rationale)

    def is_at_least(self, other: DiagnosisSeverityLevel) -> bool:
        order = (
            DiagnosisSeverityLevel.MILD,
            DiagnosisSeverityLevel.MODERATE,
            DiagnosisSeverityLevel.SUBSTANTIAL,
            DiagnosisSeverityLevel.SEVERE,
        )
        if other not in order:
            raise EducationalInvariantViolation(
                "comparison requires a known DiagnosisSeverityLevel",
                invariant="DiagnosisSeverity.is_at_least.level",
            )
        return order.index(self.level) >= order.index(other)

    def __str__(self) -> str:
        if self.rationale is None:
            return self.level.value
        return f"{self.level.value}: {self.rationale}"
