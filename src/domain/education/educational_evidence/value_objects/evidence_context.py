"""Evidence context — full contextual envelope for a piece of evidence.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Context
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.educational_evidence.value_objects.learning_context import (
    LearningContext,
)
from domain.education.educational_evidence.value_objects.learning_environment import (
    LearningEnvironment,
)
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EvidenceContext(EducationalValueObject):
    """Immutable composition of curriculum coordinates and setting.

    Combines *where in the syllabus/journey* (``LearningContext``) with
    *how/where the interaction happened* (``LearningEnvironment``) into a
    single contextual envelope attached to one piece of evidence.
    """

    learning_context: LearningContext
    learning_environment: LearningEnvironment

    def _validate(self) -> None:
        if not isinstance(self.learning_context, LearningContext):
            raise EducationalInvariantViolation(
                "learning_context must be a LearningContext",
                invariant="EvidenceContext.learning_context.type",
            )
        if not isinstance(self.learning_environment, LearningEnvironment):
            raise EducationalInvariantViolation(
                "learning_environment must be a LearningEnvironment",
                invariant="EvidenceContext.learning_environment.type",
            )

    @classmethod
    def of(
        cls,
        learning_environment: LearningEnvironment,
        *,
        learning_context: LearningContext | None = None,
    ) -> EvidenceContext:
        return cls(
            learning_context=learning_context or LearningContext.empty(),
            learning_environment=learning_environment,
        )

    def has_subject(self) -> bool:
        return self.learning_context.subject_id is not None

    def has_competency(self) -> bool:
        return self.learning_context.competency_id is not None

    def has_mission(self) -> bool:
        return self.learning_context.mission_id is not None

    def has_checkpoint(self) -> bool:
        return self.learning_context.checkpoint_id is not None

    def has_learning_episode(self) -> bool:
        return self.learning_context.learning_episode_id is not None
