"""Volume matrices for Learning Session Experience application layer."""

from __future__ import annotations

import pytest

from app.domain.session_experience.session_workspace import SessionSurface
from tests.application.session_experience.helpers import (
    FakeActivityEnginePort,
    FakeAdaptivePort,
    FakeMissionPort,
    FakeSessionRuntimePort,
    FakeTwinPort,
    make_session_experience,
)


@pytest.mark.parametrize("mask", range(32))
def test_port_availability_mask(mask):
    runtime_on = bool(mask & 1)
    activity_on = bool(mask & 2)
    mission_on = bool(mask & 4)
    twin_on = bool(mask & 8)
    adaptive_on = bool(mask & 16)
    svc = make_session_experience(
        session_runtime=FakeSessionRuntimePort(available=runtime_on),
        activity_engine=FakeActivityEnginePort(available=activity_on),
        mission=FakeMissionPort(available=mission_on),
        student_twin=FakeTwinPort(available=twin_on),
        adaptive_decision=FakeAdaptivePort(available=adaptive_on),
    )
    report = svc.diagnostics()
    assert report.port_availability["session_runtime"] is runtime_on
    assert report.port_availability["activity_engine"] is activity_on
    assert report.port_availability["mission"] is mission_on
    assert report.port_availability["student_twin"] is twin_on
    assert report.port_availability["adaptive_decision"] is adaptive_on


@pytest.mark.parametrize("activities", range(1, 9))
def test_activity_counts_through_sequence(activities):
    engine = FakeActivityEnginePort(activities=activities)
    svc = make_session_experience(activity_engine=engine)
    svc.open_session("stu-1", session_id="sess-1")
    svc.begin_session("stu-1", session_id="sess-1")
    seen = 0
    while True:
        current = svc.get_activity("stu-1", session_id="sess-1")
        svc.submit_response(
            "stu-1",
            session_id="sess-1",
            activity_id=current.activity_id,
            response=f"answer-{seen}",
        )
        seen += 1
        nxt = svc.advance_activity("stu-1", session_id="sess-1")
        if nxt is None:
            break
    assert seen == activities
    ws = svc.registry.get_workspace_for_session("sess-1")
    assert ws is not None
    assert ws.is_on(SessionSurface.REFLECTION)


@pytest.mark.parametrize("student_i", range(20))
def test_multi_student_workspaces(student_i):
    svc = make_session_experience()
    sid = f"stu-{student_i}"
    sess = f"sess-{student_i}"
    overview = svc.open_session(sid, session_id=sess)
    assert overview.student_id == sid
    assert overview.session_id == sess


@pytest.mark.parametrize("step", range(4))
def test_linear_navigate_steps(step):
    surfaces = [
        SessionSurface.OVERVIEW,
        SessionSurface.ACTIVITY,
        SessionSurface.REFLECTION,
        SessionSurface.SUMMARY,
        SessionSurface.COMPLETE,
    ]
    svc = make_session_experience()
    svc.open_session("stu-1", session_id="sess-1")
    ws = svc.registry.get_workspace_for_session("sess-1")
    assert ws is not None
    for idx in range(step):
        ws = ws.navigate_to(surfaces[idx + 1])
        svc.registry.put_workspace(ws)
    target = surfaces[step + 1]
    updated = svc.navigate("sess-1", target)
    assert updated.active_surface is target


@pytest.mark.parametrize("progress_i", range(0, 101, 5))
def test_progress_percent_stable(progress_i):
    runtime = FakeSessionRuntimePort()

    def snapshot(student_id, *, session_id):
        return {
            "activities_completed": progress_i,
            "activities_remaining": 100 - progress_i,
            "activities_total": 100,
            "overall_progress": progress_i / 100,
            "current_topic": "Equity",
            "estimated_remaining_minutes": max(0, 100 - progress_i),
        }

    runtime.get_runtime_snapshot = snapshot  # type: ignore[method-assign]
    svc = make_session_experience(session_runtime=runtime)
    svc.open_session("stu-1", session_id="sess-1")
    progress = svc.get_progress("stu-1", session_id="sess-1")
    assert progress.progress_percent == progress_i
