"""Subsection — ordered subsection within a CKG Section."""

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
class Subsection:
    """Ordered subsection owned by a Section."""

    stable_id: StableCurriculumId
    section_id: StableCurriculumId
    code: str
    title: str
    display_order: int = 0
    difficulty: DifficultyBand = DifficultyBand.FOUNDATIONAL
    estimated_study_minutes: int = 0

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        section_id: str | StableCurriculumId,
        title: str,
        *,
        code: str | None = None,
        display_order: int = 0,
        difficulty: DifficultyBand | str = DifficultyBand.FOUNDATIONAL,
        estimated_study_minutes: int | EstimatedStudyTime = 0,
    ) -> Subsection:
        """Construct a Subsection after validating invariants."""
        sid = StableCurriculumId.of(stable_id)
        parent = StableCurriculumId.of(section_id)
        if sid.depth != StableIdDepth.SUBSECTION:
            raise ValueError("Subsection.stable_id must be subsection-depth")
        if parent.depth != StableIdDepth.SECTION:
            raise ValueError("Subsection.section_id must be section-depth")
        if sid.parent_id() != parent:
            raise ValueError("Subsection.stable_id must be a child of section_id")
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
            section_id=parent,
            code=require_non_empty(code or sid.value.split(".")[-1], "code"),
            title=require_non_empty(title, "title"),
            display_order=display_order,
            difficulty=difficulty_v,
            estimated_study_minutes=minutes,
        )
