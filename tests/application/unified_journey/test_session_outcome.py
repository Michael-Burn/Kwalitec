"""Unit tests — SessionOutcomeAssembler (P2-MS005)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.unified_journey import (
    COMPLETION_COMPLETE,
    COMPLETION_NOT_STARTED,
    DailyMission,
    DayExperienceAssembler,
    MissionStartAction,
    SessionOutcome,
    SessionOutcomeAssembler,
    SessionPhase,
    empty_session_outcome,
)


@pytest.fixture
def assembler() -> SessionOutcomeAssembler:
    return SessionOutcomeAssembler()


def _day(*, phase=SessionPhase.COMPLETE, completion=COMPLETION_COMPLETE):
    mission = DailyMission(
        title="Revise equity",
        expected_outcome="Strengthen readiness",
        completion_status=completion,
        start_action=MissionStartAction(enabled=False, label="Start"),
        metadata=(("availability", "available"),),
    )
    return DayExperienceAssembler().assemble(mission, phase=phase)


def test_assemble_session_outcome_after_complete(
    assembler: SessionOutcomeAssembler,
):
    outcome = assembler.assemble(_day())
    assert isinstance(outcome, SessionOutcome)
    assert outcome.mission_title == "Revise equity"
    assert outcome.completion_status == COMPLETION_COMPLETE
    assert outcome.reflection_available is True
    assert "completed" in outcome.summary_message.casefold()
    assert "reflect" in outcome.next_transition.casefold() or "tomorrow" in outcome.next_transition.casefold()
    assert outcome.upcoming_action
    with pytest.raises(FrozenInstanceError):
        outcome.mission_title = "changed"  # type: ignore[misc]


def test_wrapping_up_outcome(assembler: SessionOutcomeAssembler):
    outcome = assembler.assemble(_day(phase=SessionPhase.WRAPPING_UP))
    assert outcome.reflection_available is True
    assert "wrap" in outcome.summary_message.casefold()


def test_ready_phase_yields_empty(assembler: SessionOutcomeAssembler):
    mission = DailyMission(
        title="Revise equity",
        completion_status=COMPLETION_NOT_STARTED,
        metadata=(("availability", "available"),),
    )
    day = DayExperienceAssembler().assemble(mission, phase=SessionPhase.READY)
    outcome = assembler.assemble(day)
    assert outcome.reflection_available is False
    assert outcome.mission_title == ""


def test_no_educational_metrics(assembler: SessionOutcomeAssembler):
    outcome = assembler.assemble(_day())
    assert not hasattr(outcome, "mastery")
    assert not hasattr(outcome, "readiness")
    assert not hasattr(outcome, "evidence_id")


def test_placeholder():
    outcome = empty_session_outcome()
    assert outcome.reflection_available is False
