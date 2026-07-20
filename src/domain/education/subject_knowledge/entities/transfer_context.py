"""Transfer context — controlled surface variation of application demand.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md / APPLICATION_AND_TRANSFER_MODEL.md
Concept
    Transfer Context
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import TransferLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId
from domain.education.subject_knowledge.entities.application_context import (
    ApplicationContextId,
)


@dataclass(frozen=True, slots=True)
class TransferContextId(EducationalValueObject):
    """Identity of a transfer context."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "TransferContextId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class TransferContext(EducationalEntity):
    """Application situation with surface variation preserving underlying demand.

    Transfer contexts probe structure, not tricks (Subject Invariant K15).
    ``TransferLevel.NONE`` is forbidden — that denotes clone competence.
    """

    context_id: TransferContextId
    concept_id: ConceptId
    description: str
    surface_variation: str
    underlying_demand: str
    transfer_level: TransferLevel
    base_application_context_id: ApplicationContextId | None = None

    @property
    def entity_id(self) -> TransferContextId:
        return self.context_id

    def _validate(self) -> None:
        if not isinstance(self.context_id, TransferContextId):
            raise EducationalInvariantViolation(
                "context_id must be a TransferContextId",
                invariant="TransferContext.context_id.type",
            )
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="TransferContext.concept_id.type",
            )
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "surface_variation",
            require_non_empty_text(self.surface_variation, "surface_variation"),
        )
        object.__setattr__(
            self,
            "underlying_demand",
            require_non_empty_text(self.underlying_demand, "underlying_demand"),
        )
        if not isinstance(self.transfer_level, TransferLevel):
            raise EducationalInvariantViolation(
                "transfer_level must be a TransferLevel",
                invariant="TransferContext.transfer_level.type",
            )
        if self.transfer_level is TransferLevel.NONE:
            raise EducationalInvariantViolation(
                "transfer contexts require NEAR or FAR transfer_level "
                "(NONE denotes clone competence, not transfer)",
                invariant="TransferContext.transfer_level.not_none",
            )
        if self.base_application_context_id is not None and not isinstance(
            self.base_application_context_id, ApplicationContextId
        ):
            raise EducationalInvariantViolation(
                "base_application_context_id must be an ApplicationContextId",
                invariant="TransferContext.base_application_context_id.type",
            )

    def belongs_to(self, concept_id: ConceptId) -> bool:
        """Return True when this context belongs to ``concept_id``."""
        return self.concept_id == concept_id
