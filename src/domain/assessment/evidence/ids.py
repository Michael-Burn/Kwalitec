"""Identity value objects for assessment evidence packaging.

Architecture Source
    knowledge/product/AP-002/EVIDENCE_MODEL.md
    knowledge/product/AP-002/SCORING_MODEL.md
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class EvidenceBundleId(EducationalValueObject):
    """Identity of an immutable EvidenceBundle."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "EvidenceBundleId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class EvidenceItemId(EducationalValueObject):
    """Identity of a single EvidenceItem within a bundle."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "EvidenceItemId")
        )

    def __str__(self) -> str:
        return self.value
