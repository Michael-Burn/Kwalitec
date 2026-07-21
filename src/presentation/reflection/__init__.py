"""Reflection Workspace — structured post-session evidence capture surface.

Consumes ``StudySessionViewModel`` and ``SessionState``. Formats display chrome
for confidence, difficulty, mission completion, weak concepts, student notes,
and a reflection summary. Never diagnoses, recommends, persists, orchestrates
learning, or invokes AI.
"""

from __future__ import annotations

from presentation.reflection.confidence_scale import (
    ConfidenceLevel,
    ConfidenceScale,
    ConfidenceScaleView,
    DifficultyLevel,
    ScaleOptionView,
)
from presentation.reflection.reflection_mapper import ReflectionMapper
from presentation.reflection.reflection_presenter import ReflectionPresenter
from presentation.reflection.reflection_view_model import (
    ConfidenceFieldView,
    DifficultyFieldView,
    MissionCompletionFieldView,
    ReflectionSummaryFieldView,
    ReflectionViewModel,
    StudentNotesFieldView,
    WeakConceptFieldView,
)

__all__ = [
    "ConfidenceFieldView",
    "ConfidenceLevel",
    "ConfidenceScale",
    "ConfidenceScaleView",
    "DifficultyFieldView",
    "DifficultyLevel",
    "MissionCompletionFieldView",
    "ReflectionMapper",
    "ReflectionPresenter",
    "ReflectionSummaryFieldView",
    "ReflectionViewModel",
    "ScaleOptionView",
    "StudentNotesFieldView",
    "WeakConceptFieldView",
]
