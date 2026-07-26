"""Guided session phase transition tests (P2-MS004)."""

from __future__ import annotations

from app.application.unified_journey import (
    COMPLETION_NOT_STARTED,
    DailyMission,
    DayExperienceAssembler,
    JourneyEventType,
    MissionStartAction,
    SessionControl,
    SessionPhase,
    apply_session_control,
)


def _ready_day():
    mission = DailyMission(
        title="Revise equity",
        expected_outcome="Strengthen readiness",
        completion_status=COMPLETION_NOT_STARTED,
        start_action=MissionStartAction(enabled=True, label="Start"),
        metadata=(("availability", "available"),),
    )
    return DayExperienceAssembler().assemble(mission)


def test_start_ready_to_studying():
    day = _ready_day()
    result = apply_session_control(day, SessionControl.START)
    assert result.applied is True
    assert result.day_experience.current_phase is SessionPhase.STUDYING
    assert result.event is not None
    assert result.event.event_type is JourneyEventType.SESSION_STARTED


def test_finish_studying_to_wrapping_up():
    day = _ready_day()
    studying = apply_session_control(day, "start").day_experience
    result = apply_session_control(studying, SessionControl.FINISH)
    assert result.applied is True
    assert result.day_experience.current_phase is SessionPhase.WRAPPING_UP
    assert result.event is not None
    assert result.event.event_type is JourneyEventType.WRAP_UP_STARTED
    assert result.day_experience.reflection_available is True


def test_finish_wrapping_up_to_complete():
    day = _ready_day()
    studying = apply_session_control(day, "start").day_experience
    wrapping = apply_session_control(studying, "finish").day_experience
    result = apply_session_control(wrapping, "finish")
    assert result.applied is True
    assert result.day_experience.current_phase is SessionPhase.COMPLETE
    assert result.event is not None
    assert result.event.event_type is JourneyEventType.SESSION_COMPLETED


def test_resume_from_ready():
    day = _ready_day()
    result = apply_session_control(day, SessionControl.RESUME)
    assert result.applied is True
    assert result.day_experience.current_phase is SessionPhase.STUDYING
    assert result.event is not None
    assert result.event.event_type is JourneyEventType.SESSION_RESUMED


def test_start_rejected_when_not_ready():
    day = _ready_day()
    studying = apply_session_control(day, "start").day_experience
    result = apply_session_control(studying, "start")
    assert result.applied is False
    assert result.reason == "start_requires_ready"
    assert result.day_experience.current_phase is SessionPhase.STUDYING


def test_controls_do_not_mutate_mission():
    day = _ready_day()
    original_title = day.daily_mission.title
    result = apply_session_control(day, "start")
    assert result.day_experience.daily_mission.title == original_title
    assert day.current_phase is SessionPhase.READY  # original unchanged
