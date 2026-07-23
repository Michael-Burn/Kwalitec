"""Immutable view models for Learning Journey Experience."""

from __future__ import annotations

from application.student_experience.progress.models.achievement_timeline import (
    AchievementTimeline,
    AchievementTimelineItem,
)
from application.student_experience.progress.models.consistency_card import (
    ConsistencyCard,
)
from application.student_experience.progress.models.growth_card import GrowthCard
from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.progress.models.learning_journey_view_model import (
    LearningJourneyViewModel,
)
from application.student_experience.progress.models.learning_trend_card import (
    LearningTrendCard,
)
from application.student_experience.progress.models.milestone_card import (
    JourneyMilestone,
    MilestoneCard,
)
from application.student_experience.progress.models.monthly_summary import (
    MonthlySummary,
)
from application.student_experience.progress.models.progress_overview_card import (
    ProgressOverviewCard,
)
from application.student_experience.progress.models.study_habits_card import (
    StudyHabitsCard,
)
from application.student_experience.progress.models.timeline_card import (
    TimelineCard,
    TimelineEvent,
)
from application.student_experience.progress.models.weekly_summary import WeeklySummary

__all__ = [
    "AchievementTimeline",
    "AchievementTimelineItem",
    "ConsistencyCard",
    "GrowthCard",
    "JourneyMilestone",
    "JourneySnapshot",
    "LearningJourneyViewModel",
    "LearningTrendCard",
    "MilestoneCard",
    "MonthlySummary",
    "ProgressOverviewCard",
    "StudyHabitsCard",
    "TimelineCard",
    "TimelineEvent",
    "WeeklySummary",
]
