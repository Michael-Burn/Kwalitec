"""Domain event: teaching intention was revised.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    TeachingIntentionRevised
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
from domain.education.teaching_intention.enums import (
    IntentionRevisionKind,
    IntentionStrengthLevel,
)


@dataclass(frozen=True, slots=True)
class TeachingIntentionRevised(EducationalValueObject):
    """Immutable record that a TeachingIntention was revised."""

    intention_id: TeachingIntentionId
    student_id: str
    intention_type: TeachingIntentionType
    strength_level: IntentionStrengthLevel
    revision_kind: IntentionRevisionKind

    def _validate(self) -> None:
        if not isinstance(self.intention_id, TeachingIntentionId):
            raise EducationalInvariantViolation(
                "intention_id must be a TeachingIntentionId",
                invariant="TeachingIntentionRevised.intention_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.intention_type, TeachingIntentionType):
            raise EducationalInvariantViolation(
                "intention_type must be a TeachingIntentionType",
                invariant="TeachingIntentionRevised.intention_type.type",
            )
        if not isinstance(self.strength_level, IntentionStrengthLevel):
            raise EducationalInvariantViolation(
                "strength_level must be an IntentionStrengthLevel",
                invariant="TeachingIntentionRevised.strength_level.type",
            )
        if not isinstance(self.revision_kind, IntentionRevisionKind):
            raise EducationalInvariantViolation(
                "revision_kind must be an IntentionRevisionKind",
                invariant="TeachingIntentionRevised.revision_kind.type",
            )
