"""Learning Journey Experience — XP-002.

Application-layer composition of Education OS histories into a coherent
learning narrative.

Responsibilities
    Project educational history into immutable view models.

Non-responsibilities
    Estimate mastery, generate recommendations, generate missions,
    schedule work, persist data, call AI, or render charts.
"""

from __future__ import annotations

from application.student_experience.progress.enums import (
    JourneyMilestoneKind,
    StudyTimeBand,
    TimelineEventKind,
    TrajectoryLabel,
    TrendDirection,
    WeekdayLabel,
)
from application.student_experience.progress.errors import (
    JourneyExperienceError,
    JourneyInvariantViolation,
)
from application.student_experience.progress.ids import JourneyId, JourneySnapshotId
from application.student_experience.progress.journey_inputs import (
    JourneyInputs,
    StudyStatistics,
)
from application.student_experience.progress.learning_journey_service import (
    LearningJourneyService,
)
from application.student_experience.progress.models import (
    AchievementTimeline,
    AchievementTimelineItem,
    ConsistencyCard,
    GrowthCard,
    JourneyMilestone,
    JourneySnapshot,
    LearningJourneyViewModel,
    LearningTrendCard,
    MilestoneCard,
    MonthlySummary,
    ProgressOverviewCard,
    StudyHabitsCard,
    TimelineCard,
    TimelineEvent,
    WeeklySummary,
)
from application.student_experience.progress.ports import (
    JourneyExportProvider,
    JourneyPublisher,
    MilestoneProvider,
    ProvidedMilestone,
)

__all__ = [
    # Service
    "LearningJourneyService",
    # Inputs
    "JourneyInputs",
    "StudyStatistics",
    # Identity
    "JourneyId",
    "JourneySnapshotId",
    # View models
    "LearningJourneyViewModel",
    "JourneySnapshot",
    "TimelineCard",
    "TimelineEvent",
    "ProgressOverviewCard",
    "GrowthCard",
    "ConsistencyCard",
    "StudyHabitsCard",
    "MilestoneCard",
    "JourneyMilestone",
    "LearningTrendCard",
    "AchievementTimeline",
    "AchievementTimelineItem",
    "WeeklySummary",
    "MonthlySummary",
    # Enums
    "TimelineEventKind",
    "TrendDirection",
    "TrajectoryLabel",
    "StudyTimeBand",
    "JourneyMilestoneKind",
    "WeekdayLabel",
    # Errors
    "JourneyExperienceError",
    "JourneyInvariantViolation",
    # Ports
    "JourneyPublisher",
    "JourneyExportProvider",
    "MilestoneProvider",
    "ProvidedMilestone",
]
