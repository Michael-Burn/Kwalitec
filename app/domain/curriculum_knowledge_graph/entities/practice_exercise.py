"""Practice Exercise — educational object owned by a Subsection or LO."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_knowledge_graph._text import require_non_empty
from app.domain.curriculum_knowledge_graph.value_objects.difficulty import (
    DifficultyBand,
)
from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)


@dataclass(frozen=True)
class PracticeExercise:
    """Practice-exercise educational object (structure only — no item bank)."""

    stable_id: StableCurriculumId
    owner_id: StableCurriculumId
    title: str
    difficulty: DifficultyBand = DifficultyBand.FOUNDATIONAL

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        owner_id: str | StableCurriculumId,
        title: str,
        *,
        difficulty: DifficultyBand | str = DifficultyBand.FOUNDATIONAL,
    ) -> PracticeExercise:
        """Construct a PracticeExercise owned by a subsection or LO."""
        sid = StableCurriculumId.of(stable_id)
        owner = StableCurriculumId.of(owner_id)
        if sid.kind != CkgNodeKind.PRACTICE_EXERCISE:
            raise ValueError(
                "PracticeExercise.stable_id must be a practice_exercise id"
            )
        if owner.depth not in {
            StableIdDepth.SUBSECTION,
            StableIdDepth.LEARNING_OBJECTIVE,
        }:
            raise ValueError("PracticeExercise.owner_id must be subsection or LO")
        if sid.parent_id() != owner:
            raise ValueError(
                "PracticeExercise.stable_id must be a child of owner_id"
            )
        difficulty_v = (
            difficulty
            if isinstance(difficulty, DifficultyBand)
            else DifficultyBand(difficulty)
        )
        return cls(
            stable_id=sid,
            owner_id=owner,
            title=require_non_empty(title, "title"),
            difficulty=difficulty_v,
        )
