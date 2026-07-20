"""Domain event: reflection was recorded on a Learning Episode.

Architecture Source
    LEARNING_EPISODE_INVARIANTS.md (E6)
Concept
    ReflectionRecorded
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import ReflectionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId, ReflectionId


@dataclass(frozen=True, slots=True)
class ReflectionRecorded(EducationalValueObject):
    """Immutable record that episode reflection was captured."""

    episode_id: LearningEpisodeId
    reflection_id: ReflectionId
    reflection_type: ReflectionType

    def _validate(self) -> None:
        if not isinstance(self.episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "episode_id must be a LearningEpisodeId",
                invariant="ReflectionRecorded.episode_id.type",
            )
        if not isinstance(self.reflection_id, ReflectionId):
            raise EducationalInvariantViolation(
                "reflection_id must be a ReflectionId",
                invariant="ReflectionRecorded.reflection_id.type",
            )
        if not isinstance(self.reflection_type, ReflectionType):
            raise EducationalInvariantViolation(
                "reflection_type must be a ReflectionType",
                invariant="ReflectionRecorded.reflection_type.type",
            )
