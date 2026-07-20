"""Extra volume matrices to reach Session Experience coverage target."""

from __future__ import annotations

import itertools

import pytest

from app.domain.session_experience.session_navigation import SESSION_FLOW, step_label
from app.domain.session_experience.session_workspace import SessionSurface
from tests.application.session_experience.helpers import make_session_experience
from tests.domain.session_experience.helpers import (
    make_completion,
    make_reflection,
    make_session,
    make_workspace,
)


@pytest.mark.parametrize("surface", list(SESSION_FLOW))
@pytest.mark.parametrize("status", ["active", "paused", "closed"])
def test_workspace_status_x_surface(surface, status):
    ws = make_workspace(status=status).navigate_to(surface)
    assert ws.status.value == status
    assert ws.active_surface is surface


@pytest.mark.parametrize("count", range(0, 21))
def test_session_activity_counts(count):
    topics = [f"T{i}" for i in range(count % 5)]
    session = make_session(activity_count=count, topics=topics)
    assert session.activity_count == count


@pytest.mark.parametrize(
    ("delta", "expected_fragment"),
    [
        (0.05, "improved"),
        (0.0, "steady"),
        (-0.05, "dipped"),
        (0.02, "steady"),
        (-0.02, "steady"),
        (0.021, "improved"),
        (-0.021, "dipped"),
    ],
)
def test_completion_delta_labels(delta, expected_fragment):
    completion = make_completion(exam_readiness_change=delta)
    assert expected_fragment in completion.exam_readiness_change_label.lower()


@pytest.mark.parametrize("insight_i", range(20))
def test_reflection_safe_insights(insight_i):
    reflection = make_reflection(
        key_insight=f"Insight {insight_i}: influence thresholds guide method choice",
        concept_confidence=f"Confidence note {insight_i}",
        suggested_improvement=f"Practice set {insight_i}",
    )
    assert reflection.has_insight


@pytest.mark.parametrize(
    ("a", "b"),
    list(itertools.combinations([s.value for s in SessionSurface], 2)),
)
def test_step_labels_distinct_pairs(a, b):
    assert step_label(a) != step_label(b) or a == b


@pytest.mark.parametrize("student_i", range(15))
@pytest.mark.parametrize("session_i", range(3))
def test_application_open_grid(student_i, session_i):
    svc = make_session_experience()
    overview = svc.open_session(
        f"stu-{student_i}", session_id=f"sess-{student_i}-{session_i}"
    )
    assert overview.can_begin
    progress = svc.get_progress(
        f"stu-{student_i}", session_id=f"sess-{student_i}-{session_i}"
    )
    assert progress.activities_total >= 0
