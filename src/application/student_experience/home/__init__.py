"""Student Home Experience — XP-001.

Application-layer composition of Education OS outputs into a single
personalised home experience.

Responsibilities
    Compose existing artefacts into immutable view models.

Non-responsibilities
    Estimate mastery, generate recommendations, generate missions,
    schedule work, persist data, call AI, or implement UI.
"""

from __future__ import annotations

from application.student_experience.home.enums import (
    FocusActionKind,
    InsightKind,
    MasteryTrendLabel,
    MilestoneKind,
    QuickActionKind,
    ReadinessTrend,
)
from application.student_experience.home.errors import (
    HomeExperienceError,
    HomeInvariantViolation,
)
from application.student_experience.home.home_inputs import HomeInputs
from application.student_experience.home.ids import HomeId, SnapshotId
from application.student_experience.home.models import (
    AchievementCard,
    AchievementItem,
    ExamReadinessCard,
    HomeSnapshot,
    HomeViewModel,
    LearningInsight,
    LearningInsightCard,
    MomentumCard,
    PrimaryFocus,
    ProgressCard,
    ProgressSummary,
    QuickAction,
    QuickActionsCard,
    TodaysFocusCard,
    TodaysStudySessionCard,
    UpcomingMilestoneCard,
)
from application.student_experience.home.ports import (
    AchievementProvider,
    HomeAchievement,
    HomeNotification,
    HomePublisher,
    NotificationProvider,
)
from application.student_experience.home.student_home_service import StudentHomeService

__all__ = [
    # Service
    "StudentHomeService",
    # Inputs
    "HomeInputs",
    # Identity
    "HomeId",
    "SnapshotId",
    # View models
    "HomeViewModel",
    "HomeSnapshot",
    "TodaysFocusCard",
    "TodaysStudySessionCard",
    "ProgressCard",
    "ProgressSummary",
    "MomentumCard",
    "UpcomingMilestoneCard",
    "ExamReadinessCard",
    "AchievementCard",
    "AchievementItem",
    "LearningInsightCard",
    "LearningInsight",
    "QuickActionsCard",
    "QuickAction",
    "PrimaryFocus",
    # Enums
    "FocusActionKind",
    "QuickActionKind",
    "InsightKind",
    "ReadinessTrend",
    "MasteryTrendLabel",
    "MilestoneKind",
    # Errors
    "HomeExperienceError",
    "HomeInvariantViolation",
    # Ports
    "NotificationProvider",
    "AchievementProvider",
    "HomePublisher",
    "HomeNotification",
    "HomeAchievement",
]
