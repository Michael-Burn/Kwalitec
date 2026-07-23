"""Learning depth — position within a dependency chain.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Learning Depth
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class LearningDepth(EducationalValueObject):
    """Immutable, non-negative distance from a foundation in the graph.

    Depth zero denotes a foundation: a node with no further structural
    prerequisites of its own.
    """

    level: int

    def _validate(self) -> None:
        if isinstance(self.level, bool) or not isinstance(self.level, int):
            raise EducationalInvariantViolation(
                "level must be an integer",
                invariant="LearningDepth.level.type",
            )
        if self.level < 0:
            raise EducationalInvariantViolation(
                "level must be non-negative",
                invariant="LearningDepth.level.non_negative",
            )

    @classmethod
    def foundation(cls) -> LearningDepth:
        return cls(level=0)

    def is_foundation(self) -> bool:
        return self.level == 0

    def next(self) -> LearningDepth:
        return LearningDepth(level=self.level + 1)

    def deeper_than(self, other: LearningDepth) -> bool:
        return self.level > other.level

    def __str__(self) -> str:
        return str(self.level)
