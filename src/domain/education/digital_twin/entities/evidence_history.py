"""Evidence history — append-only educational evidence memory entries.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_EVIDENCE_MODEL.md
Concept
    Evidence History
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.enums import EvidenceType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId


@dataclass(frozen=True, slots=True)
class EvidenceHistoryEntryId(EducationalValueObject):
    """Identity of an EvidenceHistoryEntry within a Twin."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EvidenceHistoryEntryId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class EvidenceHistoryEntry(EducationalEntity):
    """Immutable evidence memory entry — never rewritten after recording.

    Records that evidence was remembered by the Twin. Does not interpret
    evidence or update mastery by itself.
    """

    entry_id: EvidenceHistoryEntryId
    evidence_id: EvidenceId
    evidence_type: EvidenceType
    sequence: int
    concept_id: ConceptId | None = None
    note: str | None = None

    @property
    def entity_id(self) -> EvidenceHistoryEntryId:
        return self.entry_id

    def _validate(self) -> None:
        if not isinstance(self.entry_id, EvidenceHistoryEntryId):
            raise EducationalInvariantViolation(
                "entry_id must be an EvidenceHistoryEntryId",
                invariant="EvidenceHistoryEntry.entry_id.type",
            )
        if not isinstance(self.evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence_id must be an EvidenceId",
                invariant="EvidenceHistoryEntry.evidence_id.type",
            )
        if not isinstance(self.evidence_type, EvidenceType):
            raise EducationalInvariantViolation(
                "evidence_type must be an EvidenceType",
                invariant="EvidenceHistoryEntry.evidence_type.type",
            )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="EvidenceHistoryEntry.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="EvidenceHistoryEntry.sequence.positive",
            )
        if self.concept_id is not None and not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId when provided",
                invariant="EvidenceHistoryEntry.concept_id.type",
            )
        if self.note is not None:
            cleaned = self.note.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "note must be non-empty when provided",
                    invariant="EvidenceHistoryEntry.note.non_empty",
                )
            object.__setattr__(self, "note", cleaned)
            self._reject_smuggling(cleaned)

    @staticmethod
    def _reject_smuggling(note: str) -> None:
        lowered = note.casefold()
        forbidden = (
            "therefore diagnose",
            "diagnosis is",
            "create hypothesis",
            "choose priority",
            "select strategy",
            "approve intervention",
            "orchestrate session",
        )
        for fragment in forbidden:
            if fragment in lowered:
                raise EducationalInvariantViolation(
                    "evidence history note must not encode diagnosis, "
                    "hypothesis, priority, strategy, approval, or orchestration",
                    invariant="EvidenceHistoryEntry.no_smuggling",
                )
