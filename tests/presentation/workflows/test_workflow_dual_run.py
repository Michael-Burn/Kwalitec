"""Workflow 5 — Dual-run Dashboard ↔ Student Experience navigation."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from tests.presentation.workflows.helpers import (
    dual_run_flags,
    login_student,
    wire_session,
)


@pytest.fixture
def student_client(app, client, ctx, user):
    wire_session(app)
    login_student(client)
    return client


def test_dual_run_status_active_label():
    status = build_dual_run_status(flags=dual_run_flags())
    assert status.label == "dual-run-active"
    assert status.student_experience_enabled is True
    assert status.sole_runtime is False


def test_sole_runtime_label():
    status = build_dual_run_status(flags=dual_run_flags(SOLE_RUNTIME=True))
    assert status.label == "sole-runtime-v2"


def test_v1_primary_when_student_flag_off():
    status = build_dual_run_status(
        flags=dual_run_flags(ENABLE_STUDENT_EXPERIENCE=False)
    )
    assert status.label == "v1-primary"


def test_dashboard_dual_run_cta(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.dashboard.routes.resolve_v2_feature_flags",
        return_value=dual_run_flags(),
    ):
        response = client.get("/")
        # May redirect to dashboard.index
        if response.status_code in {302, 303}:
            response = client.get(response.headers["Location"])
        html = response.get_data(as_text=True)
        assert "Version 2 Learning Experience" in html or "/student/" in html


def test_student_back_to_dashboard_when_dual_run(student_client, app):
    with patch(
        "app.__init__._resolve_v2_flags_for_templates",
        return_value=dual_run_flags(),
    ):
        # Re-hit context via request; patch the resolve used by context processor.
        pass
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(),
    ):
        response = student_client.get("/student/")
        html = response.get_data(as_text=True)
        assert "Back to Dashboard" in html
        assert "/dashboard" in html or 'href="/"' in html or "dashboard.index" in html


def test_student_hides_back_link_in_sole_runtime(student_client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        html = student_client.get("/student/").get_data(as_text=True)
        assert "Back to Dashboard" not in html


def test_student_hides_back_link_when_flag_off(student_client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(ENABLE_STUDENT_EXPERIENCE=False),
    ):
        html = student_client.get("/student/").get_data(as_text=True)
        assert "Back to Dashboard" not in html


def test_round_trip_dashboard_student_dashboard(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(),
    ):
        dash = client.get("/dashboard/")
        assert dash.status_code == 200
        student = client.get("/student/")
        assert student.status_code == 200
        assert "Back to Dashboard" in student.get_data(as_text=True)
        back = client.get("/dashboard/")
        assert back.status_code == 200


def test_session_brand_returns_to_student_home(student_client):
    html = student_client.get("/session/sess-dual/overview").get_data(as_text=True)
    assert 'href="/student/"' in html or "/student/" in html


def test_root_redirect_not_forced_to_student_in_dual_run(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=False),
    ):
        # Dual-run keeps V1 dashboard as default home.
        response = client.get("/", follow_redirects=False)
        # Either dashboard or a redirect toward dashboard — not sole student.
        if response.status_code in {302, 303}:
            loc = response.headers.get("Location", "")
            assert "/student" not in loc or "dashboard" in loc.lower()
