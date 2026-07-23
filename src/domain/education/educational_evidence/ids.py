"""Educational Evidence identity value objects.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Id / Subject Id / Competency Id / Mission Id / Checkpoint Id

Opaque, immutable identifiers scoped to this bounded context. Identities are
not database keys and carry no persistence semantics.

These identities are intentionally distinct from same-named identities
owned by other education bounded contexts (for example
``domain.education.foundation.ids.EvidenceId`` or
``domain.education.student_state.ids.SubjectId``). This context does not
import from — or assume identity equivalence with — those contexts. A
future integration milestone may introduce an explicit mapping.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class EvidenceId(EducationalValueObject):
    """Identity of a single ``EducationalEvidence`` record."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "EvidenceId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SubjectId(EducationalValueObject):
    """Identity of a subject referenced by a piece of evidence."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "SubjectId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CompetencyId(EducationalValueObject):
    """Identity of a competency referenced by a piece of evidence."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "CompetencyId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MissionId(EducationalValueObject):
    """Identity of a mission referenced by a piece of evidence.

    Opaque cross-boundary reference — this context does not own or
    interpret mission content.
    """

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "MissionId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CheckpointId(EducationalValueObject):
    """Identity of a checkpoint referenced by a piece of evidence.

    Opaque cross-boundary reference — this context does not own or
    interpret checkpoint content.
    """

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "CheckpointId")
        )

    def __str__(self) -> str:
        return self.value
