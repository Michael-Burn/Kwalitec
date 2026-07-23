"""LearningJourneyViewModel — composed student learning journey surface."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.progress.errors import JourneyInvariantViolation
from application.student_experience.progress.ids import JourneyId
from application.student_experience.progress.models.achievement_timeline import (
    AchievementTimeline,
)
from application.student_experience.progress.models.consistency_card import (
    ConsistencyCard,
)
from application.student_experience.progress.models.growth_card import GrowthCard
from application.student_experience.progress.models.learning_trend_card import (
    LearningTrendCard,
)
from application.student_experience.progress.models.milestone_card import MilestoneCard
from application.student_experience.progress.models.monthly_summary import (
    MonthlySummary,
)
from application.student_experience.progress.models.progress_overview_card import (
    ProgressOverviewCard,
)
from application.student_experience.progress.models.study_habits_card import (
    StudyHabitsCard,
)
from application.student_experience.progress.models.timeline_card import TimelineCard
from application.student_experience.progress.models.weekly_summary import WeeklySummary


@dataclass(frozen=True, slots=True)
class LearningJourneyViewModel:
    """Immutable composed learning journey experience.

    Projects educational history into student-facing language. Never exposes
    Education OS type names or internal architecture.
    """

    journey_id: JourneyId
    student_id: str
    composed_at: datetime
    timeline: TimelineCard
    progress_overview: ProgressOverviewCard
    growth: GrowthCard
    consistency: ConsistencyCard
    study_habits: StudyHabitsCard
    milestones: MilestoneCard
    learning_trends: LearningTrendCard
    achievement_timeline: AchievementTimeline
    weekly_summary: WeeklySummary
    monthly_summary: MonthlySummary

    def __post_init__(self) -> None:
        if not isinstance(self.journey_id, JourneyId):
            raise JourneyInvariantViolation(
                "journey_id must be a JourneyId",
                invariant="LearningJourneyViewModel.journey_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise JourneyInvariantViolation(
                "student_id must be a non-empty string",
                invariant="LearningJourneyViewModel.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.composed_at, datetime):
            raise JourneyInvariantViolation(
                "composed_at must be a datetime",
                invariant="LearningJourneyViewModel.composed_at.type",
            )
        expected = {
            "timeline": TimelineCard,
            "progress_overview": ProgressOverviewCard,
            "growth": GrowthCard,
            "consistency": ConsistencyCard,
            "study_habits": StudyHabitsCard,
            "milestones": MilestoneCard,
            "learning_trends": LearningTrendCard,
            "achievement_timeline": AchievementTimeline,
            "weekly_summary": WeeklySummary,
            "monthly_summary": MonthlySummary,
        }
        for name, expected_type in expected.items():
            value = getattr(self, name)
            if not isinstance(value, expected_type):
                raise JourneyInvariantViolation(
                    f"{name} must be a {expected_type.__name__}",
                    invariant=f"LearningJourneyViewModel.{name}.type",
                )
