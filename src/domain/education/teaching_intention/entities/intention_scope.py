"""Intention scope — instructional locus of a teaching intention.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Intention Scope / Instructional Scope
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
from domain.education.foundation.ids import ConceptId, MisconceptionId
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
    MisconceptionReference,
)
from domain.education.teaching_intention.enums import IntentionScopeKind


@dataclass(frozen=True, slots=True)
class IntentionScopeId(EducationalValueObject):
    """Identity of an instructional scope statement."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "IntentionScopeId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class IntentionScope(EducationalEntity):
    """Instructional scope in which the educational change is sought.

    Intention without scope is fog — the tutor must name the locus of the
    intended improvement. Scope does not assemble episodes or select strategy.
    """

    scope_id: IntentionScopeId
    statement: str
    scope_kind: IntentionScopeKind
    learning_dimension: LearningDimension | None = None
    concept_references: tuple[ConceptReference, ...] = ()
    learning_objective_references: tuple[LearningObjectiveReference, ...] = ()
    misconception_references: tuple[MisconceptionReference, ...] = ()

    @property
    def entity_id(self) -> IntentionScopeId:
        return self.scope_id

    def _validate(self) -> None:
        if not isinstance(self.scope_id, IntentionScopeId):
            raise EducationalInvariantViolation(
                "scope_id must be an IntentionScopeId",
                invariant="IntentionScope.scope_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if not isinstance(self.scope_kind, IntentionScopeKind):
            raise EducationalInvariantViolation(
                "scope_kind must be an IntentionScopeKind",
                invariant="IntentionScope.scope_kind.type",
            )
        if self.learning_dimension is not None and not isinstance(
            self.learning_dimension, LearningDimension
        ):
            raise EducationalInvariantViolation(
                "learning_dimension must be a LearningDimension when provided",
                invariant="IntentionScope.learning_dimension.type",
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
            "misconception_references",
            self._validate_misconception_references(self.misconception_references),
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
                    invariant="IntentionScope.concept_references.type",
                )
            if ref.concept_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept reference is not allowed in intention scope",
                    invariant="IntentionScope.concept_references.no_duplicate",
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
                    invariant="IntentionScope.learning_objective_references.type",
                )
            if ref.objective_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning objective reference is not allowed "
                    "in intention scope",
                    invariant=(
                        "IntentionScope.learning_objective_references.no_duplicate"
                    ),
                )
            seen.add(ref.objective_id.value)
        return items

    @staticmethod
    def _validate_misconception_references(
        refs: tuple[MisconceptionReference, ...] | list[MisconceptionReference],
    ) -> tuple[MisconceptionReference, ...]:
        items = tuple(refs)
        seen: set[str] = set()
        for ref in items:
            if not isinstance(ref, MisconceptionReference):
                raise EducationalInvariantViolation(
                    "misconception_references must be MisconceptionReference values",
                    invariant="IntentionScope.misconception_references.type",
                )
            if ref.misconception_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate misconception reference is not allowed "
                    "in intention scope",
                    invariant="IntentionScope.misconception_references.no_duplicate",
                )
            seen.add(ref.misconception_id.value)
        return items

    def concept_ids(self) -> frozenset[ConceptId]:
        return frozenset(ref.concept_id for ref in self.concept_references)

    def misconception_ids(self) -> frozenset[MisconceptionId]:
        return frozenset(ref.misconception_id for ref in self.misconception_references)

    def with_statement(self, statement: str) -> IntentionScope:
        return IntentionScope(
            scope_id=self.scope_id,
            statement=statement,
            scope_kind=self.scope_kind,
            learning_dimension=self.learning_dimension,
            concept_references=self.concept_references,
            learning_objective_references=self.learning_objective_references,
            misconception_references=self.misconception_references,
        )
