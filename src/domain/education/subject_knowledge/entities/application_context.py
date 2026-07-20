"""Application context — legitimate use situation for knowledge.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md / APPLICATION_AND_TRANSFER_MODEL.md
Concept
    Application Context
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId


@dataclass(frozen=True, slots=True)
class ApplicationContextId(EducationalValueObject):
    """Identity of an application context."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ApplicationContextId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class ApplicationContext(EducationalEntity):
    """Situation type in which a concept is legitimately used (K14).

    Characterised by task demand, assumptions, and constraints — not decorative
    narrative without structural demand.
    """

    context_id: ApplicationContextId
    concept_id: ConceptId
    description: str
    task_demand: str
    assumptions: str | None = None
    constraints: str | None = None

    @property
    def entity_id(self) -> ApplicationContextId:
        return self.context_id

    def _validate(self) -> None:
        if not isinstance(self.context_id, ApplicationContextId):
            raise EducationalInvariantViolation(
                "context_id must be an ApplicationContextId",
                invariant="ApplicationContext.context_id.type",
            )
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="ApplicationContext.concept_id.type",
            )
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "task_demand",
            require_non_empty_text(self.task_demand, "task_demand"),
        )
        if self.assumptions is not None:
            object.__setattr__(
                self,
                "assumptions",
                require_non_empty_text(self.assumptions, "assumptions"),
            )
        if self.constraints is not None:
            object.__setattr__(
                self,
                "constraints",
                require_non_empty_text(self.constraints, "constraints"),
            )

    def belongs_to(self, concept_id: ConceptId) -> bool:
        """Return True when this context belongs to ``concept_id``."""
        return self.concept_id == concept_id
