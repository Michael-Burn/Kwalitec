"""Hypothesis scope — educational locus of an explanation.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Hypothesis Scope
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
from domain.education.hypothesis.enums import HypothesisScopeKind


@dataclass(frozen=True, slots=True)
class HypothesisScopeId(EducationalValueObject):
    """Identity of an educational hypothesis scope statement."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "HypothesisScopeId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class HypothesisScope(EducationalEntity):
    """Educational scope in which a hypothesis explanation applies.

    Anchors explanatory belief to curriculum-grounded aims. A hypothesis
    without scope is fog — explanation must be relative to identifiable
    educational locus.
    """

    scope_id: HypothesisScopeId
    statement: str
    scope_kind: HypothesisScopeKind
    learning_dimension: LearningDimension | None = None
    concept_references: tuple[ConceptReference, ...] = ()
    learning_objective_references: tuple[LearningObjectiveReference, ...] = ()
    learning_episode_ids: tuple[LearningEpisodeId, ...] = ()

    @property
    def entity_id(self) -> HypothesisScopeId:
        return self.scope_id

    def _validate(self) -> None:
        if not isinstance(self.scope_id, HypothesisScopeId):
            raise EducationalInvariantViolation(
                "scope_id must be a HypothesisScopeId",
                invariant="HypothesisScope.scope_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if not isinstance(self.scope_kind, HypothesisScopeKind):
            raise EducationalInvariantViolation(
                "scope_kind must be a HypothesisScopeKind",
                invariant="HypothesisScope.scope_kind.type",
            )
        if self.learning_dimension is not None and not isinstance(
            self.learning_dimension, LearningDimension
        ):
            raise EducationalInvariantViolation(
                "learning_dimension must be a LearningDimension when provided",
                invariant="HypothesisScope.learning_dimension.type",
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
        self._assert_scope_anchors()

    def _assert_scope_anchors(self) -> None:
        """Scope must identify at least one educational anchor."""
        if (
            self.concept_references
            or self.learning_objective_references
            or self.learning_episode_ids
            or self.learning_dimension is not None
        ):
            return
        raise EducationalInvariantViolation(
            "hypothesis scope must identify at least one educational anchor "
            "(concept, objective, episode, or learning dimension)",
            invariant="HypothesisScope.anchor.required",
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
                    invariant="HypothesisScope.concept_references.type",
                )
            if ref.concept_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept reference is not allowed in scope",
                    invariant="HypothesisScope.concept_references.no_duplicate",
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
                    invariant="HypothesisScope.learning_objective_references.type",
                )
            if ref.objective_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate objective reference is not allowed in scope",
                    invariant=(
                        "HypothesisScope.learning_objective_references.no_duplicate"
                    ),
                )
            seen.add(ref.objective_id.value)
        return items

    @staticmethod
    def _validate_episode_ids(
        ids: tuple[LearningEpisodeId, ...] | list[LearningEpisodeId],
    ) -> tuple[LearningEpisodeId, ...]:
        items = tuple(ids)
        seen: set[str] = set()
        for episode_id in items:
            if not isinstance(episode_id, LearningEpisodeId):
                raise EducationalInvariantViolation(
                    "learning_episode_ids must be LearningEpisodeId values",
                    invariant="HypothesisScope.learning_episode_ids.type",
                )
            if episode_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate episode id is not allowed in scope",
                    invariant="HypothesisScope.learning_episode_ids.no_duplicate",
                )
            seen.add(episode_id.value)
        return items

    def concept_ids(self) -> frozenset[ConceptId]:
        return frozenset(ref.concept_id for ref in self.concept_references)

    def episode_ids(self) -> frozenset[LearningEpisodeId]:
        return frozenset(self.learning_episode_ids)

    def with_statement(self, statement: str) -> HypothesisScope:
        """Return a copy with an amended scope statement."""
        return HypothesisScope(
            scope_id=self.scope_id,
            statement=statement,
            scope_kind=self.scope_kind,
            learning_dimension=self.learning_dimension,
            concept_references=self.concept_references,
            learning_objective_references=self.learning_objective_references,
            learning_episode_ids=self.learning_episode_ids,
        )
