"""RC-2026.07.29-03 — Student shell unification presentation regressions.

Authenticated Student surfaces render inside one Education Operating System
shell. Legacy workspace chrome and runtime shell switching are retired.
Controllers and engines are unchanged.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from tests.presentation.workflows.helpers import dual_run_flags, login_student

ROOT = Path(__file__).resolve().parents[2]

# Student journey + shared surfaces that must share one EOS shell.
STUDENT_SHELL_PATHS = (
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


@pytest.fixture
def dual_flags():
    return dual_run_flags(SOLE_RUNTIME=False)


def _html(client, path: str, flags) -> str:
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=flags,
    ):
        response = client.get(path, follow_redirects=True)
        assert response.status_code == 200, path
        return response.get_data(as_text=True)


def _assert_eos_shell(html: str) -> None:
    assert "student-shell" in html
    assert "student-topbar" in html
    assert 'aria-label="Student experience"' in html
    assert "student.css" in html
    assert 'id="app-sidebar"' not in html
    assert "app-shell" not in html
    assert "Sign out" in html
    assert 'aria-label="Appearance"' in html or "appearance-switcher" in html


@pytest.mark.parametrize("path", STUDENT_SHELL_PATHS)
def test_student_pages_use_eos_shell_under_sole(
    app, client, ctx, user, sole_flags, path
):
    login_student(client)
    _assert_eos_shell(_html(client, path, sole_flags))


@pytest.mark.parametrize("path", STUDENT_SHELL_PATHS)
def test_student_pages_use_eos_shell_without_sole(
    app, client, ctx, user, dual_flags, path
):
    """Chrome no longer depends on SOLE_RUNTIME (RC-2026.07.29-03)."""
    login_student(client)
    _assert_eos_shell(_html(client, path, dual_flags))


def test_choose_exam_keeps_form_controls(app, client, ctx, user, dual_flags):
    login_student(client)
    html = _html(client, "/study-plan/wizard/1", dual_flags)
    assert "wizard-container" in html or "wizard-form" in html or "ds-page" in html
    _assert_eos_shell(html)


def test_help_keeps_search(app, client, ctx, user, sole_flags):
    login_student(client)
    html = _html(client, "/alpha/help", sole_flags)
    assert "help-search" in html
    _assert_eos_shell(html)


def test_layout_router_always_selects_eos_shell():
    base = (ROOT / "app/templates/layouts/base.html").read_text(encoding="utf-8")
    assert "layouts/eos_student.html" in base
    assert "legacy_workspace" not in base
    assert "SOLE_RUNTIME" not in base
    eos = (ROOT / "app/templates/layouts/eos_student.html").read_text(
        encoding="utf-8"
    )
    assert "student-shell" in eos
    assert "student/components/navigation.html" in eos
    assert "auth.logout" in eos
    assert "appearance_switcher" in eos
    assert not (ROOT / "app/templates/layouts/legacy_workspace.html").exists()
    assert not (ROOT / "app/templates/partials/sidebar.html").exists()
    assert not (ROOT / "app/templates/partials/topnav.html").exists()


def test_session_base_extends_eos_shell():
    text = (ROOT / "app/templates/session/base.html").read_text(encoding="utf-8")
    assert 'extends "layouts/eos_student.html"' in text
    assert "ds-session-shell" not in text
    assert "design_system.css" in text


def test_student_base_extends_shared_eos_layout():
    text = (ROOT / "app/templates/student/base.html").read_text(encoding="utf-8")
    assert 'extends "layouts/eos_student.html"' in text


def test_no_blueprints_deleted():
    """Shell unification must not remove student or shared educational blueprints."""
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
