"""Policy governing Concept aggregate educational integrity.

Architecture Source
    CONCEPT_ARCHITECTURE.md / SUBJECT_INVARIANTS.md
Concept
    Concept Validation Policy
"""

from __future__ import annotations

from domain.education.foundation.base import require_non_empty_text
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, LearningObjectiveId
from domain.education.subject_knowledge.entities.application_context import (
    ApplicationContext,
)
from domain.education.subject_knowledge.entities.learning_objective import (
    LearningObjective,
)
from domain.education.subject_knowledge.entities.misconception import Misconception
from domain.education.subject_knowledge.entities.transfer_context import (
    TransferContext,
)
from domain.education.subject_knowledge.value_objects.concept_boundary import (
    ConceptBoundary,
)


class ConceptValidationPolicy:
    """Enforces Concept identity, naming, ownership, and uniqueness invariants."""

    @staticmethod
    def assert_identity(concept_id: ConceptId) -> ConceptId:
        """Require a valid ConceptId identity."""
        if not isinstance(concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept must possess a ConceptId identity",
                invariant="Concept.identity.required",
            )
        return concept_id

    @staticmethod
    def assert_canonical_name(canonical_name: str) -> str:
        """Require a non-empty canonical concept name."""
        return require_non_empty_text(canonical_name, "canonical_name")

    @staticmethod
    def assert_core_meaning(core_meaning: str) -> str:
        """Require non-empty core meaning (Concept Architecture §4.1)."""
        return require_non_empty_text(core_meaning, "core_meaning")

    @staticmethod
    def assert_boundary(boundary: ConceptBoundary) -> ConceptBoundary:
        """Require a ConceptBoundary value object."""
        if not isinstance(boundary, ConceptBoundary):
            raise EducationalInvariantViolation(
                "concept must have a ConceptBoundary",
                invariant="Concept.boundary.required",
            )
        return boundary

    @staticmethod
    def assert_has_learning_objective(
        objectives: tuple[LearningObjective, ...] | list[LearningObjective],
    ) -> None:
        """A teachable concept must contain at least one learning objective."""
        if not objectives:
            raise EducationalInvariantViolation(
                "concept must contain at least one learning objective",
                invariant="Concept.learning_objectives.min_one",
            )

    @staticmethod
    def assert_can_remove_learning_objective(
        objectives: tuple[LearningObjective, ...] | list[LearningObjective],
        objective_id: LearningObjectiveId,
    ) -> LearningObjective:
        """Forbid removing the final learning objective; return the match."""
        ConceptValidationPolicy.assert_has_learning_objective(objectives)
        match = next(
            (obj for obj in objectives if obj.objective_id == objective_id),
            None,
        )
        if match is None:
            raise EducationalInvariantViolation(
                "learning objective is not owned by this concept",
                invariant="Concept.learning_objective.not_found",
            )
        if len(objectives) <= 1:
            raise EducationalInvariantViolation(
                "cannot remove the final learning objective from a concept",
                invariant="Concept.learning_objectives.cannot_remove_final",
            )
        return match

    @staticmethod
    def assert_objective_belongs(
        concept_id: ConceptId,
        objective: LearningObjective,
    ) -> None:
        """Require the objective to declare ownership of this concept."""
        if not objective.belongs_to(concept_id):
            raise EducationalInvariantViolation(
                "learning objective must belong to this concept",
                invariant="Concept.learning_objective.ownership",
            )

    @staticmethod
    def assert_objective_not_duplicate(
        existing: tuple[LearningObjective, ...] | list[LearningObjective],
        candidate: LearningObjective,
    ) -> None:
        """Forbid duplicate learning objective identities."""
        for obj in existing:
            if obj.objective_id == candidate.objective_id:
                raise EducationalInvariantViolation(
                    "duplicate learning objective is not allowed",
                    invariant="Concept.learning_objective.no_duplicate",
                )

    @staticmethod
    def assert_misconception_belongs(
        concept_id: ConceptId,
        misconception: Misconception,
    ) -> None:
        """Require misconception attachment to this concept (K4)."""
        if not misconception.belongs_to(concept_id):
            raise EducationalInvariantViolation(
                "misconception must belong to this concept",
                invariant="Concept.misconception.ownership",
            )

    @staticmethod
    def assert_misconception_not_duplicate(
        existing: tuple[Misconception, ...] | list[Misconception],
        candidate: Misconception,
    ) -> None:
        """Forbid duplicate misconception identities on a concept."""
        for item in existing:
            if item.misconception_id == candidate.misconception_id:
                raise EducationalInvariantViolation(
                    "duplicate misconception is not allowed",
                    invariant="Concept.misconception.no_duplicate",
                )

    @staticmethod
    def assert_application_context_belongs(
        concept_id: ConceptId,
        context: ApplicationContext,
    ) -> None:
        """Require application context ownership."""
        if not context.belongs_to(concept_id):
            raise EducationalInvariantViolation(
                "application context must belong to this concept",
                invariant="Concept.application_context.ownership",
            )

    @staticmethod
    def assert_application_context_not_duplicate(
        existing: tuple[ApplicationContext, ...] | list[ApplicationContext],
        candidate: ApplicationContext,
    ) -> None:
        """Forbid duplicate application context identities."""
        for item in existing:
            if item.context_id == candidate.context_id:
                raise EducationalInvariantViolation(
                    "duplicate application context is not allowed",
                    invariant="Concept.application_context.no_duplicate",
                )

    @staticmethod
    def assert_transfer_context_belongs(
        concept_id: ConceptId,
        context: TransferContext,
    ) -> None:
        """Require transfer context ownership."""
        if not context.belongs_to(concept_id):
            raise EducationalInvariantViolation(
                "transfer context must belong to this concept",
                invariant="Concept.transfer_context.ownership",
            )

    @staticmethod
    def assert_transfer_context_not_duplicate(
        existing: tuple[TransferContext, ...] | list[TransferContext],
        candidate: TransferContext,
    ) -> None:
        """Forbid duplicate transfer context identities."""
        for item in existing:
            if item.context_id == candidate.context_id:
                raise EducationalInvariantViolation(
                    "duplicate transfer context is not allowed",
                    invariant="Concept.transfer_context.no_duplicate",
                )
