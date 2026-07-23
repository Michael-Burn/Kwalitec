"""Snapshot tests for Learning Journey (XP-002)."""

from __future__ import annotations

from application.student_experience.progress import (
    JourneySnapshotId,
    LearningJourneyService,
)
from tests.application.student_experience.progress.conftest import (
    FakeExportProvider,
    make_rich_inputs,
)


def test_build_snapshot(service: LearningJourneyService) -> None:
    inputs = make_rich_inputs()
    journey = service.build_journey(inputs, journey_id="journey-snap")
    snapshot = service.build_snapshot(
        journey,
        snapshot_id=JourneySnapshotId("jsnap-001"),
        home_focus_headline=inputs.home_snapshot.focus_headline
        if inputs.home_snapshot
        else None,
    )
    assert snapshot.snapshot_id.value == "jsnap-001"
    assert snapshot.student_id == journey.student_id
    assert snapshot.timeline_event_count == len(journey.timeline.events)
    assert snapshot.milestone_count == len(journey.milestones.milestones)
    assert (
        snapshot.weekly_missions_completed
        == journey.growth.weekly_missions_completed
    )
    assert snapshot.home_focus_headline is not None


def test_export_journey_when_provider_configured() -> None:
    exporter = FakeExportProvider()
    service = LearningJourneyService(journey_export_provider=exporter)
    journey = service.build_journey(make_rich_inputs(), journey_id="journey-export")
    assert service.export_journey(journey) == "export:journey-export"


def test_export_journey_without_provider(service: LearningJourneyService) -> None:
    journey = service.build_journey(make_rich_inputs())
    assert service.export_journey(journey) is None
