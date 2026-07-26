"""Guided Reflection state transition tests (P2-MS005)."""

from __future__ import annotations

from app.application.unified_journey import (
    COMPLETION_COMPLETE,
    DailyMission,
    DayExperienceAssembler,
    JourneyEventType,
    MissionStartAction,
    ReflectionControl,
    ReflectionState,
    SessionPhase,
    apply_reflection_control,
    apply_session_control,
)


def _complete_day():
    mission = DailyMission(
        title="Revise equity",
        expected_outcome="Strengthen readiness",
        completion_status=COMPLETION_COMPLETE,
        start_action=MissionStartAction(enabled=False, label="Start"),
        metadata=(("availability", "available"),),
    )
    return DayExperienceAssembler().assemble(
        mission,
        phase=SessionPhase.COMPLETE,
    )


def test_complete_day_unlocks_reflection_available():
    day = _complete_day()
    assert day.session_outcome is not None
    assert day.session_outcome.reflection_available is True
    assert day.reflection_state is ReflectionState.AVAILABLE
    assert day.reflection_active is True
    assert day.reflection_available is True


def test_start_available_to_in_progress():
    day = _complete_day()
    result = apply_reflection_control(day, ReflectionControl.START)
    assert result.applied is True
    assert result.day_experience.reflection_state is ReflectionState.IN_PROGRESS
    assert result.event is not None
    assert result.event.event_type is JourneyEventType.REFLECTION_STARTED


def test_complete_reflection():
    day = _complete_day()
    started = apply_reflection_control(day, "start").day_experience
    result = apply_reflection_control(started, ReflectionControl.COMPLETE)
    assert result.applied is True
    assert result.day_experience.reflection_state is ReflectionState.COMPLETED
    assert result.event is not None
    assert result.event.event_type is JourneyEventType.REFLECTION_COMPLETED
    assert result.day_experience.reflection_active is False


def test_skip_from_available():
    day = _complete_day()
    result = apply_reflection_control(day, ReflectionControl.SKIP)
    assert result.applied is True
    assert result.day_experience.reflection_state is ReflectionState.SKIPPED
    assert result.event is not None
    assert result.event.event_type is JourneyEventType.REFLECTION_SKIPPED
    assert result.day_experience.reflection_active is False


def test_finish_session_unlocks_reflection():
    mission = DailyMission(
        title="Revise equity",
        completion_status="not_started",
        start_action=MissionStartAction(enabled=True, label="Start"),
        metadata=(("availability", "available"),),
    )
    ready = DayExperienceAssembler().assemble(mission)
    studying = apply_session_control(ready, "start").day_experience
    wrapping = apply_session_control(studying, "finish").day_experience
    complete = apply_session_control(wrapping, "finish").day_experience
    assert complete.current_phase is SessionPhase.COMPLETE
    assert complete.reflection_state is ReflectionState.AVAILABLE
    assert complete.session_outcome is not None
    assert complete.timeline.active_step is not None
    assert complete.timeline.active_step.key == "reflection"


def test_reflection_rejected_when_not_available():
    mission = DailyMission(
        title="Revise equity",
        completion_status="not_started",
        metadata=(("availability", "available"),),
    )
    ready = DayExperienceAssembler().assemble(mission)
    result = apply_reflection_control(ready, "start")
    assert result.applied is False
    assert result.reason == "reflection_not_available"
