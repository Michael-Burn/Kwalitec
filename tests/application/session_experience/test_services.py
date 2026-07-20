"""Service and end-to-end workflow tests for Session Experience."""

from __future__ import annotations

import pytest

from app.application.session_experience.exceptions import (
    NavigationError,
    PortUnavailable,
)
from app.domain.session_experience.session_workspace import SessionSurface
from tests.application.session_experience.helpers import (
    FakeActivityEnginePort,
    FakeSessionRuntimePort,
    make_session_experience,
)


def test_open_overview_and_begin():
    svc = make_session_experience()
    overview = svc.open_session("stu-1", session_id="sess-1")
    assert overview.can_begin
    assert overview.objective
    begun = svc.begin_session("stu-1", session_id="sess-1")
    assert begun.status == "in_progress"
    ws = svc.registry.get_workspace_for_session("sess-1")
    assert ws is not None
    assert ws.is_on(SessionSurface.ACTIVITY)


def test_activity_submit_and_advance_to_reflection():
    runtime = FakeSessionRuntimePort()
    activity = FakeActivityEnginePort(activities=2)
    svc = make_session_experience(session_runtime=runtime, activity_engine=activity)
    svc.open_session("stu-1", session_id="sess-1")
    svc.begin_session("stu-1", session_id="sess-1")
    current = svc.get_activity("stu-1", session_id="sess-1")
    explained = svc.submit_response(
        "stu-1",
        session_id="sess-1",
        activity_id=current.activity_id,
        response="Significant influence indicates equity method.",
    )
    assert explained.has_explanation
    assert runtime.response_calls
    nxt = svc.advance_activity("stu-1", session_id="sess-1")
    assert nxt is not None
    svc.submit_response(
        "stu-1",
        session_id="sess-1",
        activity_id=nxt.activity_id,
        response="Associates use equity method.",
    )
    finished = svc.advance_activity("stu-1", session_id="sess-1")
    assert finished is None
    ws = svc.registry.get_workspace_for_session("sess-1")
    assert ws is not None
    assert ws.is_on(SessionSurface.REFLECTION)


def test_reflection_summary_complete_flow():
    runtime = FakeSessionRuntimePort()
    svc = make_session_experience(session_runtime=runtime)
    svc.open_session("stu-1", session_id="sess-1")
    svc.begin_session("stu-1", session_id="sess-1")
    reflection = svc.get_reflection("stu-1", session_id="sess-1")
    assert reflection.has_insight
    svc.continue_from_reflection("stu-1", session_id="sess-1")
    summary = svc.get_summary("stu-1", session_id="sess-1")
    assert summary.can_return_home
    assert summary.next_recommendation
    done = svc.complete_session("stu-1", session_id="sess-1")
    assert runtime.complete_calls == ["sess-1"]
    assert done.activities_completed == 3


def test_progress_projection():
    svc = make_session_experience()
    svc.open_session("stu-1", session_id="sess-1")
    progress = svc.get_progress("stu-1", session_id="sess-1")
    assert progress.activities_total == 3
    assert 0 <= progress.progress_percent <= 100


def test_navigate_rejects_skip():
    svc = make_session_experience()
    svc.open_session("stu-1", session_id="sess-1")
    with pytest.raises(NavigationError):
        svc.navigate("sess-1", SessionSurface.SUMMARY)


def test_runtime_unavailable():
    runtime = FakeSessionRuntimePort(available=False)
    svc = make_session_experience(session_runtime=runtime)
    with pytest.raises(PortUnavailable):
        svc.open_session("stu-1", session_id="sess-1")


def test_diagnostics_report():
    svc = make_session_experience()
    report = svc.diagnostics()
    assert "session_runtime" in report.registered_ports
    assert report.workspace_count == 0
    svc.open_session("stu-1", session_id="sess-1")
    report2 = svc.diagnostics()
    assert report2.workspace_count == 1


def test_get_flow_overview_surface():
    svc = make_session_experience()
    svc.open_session("stu-1", session_id="sess-1")
    flow = svc.get_flow("stu-1", session_id="sess-1")
    assert flow.surface == "overview"
    assert flow.overview is not None
    assert flow.next_surface == "activity"


def test_end_to_end_session_lifecycle():
    """Full linear session from open through return-home completion."""
    activity = FakeActivityEnginePort(activities=1)
    runtime = FakeSessionRuntimePort()
    svc = make_session_experience(activity_engine=activity, session_runtime=runtime)
    overview = svc.open_session("stu-1", session_id="sess-1")
    assert overview.can_begin
    svc.begin_session("stu-1", session_id="sess-1")
    act = svc.get_activity("stu-1", session_id="sess-1")
    svc.submit_response(
        "stu-1",
        session_id="sess-1",
        activity_id=act.activity_id,
        response="Equity method applies under significant influence.",
    )
    assert svc.advance_activity("stu-1", session_id="sess-1") is None
    svc.continue_from_reflection("stu-1", session_id="sess-1")
    completion = svc.complete_session("stu-1", session_id="sess-1")
    assert completion.can_return_home
    ws = svc.registry.get_workspace_for_session("sess-1")
    assert ws is not None
    assert ws.is_on(SessionSurface.COMPLETE)
