"""Evidence source — provenance of an educational observation.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model, Evidence rules)
Concept
    Evidence Source
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.educational_evidence.enums import EvidenceSourceKind
from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EvidenceSource(EducationalValueObject):
    """Immutable provenance of a piece of educational evidence.

    Identifies *what produced* the observation — a student action, a
    system observation, or a self report — and the originating subsystem,
    without interpreting or scoring the observation.
    """

    kind: EvidenceSourceKind
    origin: str

    def _validate(self) -> None:
        if not isinstance(self.kind, EvidenceSourceKind):
            raise EducationalInvariantViolation(
                "kind must be an EvidenceSourceKind",
                invariant="EvidenceSource.kind.type",
            )
        object.__setattr__(
            self, "origin", require_non_empty_text(self.origin, "origin")
        )

    @classmethod
    def student_action(cls, origin: str) -> EvidenceSource:
        return cls(kind=EvidenceSourceKind.STUDENT_ACTION, origin=origin)

    @classmethod
    def system_observation(cls, origin: str) -> EvidenceSource:
        return cls(kind=EvidenceSourceKind.SYSTEM_OBSERVATION, origin=origin)

    @classmethod
    def self_report(cls, origin: str) -> EvidenceSource:
        return cls(kind=EvidenceSourceKind.SELF_REPORT, origin=origin)

    def is_self_report(self) -> bool:
        return self.kind is EvidenceSourceKind.SELF_REPORT

    def is_student_action(self) -> bool:
        return self.kind is EvidenceSourceKind.STUDENT_ACTION

    def is_system_observation(self) -> bool:
        return self.kind is EvidenceSourceKind.SYSTEM_OBSERVATION

    def __str__(self) -> str:
        return f"{self.kind.value}:{self.origin}"
