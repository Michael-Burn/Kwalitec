"""Interpretation context — educational scope of an Interpretation.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Interpretation Context
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence_interpretation.enums import EducationalScopeKind
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


@dataclass(frozen=True, slots=True)
class InterpretationContextId(EducationalValueObject):
    """Identity of an educational interpretation context."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "InterpretationContextId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class InterpretationContext(EducationalEntity):
    """Educational scope in which patterns were interpreted.

    Anchors interpretation to syllabus-safe educational meaning without
    diagnosing or recommending. Must identify educational scope.
    """

    context_id: InterpretationContextId
    educational_scope: str
    scope_kind: EducationalScopeKind
    learning_dimension: LearningDimension | None = None
    concept_references: tuple[ConceptReference, ...] = ()
    learning_objective_references: tuple[LearningObjectiveReference, ...] = ()
    learning_episode_ids: tuple[LearningEpisodeId, ...] = ()

    @property
    def entity_id(self) -> InterpretationContextId:
        return self.context_id

    def _validate(self) -> None:
        if not isinstance(self.context_id, InterpretationContextId):
            raise EducationalInvariantViolation(
                "context_id must be an InterpretationContextId",
                invariant="InterpretationContext.context_id.type",
            )
        object.__setattr__(
            self,
            "educational_scope",
            require_non_empty_text(self.educational_scope, "educational_scope"),
        )
        if not isinstance(self.scope_kind, EducationalScopeKind):
            raise EducationalInvariantViolation(
                "scope_kind must be an EducationalScopeKind",
                invariant="InterpretationContext.scope_kind.type",
            )
        if self.learning_dimension is not None and not isinstance(
            self.learning_dimension, LearningDimension
        ):
            raise EducationalInvariantViolation(
                "learning_dimension must be a LearningDimension when provided",
                invariant="InterpretationContext.learning_dimension.type",
            )
        object.__setattr__(
            self,
            "concept_references",
            self._validate_concept_refs(self.concept_references),
        )
        object.__setattr__(
            self,
            "learning_objective_references",
            self._validate_objective_refs(self.learning_objective_references),
        )
        object.__setattr__(
            self,
            "learning_episode_ids",
            self._validate_episode_ids(self.learning_episode_ids),
        )

    @staticmethod
    def _validate_concept_refs(
        refs: tuple[ConceptReference, ...] | list[ConceptReference],
    ) -> tuple[ConceptReference, ...]:
        items = tuple(refs)
        seen: set[str] = set()
        for ref in items:
            if not isinstance(ref, ConceptReference):
                raise EducationalInvariantViolation(
                    "concept_references must be ConceptReference values",
                    invariant="InterpretationContext.concept_references.type",
                )
            key = ref.concept_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept reference is not allowed in context",
                    invariant="InterpretationContext.concept_references.no_duplicate",
                )
            seen.add(key)
        return items

    @staticmethod
    def _validate_objective_refs(
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
                    invariant="InterpretationContext.learning_objective_references.type",
                )
            key = ref.objective_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning objective reference is not allowed",
                    invariant=(
                        "InterpretationContext.learning_objective_references."
                        "no_duplicate"
                    ),
                )
            seen.add(key)
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
                    invariant="InterpretationContext.learning_episode_ids.type",
                )
            if episode_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning episode id is not allowed in context",
                    invariant="InterpretationContext.learning_episode_ids.no_duplicate",
                )
            seen.add(episode_id.value)
        return items

    def concept_ids(self) -> frozenset[ConceptId]:
        return frozenset(ref.concept_id for ref in self.concept_references)

    def episode_ids(self) -> frozenset[LearningEpisodeId]:
        return frozenset(self.learning_episode_ids)

    def with_concept_reference(
        self, reference: ConceptReference
    ) -> InterpretationContext:
        """Return a copy that adds a concept reference (no duplicates)."""
        if not isinstance(reference, ConceptReference):
            raise EducationalInvariantViolation(
                "reference must be a ConceptReference",
                invariant="InterpretationContext.with_concept_reference.type",
            )
        if any(
            ref.concept_id == reference.concept_id for ref in self.concept_references
        ):
            raise EducationalInvariantViolation(
                "concept reference already present in context",
                invariant="InterpretationContext.with_concept_reference.duplicate",
            )
        return InterpretationContext(
            context_id=self.context_id,
            educational_scope=self.educational_scope,
            scope_kind=self.scope_kind,
            learning_dimension=self.learning_dimension,
            concept_references=(*self.concept_references, reference),
            learning_objective_references=self.learning_objective_references,
            learning_episode_ids=self.learning_episode_ids,
        )

    def with_learning_episode(
        self, episode_id: LearningEpisodeId
    ) -> InterpretationContext:
        """Return a copy that adds a learning episode reference."""
        if not isinstance(episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "episode_id must be a LearningEpisodeId",
                invariant="InterpretationContext.with_learning_episode.type",
            )
        if episode_id in self.learning_episode_ids:
            raise EducationalInvariantViolation(
                "learning episode already present in context",
                invariant="InterpretationContext.with_learning_episode.duplicate",
            )
        return InterpretationContext(
            context_id=self.context_id,
            educational_scope=self.educational_scope,
            scope_kind=self.scope_kind,
            learning_dimension=self.learning_dimension,
            concept_references=self.concept_references,
            learning_objective_references=self.learning_objective_references,
            learning_episode_ids=(*self.learning_episode_ids, episode_id),
        )
