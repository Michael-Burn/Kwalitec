"""Projection correctness across surfaces."""

from __future__ import annotations

import pytest

from app.domain.student_experience.recommendation_explanation import is_student_safe
from tests.application.student_experience.helpers import make_experience


@pytest.mark.parametrize("field", [
    "greeting",
    "examination_label",
    "exam_readiness_label",
    "recommendation_title",
    "recommendation_summary",
])
def test_home_fields_student_safe(field):
    home = make_experience().get_home("stu-1")
    assert is_student_safe(getattr(home, field))


def test_journey_hides_graph_jargon():
    journey = make_experience().get_journey("stu-1")
    blob = " ".join(journey.prerequisite_visibility)
    assert "graph" not in blob.lower()
    assert "node" not in blob.lower()
    assert "edge" not in blob.lower()


def test_history_strips_raw_events():
    from tests.application.student_experience.helpers import FakeTwinPort

    twin = FakeTwinPort()
    # inject raw events into insights
    original = twin.get_learning_insights

    def polluted(student_id):
        data = original(student_id)
        data = dict(data or {})
        data["events"] = [{"raw": True}]
        data["event_log"] = ["x"]
        return data

    twin.get_learning_insights = polluted  # type: ignore[method-assign]
    hist = make_experience(student_twin=twin).get_history("stu-1")
    assert hist.session_count >= 1
    assert not hasattr(hist, "events")


@pytest.mark.parametrize(
    "surface",
    ["home", "journey", "revision", "history", "profile"],
)
def test_dashboard_loads_requested_surface(surface):
    dash = make_experience().get_dashboard("stu-1", surface=surface)
    assert dash.active_surface == surface
    mapping = {
        "home": dash.home,
        "journey": dash.journey,
        "revision": dash.revision,
        "history": dash.history,
        "profile": dash.profile,
    }
    assert mapping[surface] is not None
