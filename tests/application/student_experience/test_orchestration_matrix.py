"""Orchestration / regression / volume matrices."""

from __future__ import annotations

import pytest

from app.domain.student_experience.experience_workspace import ExperienceSurface
from app.domain.student_experience.recommendation_explanation import is_student_safe
from tests.application.student_experience.helpers import make_experience

SURFACES = list(ExperienceSurface)


@pytest.mark.parametrize("a", SURFACES)
@pytest.mark.parametrize("b", SURFACES)
def test_navigate_pairs(a, b):
    exp = make_experience()
    ws = exp.open_workspace("stu-1")
    exp.navigate(ws.workspace_id, a)
    updated = exp.navigate(ws.workspace_id, b)
    assert updated.active_surface is b


@pytest.mark.parametrize("i", range(25))
def test_repeated_home_idempotent(i):
    exp = make_experience()
    first = exp.get_home("stu-1")
    second = exp.get_home("stu-1")
    assert first.recommendation_title == second.recommendation_title
    assert first.exam_readiness == second.exam_readiness


@pytest.mark.parametrize("i", range(10))
def test_dashboard_port_availability_shape(i):
    dash = make_experience().get_dashboard("stu-1")
    names = [n for n, _ in dash.port_availability]
    assert "student_twin" in names
    assert "adaptive_decision" in names


FORBIDDEN = (
    "digital twin",
    "adaptive decision",
    "learning orchestrator",
    "mission engine",
    "readiness score",
)


@pytest.mark.parametrize("surface", SURFACES)
def test_surface_copy_student_safe(surface):
    dash = make_experience().get_dashboard(
        "stu-1", surface=surface, include_all_surfaces=True
    )
    chunks = [dash.learning_activity_status]
    if dash.home:
        chunks.extend(
            [
                dash.home.greeting,
                dash.home.recommendation_title,
                dash.home.recommendation_summary,
            ]
        )
    if dash.revision and dash.revision.primary:
        chunks.append(dash.revision.primary.topic_title)
        chunks.append(dash.revision.primary.expected_benefit)
    if dash.journey and dash.journey.current_topic:
        chunks.append(dash.journey.current_topic.title)
    blob = " ".join(chunks).lower()
    for term in FORBIDDEN:
        assert term not in blob
    assert is_student_safe(" ".join(chunks))
