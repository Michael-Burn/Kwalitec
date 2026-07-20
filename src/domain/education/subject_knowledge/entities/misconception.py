"""Misconception — stable incorrect mental model about a concept.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md / MISCONCEPTION_AUTHORING_MODEL.md
Concept
    Misconception
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    require_non_empty_text,
)
from domain.education.foundation.enums import (
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, MisconceptionId


@dataclass(frozen=True, slots=True, eq=False)
class Misconception(EducationalEntity):
    """Named stable wrong model attached to one or more concepts (K4).

    Captures description, incorrect reasoning, causes, observable evidence,
    recommended teaching response, and repair evidence so tutoring can confront
    patterned error explicitly.
    """

    misconception_id: MisconceptionId
    concept_id: ConceptId
    description: str
    incorrect_reasoning: str
    likely_causes: tuple[str, ...]
    observable_evidence: tuple[str, ...]
    recommended_teaching_intentions: tuple[TeachingIntentionType, ...]
    recommended_strategies: tuple[TeachingStrategyType, ...]
    repair_evidence: tuple[str, ...]

    @property
    def entity_id(self) -> MisconceptionId:
        return self.misconception_id

    def _validate(self) -> None:
        if not isinstance(self.misconception_id, MisconceptionId):
            raise EducationalInvariantViolation(
                "misconception_id must be a MisconceptionId",
                invariant="Misconception.misconception_id.type",
            )
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="Misconception.concept_id.type",
            )
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "incorrect_reasoning",
            require_non_empty_text(self.incorrect_reasoning, "incorrect_reasoning"),
        )
        object.__setattr__(
            self,
            "likely_causes",
            _require_non_empty_text_tuple(self.likely_causes, "likely_causes"),
        )
        object.__setattr__(
            self,
            "observable_evidence",
            _require_non_empty_text_tuple(
                self.observable_evidence, "observable_evidence"
            ),
        )
        object.__setattr__(
            self,
            "repair_evidence",
            _require_non_empty_text_tuple(self.repair_evidence, "repair_evidence"),
        )
        intentions = tuple(self.recommended_teaching_intentions)
        if not intentions:
            raise EducationalInvariantViolation(
                "misconception must recommend at least one teaching intention",
                invariant="Misconception.recommended_teaching_intentions.non_empty",
            )
        for intention in intentions:
            if not isinstance(intention, TeachingIntentionType):
                raise EducationalInvariantViolation(
                    "recommended teaching intentions must be TeachingIntentionType",
                    invariant="Misconception.recommended_teaching_intentions.type",
                )
        object.__setattr__(self, "recommended_teaching_intentions", intentions)
        strategies = tuple(self.recommended_strategies)
        if not strategies:
            raise EducationalInvariantViolation(
                "misconception must recommend at least one teaching strategy",
                invariant="Misconception.recommended_strategies.non_empty",
            )
        for strategy in strategies:
            if not isinstance(strategy, TeachingStrategyType):
                raise EducationalInvariantViolation(
                    "recommended strategies must be TeachingStrategyType",
                    invariant="Misconception.recommended_strategies.type",
                )
        object.__setattr__(self, "recommended_strategies", strategies)

    def belongs_to(self, concept_id: ConceptId) -> bool:
        """Return True when this misconception is attached to ``concept_id``."""
        return self.concept_id == concept_id


def _require_non_empty_text_tuple(
    values: tuple[str, ...] | list[str],
    field_name: str,
) -> tuple[str, ...]:
    cleaned = tuple(
        require_non_empty_text(item, f"{field_name} item") for item in values
    )
    if not cleaned:
        raise EducationalInvariantViolation(
            f"{field_name} must contain at least one entry",
            invariant=f"Misconception.{field_name}.non_empty",
        )
    return cleaned
