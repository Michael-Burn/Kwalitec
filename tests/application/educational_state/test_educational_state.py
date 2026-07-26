"""Unit tests for EducationalStateService (Phase 1 consolidation)."""

from __future__ import annotations

from app.application.educational_state import EducationalStateService
from app.application.student_experience.history_service import HistoryService
from app.application.student_experience.home_service import HomeService
from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    FakeJourneyPort,
    FakeMissionPort,
    FakeTwinPort,
)


def test_load_assembles_shared_state_once():
    twin = FakeTwinPort()
    adaptive = FakeAdaptivePort()
    mission = FakeMissionPort()
    journey = FakeJourneyPort()
    service = EducationalStateService(
        student_twin=twin,
        adaptive_decision=adaptive,
        mission=mission,
        learning_journey=journey,
    )
    first = service.load("stu-1")
    second = service.load("stu-1")
    assert first is second
    assert first.student_id == "stu-1"
    assert first.twin_available is True
    assert first.adaptive_available is True
    assert first.mission_available is True
    assert first.journey_available is True


def test_home_history_and_profile_share_cached_state():
    twin = FakeTwinPort()
    adaptive = FakeAdaptivePort()
    mission = FakeMissionPort()
    state = EducationalStateService(
        student_twin=twin,
        adaptive_decision=adaptive,
        mission=mission,
    )
    home = HomeService(
        student_twin=twin,
        adaptive_decision=adaptive,
        mission=mission,
        educational_state=state,
    )
    history = HistoryService(student_twin=twin, educational_state=state)
    from app.application.student_experience.profile_service import ProfileService

    profile = ProfileService(student_twin=twin, educational_state=state)
    home.home("stu-1")
    history.history("stu-1")
    profile.profile("stu-1")
    assert len(state._cache) == 1
    readiness_calls = [c for c in twin.calls if c.startswith("readiness:")]
    assert len(readiness_calls) == 1


def test_home_and_history_share_cached_state():
    twin = FakeTwinPort()
    adaptive = FakeAdaptivePort()
    mission = FakeMissionPort()
    state = EducationalStateService(
        student_twin=twin,
        adaptive_decision=adaptive,
        mission=mission,
    )
    home = HomeService(
        student_twin=twin,
        adaptive_decision=adaptive,
        mission=mission,
        educational_state=state,
    )
    history = HistoryService(student_twin=twin, educational_state=state)
    home.home("stu-1")
    history.history("stu-1")
    assert len(state._cache) == 1
    # Twin methods invoked once via EducationalState assembly, not per surface.
    readiness_calls = [c for c in twin.calls if c.startswith("readiness:")]
    assert len(readiness_calls) == 1
