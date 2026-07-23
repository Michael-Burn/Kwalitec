"""Immutable view models for Student Home Experience."""

from __future__ import annotations

from application.student_experience.home.models.achievement_card import (
    AchievementCard,
    AchievementItem,
)
from application.student_experience.home.models.exam_readiness_card import (
    ExamReadinessCard,
)
from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.home.models.home_view_model import HomeViewModel
from application.student_experience.home.models.learning_insight_card import (
    LearningInsight,
    LearningInsightCard,
)
from application.student_experience.home.models.momentum_card import MomentumCard
from application.student_experience.home.models.primary_focus import PrimaryFocus
from application.student_experience.home.models.progress_card import ProgressCard
from application.student_experience.home.models.progress_summary import ProgressSummary
from application.student_experience.home.models.quick_actions_card import (
    QuickAction,
    QuickActionsCard,
)
from application.student_experience.home.models.todays_focus_card import TodaysFocusCard
from application.student_experience.home.models.todays_study_session_card import (
    TodaysStudySessionCard,
)
from application.student_experience.home.models.upcoming_milestone_card import (
    UpcomingMilestoneCard,
)

__all__ = [
    "AchievementCard",
    "AchievementItem",
    "ExamReadinessCard",
    "HomeSnapshot",
    "HomeViewModel",
    "LearningInsight",
    "LearningInsightCard",
    "MomentumCard",
    "PrimaryFocus",
    "ProgressCard",
    "ProgressSummary",
    "QuickAction",
    "QuickActionsCard",
    "TodaysFocusCard",
    "TodaysStudySessionCard",
    "UpcomingMilestoneCard",
]
