"""Learning context — curriculum/journey coordinates for a piece of evidence.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Learning Context

These are lightweight, immutable citations. They do not load a referenced
aggregate, persist state, or encode a transport DTO — and, per this
milestone's isolation decision, they do not reuse identity types owned by
other education bounded contexts (for example ``student_state``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.education.educational_evidence.ids import (
    CheckpointId,
    CompetencyId,
    MissionId,
    SubjectId,
)
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId


def _require_optional_type(value: Any, expected_type: type, field_name: str) -> None:
    if value is not None and not isinstance(value, expected_type):
        raise EducationalInvariantViolation(
            f"{field_name} must be a {expected_type.__name__} when provided",
            invariant=f"LearningContext.{field_name}.type",
        )


@dataclass(frozen=True, slots=True)
class LearningContext(EducationalValueObject):
    """Immutable, optional curriculum/journey coordinates for evidence.

    Every field is optional: which coordinates are relevant depends on the
    evidence type. An empty context is valid for evidence that carries no
    specific curriculum scope (for example general time investment).
    """

    subject_id: SubjectId | None = None
    competency_id: CompetencyId | None = None
    mission_id: MissionId | None = None
    checkpoint_id: CheckpointId | None = None
    learning_episode_id: LearningEpisodeId | None = None

    def _validate(self) -> None:
        _require_optional_type(self.subject_id, SubjectId, "subject_id")
        _require_optional_type(self.competency_id, CompetencyId, "competency_id")
        _require_optional_type(self.mission_id, MissionId, "mission_id")
        _require_optional_type(self.checkpoint_id, CheckpointId, "checkpoint_id")
        _require_optional_type(
            self.learning_episode_id, LearningEpisodeId, "learning_episode_id"
        )

    @classmethod
    def empty(cls) -> LearningContext:
        return cls()

    def is_empty(self) -> bool:
        return (
            self.subject_id is None
            and self.competency_id is None
            and self.mission_id is None
            and self.checkpoint_id is None
            and self.learning_episode_id is None
        )
