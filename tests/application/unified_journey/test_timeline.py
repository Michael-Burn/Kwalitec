"""Experience Timeline tests (P2-MS003)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.unified_journey import (
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    COMPLETION_NOT_STARTED,
    TIMELINE_STATUS_COMPLETE,
    TIMELINE_STATUS_CURRENT,
    TIMELINE_STATUS_PENDING,
    DailyMission,
    ExperienceTimeline,
    JourneyStage,
    build_experience_timeline,
    empty_experience_timeline,
    timeline_from_daily_mission,
)


def test_today_timeline_order():
    timeline = empty_experience_timeline()
    assert [step.key for step in timeline.steps] == [
        "mission",
        "study_session",
        "reflection",
        "complete",
    ]
    assert [step.label for step in timeline.steps] == [
        "Mission",
        "Study Session",
        "Reflection",
        "Complete",
    ]
    assert timeline.steps[0].status == TIMELINE_STATUS_CURRENT
    assert timeline.steps[1].status == TIMELINE_STATUS_PENDING


def test_in_progress_highlights_study_session():
    timeline = build_experience_timeline(
        completion_status=COMPLETION_IN_PROGRESS
    )
    assert timeline.steps[0].status == TIMELINE_STATUS_COMPLETE
    assert timeline.steps[1].status == TIMELINE_STATUS_CURRENT
    assert timeline.active_step is not None
    assert timeline.active_step.key == "study_session"


def test_completed_marks_final_step():
    timeline = build_experience_timeline(completion_status=COMPLETION_COMPLETE)
    assert all(
        step.status == TIMELINE_STATUS_COMPLETE for step in timeline.steps[:-1]
    )
    assert timeline.steps[-1].status == TIMELINE_STATUS_COMPLETE
    assert timeline.active_index == 3


def test_timeline_from_daily_mission():
    mission = DailyMission(
        title="Topic",
        completion_status=COMPLETION_NOT_STARTED,
        stage=JourneyStage.DAILY_MISSION,
    )
    timeline = timeline_from_daily_mission(mission)
    assert timeline.steps[0].is_current
    with pytest.raises(FrozenInstanceError):
        timeline.active_index = 2  # type: ignore[misc]


def test_rejects_invalid_step_status():
    from app.application.unified_journey import TimelineStep

    with pytest.raises(ValueError):
        TimelineStep(key="mission", label="Mission", status="skipped")


def test_timeline_is_presentation_only():
    timeline = build_experience_timeline(
        completion_status=COMPLETION_NOT_STARTED
    )
    assert isinstance(timeline, ExperienceTimeline)
    assert timeline.contract_version.startswith("p2.ms005")
    # No educational fields.
    assert not hasattr(timeline, "mastery")
    assert not hasattr(timeline, "readiness")
