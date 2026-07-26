"""Unit tests — DailyMissionAssembler (P2-MS003)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.unified_journey import (
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    COMPLETION_NOT_STARTED,
    PRIORITY_HIGH,
    DailyMission,
    DailyMissionAssembler,
    JourneyContext,
    JourneyStage,
    empty_daily_mission,
    empty_journey_context,
)


@pytest.fixture
def assembler() -> DailyMissionAssembler:
    return DailyMissionAssembler()


def test_assemble_from_available_context(assembler: DailyMissionAssembler):
    context = JourneyContext(
        stage=JourneyStage.DAILY_MISSION,
        mission_title="Revise equity",
        mission_reason="High educational return for this topic.",
        estimated_duration="25 minutes",
        expected_outcome="Strengthen readiness",
        completion_state=COMPLETION_NOT_STARTED,
        urgency="high",
        cta_label="Start Today's Session",
        cta_enabled=True,
        endpoint="student.start_session",
        source="runtime_a",
        availability="available",
        unavailable_reason="",
    )
    mission = assembler.assemble(context)
    assert isinstance(mission, DailyMission)
    assert mission.title == "Revise equity"
    assert mission.reason == "High educational return for this topic."
    assert mission.estimated_duration == "25 minutes"
    assert mission.expected_outcome == "Strengthen readiness"
    assert mission.priority == PRIORITY_HIGH
    assert mission.completion_status == COMPLETION_NOT_STARTED
    assert mission.completion_status_label == "Not Started"
    assert mission.start_action.enabled is True
    assert mission.start_action.label == "Start Today's Session"
    assert "High educational return" in mission.mission_summary
    with pytest.raises(FrozenInstanceError):
        mission.title = "changed"  # type: ignore[misc]


def test_available_context_defaults_to_not_started(
    assembler: DailyMissionAssembler,
):
    context = JourneyContext(
        mission_title="Topic A",
        availability="available",
        source="runtime_a",
        unavailable_reason="",
        cta_enabled=True,
        endpoint="student.start_session",
    )
    mission = assembler.assemble(context)
    assert mission.completion_status == COMPLETION_NOT_STARTED


def test_completion_states_drive_cta(assembler: DailyMissionAssembler):
    in_progress = assembler.assemble(
        JourneyContext(
            mission_title="Topic A",
            completion_state=COMPLETION_IN_PROGRESS,
            cta_label="Continue",
            cta_enabled=True,
            endpoint="student.start_session",
            availability="available",
            source="runtime_a",
            unavailable_reason="",
        )
    )
    assert in_progress.is_in_progress
    assert in_progress.start_action.label == "Continue"
    assert in_progress.start_action.enabled is True

    completed = assembler.assemble(
        JourneyContext(
            mission_title="Topic A",
            completion_state=COMPLETION_COMPLETE,
            cta_enabled=True,
            endpoint="student.start_session",
            availability="available",
            source="runtime_a",
            unavailable_reason="",
        )
    )
    assert completed.is_completed
    assert completed.completion_status_label == "Completed"
    assert completed.start_action.enabled is False
    assert completed.start_action.label == "Mission complete"


def test_strips_subsystem_terminology(assembler: DailyMissionAssembler):
    context = JourneyContext(
        mission_title="Review from Digital Twin signal",
        mission_reason="Adaptive Engine suggests this next.",
        expected_outcome="Evidence Platform coverage improves.",
        availability="available",
        source="runtime_a",
        unavailable_reason="",
    )
    mission = assembler.assemble(context)
    assert "digital twin" not in mission.title.lower()
    assert "adaptive engine" not in mission.reason.lower()
    assert "evidence platform" not in mission.expected_outcome.lower()
    assert "learning profile" in mission.title.lower()
    assert "study guidance" in mission.reason.lower()


def test_placeholder_and_none(assembler: DailyMissionAssembler):
    assert assembler.assemble(None).title == empty_daily_mission().title
    placeholder = assembler.assemble(empty_journey_context())
    assert placeholder.title == "Today's primary mission"
    assert placeholder.start_action.enabled is False


def test_rejects_invalid_priority():
    with pytest.raises(ValueError):
        DailyMission(priority="urgent")
