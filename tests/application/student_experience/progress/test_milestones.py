"""Milestone and trend projection tests (XP-002)."""

from __future__ import annotations

from application.student_experience.progress import (
    JourneyMilestoneKind,
    LearningJourneyService,
    TrendDirection,
)
from tests.application.student_experience.progress.conftest import make_rich_inputs


def test_milestones_projected_from_history(
    service: LearningJourneyService,
) -> None:
    journey = service.build_journey(make_rich_inputs())
    kinds = {item.kind for item in journey.milestones.milestones}
    assert JourneyMilestoneKind.FIRST_MISSION in kinds
    assert JourneyMilestoneKind.FIRST_REVISION_CYCLE in kinds
    assert JourneyMilestoneKind.COMPETENCY_MASTERED in kinds


def test_achievement_timeline_follows_milestones(
    service: LearningJourneyService,
) -> None:
    journey = service.build_journey(make_rich_inputs())
    stamped = [
        item for item in journey.milestones.milestones if item.reached_at is not None
    ]
    assert journey.achievement_timeline.has_items is True
    assert len(journey.achievement_timeline.items) == len(stamped)
    stamps = [item.earned_at for item in journey.achievement_timeline.items]
    assert stamps == sorted(stamps)


def test_learning_trends_are_historical_only(
    service: LearningJourneyService,
) -> None:
    journey = service.build_journey(make_rich_inputs())
    trends = journey.learning_trends
    assert trends.mastery_trend is TrendDirection.IMPROVING
    assert trends.confidence_trend is TrendDirection.IMPROVING
    assert trends.mastery_trend_message
    assert "forecast" not in trends.mastery_trend_message.lower()
    assert "predict" not in trends.mastery_trend_message.lower()
