"""Section — ordered section within a CKG Topic."""

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
class Section:
    """Ordered section owned by a Topic."""

    stable_id: StableCurriculumId
    topic_id: StableCurriculumId
    code: str
    title: str
    display_order: int = 0
    difficulty: DifficultyBand = DifficultyBand.FOUNDATIONAL
    estimated_study_minutes: int = 0

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        topic_id: str | StableCurriculumId,
        title: str,
        *,
        code: str | None = None,
        display_order: int = 0,
        difficulty: DifficultyBand | str = DifficultyBand.FOUNDATIONAL,
        estimated_study_minutes: int | EstimatedStudyTime = 0,
    ) -> Section:
        """Construct a Section after validating invariants."""
        sid = StableCurriculumId.of(stable_id)
        parent = StableCurriculumId.of(topic_id)
        if sid.depth != StableIdDepth.SECTION:
            raise ValueError("Section.stable_id must be section-depth")
        if parent.depth != StableIdDepth.TOPIC:
            raise ValueError("Section.topic_id must be topic-depth")
        if sid.parent_id() != parent:
            raise ValueError("Section.stable_id must be a child of topic_id")
        if display_order < 0:
            raise ValueError("display_order must be non-negative")
        minutes = int(EstimatedStudyTime.of(estimated_study_minutes))
        difficulty_v = (
            difficulty
            if isinstance(difficulty, DifficultyBand)
            else DifficultyBand(difficulty)
        )
        # Code defaults to ``S{ss}.{oo}`` trailing pair.
        default_code = ".".join(sid.value.split(".")[-2:])
        return cls(
            stable_id=sid,
            topic_id=parent,
            code=require_non_empty(code or default_code, "code"),
            title=require_non_empty(title, "title"),
            display_order=display_order,
            difficulty=difficulty_v,
            estimated_study_minutes=minutes,
        )
