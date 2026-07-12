"""Application curriculum Integration adapters.

Produces domain ``CurriculumContext`` from Curriculum authority without
owning syllabus structure or educational judgement.
"""

from __future__ import annotations

from app.application.curriculum.curriculum_context_builder import (
    CurriculumContextBuilder,
    CurriculumContextBuildError,
    InvalidCurriculumError,
    MissingCurriculumError,
    UnsupportedCurriculumVersionError,
)

__all__ = [
    "CurriculumContextBuildError",
    "CurriculumContextBuilder",
    "InvalidCurriculumError",
    "MissingCurriculumError",
    "UnsupportedCurriculumVersionError",
]
