"""Mastery indicator — observable pattern suggesting conceptual command.

Architecture Source
    CONCEPT_ARCHITECTURE.md
Concept
    Mastery Indicator
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class MasteryIndicator(EducationalValueObject):
    """Observable educational signal that supports — never alone proves — mastery.

    Indicators guide evidence interpretation so mastery does not collapse into
    coverage or a single correct answer (Concept Architecture §4.11).
    """

    description: str
    observable_signal: str
    dimension: LearningDimension | None = None

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "observable_signal",
            require_non_empty_text(self.observable_signal, "observable_signal"),
        )
        if self.dimension is not None and not isinstance(
            self.dimension, LearningDimension
        ):
            raise EducationalInvariantViolation(
                "dimension must be a LearningDimension when provided",
                invariant="MasteryIndicator.dimension.type",
            )
