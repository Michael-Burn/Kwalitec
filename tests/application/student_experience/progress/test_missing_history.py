"""Missing history — graceful degradation (XP-002)."""

from __future__ import annotations

from application.student_experience.progress import (
    LearningJourneyService,
    StudyTimeBand,
    TrajectoryLabel,
    TrendDirection,
    WeekdayLabel,
)
from tests.application.student_experience.progress.conftest import make_empty_inputs


def test_journey_with_only_student_and_as_of(
    service: LearningJourneyService,
) -> None:
    journey = service.build_journey(make_empty_inputs())
    assert journey.timeline.has_events is False
    assert journey.progress_overview.trajectory in {
        TrajectoryLabel.UNKNOWN,
        TrajectoryLabel.JUST_STARTING,
    }
    assert journey.growth.has_growth_data is False
    assert journey.consistency.current_streak_days == 0
    assert journey.study_habits.preferred_study_time is StudyTimeBand.UNKNOWN
    assert journey.study_habits.most_productive_weekday is WeekdayLabel.UNKNOWN
    assert journey.milestones.has_milestones is False
    assert journey.learning_trends.mastery_trend is TrendDirection.UNKNOWN
    assert journey.weekly_summary.has_activity is False
    assert journey.monthly_summary.has_activity is False


def test_summaries_with_empty_history(service: LearningJourneyService) -> None:
    inputs = make_empty_inputs()
    growth = service.summarise_growth(inputs)
    consistency = service.summarise_consistency(inputs)
    habits = service.summarise_habits(inputs)
    assert growth.weekly_missions_completed == 0
    assert consistency.longest_streak_days == 0
    assert habits.average_session_duration_minutes == 0.0
    assert "will appear" in growth.weekly_growth_message.lower()
