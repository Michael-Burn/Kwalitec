"""Evidence context — educational situation of an observation.

Architecture Source
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md (§2 Attribution) /
    EDUCATIONAL_EVIDENCE_MODEL.md
Concept
    Evidence Context
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


@dataclass(frozen=True, slots=True)
class EvidenceContextId(EducationalValueObject):
    """Identity of an educational evidence context."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EvidenceContextId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class EvidenceContext(EducationalEntity):
    """Educational situation in which evidence was observed.

    Anchors observations to syllabus-safe educational meaning without diagnosing
    or recommending. Concept and episode references cite known educational
    identities; they do not load aggregates.
    """

    context_id: EvidenceContextId
    situation: str
    learning_dimension: LearningDimension | None = None
    concept_references: tuple[ConceptReference, ...] = ()
    learning_objective_references: tuple[LearningObjectiveReference, ...] = ()
    learning_episode_ids: tuple[LearningEpisodeId, ...] = ()

    @property
    def entity_id(self) -> EvidenceContextId:
        return self.context_id

    def _validate(self) -> None:
        if not isinstance(self.context_id, EvidenceContextId):
            raise EducationalInvariantViolation(
                "context_id must be an EvidenceContextId",
                invariant="EvidenceContext.context_id.type",
            )
        object.__setattr__(
            self,
            "situation",
            require_non_empty_text(self.situation, "situation"),
        )
        if self.learning_dimension is not None and not isinstance(
            self.learning_dimension, LearningDimension
        ):
            raise EducationalInvariantViolation(
                "learning_dimension must be a LearningDimension when provided",
                invariant="EvidenceContext.learning_dimension.type",
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
                    invariant="EvidenceContext.concept_references.type",
                )
            key = ref.concept_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept reference is not allowed in context",
                    invariant="EvidenceContext.concept_references.no_duplicate",
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
                    invariant="EvidenceContext.learning_objective_references.type",
                )
            key = ref.objective_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning objective reference is not allowed",
                    invariant="EvidenceContext.learning_objective_references.no_duplicate",
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
                    invariant="EvidenceContext.learning_episode_ids.type",
                )
            if episode_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning episode id is not allowed in context",
                    invariant="EvidenceContext.learning_episode_ids.no_duplicate",
                )
            seen.add(episode_id.value)
        return items

    def concept_ids(self) -> frozenset[ConceptId]:
        return frozenset(ref.concept_id for ref in self.concept_references)

    def episode_ids(self) -> frozenset[LearningEpisodeId]:
        return frozenset(self.learning_episode_ids)

    def with_concept_reference(self, reference: ConceptReference) -> EvidenceContext:
        """Return a copy that adds a concept reference (no duplicates)."""
        if not isinstance(reference, ConceptReference):
            raise EducationalInvariantViolation(
                "reference must be a ConceptReference",
                invariant="EvidenceContext.with_concept_reference.type",
            )
        if any(
            ref.concept_id == reference.concept_id for ref in self.concept_references
        ):
            raise EducationalInvariantViolation(
                "concept reference already present in context",
                invariant="EvidenceContext.with_concept_reference.duplicate",
            )
        return EvidenceContext(
            context_id=self.context_id,
            situation=self.situation,
            learning_dimension=self.learning_dimension,
            concept_references=(*self.concept_references, reference),
            learning_objective_references=self.learning_objective_references,
            learning_episode_ids=self.learning_episode_ids,
        )

    def with_learning_episode(self, episode_id: LearningEpisodeId) -> EvidenceContext:
        """Return a copy that adds a learning episode reference."""
        if not isinstance(episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "episode_id must be a LearningEpisodeId",
                invariant="EvidenceContext.with_learning_episode.type",
            )
        if episode_id in self.learning_episode_ids:
            raise EducationalInvariantViolation(
                "learning episode already present in context",
                invariant="EvidenceContext.with_learning_episode.duplicate",
            )
        return EvidenceContext(
            context_id=self.context_id,
            situation=self.situation,
            learning_dimension=self.learning_dimension,
            concept_references=self.concept_references,
            learning_objective_references=self.learning_objective_references,
            learning_episode_ids=(*self.learning_episode_ids, episode_id),
        )
