"""Domain event: teaching intention was created.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    TeachingIntentionCreated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.enums import TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import TeachingIntentionId
from domain.education.teaching_intention.enums import IntentionStrengthLevel


@dataclass(frozen=True, slots=True)
class TeachingIntentionCreated(EducationalValueObject):
    """Immutable record that a TeachingIntention was created."""

    intention_id: TeachingIntentionId
    student_id: str
    intention_type: TeachingIntentionType
    strength_level: IntentionStrengthLevel
    priority_count: int
    diagnosis_count: int
    hypothesis_count: int

    def _validate(self) -> None:
        if not isinstance(self.intention_id, TeachingIntentionId):
            raise EducationalInvariantViolation(
                "intention_id must be a TeachingIntentionId",
                invariant="TeachingIntentionCreated.intention_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.intention_type, TeachingIntentionType):
            raise EducationalInvariantViolation(
                "intention_type must be a TeachingIntentionType",
                invariant="TeachingIntentionCreated.intention_type.type",
            )
        if not isinstance(self.strength_level, IntentionStrengthLevel):
            raise EducationalInvariantViolation(
                "strength_level must be an IntentionStrengthLevel",
                invariant="TeachingIntentionCreated.strength_level.type",
            )
        if not isinstance(self.priority_count, int) or self.priority_count < 1:
            raise EducationalInvariantViolation(
                "priority_count must be a positive integer",
                invariant="TeachingIntentionCreated.priority_count.positive",
            )
        if not isinstance(self.diagnosis_count, int) or self.diagnosis_count < 1:
            raise EducationalInvariantViolation(
                "diagnosis_count must be a positive integer",
                invariant="TeachingIntentionCreated.diagnosis_count.positive",
            )
        if not isinstance(self.hypothesis_count, int) or self.hypothesis_count < 0:
            raise EducationalInvariantViolation(
                "hypothesis_count must be a non-negative integer",
                invariant="TeachingIntentionCreated.hypothesis_count.non_negative",
            )
