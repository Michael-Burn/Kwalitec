"""Episode reflection — structured metacognitive close of an episode.

Architecture Source
    LEARNING_EPISODE_ARCHITECTURE.md / LEARNING_EPISODE_INVARIANTS.md (E6)
Concept
    Episode Reflection
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    require_non_empty_text,
)
from domain.education.foundation.enums import ConfidenceLevel, ReflectionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ReflectionId


@dataclass(frozen=True, slots=True, eq=False)
class EpisodeReflection(EducationalEntity):
    """Student reflection belonging to a Learning Episode (Invariant E6).

    Soft evidence with consequence for the next educational decision.
    Fabricated / empty reflection is educationally void.
    """

    reflection_id: ReflectionId
    reflection_type: ReflectionType
    content: str
    perceived_difficulty: ConfidenceLevel | None = None
    perceived_understanding: ConfidenceLevel | None = None

    @property
    def entity_id(self) -> ReflectionId:
        return self.reflection_id

    def _validate(self) -> None:
        if not isinstance(self.reflection_id, ReflectionId):
            raise EducationalInvariantViolation(
                "reflection_id must be a ReflectionId",
                invariant="EpisodeReflection.reflection_id.type",
            )
        if not isinstance(self.reflection_type, ReflectionType):
            raise EducationalInvariantViolation(
                "reflection_type must be a ReflectionType",
                invariant="EpisodeReflection.reflection_type.type",
            )
        object.__setattr__(
            self,
            "content",
            require_non_empty_text(self.content, "content"),
        )
        if self.perceived_difficulty is not None and not isinstance(
            self.perceived_difficulty, ConfidenceLevel
        ):
            raise EducationalInvariantViolation(
                "perceived_difficulty must be a ConfidenceLevel",
                invariant="EpisodeReflection.perceived_difficulty.type",
            )
        if self.perceived_understanding is not None and not isinstance(
            self.perceived_understanding, ConfidenceLevel
        ):
            raise EducationalInvariantViolation(
                "perceived_understanding must be a ConfidenceLevel",
                invariant="EpisodeReflection.perceived_understanding.type",
            )

    def can_influence_next_decision(self) -> bool:
        """Reflection has consequence when content is substantive."""
        return len(self.content.strip()) >= 3
