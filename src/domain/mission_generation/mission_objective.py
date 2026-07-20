"""MissionObjective — educational aim of a generated mission.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    Mission Objective
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    require_non_empty_text,
)
from domain.education.foundation.enums import (
    DiagnosisType,
    LearningDimension,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId
from domain.mission_generation.ids import MissionObjectiveId


@dataclass(frozen=True, slots=True, eq=False)
class MissionObjective(EducationalEntity):
    """Educational aim the mission pursues for one sitting.

    States *what educational change* the ordered tasks advance. Must not claim
    mastery as an outcome.
    """

    objective_id: MissionObjectiveId
    statement: str
    diagnosis_type: DiagnosisType
    primary_strategy: TeachingStrategyType
    concept_ids: tuple[ConceptId, ...] = ()
    learning_dimension: LearningDimension | None = None
    scope_statement: str | None = None

    @property
    def entity_id(self) -> MissionObjectiveId:
        return self.objective_id

    def _validate(self) -> None:
        if not isinstance(self.objective_id, MissionObjectiveId):
            raise EducationalInvariantViolation(
                "objective_id must be a MissionObjectiveId",
                invariant="MissionObjective.objective_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        self._assert_no_mastery_claim(self.statement)
        if not isinstance(self.diagnosis_type, DiagnosisType):
            raise EducationalInvariantViolation(
                "diagnosis_type must be a DiagnosisType",
                invariant="MissionObjective.diagnosis_type.type",
            )
        if not isinstance(self.primary_strategy, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "primary_strategy must be a TeachingStrategyType",
                invariant="MissionObjective.primary_strategy.type",
            )
        if not isinstance(self.concept_ids, tuple):
            raise EducationalInvariantViolation(
                "concept_ids must be a tuple of ConceptId",
                invariant="MissionObjective.concept_ids.type",
            )
        seen: set[str] = set()
        for concept_id in self.concept_ids:
            if not isinstance(concept_id, ConceptId):
                raise EducationalInvariantViolation(
                    "concept_ids must contain ConceptId values",
                    invariant="MissionObjective.concept_ids.item_type",
                )
            if concept_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept ids are not allowed",
                    invariant="MissionObjective.concept_ids.unique",
                )
            seen.add(concept_id.value)
        if self.learning_dimension is not None and not isinstance(
            self.learning_dimension, LearningDimension
        ):
            raise EducationalInvariantViolation(
                "learning_dimension must be a LearningDimension when provided",
                invariant="MissionObjective.learning_dimension.type",
            )
        if self.scope_statement is not None:
            object.__setattr__(
                self,
                "scope_statement",
                require_non_empty_text(self.scope_statement, "scope_statement"),
            )

    @staticmethod
    def _assert_no_mastery_claim(text: str) -> None:
        lowered = text.casefold()
        forbidden = ("mastered", "achieve mastery", "declare mastery", "full mastery")
        for token in forbidden:
            if token in lowered:
                raise EducationalInvariantViolation(
                    "mission objective must never claim mastery as outcome",
                    invariant="MissionObjective.no_mastery_claim",
                )
