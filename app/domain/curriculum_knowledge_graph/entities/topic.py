"""Topic — CMP-level topic within a Subject."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_knowledge_graph._text import require_non_empty
from app.domain.curriculum_knowledge_graph.value_objects.difficulty import (
    DifficultyBand,
)
from app.domain.curriculum_knowledge_graph.value_objects.estimated_study_time import (
    EstimatedStudyTime,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)


@dataclass(frozen=True)
class Topic:
    """Ordered CMP topic owned by a Subject."""

    stable_id: StableCurriculumId
    subject_id: StableCurriculumId
    code: str
    title: str
    display_order: int = 0
    difficulty: DifficultyBand = DifficultyBand.FOUNDATIONAL
    estimated_study_minutes: int = 0

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        subject_id: str | StableCurriculumId,
        title: str,
        *,
        code: str | None = None,
        display_order: int = 0,
        difficulty: DifficultyBand | str = DifficultyBand.FOUNDATIONAL,
        estimated_study_minutes: int | EstimatedStudyTime = 0,
    ) -> Topic:
        """Construct a Topic after validating invariants."""
        sid = StableCurriculumId.of(stable_id)
        parent = StableCurriculumId.of(subject_id)
        if sid.depth != StableIdDepth.TOPIC:
            raise ValueError("Topic.stable_id must be topic-depth")
        if parent.depth != StableIdDepth.SUBJECT:
            raise ValueError("Topic.subject_id must be subject-depth")
        if sid.parent_id() != parent:
            raise ValueError("Topic.stable_id must be a child of subject_id")
        if display_order < 0:
            raise ValueError("display_order must be non-negative")
        minutes = int(EstimatedStudyTime.of(estimated_study_minutes))
        difficulty_v = (
            difficulty
            if isinstance(difficulty, DifficultyBand)
            else DifficultyBand(difficulty)
        )
        return cls(
            stable_id=sid,
            subject_id=parent,
            code=require_non_empty(code or sid.value.split(".")[-1], "code"),
            title=require_non_empty(title, "title"),
            display_order=display_order,
            difficulty=difficulty_v,
            estimated_study_minutes=minutes,
        )
