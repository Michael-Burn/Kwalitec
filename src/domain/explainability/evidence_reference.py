"""EvidenceReference — citation of Educational OS state supporting an explanation.

Architecture Source
    EDU-005 Educational Explainability Engine
    EDUCATIONAL_EXPLAINABILITY_STANDARD.md (EIP-003)
Concept
    Evidence Reference
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.explainability.enums import EvidenceSourceKind
from domain.explainability.ids import EvidenceReferenceId


@dataclass(frozen=True, slots=True)
class EvidenceReference(EducationalValueObject):
    """Immutable citation of Educational OS state used in an explanation.

    Evidence references cite lawful educational projections (mission, plan,
    progress, recommendation, twin, diagnosis, priority, strategy). They are
    not Educational Evidence of understanding and must not invent mastery.
    """

    reference_id: EvidenceReferenceId
    source_kind: EvidenceSourceKind
    source_id: str
    statement: str
    sequence: int
    code: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.reference_id, EvidenceReferenceId):
            raise EducationalInvariantViolation(
                "reference_id must be an EvidenceReferenceId",
                invariant="EvidenceReference.reference_id.type",
            )
        if not isinstance(self.source_kind, EvidenceSourceKind):
            raise EducationalInvariantViolation(
                "source_kind must be an EvidenceSourceKind",
                invariant="EvidenceReference.source_kind.type",
            )
        object.__setattr__(
            self,
            "source_id",
            require_non_empty_text(self.source_id, "source_id"),
        )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if len(self.statement) < 12:
            raise EducationalInvariantViolation(
                "evidence reference statement must be educationally substantive",
                invariant="EvidenceReference.statement.substantive",
            )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="EvidenceReference.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="EvidenceReference.sequence.positive",
            )
        if self.code is not None:
            object.__setattr__(
                self,
                "code",
                require_non_empty_text(self.code, "code"),
            )
