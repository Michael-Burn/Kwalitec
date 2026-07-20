"""Motivation — deterministic motivational presentation messaging.

Architecture Source
    EXP-001 Student Experience Engine
Concept
    Motivation
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.student_experience.enums import MotivationTone
from domain.student_experience.ids import MotivationId


@dataclass(frozen=True, slots=True)
class Motivation(EducationalValueObject):
    """Immutable motivational message selected from Educational OS presentation signals.

    Motivation is engagement copy. It must not issue educational decisions,
    alter recommendations, or claim mastery.
    """

    motivation_id: MotivationId
    tone: MotivationTone
    message: str
    supporting_signal: str

    def _validate(self) -> None:
        if not isinstance(self.motivation_id, MotivationId):
            raise EducationalInvariantViolation(
                "motivation_id must be a MotivationId",
                invariant="Motivation.motivation_id.type",
            )
        if not isinstance(self.tone, MotivationTone):
            raise EducationalInvariantViolation(
                "tone must be a MotivationTone",
                invariant="Motivation.tone.type",
            )
        object.__setattr__(
            self,
            "message",
            require_non_empty_text(self.message, "message"),
        )
        if len(self.message) < 12:
            raise EducationalInvariantViolation(
                "message must be substantive",
                invariant="Motivation.message.substantive",
            )
        object.__setattr__(
            self,
            "supporting_signal",
            require_non_empty_text(self.supporting_signal, "supporting_signal"),
        )
