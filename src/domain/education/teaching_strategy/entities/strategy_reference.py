"""Opaque references to intention, diagnosis, and hypothesis aggregates.

Architecture Source
    TEACHING_STRATEGY_ARCHITECTURE.md
Concept
    Intention Reference / Diagnosis Reference / Hypothesis Reference
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    DiagnosisId,
    HypothesisId,
    TeachingIntentionId,
)


@dataclass(frozen=True, slots=True)
class IntentionReference(EducationalValueObject):
    """Opaque citation of an upstream TeachingIntention.

    Teaching Strategy must reference a Teaching Intention. It does not import
    or load the Intention package aggregate or redefine the educational change.
    """

    intention_id: TeachingIntentionId
    intention_type: TeachingIntentionType

    def _validate(self) -> None:
        if not isinstance(self.intention_id, TeachingIntentionId):
            raise EducationalInvariantViolation(
                "intention_id must be a TeachingIntentionId",
                invariant="IntentionReference.intention_id.type",
            )
        if not isinstance(self.intention_type, TeachingIntentionType):
            raise EducationalInvariantViolation(
                "intention_type must be a TeachingIntentionType",
                invariant="IntentionReference.intention_type.type",
            )

    def __str__(self) -> str:
        return f"{self.intention_id.value}:{self.intention_type.value}"


@dataclass(frozen=True, slots=True)
class DiagnosisReference(EducationalValueObject):
    """Opaque citation of an upstream EducationalDiagnosis.

    Strategy references diagnoses by identity and type only. Selection
    policies use diagnosis_type without loading Diagnosis aggregates.
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
class HypothesisReference(EducationalValueObject):
    """Opaque citation of an upstream EducationalHypothesis.

    Hypothesis informs strategy; it does not select strategy alone (S10).
    """

    hypothesis_id: HypothesisId

    def _validate(self) -> None:
        if not isinstance(self.hypothesis_id, HypothesisId):
            raise EducationalInvariantViolation(
                "hypothesis_id must be a HypothesisId",
                invariant="HypothesisReference.hypothesis_id.type",
            )

    def __str__(self) -> str:
        return self.hypothesis_id.value


@dataclass(frozen=True, slots=True)
class SecondaryStrategyReference(EducationalValueObject):
    """Ordered secondary strategy in a composition arc.

    Secondaries are subordinate supportive stages across episodes — never
    co-equal primary strategies within one episode (Composition Model C1).
    """

    strategy_type: TeachingStrategyType
    sequence_order: int

    def _validate(self) -> None:
        if not isinstance(self.strategy_type, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "strategy_type must be a TeachingStrategyType",
                invariant="SecondaryStrategyReference.strategy_type.type",
            )
        if not isinstance(self.sequence_order, int) or self.sequence_order < 1:
            raise EducationalInvariantViolation(
                "sequence_order must be a positive integer",
                invariant="SecondaryStrategyReference.sequence_order.positive",
            )

    def __str__(self) -> str:
        return f"{self.sequence_order}:{self.strategy_type.value}"
