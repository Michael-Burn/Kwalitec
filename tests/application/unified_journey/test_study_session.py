"""Unit tests — StudySessionAssembler (P2-MS004)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.unified_journey import (
    COMPLETION_IN_PROGRESS,
    COMPLETION_NOT_STARTED,
    DailyMission,
    DayExperienceAssembler,
    MissionStartAction,
    SessionPhase,
    StudySession,
    StudySessionAssembler,
    empty_study_session,
)


@pytest.fixture
def assembler() -> StudySessionAssembler:
    return StudySessionAssembler()


def _day(*, completion: str = COMPLETION_NOT_STARTED, phase=None):
    mission = DailyMission(
        title="Revise equity",
        reason="High educational return for this topic.",
        estimated_duration="25 minutes",
        expected_outcome="Strengthen readiness",
        completion_status=completion,
        start_action=MissionStartAction(enabled=True, label="Start"),
        mission_summary="High educational return",
        metadata=(("availability", "available"),),
    )
    return DayExperienceAssembler().assemble(mission, phase=phase)


def test_assemble_study_session_from_day(assembler: StudySessionAssembler):
    session = assembler.assemble(_day())
    assert isinstance(session, StudySession)
    assert session.mission_title == "Revise equity"
    assert session.learning_objective == "Strengthen readiness"
    assert session.estimated_duration == "25 minutes"
    assert session.current_phase is SessionPhase.READY
    assert session.elapsed_state == "not_started"
    assert session.start_time == ""
    assert session.completion_state == COMPLETION_NOT_STARTED
    assert "Start" in session.next_step
    with pytest.raises(FrozenInstanceError):
        session.mission_title = "changed"  # type: ignore[misc]


def test_studying_phase_presentation_fields(assembler: StudySessionAssembler):
    session = assembler.assemble(
        _day(completion=COMPLETION_IN_PROGRESS)
    )
    assert session.current_phase is SessionPhase.STUDYING
    assert session.elapsed_state == "in_progress"
    assert session.start_time == "Session in progress"
    assert session.completion_state == COMPLETION_IN_PROGRESS
    assert session.is_studying


def test_wrapping_up_and_complete(assembler: StudySessionAssembler):
    wrapping = assembler.assemble(_day(phase=SessionPhase.WRAPPING_UP))
    assert wrapping.is_wrapping_up
    assert wrapping.elapsed_state == "in_progress"
    assert wrapping.start_time == "Session wrapping up"

    done = assembler.assemble(_day(phase=SessionPhase.COMPLETE))
    assert done.is_complete
    assert done.elapsed_state == "ended"
    assert done.completion_state == "complete"


def test_softens_subsystem_terms(assembler: StudySessionAssembler):
    mission = DailyMission(
        title="Topic",
        expected_outcome="Follow adaptive recommendation from Runtime A",
        completion_status=COMPLETION_NOT_STARTED,
        metadata=(("availability", "available"),),
    )
    day = DayExperienceAssembler().assemble(mission)
    session = assembler.assemble(day)
    assert "Runtime A" not in session.learning_objective
    assert "adaptive recommendation" not in session.learning_objective.casefold()


def test_placeholder(assembler: StudySessionAssembler):
    session = empty_study_session()
    assert session.mission_title == "Today's Mission"
    assert session.current_phase is SessionPhase.READY
