"""Presentation matrix / volume tests for Session Experience."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.application.session_experience.dto.overview_snapshot import (
    BeginSessionActionSnapshot,
    OverviewSnapshot,
)
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.navigation import SURFACE_ENDPOINTS, build_session_steps
from app.presentation.session.view_models import overview_vm

TEMPLATE_ROOT = (
    Path(__file__).resolve().parents[3] / "app" / "templates" / "session"
)


@pytest.mark.parametrize("surface", list(SessionSurface))
def test_steps_mark_active_surface(surface):
    steps = build_session_steps(surface, session_id="sess-1")
    active = [s for s in steps if s.is_active]
    assert len(active) == 1
    assert active[0].surface == surface.value


@pytest.mark.parametrize("surface", list(SessionSurface))
def test_surface_endpoints_mapped(surface):
    assert surface in SURFACE_ENDPOINTS
    assert SURFACE_ENDPOINTS[surface].startswith("session.")


@pytest.mark.parametrize("minutes", range(0, 121, 5))
def test_overview_duration_labels(minutes):
    vm = overview_vm(
        OverviewSnapshot(
            experience_session_id="es-1",
            student_id="stu-1",
            session_id="sess-1",
            estimated_minutes=minutes,
            activity_count=1,
            begin_action=BeginSessionActionSnapshot(session_id="sess-1"),
        )
    )
    assert str(minutes) in vm.estimated_duration_label


@pytest.mark.parametrize("count", range(0, 16))
def test_overview_activity_count_labels(count):
    vm = overview_vm(
        OverviewSnapshot(
            experience_session_id="es-1",
            student_id="stu-1",
            session_id="sess-1",
            activity_count=count,
            begin_action=BeginSessionActionSnapshot(session_id="sess-1"),
        )
    )
    assert vm.activity_count_label


@pytest.mark.parametrize(
    "name",
    [
        "base.html",
        "overview.html",
        "activity.html",
        "reflection.html",
        "summary.html",
        "complete.html",
    ],
)
def test_templates_exist(name):
    assert (TEMPLATE_ROOT / name).is_file()


@pytest.mark.parametrize(
    "name",
    [
        "progress_bar.html",
        "activity_card.html",
        "question_card.html",
        "explanation_card.html",
        "reflection_card.html",
        "completion_card.html",
        "timer_card.html",
        "navigation.html",
    ],
)
def test_component_templates_exist(name):
    assert (TEMPLATE_ROOT / "components" / name).is_file()


@pytest.mark.parametrize("surface", list(SessionSurface))
@pytest.mark.parametrize("exam", ["CPA", "CFA", "ACCA", "Bar"])
def test_step_labels_stable_across_exams(surface, exam):
    steps = build_session_steps(surface, session_id=f"{exam}-sess")
    assert len(steps) == 5
    assert any(s.is_active for s in steps)
