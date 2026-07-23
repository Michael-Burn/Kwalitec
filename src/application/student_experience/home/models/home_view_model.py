"""HomeViewModel — composed student home surface."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.home.errors import HomeInvariantViolation
from application.student_experience.home.ids import HomeId
from application.student_experience.home.models.achievement_card import AchievementCard
from application.student_experience.home.models.exam_readiness_card import (
    ExamReadinessCard,
)
from application.student_experience.home.models.learning_insight_card import (
    LearningInsightCard,
)
from application.student_experience.home.models.momentum_card import MomentumCard
from application.student_experience.home.models.progress_card import ProgressCard
from application.student_experience.home.models.quick_actions_card import (
    QuickActionsCard,
)
from application.student_experience.home.models.todays_focus_card import TodaysFocusCard
from application.student_experience.home.models.todays_study_session_card import (
    TodaysStudySessionCard,
)
from application.student_experience.home.models.upcoming_milestone_card import (
    UpcomingMilestoneCard,
)


@dataclass(frozen=True, slots=True)
class HomeViewModel:
    """Immutable composed student home experience.

    Answers student questions. Never exposes Education OS type names or
    internal architecture.
    """

    home_id: HomeId
    student_id: str
    composed_at: datetime
    todays_focus: TodaysFocusCard
    todays_study_session: TodaysStudySessionCard
    progress: ProgressCard
    momentum: MomentumCard
    upcoming_milestone: UpcomingMilestoneCard
    exam_readiness: ExamReadinessCard
    achievements: AchievementCard
    learning_insights: LearningInsightCard
    quick_actions: QuickActionsCard

    def __post_init__(self) -> None:
        if not isinstance(self.home_id, HomeId):
            raise HomeInvariantViolation(
                "home_id must be a HomeId",
                invariant="HomeViewModel.home_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise HomeInvariantViolation(
                "student_id must be a non-empty string",
                invariant="HomeViewModel.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.composed_at, datetime):
            raise HomeInvariantViolation(
                "composed_at must be a datetime",
                invariant="HomeViewModel.composed_at.type",
            )
        expected = {
            "todays_focus": TodaysFocusCard,
            "todays_study_session": TodaysStudySessionCard,
            "progress": ProgressCard,
            "momentum": MomentumCard,
            "upcoming_milestone": UpcomingMilestoneCard,
            "exam_readiness": ExamReadinessCard,
            "achievements": AchievementCard,
            "learning_insights": LearningInsightCard,
            "quick_actions": QuickActionsCard,
        }
        for name, expected_type in expected.items():
            value = getattr(self, name)
            if not isinstance(value, expected_type):
                raise HomeInvariantViolation(
                    f"{name} must be a {expected_type.__name__}",
                    invariant=f"HomeViewModel.{name}.type",
                )
