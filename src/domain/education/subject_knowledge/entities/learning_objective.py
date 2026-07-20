"""Learning objective targeting a teachable concept.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md
Concept
    Learning Objective
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, LearningObjectiveId
from domain.education.subject_knowledge.value_objects.mastery_indicator import (
    MasteryIndicator,
)


@dataclass(frozen=True, slots=True, eq=False)
class LearningObjective(EducationalEntity):
    """Precise educational aim for what a student should know, explain, or do.

    Belongs to exactly one Concept. Targets knowledge entities — not containers
    (Subject Invariant K9).
    """

    objective_id: LearningObjectiveId
    concept_id: ConceptId
    statement: str
    success_criteria: tuple[str, ...]
    mastery_indicators: tuple[MasteryIndicator, ...]

    @property
    def entity_id(self) -> LearningObjectiveId:
        return self.objective_id

    def _validate(self) -> None:
        if not isinstance(self.objective_id, LearningObjectiveId):
            raise EducationalInvariantViolation(
                "objective_id must be a LearningObjectiveId",
                invariant="LearningObjective.objective_id.type",
            )
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="LearningObjective.concept_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        criteria = tuple(
            require_non_empty_text(item, "success_criteria item")
            for item in self.success_criteria
        )
        if not criteria:
            raise EducationalInvariantViolation(
                "learning objective must have at least one success criterion",
                invariant="LearningObjective.success_criteria.non_empty",
            )
        object.__setattr__(self, "success_criteria", criteria)
        indicators = tuple(self.mastery_indicators)
        for indicator in indicators:
            if not isinstance(indicator, MasteryIndicator):
                raise EducationalInvariantViolation(
                    "mastery_indicators must contain MasteryIndicator values",
                    invariant="LearningObjective.mastery_indicators.type",
                )
        if not indicators:
            raise EducationalInvariantViolation(
                "learning objective must have at least one mastery indicator",
                invariant="LearningObjective.mastery_indicators.non_empty",
            )
        object.__setattr__(self, "mastery_indicators", indicators)

    def belongs_to(self, concept_id: ConceptId) -> bool:
        """Return True when this objective is owned by ``concept_id``."""
        return self.concept_id == concept_id
