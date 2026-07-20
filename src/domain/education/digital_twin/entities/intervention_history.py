"""Intervention history — append-only intervention memory entries.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Intervention History
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import (
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId


@dataclass(frozen=True, slots=True)
class InterventionHistoryEntryId(EducationalValueObject):
    """Identity of an InterventionHistoryEntry within a Twin."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "InterventionHistoryEntryId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class InterventionHistoryEntry(EducationalEntity):
    """Immutable intervention memory entry — never rewritten after recording.

    Records that an intervention occurred. Does not approve, choose, or
    orchestrate interventions.
    """

    entry_id: InterventionHistoryEntryId
    intervention_ref: str
    sequence: int
    strategy_type: TeachingStrategyType | None = None
    intention_type: TeachingIntentionType | None = None
    concept_id: ConceptId | None = None
    note: str | None = None

    @property
    def entity_id(self) -> InterventionHistoryEntryId:
        return self.entry_id

    def _validate(self) -> None:
        if not isinstance(self.entry_id, InterventionHistoryEntryId):
            raise EducationalInvariantViolation(
                "entry_id must be an InterventionHistoryEntryId",
                invariant="InterventionHistoryEntry.entry_id.type",
            )
        object.__setattr__(
            self,
            "intervention_ref",
            require_identity_value(self.intervention_ref, "intervention_ref"),
        )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="InterventionHistoryEntry.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="InterventionHistoryEntry.sequence.positive",
            )
        if self.strategy_type is not None and not isinstance(
            self.strategy_type, TeachingStrategyType
        ):
            raise EducationalInvariantViolation(
                "strategy_type must be a TeachingStrategyType when provided",
                invariant="InterventionHistoryEntry.strategy_type.type",
            )
        if self.intention_type is not None and not isinstance(
            self.intention_type, TeachingIntentionType
        ):
            raise EducationalInvariantViolation(
                "intention_type must be a TeachingIntentionType when provided",
                invariant="InterventionHistoryEntry.intention_type.type",
            )
        if self.concept_id is not None and not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId when provided",
                invariant="InterventionHistoryEntry.concept_id.type",
            )
        if self.note is not None:
            object.__setattr__(
                self,
                "note",
                require_non_empty_text(self.note, "note"),
            )
            self._reject_smuggling(self.note)

    @staticmethod
    def _reject_smuggling(note: str) -> None:
        lowered = note.casefold()
        forbidden = (
            "therefore diagnose",
            "diagnosis is",
            "create hypothesis",
            "choose priority",
            "approve this intervention",
            "orchestrate session",
            "select next strategy",
        )
        for fragment in forbidden:
            if fragment in lowered:
                raise EducationalInvariantViolation(
                    "intervention history note must not encode diagnosis, "
                    "hypothesis, priority, approval, or orchestration",
                    invariant="InterventionHistoryEntry.no_smuggling",
                )
