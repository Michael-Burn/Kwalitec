"""Growth, consistency, and habits summary tests (XP-002)."""

from __future__ import annotations

from application.student_experience.progress import (
    LearningJourneyService,
    StudyTimeBand,
    TrendDirection,
    WeekdayLabel,
)
from tests.application.student_experience.progress.conftest import make_rich_inputs


def test_summarise_growth(service: LearningJourneyService) -> None:
    growth = service.summarise_growth(make_rich_inputs())
    assert growth.weekly_missions_completed >= 1
    assert growth.monthly_missions_completed >= growth.weekly_missions_completed
    assert growth.mastery_trend is TrendDirection.IMPROVING
    assert "week" in growth.weekly_growth_message.lower()
    assert "month" in growth.monthly_growth_message.lower()


def test_summarise_consistency(service: LearningJourneyService) -> None:
    consistency = service.summarise_consistency(make_rich_inputs())
    assert consistency.has_consistency_data is True
    assert consistency.longest_streak_days >= consistency.current_streak_days
    assert 0.0 <= consistency.average_completion_rate_percent <= 100.0
    assert consistency.average_weekly_sessions >= 0.0
    assert consistency.study_frequency_message
    assert consistency.consistency_message


def test_summarise_habits(service: LearningJourneyService) -> None:
    habits = service.summarise_habits(make_rich_inputs())
    assert habits.has_habits_data is True
    assert habits.preferred_study_time is not StudyTimeBand.UNKNOWN
    assert habits.most_productive_weekday is not WeekdayLabel.UNKNOWN
    assert habits.average_session_duration_minutes > 0.0
    assert 0.0 < habits.completion_reliability_percent <= 100.0
    assert "MissionExecution" not in habits.mission_completion_quality_message
