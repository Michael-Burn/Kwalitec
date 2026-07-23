"""Timeline composition tests for Learning Journey (XP-002)."""

from __future__ import annotations

from application.student_experience.progress import (
    LearningJourneyService,
    TimelineEventKind,
)
from tests.application.student_experience.progress.conftest import make_rich_inputs


def test_timeline_is_chronological(service: LearningJourneyService) -> None:
    timeline = service.build_timeline(make_rich_inputs())
    assert timeline.has_events is True
    stamps = [event.occurred_at for event in timeline.events]
    assert stamps == sorted(stamps)


def test_timeline_includes_mission_and_mastery_events(
    service: LearningJourneyService,
) -> None:
    timeline = service.build_timeline(make_rich_inputs())
    kinds = {event.kind for event in timeline.events}
    assert TimelineEventKind.MISSION_COMPLETED in kinds
    assert TimelineEventKind.MASTERY_IMPROVED in kinds
    assert TimelineEventKind.RECOMMENDATION_CHANGED in kinds
    assert TimelineEventKind.MISSION_SCHEDULED in kinds
    assert TimelineEventKind.CHECKPOINT_COMPLETED in kinds
    assert TimelineEventKind.COMPETENCY_STRENGTHENED in kinds


def test_timeline_messages_are_descriptive(
    service: LearningJourneyService,
) -> None:
    timeline = service.build_timeline(make_rich_inputs())
    for event in timeline.events:
        assert event.title
        assert event.message
        assert "because" not in event.message.lower()
        assert "MasteryAssessment" not in event.message
        assert "RecommendationSet" not in event.message
