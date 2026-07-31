"""Educational Authoring — Educational Experience Phase 2 (KWP-015).

Transforms curriculum intelligence into Learning Episodes and authored
Mission composition for Adaptive Workspace.

Does not redesign Learning Runtime, Evidence, Progress, Strategy,
Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory,
Readiness Forecast, Knowledge Architecture, Adaptive Workspace engines,
or Mission Runtime.
"""

from __future__ import annotations

from app.application.educational_authoring.dto import (
    ACTIVITY_TITLES,
    AuthoringContext,
    EducationalAuthoringSnapshot,
    EpisodeActivity,
    EpisodeActivityKind,
    ExtraStudyKind,
    ExtraStudyOffer,
    LearningEpisode,
    MissionComposition,
    TomorrowPreview,
)
from app.application.educational_authoring.engine import (
    EducationalAuthoringEngine,
    authoring_context_from_mapping,
    get_educational_authoring_engine,
    reset_educational_authoring_engine,
)

__all__ = [
    "ACTIVITY_TITLES",
    "AuthoringContext",
    "EducationalAuthoringEngine",
    "EducationalAuthoringSnapshot",
    "EpisodeActivity",
    "EpisodeActivityKind",
    "ExtraStudyKind",
    "ExtraStudyOffer",
    "LearningEpisode",
    "MissionComposition",
    "TomorrowPreview",
    "authoring_context_from_mapping",
    "get_educational_authoring_engine",
    "reset_educational_authoring_engine",
]
