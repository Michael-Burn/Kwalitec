"""Learning Objective — measurable objective under a Subsection."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

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


class CognitiveLevel(StrEnum):
    """Bloom-aligned cognitive level for a learning objective."""

    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class LearningType(StrEnum):
    """Educational learning type for a learning objective."""

    CONCEPT = "concept"
    PROCEDURE = "procedure"
    PROBLEM_SOLVING = "problem_solving"
    APPLICATION = "application"
    ANALYSIS = "analysis"


@dataclass(frozen=True)
class LearningObjective:
    """Measurable learning objective owned by a Subsection."""

    stable_id: StableCurriculumId
    subsection_id: StableCurriculumId
    code: str
    statement: str
    cognitive_level: CognitiveLevel = CognitiveLevel.UNDERSTAND
    learning_type: LearningType = LearningType.CONCEPT
    display_order: int = 0
    difficulty: DifficultyBand = DifficultyBand.FOUNDATIONAL
    estimated_study_minutes: int = 0

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        subsection_id: str | StableCurriculumId,
        statement: str,
        *,
        code: str | None = None,
        cognitive_level: CognitiveLevel | str = CognitiveLevel.UNDERSTAND,
        learning_type: LearningType | str = LearningType.CONCEPT,
        display_order: int = 0,
        difficulty: DifficultyBand | str = DifficultyBand.FOUNDATIONAL,
        estimated_study_minutes: int | EstimatedStudyTime = 0,
    ) -> LearningObjective:
        """Construct a LearningObjective after validating invariants."""
        sid = StableCurriculumId.of(stable_id)
        parent = StableCurriculumId.of(subsection_id)
        if sid.depth != StableIdDepth.LEARNING_OBJECTIVE:
            raise ValueError(
                "LearningObjective.stable_id must be learning_objective-depth"
            )
        if parent.depth != StableIdDepth.SUBSECTION:
            raise ValueError(
                "LearningObjective.subsection_id must be subsection-depth"
            )
        if sid.parent_id() != parent:
            raise ValueError(
                "LearningObjective.stable_id must be a child of subsection_id"
            )
        if display_order < 0:
            raise ValueError("display_order must be non-negative")
        minutes = int(EstimatedStudyTime.of(estimated_study_minutes))
        difficulty_v = (
            difficulty
            if isinstance(difficulty, DifficultyBand)
            else DifficultyBand(difficulty)
        )
        cog = (
            cognitive_level
            if isinstance(cognitive_level, CognitiveLevel)
            else CognitiveLevel(cognitive_level)
        )
        ltype = (
            learning_type
            if isinstance(learning_type, LearningType)
            else LearningType(learning_type)
        )
        return cls(
            stable_id=sid,
            subsection_id=parent,
            code=require_non_empty(code or sid.value.split(".")[-1], "code"),
            statement=require_non_empty(statement, "statement"),
            cognitive_level=cog,
            learning_type=ltype,
            display_order=display_order,
            difficulty=difficulty_v,
            estimated_study_minutes=minutes,
        )
