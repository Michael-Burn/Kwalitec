"""Study Curriculum learning-state assembler (read-side join).

Framework-independent application layer. Persistence and Runtime C wiring
live under ``app.infrastructure.adapters.study_curriculum``.
"""

from __future__ import annotations

from app.application.study_curriculum.assembler import (
    CurriculumLearningStateAssembler,
    resolve_topic_learning_state,
    topic_has_been_reached,
)
from app.application.study_curriculum.states import (
    EVIDENCE_RELIABILITY_FLOOR,
    MASTERY_THRESHOLD,
    TopicLearningState,
)
from app.application.study_curriculum.types import (
    CurriculumLearningSnapshot,
    TopicCurriculumState,
)

__all__ = [
    "CurriculumLearningSnapshot",
    "CurriculumLearningStateAssembler",
    "EVIDENCE_RELIABILITY_FLOOR",
    "MASTERY_THRESHOLD",
    "TopicCurriculumState",
    "TopicLearningState",
    "resolve_topic_learning_state",
    "topic_has_been_reached",
]
