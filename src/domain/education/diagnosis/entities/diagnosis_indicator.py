"""Diagnosis indicator — supporting signal for an educational diagnosis.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    Diagnosis Indicator
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.diagnosis.enums import IndicatorKind
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId


@dataclass(frozen=True, slots=True)
class InterpretationReference(EducationalValueObject):
    """Opaque citation of an upstream Interpretation aggregate.

    Diagnosis references interpretations by identity only. It does not import
    or load the Evidence Interpretation package.
    """

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
class DiagnosisIndicatorId(EducationalValueObject):
    """Identity of a diagnosis indicator within an EducationalDiagnosis."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "DiagnosisIndicatorId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class DiagnosisIndicator(EducationalEntity):
    """Supporting educational signal that warrants a diagnosis.

    Each indicator must cite at least one Interpretation and at least one
    Evidence observation. Indicators describe warrant — never priority or
    teaching strategy.
    """

    indicator_id: DiagnosisIndicatorId
    kind: IndicatorKind
    description: str
    interpretation_references: tuple[InterpretationReference, ...]
    evidence_ids: tuple[EvidenceId, ...]

    @property
    def entity_id(self) -> DiagnosisIndicatorId:
        return self.indicator_id

    def _validate(self) -> None:
        if not isinstance(self.indicator_id, DiagnosisIndicatorId):
            raise EducationalInvariantViolation(
                "indicator_id must be a DiagnosisIndicatorId",
                invariant="DiagnosisIndicator.indicator_id.type",
            )
        if not isinstance(self.kind, IndicatorKind):
            raise EducationalInvariantViolation(
                "kind must be an IndicatorKind",
                invariant="DiagnosisIndicator.kind.type",
            )
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "interpretation_references",
            self._validate_interpretation_references(self.interpretation_references),
        )
        object.__setattr__(
            self,
            "evidence_ids",
            self._validate_evidence_ids(self.evidence_ids),
        )

    @staticmethod
    def _validate_interpretation_references(
        refs: tuple[InterpretationReference, ...] | list[InterpretationReference],
    ) -> tuple[InterpretationReference, ...]:
        items = tuple(refs)
        if not items:
            raise EducationalInvariantViolation(
                "diagnosis indicator must reference at least one Interpretation",
                invariant="DiagnosisIndicator.interpretation_references.min_one",
            )
        seen: set[str] = set()
        for ref in items:
            if not isinstance(ref, InterpretationReference):
                raise EducationalInvariantViolation(
                    "interpretation_references must be InterpretationReference "
                    "values",
                    invariant="DiagnosisIndicator.interpretation_references.type",
                )
            if ref.interpretation_id in seen:
                raise EducationalInvariantViolation(
                    "duplicate interpretation reference is not allowed "
                    "in an indicator",
                    invariant=(
                        "DiagnosisIndicator.interpretation_references.no_duplicate"
                    ),
                )
            seen.add(ref.interpretation_id)
        return items

    @staticmethod
    def _validate_evidence_ids(
        evidence_ids: tuple[EvidenceId, ...] | list[EvidenceId],
    ) -> tuple[EvidenceId, ...]:
        items = tuple(evidence_ids)
        if not items:
            raise EducationalInvariantViolation(
                "diagnosis indicator must reference supporting Evidence",
                invariant="DiagnosisIndicator.evidence_ids.min_one",
            )
        seen: set[str] = set()
        for evidence_id in items:
            if not isinstance(evidence_id, EvidenceId):
                raise EducationalInvariantViolation(
                    "evidence_ids must be EvidenceId values",
                    invariant="DiagnosisIndicator.evidence_ids.type",
                )
            if evidence_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate evidence id is not allowed in an indicator",
                    invariant="DiagnosisIndicator.evidence_ids.no_duplicate",
                )
            seen.add(evidence_id.value)
        return items

    def support_signature(self) -> tuple[str, frozenset[str], frozenset[str]]:
        """Structural fingerprint used to reject duplicate support."""
        return (
            self.kind.value,
            frozenset(ref.interpretation_id for ref in self.interpretation_references),
            frozenset(eid.value for eid in self.evidence_ids),
        )

    def with_description(self, description: str) -> DiagnosisIndicator:
        """Return a copy with an amended indicator description."""
        return DiagnosisIndicator(
            indicator_id=self.indicator_id,
            kind=self.kind,
            description=description,
            interpretation_references=self.interpretation_references,
            evidence_ids=self.evidence_ids,
        )
