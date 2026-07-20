"""Evidence item — one educational observation within an EvidenceRecord.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md
Concept
    Evidence Item
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence.enums import EvidenceItemKind
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, LearningEpisodeId


@dataclass(frozen=True, slots=True)
class EvidenceItemId(EducationalValueObject):
    """Identity of an evidence item within an EvidenceRecord."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EvidenceItemId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class EvidenceItem(EducationalEntity):
    """Single educational observation item.

    Records what was observed (question response, reflection, retrieval, …).
    Never stores diagnoses, recommendations, or priority rankings.
    """

    item_id: EvidenceItemId
    kind: EvidenceItemKind
    observation: str
    concept_id: ConceptId | None = None
    learning_episode_id: LearningEpisodeId | None = None

    @property
    def entity_id(self) -> EvidenceItemId:
        return self.item_id

    def _validate(self) -> None:
        if not isinstance(self.item_id, EvidenceItemId):
            raise EducationalInvariantViolation(
                "item_id must be an EvidenceItemId",
                invariant="EvidenceItem.item_id.type",
            )
        if not isinstance(self.kind, EvidenceItemKind):
            raise EducationalInvariantViolation(
                "kind must be an EvidenceItemKind",
                invariant="EvidenceItem.kind.type",
            )
        object.__setattr__(
            self,
            "observation",
            require_non_empty_text(self.observation, "observation"),
        )
        if self.concept_id is not None and not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId when provided",
                invariant="EvidenceItem.concept_id.type",
            )
        if self.learning_episode_id is not None and not isinstance(
            self.learning_episode_id, LearningEpisodeId
        ):
            raise EducationalInvariantViolation(
                "learning_episode_id must be a LearningEpisodeId when provided",
                invariant="EvidenceItem.learning_episode_id.type",
            )

    def observational_signature(self) -> tuple[str, str, str | None, str | None]:
        """Structural fingerprint used to prevent identical duplicate evidence."""
        return (
            self.kind.value,
            self.observation.casefold(),
            None if self.concept_id is None else self.concept_id.value,
            None
            if self.learning_episode_id is None
            else self.learning_episode_id.value,
        )

    def with_observation(self, observation: str) -> EvidenceItem:
        """Return a copy with amended observational text."""
        return EvidenceItem(
            item_id=self.item_id,
            kind=self.kind,
            observation=observation,
            concept_id=self.concept_id,
            learning_episode_id=self.learning_episode_id,
        )
