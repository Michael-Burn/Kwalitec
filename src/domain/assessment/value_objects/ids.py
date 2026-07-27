"""Assessment identity value objects.

Architecture Source
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md
    knowledge/product/AP-002/QUESTION_MODEL.md
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class AssessmentId(EducationalValueObject):
    """Identity of an Assessment Engine assessment run / coordination record."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "AssessmentId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SessionId(EducationalValueObject):
    """Identity of an AssessmentSession."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "SessionId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class InstrumentId(EducationalValueObject):
    """Identity of an AssessmentInstrument in the catalogue."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "InstrumentId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ObservationId(EducationalValueObject):
    """Identity of an AssessmentObservation (immutable fact)."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "ObservationId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class QuestionId(EducationalValueObject):
    """Identity of an assessment item / question version reference."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "QuestionId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ResultId(EducationalValueObject):
    """Identity of an AssessmentResult (evidence packaging, not a grade)."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "ResultId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class AttemptNumber(EducationalValueObject):
    """1-based attempt counter for a question within a session."""

    value: int

    def _validate(self) -> None:
        if not isinstance(self.value, int) or isinstance(self.value, bool):
            raise AssessmentInvariantViolation(
                "AttemptNumber must be an integer",
                invariant="AttemptNumber.type",
            )
        if self.value < 1:
            raise AssessmentInvariantViolation(
                "AttemptNumber must be >= 1",
                invariant="AttemptNumber.range",
            )

    def __str__(self) -> str:
        return str(self.value)

    def next(self) -> AttemptNumber:
        return AttemptNumber(self.value + 1)
