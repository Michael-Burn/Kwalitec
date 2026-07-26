"""Unit tests — DayExperienceAssembler (P2-MS004)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.unified_journey import (
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    COMPLETION_NOT_STARTED,
    DailyMission,
    DayExperience,
    DayExperienceAssembler,
    MissionStartAction,
    SessionPhase,
    empty_day_experience,
)


@pytest.fixture
def assembler() -> DayExperienceAssembler:
    return DayExperienceAssembler()


def _mission(**overrides) -> DailyMission:
    base = dict(
        title="Revise equity",
        reason="High educational return",
        estimated_duration="25 minutes",
        expected_outcome="Strengthen readiness",
        completion_status=COMPLETION_NOT_STARTED,
        start_action=MissionStartAction(
            label="Start Today's Session",
            enabled=True,
            endpoint="student.start_session",
        ),
        mission_summary="High educational return",
        metadata=(("availability", "available"), ("source", "runtime_a")),
    )
    base.update(overrides)
    return DailyMission(**base)


def test_assemble_ready_day_experience(assembler: DayExperienceAssembler):
    day = assembler.assemble(_mission())
    assert isinstance(day, DayExperience)
    assert day.current_phase is SessionPhase.READY
    assert day.session_status == "Ready"
    assert day.mission_active is True
    assert day.reflection_available is False
    assert "Start" in day.upcoming_transition
    assert day.timeline.steps
    assert day.daily_mission.title == "Revise equity"
    with pytest.raises(FrozenInstanceError):
        day.session_status = "changed"  # type: ignore[misc]


def test_assemble_studying_from_in_progress(assembler: DayExperienceAssembler):
    day = assembler.assemble(
        _mission(completion_status=COMPLETION_IN_PROGRESS)
    )
    assert day.current_phase is SessionPhase.STUDYING
    assert day.session_status == "Studying"
    assert day.mission_active is True
    transition = day.upcoming_transition.casefold()
    assert "finish" in transition or "wrap" in transition


def test_assemble_complete_phase(assembler: DayExperienceAssembler):
    day = assembler.assemble(_mission(completion_status=COMPLETION_COMPLETE))
    assert day.current_phase is SessionPhase.COMPLETE
    assert day.mission_active is False
    assert day.reflection_available is True
    assert day.session_outcome is not None
    assert day.session_outcome.reflection_available is True
    assert day.reflection_state is not None
    assert day.reflection_active is True


def test_phase_override(assembler: DayExperienceAssembler):
    day = assembler.assemble(
        _mission(),
        phase=SessionPhase.WRAPPING_UP,
    )
    assert day.current_phase is SessionPhase.WRAPPING_UP
    assert day.reflection_available is True
    assert day.session_status == "Wrapping Up"
    assert day.session_outcome is not None
    assert day.reflection_state is None


def test_placeholder_not_mission_active(assembler: DayExperienceAssembler):
    day = empty_day_experience()
    assert day.mission_active is False
    assert day.current_phase is SessionPhase.READY
