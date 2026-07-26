"""Workflow 5 — Dual-run Dashboard ↔ Student Experience navigation.

Phase 1 consolidation: student-visible Version 2 / competing-experience CTAs
are removed. Dual-run remains via flags and direct URLs; sole runtime redirects
legacy surfaces to the canonical Student Experience.
"""

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


def test_dashboard_has_no_version_terminology(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.dashboard.routes.resolve_v2_feature_flags",
        return_value=dual_run_flags(),
    ):
        response = client.get("/")
        if response.status_code in {302, 303}:
            response = client.get(response.headers["Location"])
        html = response.get_data(as_text=True)
        assert "Version 2" not in html
        assert "Learning Experience V2" not in html
        assert "Alternative Experience" not in html
        assert "Beta Experience" not in html


def test_student_has_no_competing_experience_cta(student_client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(),
    ):
        html = student_client.get("/student/").get_data(as_text=True)
        assert "Back to Dashboard" not in html
        assert "Version 2" not in html


def test_student_hides_back_link_in_sole_runtime(student_client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        html = student_client.get("/student/").get_data(as_text=True)
        assert "Back to Dashboard" not in html


def test_legacy_dashboard_redirects_under_sole_runtime(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        response = client.get("/dashboard/", follow_redirects=False)
        assert response.status_code in {302, 303}
        assert "/student" in response.headers.get("Location", "")


def test_legacy_analytics_redirects_under_sole_runtime(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        response = client.get("/analytics/", follow_redirects=False)
        assert response.status_code in {302, 303}
        assert "/student/history" in response.headers.get("Location", "")


def test_legacy_missions_redirect_under_sole_runtime(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        response = client.get("/missions/", follow_redirects=False)
        assert response.status_code in {302, 303}
        assert "/student" in response.headers.get("Location", "")


def test_nested_legacy_session_redirects_under_sole_runtime(app, client, ctx, user):
    """V2-023: nested LXP session chrome must not remain live under sole runtime."""
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        for path in (
            "/missions/1/session",
            "/missions/1/session/finish",
            "/missions/1/session/recorded",
            "/missions/review/1",
        ):
            response = client.get(path, follow_redirects=False)
            assert response.status_code in {302, 303}, path
            assert "/student" in response.headers.get("Location", ""), path


def test_dual_run_keeps_legacy_dashboard_reachable(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(),
    ):
        dash = client.get("/dashboard/")
        assert dash.status_code == 200
        student = client.get("/student/")
        assert student.status_code == 200


def test_session_brand_returns_to_student_home(student_client):
    html = student_client.get("/session/sess-dual/overview").get_data(as_text=True)
    assert 'href="/student/"' in html or "/student/" in html


def test_root_redirect_not_forced_to_student_in_dual_run(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=False),
    ):
        response = client.get("/", follow_redirects=False)
        if response.status_code in {302, 303}:
            loc = response.headers.get("Location", "")
            assert "/student" not in loc or "dashboard" in loc.lower()
