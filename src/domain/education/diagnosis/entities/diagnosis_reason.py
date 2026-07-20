"""Diagnosis reason — explanatory warrant for a named deficiency.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    Diagnosis Reason
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class DiagnosisReasonId(EducationalValueObject):
    """Identity of a diagnosis reason within an EducationalDiagnosis."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "DiagnosisReasonId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class DiagnosisReason(EducationalEntity):
    """Single explanatory reason supporting an educational diagnosis.

    Reasons cite *why this deficiency category fits*. They must not encode
    teaching strategy selection, priority ranking, or hypothesis generation.
    """

    reason_id: DiagnosisReasonId
    statement: str
    code: str | None = None

    @property
    def entity_id(self) -> DiagnosisReasonId:
        return self.reason_id

    def _validate(self) -> None:
        if not isinstance(self.reason_id, DiagnosisReasonId):
            raise EducationalInvariantViolation(
                "reason_id must be a DiagnosisReasonId",
                invariant="DiagnosisReason.reason_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if self.code is not None:
            object.__setattr__(
                self,
                "code",
                require_identity_value(self.code, "code"),
            )
        self._reject_how_to_smuggling(self.statement)

    @staticmethod
    def _reject_how_to_smuggling(statement: str) -> None:
        """Refuse reasons that encode teaching moves inside diagnosis."""
        lowered = statement.casefold()
        forbidden_fragments = (
            "therefore teach",
            "therefore use",
            "recommend strategy",
            "select strategy",
            "should practise",
            "should practice",
            "assign episode",
            "priority is",
            "prioritise",
            "prioritize",
        )
        for fragment in forbidden_fragments:
            if fragment in lowered:
                raise EducationalInvariantViolation(
                    "diagnosis reason must not encode teaching strategy, "
                    "priority, or recommendation",
                    invariant="DiagnosisReason.no_how_to_smuggling",
                )

    def reason_signature(self) -> tuple[str, str | None]:
        """Structural fingerprint used to prevent duplicate reasons."""
        return (self.statement.casefold(), self.code)

    def with_statement(self, statement: str) -> DiagnosisReason:
        """Return a copy with an amended reason statement."""
        return DiagnosisReason(
            reason_id=self.reason_id,
            statement=statement,
            code=self.code,
        )
