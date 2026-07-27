"""Curriculum and question reference value objects.

Architecture Source
    knowledge/product/AP-002/QUESTION_MODEL.md
    knowledge/product/AP-002/EDUCATIONAL_MODEL.md
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.assessment.enums import ItemType, KnowledgeLevel
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.ids import QuestionId
from domain.assessment.value_objects.levels import DifficultyLevel
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.ids import ConceptId, LearningObjectiveId


@dataclass(frozen=True, slots=True)
class LearningObjectiveReference(EducationalValueObject):
    """Citation of a curriculum-grounded learning objective for assessment."""

    objective_id: LearningObjectiveId
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.objective_id, LearningObjectiveId):
            raise AssessmentInvariantViolation(
                "objective_id must be a LearningObjectiveId",
                invariant="LearningObjectiveReference.objective_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self, "label", require_non_empty_text(self.label, "label")
            )


@dataclass(frozen=True, slots=True)
class ConceptReference(EducationalValueObject):
    """Citation of a teachable concept under assessment."""

    concept_id: ConceptId
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.concept_id, ConceptId):
            raise AssessmentInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="ConceptReference.concept_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self, "label", require_non_empty_text(self.label, "label")
            )


@dataclass(frozen=True, slots=True)
class QuestionReference(EducationalValueObject):
    """Lightweight reference to a published assessment item version."""

    question_id: QuestionId
    item_type: ItemType
    version: str
    learning_objective: LearningObjectiveReference
    curriculum_entity_id: str | None = None
    knowledge_level: KnowledgeLevel | None = None
    difficulty: DifficultyLevel | None = None
    estimated_time_seconds: int | None = None

    def _validate(self) -> None:
        if not isinstance(self.question_id, QuestionId):
            raise AssessmentInvariantViolation(
                "question_id must be a QuestionId",
                invariant="QuestionReference.question_id.type",
            )
        if not isinstance(self.item_type, ItemType):
            raise AssessmentInvariantViolation(
                "item_type must be an ItemType",
                invariant="QuestionReference.item_type.type",
            )
        object.__setattr__(
            self, "version", require_identity_value(self.version, "version")
        )
        if not isinstance(self.learning_objective, LearningObjectiveReference):
            raise AssessmentInvariantViolation(
                "learning_objective must be a LearningObjectiveReference",
                invariant="QuestionReference.learning_objective.type",
            )
        if self.curriculum_entity_id is not None:
            object.__setattr__(
                self,
                "curriculum_entity_id",
                require_identity_value(
                    self.curriculum_entity_id, "curriculum_entity_id"
                ),
            )
        if self.knowledge_level is not None and not isinstance(
            self.knowledge_level, KnowledgeLevel
        ):
            raise AssessmentInvariantViolation(
                "knowledge_level must be a KnowledgeLevel when provided",
                invariant="QuestionReference.knowledge_level.type",
            )
        if self.difficulty is not None and not isinstance(
            self.difficulty, DifficultyLevel
        ):
            raise AssessmentInvariantViolation(
                "difficulty must be a DifficultyLevel when provided",
                invariant="QuestionReference.difficulty.type",
            )
        if self.estimated_time_seconds is not None and (
            not isinstance(self.estimated_time_seconds, int)
            or isinstance(self.estimated_time_seconds, bool)
            or self.estimated_time_seconds < 0
        ):
            raise AssessmentInvariantViolation(
                "estimated_time_seconds must be a non-negative integer",
                invariant="QuestionReference.estimated_time_seconds.range",
            )
