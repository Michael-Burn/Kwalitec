"""Concept state — remembered per-concept educational memory.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Concept State
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.value_objects.mastery_state import MasteryState
from domain.education.digital_twin.value_objects.retention_state import RetentionState
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId


@dataclass(frozen=True, slots=True)
class ConceptStateId(EducationalValueObject):
    """Identity of a ConceptState entity within a Twin."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ConceptStateId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class ConceptState(EducationalEntity):
    """Remembered educational state for one concept inside a Twin.

    Stores supplied mastery and retention memory. Does not interpret evidence
    or invent mastery.
    """

    concept_state_id: ConceptStateId
    concept_id: ConceptId
    mastery: MasteryState
    retention: RetentionState
    evidence_count: int = 0

    @property
    def entity_id(self) -> ConceptStateId:
        return self.concept_state_id

    def _validate(self) -> None:
        if not isinstance(self.concept_state_id, ConceptStateId):
            raise EducationalInvariantViolation(
                "concept_state_id must be a ConceptStateId",
                invariant="ConceptState.concept_state_id.type",
            )
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="ConceptState.concept_id.type",
            )
        if not isinstance(self.mastery, MasteryState):
            raise EducationalInvariantViolation(
                "mastery must be a MasteryState",
                invariant="ConceptState.mastery.type",
            )
        if not isinstance(self.retention, RetentionState):
            raise EducationalInvariantViolation(
                "retention must be a RetentionState",
                invariant="ConceptState.retention.type",
            )
        if not isinstance(self.evidence_count, int) or isinstance(
            self.evidence_count, bool
        ):
            raise EducationalInvariantViolation(
                "evidence_count must be an integer",
                invariant="ConceptState.evidence_count.type",
            )
        if self.evidence_count < 0:
            raise EducationalInvariantViolation(
                "evidence_count must be non-negative",
                invariant="ConceptState.evidence_count.non_negative",
            )

    def with_mastery(self, mastery: MasteryState) -> ConceptState:
        return ConceptState(
            concept_state_id=self.concept_state_id,
            concept_id=self.concept_id,
            mastery=mastery,
            retention=self.retention,
            evidence_count=self.evidence_count,
        )

    def with_retention(self, retention: RetentionState) -> ConceptState:
        return ConceptState(
            concept_state_id=self.concept_state_id,
            concept_id=self.concept_id,
            mastery=self.mastery,
            retention=retention,
            evidence_count=self.evidence_count,
        )

    def with_evidence_count(self, evidence_count: int) -> ConceptState:
        return ConceptState(
            concept_state_id=self.concept_state_id,
            concept_id=self.concept_id,
            mastery=self.mastery,
            retention=self.retention,
            evidence_count=evidence_count,
        )
