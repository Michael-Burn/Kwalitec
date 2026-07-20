"""Volume matrices for Learning Session Experience domain."""

from __future__ import annotations

import itertools

import pytest

from app.domain.session_experience.completion_projection import readiness_change_label
from app.domain.session_experience.session_navigation import (
    SESSION_FLOW,
    assert_linear_advance,
    flow_position,
    next_surface,
    previous_surface,
)
from app.domain.session_experience.session_workspace import (
    CANONICAL_SURFACES,
    SessionSurface,
)
from tests.domain.session_experience.helpers import (
    make_activity,
    make_progress,
    make_session,
    make_workspace,
)


@pytest.mark.parametrize(
    ("left", "right"),
    list(itertools.combinations(CANONICAL_SURFACES, 2)),
)
def test_surface_pairs_distinct(left, right):
    assert left is not right
    ws = make_workspace().navigate_to(left)
    assert ws.is_on(left)
    assert not ws.is_on(right)


@pytest.mark.parametrize("mask", range(32))
def test_surface_presence_mask(mask):
    selected = [s for i, s in enumerate(CANONICAL_SURFACES) if mask & (1 << i)]
    ws = make_workspace()
    for surface in selected:
        ws = ws.navigate_to(surface)
        assert ws.active_surface is surface


@pytest.mark.parametrize("surface", list(SessionSurface))
@pytest.mark.parametrize("topic", ["Equity", "Leases", "Tax", "Ethics", "Audit"])
def test_workspace_topic_labels(surface, topic):
    ws = make_workspace(topic_title=topic).navigate_to(surface)
    assert ws.topic_title == topic
    assert ws.active_surface is surface


@pytest.mark.parametrize("idx", range(len(SESSION_FLOW) - 1))
def test_linear_next_prev_roundtrip(idx):
    current = SESSION_FLOW[idx]
    nxt = next_surface(current)
    assert nxt is SESSION_FLOW[idx + 1]
    assert previous_surface(nxt) is current
    assert assert_linear_advance(current, nxt) is nxt


@pytest.mark.parametrize("completed", range(0, 11))
@pytest.mark.parametrize("remaining", range(0, 11))
def test_progress_grid(completed, remaining):
    progress = make_progress(
        activities_completed=completed,
        activities_remaining=remaining,
    )
    assert progress.activities_total == completed + remaining
    assert 0 <= progress.progress_percent <= 100


@pytest.mark.parametrize("delta_i", range(-10, 11))
def test_readiness_change_labels(delta_i):
    label = readiness_change_label(delta_i / 100)
    assert label in {
        "Exam readiness improved",
        "Exam readiness dipped slightly",
        "Exam readiness steady",
    }


@pytest.mark.parametrize("index", range(1, 9))
@pytest.mark.parametrize("total", range(1, 9))
def test_activity_index_matrix(index, total):
    if index > total:
        with pytest.raises(ValueError):
            make_activity(activity_index=index, activities_total=total)
    else:
        activity = make_activity(activity_index=index, activities_total=total)
        assert activity.activity_index == index
        assert activity.is_final_activity is (index == total)


@pytest.mark.parametrize("minutes", range(0, 121, 5))
def test_session_estimated_minutes(minutes):
    session = make_session(estimated_minutes=minutes, activity_count=minutes % 7)
    assert session.estimated_minutes == minutes


@pytest.mark.parametrize("surface", list(SESSION_FLOW))
def test_flow_position_bounds(surface):
    step, total = flow_position(surface)
    assert 1 <= step <= total
    assert total == len(SESSION_FLOW)
