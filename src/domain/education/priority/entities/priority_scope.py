"""Priority scope — educational locus of an instructional-ordering decision.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Priority Scope
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, LearningEpisodeId
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.priority.enums import PriorityScopeKind


@dataclass(frozen=True, slots=True)
class PriorityScopeId(EducationalValueObject):
    """Identity of an educational priority scope statement."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "PriorityScopeId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class PriorityScope(EducationalEntity):
    """Educational scope in which competing diagnoses are ordered.

    Anchors priority to curriculum-grounded aims. Priority without scope is
    fog — instructional ordering must be relative to identifiable locus.
    """

    scope_id: PriorityScopeId
    statement: str
    scope_kind: PriorityScopeKind
    learning_dimension: LearningDimension | None = None
    concept_references: tuple[ConceptReference, ...] = ()
    learning_objective_references: tuple[LearningObjectiveReference, ...] = ()
    learning_episode_ids: tuple[LearningEpisodeId, ...] = ()

    @property
    def entity_id(self) -> PriorityScopeId:
        return self.scope_id

    def _validate(self) -> None:
        if not isinstance(self.scope_id, PriorityScopeId):
            raise EducationalInvariantViolation(
                "scope_id must be a PriorityScopeId",
                invariant="PriorityScope.scope_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if not isinstance(self.scope_kind, PriorityScopeKind):
            raise EducationalInvariantViolation(
                "scope_kind must be a PriorityScopeKind",
                invariant="PriorityScope.scope_kind.type",
            )
        if self.learning_dimension is not None and not isinstance(
            self.learning_dimension, LearningDimension
        ):
            raise EducationalInvariantViolation(
                "learning_dimension must be a LearningDimension when provided",
                invariant="PriorityScope.learning_dimension.type",
            )
        object.__setattr__(
            self,
            "concept_references",
            self._validate_concept_references(self.concept_references),
        )
        object.__setattr__(
            self,
            "learning_objective_references",
            self._validate_objective_references(self.learning_objective_references),
        )
        object.__setattr__(
            self,
            "learning_episode_ids",
            self._validate_episode_ids(self.learning_episode_ids),
        )

    @staticmethod
    def _validate_concept_references(
        refs: tuple[ConceptReference, ...] | list[ConceptReference],
    ) -> tuple[ConceptReference, ...]:
        items = tuple(refs)
        seen: set[str] = set()
        for ref in items:
            if not isinstance(ref, ConceptReference):
                raise EducationalInvariantViolation(
                    "concept_references must be ConceptReference values",
                    invariant="PriorityScope.concept_references.type",
                )
            if ref.concept_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept reference is not allowed in priority scope",
                    invariant="PriorityScope.concept_references.no_duplicate",
                )
            seen.add(ref.concept_id.value)
        return items

    @staticmethod
    def _validate_objective_references(
        refs: tuple[LearningObjectiveReference, ...]
        | list[LearningObjectiveReference],
    ) -> tuple[LearningObjectiveReference, ...]:
        items = tuple(refs)
        seen: set[str] = set()
        for ref in items:
            if not isinstance(ref, LearningObjectiveReference):
                raise EducationalInvariantViolation(
                    "learning_objective_references must be "
                    "LearningObjectiveReference values",
                    invariant="PriorityScope.learning_objective_references.type",
                )
            if ref.objective_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning objective reference is not allowed "
                    "in priority scope",
                    invariant=(
                        "PriorityScope.learning_objective_references.no_duplicate"
                    ),
                )
            seen.add(ref.objective_id.value)
        return items

    @staticmethod
    def _validate_episode_ids(
        episode_ids: tuple[LearningEpisodeId, ...] | list[LearningEpisodeId],
    ) -> tuple[LearningEpisodeId, ...]:
        items = tuple(episode_ids)
        seen: set[str] = set()
        for episode_id in items:
            if not isinstance(episode_id, LearningEpisodeId):
                raise EducationalInvariantViolation(
                    "learning_episode_ids must be LearningEpisodeId values",
                    invariant="PriorityScope.learning_episode_ids.type",
                )
            if episode_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning episode id is not allowed "
                    "in priority scope",
                    invariant="PriorityScope.learning_episode_ids.no_duplicate",
                )
            seen.add(episode_id.value)
        return items

    def concept_ids(self) -> frozenset[ConceptId]:
        return frozenset(ref.concept_id for ref in self.concept_references)

    def episode_ids(self) -> frozenset[LearningEpisodeId]:
        return frozenset(self.learning_episode_ids)

    def with_statement(self, statement: str) -> PriorityScope:
        """Return a copy with an amended scope statement."""
        return PriorityScope(
            scope_id=self.scope_id,
            statement=statement,
            scope_kind=self.scope_kind,
            learning_dimension=self.learning_dimension,
            concept_references=self.concept_references,
            learning_objective_references=self.learning_objective_references,
            learning_episode_ids=self.learning_episode_ids,
        )
