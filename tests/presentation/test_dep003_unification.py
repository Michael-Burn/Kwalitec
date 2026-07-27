"""DEP-003 — Student Experience Unification presentation regressions.

Under sole runtime, every student-facing shared blueprint must render inside
the Education Operating System shell (no legacy sidebar). Dual-run rollback
keeps the Learning Workspace chrome. Controllers and engines are unchanged.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from tests.presentation.workflows.helpers import dual_run_flags, login_student

ROOT = Path(__file__).resolve().parents[2]

# Student journey surfaces that must never show legacy chrome under sole.
SOLE_STUDENT_SHELL_PATHS = (
    "/student/",
    "/study-plan/",
    "/study-plan/wizard/1",
    "/alpha/help",
    "/alpha/onboarding",
    "/settings/profile",
    "/settings/preferences",
)


@pytest.fixture
def sole_flags():
    return dual_run_flags(SOLE_RUNTIME=True)


def _html_under_sole(client, path: str, sole_flags) -> str:
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=sole_flags,
    ):
        response = client.get(path, follow_redirects=True)
        assert response.status_code == 200, path
        return response.get_data(as_text=True)


@pytest.mark.parametrize("path", SOLE_STUDENT_SHELL_PATHS)
def test_sole_runtime_student_pages_use_eos_shell(
    app, client, ctx, user, sole_flags, path
):
    login_student(client)
    html = _html_under_sole(client, path, sole_flags)
    assert "student-shell" in html
    assert "student-topbar" in html
    assert 'aria-label="Student experience"' in html
    assert "student.css" in html
    assert 'id="app-sidebar"' not in html
    assert "app-shell" not in html or "student-shell" in html
    assert "Sign out" in html


def test_sole_runtime_study_plan_wizard_keeps_form_controls(
    app, client, ctx, user, sole_flags
):
    """Login continuity: wizard renders inside EOS without losing controls."""
    login_student(client)
    html = _html_under_sole(client, "/study-plan/wizard/1", sole_flags)
    assert "wizard-container" in html or "wizard-form" in html
    assert "student-shell" in html
    assert 'id="app-sidebar"' not in html


def test_sole_runtime_help_keeps_search(app, client, ctx, user, sole_flags):
    login_student(client)
    html = _html_under_sole(client, "/alpha/help", sole_flags)
    assert "help-search" in html
    assert "student-shell" in html


def test_dual_run_preserves_legacy_workspace_chrome(app, client, ctx, user):
    """Rollback path: SOLE_RUNTIME off keeps sidebar for shared pages."""
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=False),
    ):
        html = client.get("/study-plan/", follow_redirects=True).get_data(
            as_text=True
        )
    assert 'id="app-sidebar"' in html
    assert "app-shell" in html
    assert "student-shell" not in html


def test_layout_router_and_eos_shell_exist():
    base = (ROOT / "app/templates/layouts/base.html").read_text(encoding="utf-8")
    assert "layouts/eos_student.html" in base
    assert "layouts/legacy_workspace.html" in base
    assert "SOLE_RUNTIME" in base
    eos = (ROOT / "app/templates/layouts/eos_student.html").read_text(
        encoding="utf-8"
    )
    assert "student-shell" in eos
    assert "student/components/navigation.html" in eos
    assert "auth.logout" in eos
    legacy = (ROOT / "app/templates/layouts/legacy_workspace.html").read_text(
        encoding="utf-8"
    )
    assert "partials/sidebar.html" in legacy


def test_student_base_extends_shared_eos_layout():
    text = (ROOT / "app/templates/student/base.html").read_text(encoding="utf-8")
    assert 'extends "layouts/eos_student.html"' in text


def test_no_blueprints_deleted():
    """DEP-003 must not remove student or shared educational blueprints."""
    from app import create_app

    app = create_app()
    names = set(app.blueprints)
    for required in (
        "auth",
        "dashboard",
        "mission",
        "study_plan",
        "analytics",
        "settings",
        "alpha",
        "student",
        "session",
    ):
        assert required in names, required
