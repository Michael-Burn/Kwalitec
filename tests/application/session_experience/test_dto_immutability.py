"""DTO immutability and regression for Session Experience."""

from __future__ import annotations

import pytest

from tests.application.session_experience.helpers import make_session_experience


def test_overview_snapshot_frozen():
    svc = make_session_experience()
    snap = svc.open_session("stu-1", session_id="sess-1")
    with pytest.raises(Exception):
        snap.objective = "mutated"  # type: ignore[misc]


def test_activity_snapshot_frozen():
    svc = make_session_experience()
    svc.open_session("stu-1", session_id="sess-1")
    svc.begin_session("stu-1", session_id="sess-1")
    snap = svc.get_activity("stu-1", session_id="sess-1")
    with pytest.raises(Exception):
        snap.question = "mutated"  # type: ignore[misc]


def test_progress_snapshot_frozen():
    svc = make_session_experience()
    svc.open_session("stu-1", session_id="sess-1")
    snap = svc.get_progress("stu-1", session_id="sess-1")
    with pytest.raises(Exception):
        snap.overall_progress = 0.99  # type: ignore[misc]


def test_reflection_snapshot_frozen():
    svc = make_session_experience()
    svc.open_session("stu-1", session_id="sess-1")
    snap = svc.get_reflection("stu-1", session_id="sess-1")
    with pytest.raises(Exception):
        snap.key_insight = "mutated"  # type: ignore[misc]


def test_completion_snapshot_frozen():
    svc = make_session_experience()
    svc.open_session("stu-1", session_id="sess-1")
    snap = svc.get_summary("stu-1", session_id="sess-1")
    with pytest.raises(Exception):
        snap.next_recommendation = "mutated"  # type: ignore[misc]


def test_regression_open_idempotent_same_session():
    svc = make_session_experience()
    first = svc.open_session("stu-1", session_id="sess-1")
    second = svc.get_overview("stu-1", session_id="sess-1")
    assert first.session_id == second.session_id
    assert first.objective == second.objective
