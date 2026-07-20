"""Evidence source — provenance of an educational observation.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md (§3 Source Catalogue) /
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md (§3 Provenance)
Concept
    Evidence Source
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence.enums import EvidenceSourceKind
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EvidenceSourceId(EducationalValueObject):
    """Identity of an evidence source."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EvidenceSourceId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class EvidenceSource(EducationalEntity):
    """Provenance of educational evidence.

    Identifies whence an observation came. Does not interpret educational
    meaning beyond source class and a descriptive label.
    """

    source_id: EvidenceSourceId
    kind: EvidenceSourceKind
    label: str
    channel: str | None = None

    @property
    def entity_id(self) -> EvidenceSourceId:
        return self.source_id

    def _validate(self) -> None:
        if not isinstance(self.source_id, EvidenceSourceId):
            raise EducationalInvariantViolation(
                "source_id must be an EvidenceSourceId",
                invariant="EvidenceSource.source_id.type",
            )
        if not isinstance(self.kind, EvidenceSourceKind):
            raise EducationalInvariantViolation(
                "kind must be an EvidenceSourceKind",
                invariant="EvidenceSource.kind.type",
            )
        object.__setattr__(self, "label", require_non_empty_text(self.label, "label"))
        if self.channel is not None:
            object.__setattr__(
                self,
                "channel",
                require_non_empty_text(self.channel, "channel"),
            )

    def is_assessment(self) -> bool:
        return self.kind is EvidenceSourceKind.ASSESSMENT

    def is_reflection_capture(self) -> bool:
        return self.kind is EvidenceSourceKind.REFLECTION_CAPTURE

    def is_student_action(self) -> bool:
        return self.kind is EvidenceSourceKind.STUDENT_ACTION
