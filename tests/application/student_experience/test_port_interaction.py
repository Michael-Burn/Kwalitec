"""Port interaction tests."""

from __future__ import annotations

import pytest

from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    FakeJourneyPort,
    FakeMissionPort,
    FakeOrchestratorPort,
    FakeTwinPort,
    make_experience,
)


def test_home_calls_twin_and_adaptive():
    twin = FakeTwinPort()
    adaptive = FakeAdaptivePort()
    exp = make_experience(student_twin=twin, adaptive_decision=adaptive)
    exp.get_home("stu-1")
    assert any(c.startswith("learner:") for c in twin.calls)
    assert any(c.startswith("recommend:") for c in adaptive.calls)


def test_revision_calls_adaptive_only_for_options():
    adaptive = FakeAdaptivePort()
    exp = make_experience(adaptive_decision=adaptive)
    before = list(adaptive.calls)
    exp.get_revision("stu-1")
    assert any(c.startswith("revision:") for c in adaptive.calls[len(before):])


def test_journey_calls_journey_port():
    journey = FakeJourneyPort()
    exp = make_experience(learning_journey=journey)
    snap = exp.get_journey("stu-1")
    assert snap.progress_percent == 35


def test_mission_start_recorded():
    mission = FakeMissionPort()
    exp = make_experience(mission=mission)
    exp.start_session("stu-1", mission_id="m9", session_id="s9")
    assert mission.start_calls[-1] == ("stu-1", "m9", "s9")


def test_orchestrator_acknowledge():
    orch = FakeOrchestratorPort()
    orch.acknowledge_activity("stu-1", activity_id="act-1")
    assert orch.acks == [("stu-1", "act-1")]


@pytest.mark.parametrize("available", [True, False])
def test_diagnostics_port_availability(available):
    twin = FakeTwinPort(available=available)
    exp = make_experience(student_twin=twin)
    report = exp.diagnostics()
    assert report.port_availability["student_twin"] is available
