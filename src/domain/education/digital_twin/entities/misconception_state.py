"""Misconception state — remembered misconception presence within a Twin.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Misconception State
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.enums import MisconceptionPresence
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, MisconceptionId


@dataclass(frozen=True, slots=True)
class MisconceptionStateId(EducationalValueObject):
    """Identity of a MisconceptionState entity within a Twin."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "MisconceptionStateId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class MisconceptionState(EducationalEntity):
    """Remembered presence of a misconception inside Twin memory.

    Stores supplied presence. Does not diagnose or invent misconceptions.
    """

    misconception_state_id: MisconceptionStateId
    misconception_id: MisconceptionId
    presence: MisconceptionPresence
    related_concept_id: ConceptId | None = None

    @property
    def entity_id(self) -> MisconceptionStateId:
        return self.misconception_state_id

    def _validate(self) -> None:
        if not isinstance(self.misconception_state_id, MisconceptionStateId):
            raise EducationalInvariantViolation(
                "misconception_state_id must be a MisconceptionStateId",
                invariant="MisconceptionState.misconception_state_id.type",
            )
        if not isinstance(self.misconception_id, MisconceptionId):
            raise EducationalInvariantViolation(
                "misconception_id must be a MisconceptionId",
                invariant="MisconceptionState.misconception_id.type",
            )
        if not isinstance(self.presence, MisconceptionPresence):
            raise EducationalInvariantViolation(
                "presence must be a MisconceptionPresence",
                invariant="MisconceptionState.presence.type",
            )
        if self.related_concept_id is not None and not isinstance(
            self.related_concept_id, ConceptId
        ):
            raise EducationalInvariantViolation(
                "related_concept_id must be a ConceptId when provided",
                invariant="MisconceptionState.related_concept_id.type",
            )

    def with_presence(self, presence: MisconceptionPresence) -> MisconceptionState:
        return MisconceptionState(
            misconception_state_id=self.misconception_state_id,
            misconception_id=self.misconception_id,
            presence=presence,
            related_concept_id=self.related_concept_id,
        )
