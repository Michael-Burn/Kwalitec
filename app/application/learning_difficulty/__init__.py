"""Learning Difficulty Engine — Educational Intelligence Phase 3 (KWP-009).

Answers *how educationally demanding* a topic is for this learner.
Composes with Learning Strategy (WHAT) and Learning Diagnostics (WHY)
without redesigning Strategy, Diagnostics, Evidence, Progress, Twin,
Runtime, or Mission Runtime.
"""

from __future__ import annotations

from app.application.learning_difficulty.dto import (
    LOAD_RECOMMENDATION_TITLES,
    OBJECTIVE_COMPLEXITY_LABELS,
    OBSERVED_DIFFICULTY_LABELS,
    DifficultyEvidenceInput,
    DifficultyProfile,
    EducationalPacing,
    LearningEffort,
    LoadRecommendation,
    ObjectiveComplexity,
    ObservedDifficulty,
    RevisionPressure,
    SessionIntensity,
)
from app.application.learning_difficulty.engine import (
    LearningDifficultyEngine,
    get_learning_difficulty_engine,
)

__all__ = [
    "LOAD_RECOMMENDATION_TITLES",
    "OBJECTIVE_COMPLEXITY_LABELS",
    "OBSERVED_DIFFICULTY_LABELS",
    "DifficultyEvidenceInput",
    "DifficultyProfile",
    "EducationalPacing",
    "LearningDifficultyEngine",
    "LearningEffort",
    "LoadRecommendation",
    "ObjectiveComplexity",
    "ObservedDifficulty",
    "RevisionPressure",
    "SessionIntensity",
    "get_learning_difficulty_engine",
]
