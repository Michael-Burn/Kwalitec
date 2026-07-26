"""Student Experience DTO package."""

from __future__ import annotations

from app.application.student_experience.dto.commitment_reflection_snapshot import (
    CommitmentReflectionSnapshot,
)
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.history_snapshot import (
    AchievementSnapshot,
    CompletedSessionSnapshot,
    HistorySnapshot,
    ReadinessPointSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.dto.journey_snapshot import (
    JourneySnapshot,
    JourneyTopicSnapshot,
)
from app.application.student_experience.dto.profile_snapshot import (
    AccountSettingsSnapshot,
    LearningGoalSnapshot,
    LearningStatisticsSnapshot,
    ProfileSnapshot,
    StudyPreferencesSnapshot,
)
from app.application.student_experience.dto.readiness_explanation_snapshot import (
    ReadinessExplanationSnapshot,
)
from app.application.student_experience.dto.recommendation_alternative_snapshot import (
    RecommendationAlternativeSnapshot,
)
from app.application.student_experience.dto.recommendation_commitment_snapshot import (
    RecommendationCommitmentSnapshot,
)
from app.application.student_experience.dto.recommendation_narrative_entry_snapshot import (  # noqa: E501
    RecommendationNarrativeEntrySnapshot,
)
from app.application.student_experience.dto.revision_snapshot import (
    RevisionOptionSnapshot,
    RevisionSnapshot,
)

__all__ = [
    "AccountSettingsSnapshot",
    "AchievementSnapshot",
    "CommitmentReflectionSnapshot",
    "CompletedSessionSnapshot",
    "ExplanationSnapshot",
    "HistorySnapshot",
    "HomeSnapshot",
    "JourneySnapshot",
    "JourneyTopicSnapshot",
    "LearningGoalSnapshot",
    "LearningStatisticsSnapshot",
    "ProfileSnapshot",
    "ReadinessExplanationSnapshot",
    "ReadinessPointSnapshot",
    "RecommendationAlternativeSnapshot",
    "RecommendationCommitmentSnapshot",
    "RecommendationNarrativeEntrySnapshot",
    "RevisionOptionSnapshot",
    "RevisionSnapshot",
    "StartSessionActionSnapshot",
    "StudyPreferencesSnapshot",
]
