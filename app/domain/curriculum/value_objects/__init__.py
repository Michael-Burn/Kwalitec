"""Curriculum value objects."""

from __future__ import annotations

from app.domain.curriculum.value_objects.curriculum_id import CurriculumId
from app.domain.curriculum.value_objects.dependency_type import (
    HARD_DEPENDENCY_TYPES,
    SOFT_DEPENDENCY_TYPES,
    DependencyType,
    is_hard_dependency,
)
from app.domain.curriculum.value_objects.topic_difficulty import (
    TopicDifficulty,
    difficulty_at_least,
    difficulty_rank,
)
from app.domain.curriculum.value_objects.topic_id import TopicId
from app.domain.curriculum.value_objects.topic_status import (
    TopicStatus,
    is_studyable_status,
    is_terminal_topic_status,
)

__all__ = [
    "HARD_DEPENDENCY_TYPES",
    "SOFT_DEPENDENCY_TYPES",
    "CurriculumId",
    "DependencyType",
    "TopicDifficulty",
    "TopicId",
    "TopicStatus",
    "difficulty_at_least",
    "difficulty_rank",
    "is_hard_dependency",
    "is_studyable_status",
    "is_terminal_topic_status",
]
