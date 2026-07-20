"""Hypothesis reason — warrant for an educational explanation.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Hypothesis Reason
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, EvidenceId


@dataclass(frozen=True, slots=True)
class DiagnosisReference(EducationalValueObject):
    """Opaque citation of an upstream EducationalDiagnosis.

    Hypotheses reference diagnoses by identity and type only. They do not
    import or load the Diagnosis package aggregates.
    """

    diagnosis_id: DiagnosisId
    diagnosis_type: DiagnosisType

    def _validate(self) -> None:
        if not isinstance(self.diagnosis_id, DiagnosisId):
            raise EducationalInvariantViolation(
                "diagnosis_id must be a DiagnosisId",
                invariant="DiagnosisReference.diagnosis_id.type",
            )
        if not isinstance(self.diagnosis_type, DiagnosisType):
            raise EducationalInvariantViolation(
                "diagnosis_type must be a DiagnosisType",
                invariant="DiagnosisReference.diagnosis_type.type",
            )

    def __str__(self) -> str:
        return f"{self.diagnosis_id.value}:{self.diagnosis_type.value}"


@dataclass(frozen=True, slots=True)
class InterpretationReference(EducationalValueObject):
    """Opaque citation of an upstream Interpretation aggregate."""

    interpretation_id: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "interpretation_id",
            require_identity_value(self.interpretation_id, "interpretation_id"),
        )

    def __str__(self) -> str:
        return self.interpretation_id


@dataclass(frozen=True, slots=True)
class HypothesisReasonId(EducationalValueObject):
    """Identity of a hypothesis reason within an EducationalHypothesis."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "HypothesisReasonId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class HypothesisReason(EducationalEntity):
    """Single supporting reason for an educational hypothesis.

    Reasons cite *why this explanation fits*. They must not encode teaching
    strategy selection, priority ranking, or intention.
    """

    reason_id: HypothesisReasonId
    statement: str
    code: str | None = None
    evidence_ids: tuple[EvidenceId, ...] = ()

    @property
    def entity_id(self) -> HypothesisReasonId:
        return self.reason_id

    def _validate(self) -> None:
        if not isinstance(self.reason_id, HypothesisReasonId):
            raise EducationalInvariantViolation(
                "reason_id must be a HypothesisReasonId",
                invariant="HypothesisReason.reason_id.type",
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
        object.__setattr__(
            self,
            "evidence_ids",
            self._validate_evidence_ids(self.evidence_ids),
        )
        self._reject_how_to_smuggling(self.statement)

    @staticmethod
    def _validate_evidence_ids(
        evidence_ids: tuple[EvidenceId, ...] | list[EvidenceId],
    ) -> tuple[EvidenceId, ...]:
        items = tuple(evidence_ids)
        seen: set[str] = set()
        for evidence_id in items:
            if not isinstance(evidence_id, EvidenceId):
                raise EducationalInvariantViolation(
                    "evidence_ids must be EvidenceId values",
                    invariant="HypothesisReason.evidence_ids.type",
                )
            if evidence_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate evidence id is not allowed in a reason",
                    invariant="HypothesisReason.evidence_ids.no_duplicate",
                )
            seen.add(evidence_id.value)
        return items

    @staticmethod
    def _reject_how_to_smuggling(statement: str) -> None:
        """Refuse reasons that encode teaching moves inside hypothesis."""
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
            "we should drill",
        )
        for fragment in forbidden_fragments:
            if fragment in lowered:
                raise EducationalInvariantViolation(
                    "hypothesis reason must not encode teaching strategy, "
                    "priority, or recommendation",
                    invariant="HypothesisReason.no_how_to_smuggling",
                )

    def reason_signature(self) -> tuple[str, str | None]:
        """Structural fingerprint used to prevent duplicate reasons."""
        return (self.statement.casefold(), self.code)

    def with_statement(self, statement: str) -> HypothesisReason:
        """Return a copy with an amended reason statement."""
        return HypothesisReason(
            reason_id=self.reason_id,
            statement=statement,
            code=self.code,
            evidence_ids=self.evidence_ids,
        )
