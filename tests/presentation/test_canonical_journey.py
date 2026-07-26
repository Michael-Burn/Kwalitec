"""EP-007.1 — Canonical student journey consolidation regression tests.

Covers: dual-home removal under sole runtime, login → Home entry,
session-duration single fact, session continuity, and dual-run
backwards compatibility when sole runtime is off.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.application.student_experience.session_duration import (
    resolve_planned_session_minutes,
)
from app.presentation.consolidation import (
    CANONICAL_HOME_ENDPOINT,
    LEGACY_HOME_ENDPOINT,
    canonical_home_endpoint,
    canonical_session_entry_endpoint,
)
from app.services.study_session_service import StudySessionService
from tests.presentation.workflows.helpers import dual_run_flags, login_student

# ---------------------------------------------------------------------------
# Duration model (REM-03 / one fact per day)
# ---------------------------------------------------------------------------


def test_resolve_planned_session_minutes_prefers_preferred():
    plan = SimpleNamespace(
        preferred_session_minutes=30,
        weekday_study_minutes=90,
        weekend_study_minutes=120,
    )
    assert resolve_planned_session_minutes(plan) == 30
    assert (
        resolve_planned_session_minutes(plan, mission_date=date(2026, 7, 25)) == 30
    )


def test_resolve_planned_session_minutes_falls_back_to_day_type():
    plan = SimpleNamespace(
        preferred_session_minutes=None,
        weekday_study_minutes=90,
        weekend_study_minutes=120,
    )
    saturday = date(2026, 7, 25)  # Saturday
    monday = date(2026, 7, 27)  # Monday
    assert resolve_planned_session_minutes(plan, mission_date=saturday) == 120
    assert resolve_planned_session_minutes(plan, mission_date=monday) == 90


def test_study_session_service_matches_canonical_duration():
    """Legacy mission duration must agree with preferred (fixes 30-vs-90)."""
    plan = SimpleNamespace(
        preferred_session_minutes=30,
        weekday_study_minutes=90,
        weekend_study_minutes=120,
    )
    mission = SimpleNamespace(mission_date=date.today())
    assert StudySessionService.estimated_minutes_for_mission(mission, plan) == 30


def test_resolve_planned_session_minutes_none_without_plan():
    assert resolve_planned_session_minutes(None) is None


# ---------------------------------------------------------------------------
# Canonical endpoint helpers
# ---------------------------------------------------------------------------


def test_canonical_home_endpoint_sole_runtime():
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        assert canonical_home_endpoint() == CANONICAL_HOME_ENDPOINT
        assert canonical_session_entry_endpoint() == CANONICAL_HOME_ENDPOINT


def test_canonical_home_endpoint_dual_run_compat():
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=False),
    ):
        assert canonical_home_endpoint() == LEGACY_HOME_ENDPOINT
        assert canonical_session_entry_endpoint() == "mission.missions"


# ---------------------------------------------------------------------------
# Dual-home removed under sole runtime (navigation)
# ---------------------------------------------------------------------------


def test_root_redirects_to_student_under_sole_runtime(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        response = client.get("/", follow_redirects=False)
        assert response.status_code in {302, 303}
        assert "/student" in response.headers.get("Location", "")


def test_legacy_shells_redirect_under_sole_runtime(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        for path in ("/dashboard/", "/missions/", "/analytics/"):
            response = client.get(path, follow_redirects=False)
            assert response.status_code in {302, 303}, path
            loc = response.headers.get("Location", "")
            assert "/student" in loc, f"{path} → {loc}"


def test_legacy_settings_index_redirects_under_sole_runtime(
    app, client, ctx, user
):
    """B9 (PX-003): the bare legacy Settings landing (`/settings/`, the
    'general' tab — version/support/diagnostics/about, fully duplicated by
    `alpha.help_centre`) must redirect to the canonical Settings surface
    under sole runtime, exactly like Dashboard/Mission/Analytics already do.
    """
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        response = client.get("/settings/", follow_redirects=False)
        assert response.status_code in {302, 303}
        assert "/student/profile" in response.headers.get("Location", "")


def test_legacy_settings_index_unchanged_under_dual_run(app, client, ctx, user):
    """Dual-run compatibility: legacy Settings still renders when sole
    runtime is off (matches Dashboard/Mission/Analytics' own guard)."""
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=False),
    ):
        response = client.get("/settings/", follow_redirects=False)
        assert response.status_code == 200


def test_settings_subpages_stay_reachable_under_sole_runtime(
    app, client, ctx, user
):
    """B9 scope: only the duplicate bare landing redirects. The functional
    sub-pages (profile/preferences/data/internal-alpha) are not yet migrated
    to Student Profile, so they must stay reachable — including from
    Profile's own "Open account settings" CTA (see profile_vm)."""
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        for path in (
            "/settings/profile",
            "/settings/preferences",
            "/settings/data",
            "/settings/internal-alpha",
        ):
            response = client.get(path, follow_redirects=False)
            assert response.status_code == 200, path


def test_login_lands_on_student_home_under_sole_runtime(
    app, client, ctx, user, study_plan
):
    """EP-007.1: no dual-home bounce — login → student.home directly."""
    del study_plan  # ensure active plan exists via fixture
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        response = client.post(
            "/auth/login",
            data={"email": user.email, "password": "password123"},
            follow_redirects=False,
        )
        assert response.status_code in {302, 303}
        assert "/student" in response.headers.get("Location", "")


def test_authenticated_login_get_redirects_to_canonical_home(
    app, client, ctx, user
):
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        response = client.get("/auth/login", follow_redirects=False)
        assert response.status_code in {302, 303}
        assert "/student" in response.headers.get("Location", "")


# ---------------------------------------------------------------------------
# Session continuity + journey consistency
# ---------------------------------------------------------------------------


def test_student_home_reachable_as_sole_entry(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        # Patch home load so missing Experience DI does not fail the route.
        with patch(
            "app.presentation.student.routes.load_page",
            return_value=_fake_home_page(),
        ):
            response = client.get("/student/", follow_redirects=False)
            assert response.status_code == 200
            html = response.get_data(as_text=True)
            assert "Back to Dashboard" not in html


def test_student_home_gates_first_time_student_into_onboarding(
    app, client, ctx, user
):
    """B8 (PX-003): under sole runtime, ``student.home`` is the canonical
    post-login landing surface, so it must apply the same first-time
    onboarding gate ``dashboard.index`` already applies — otherwise a brand
    new external student never sees onboarding at all."""
    user.alpha_onboarding_completed = False
    user.alpha_onboarding_skipped = False
    from app.extensions import db

    db.session.commit()
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        response = client.get("/student/", follow_redirects=False)
        assert response.status_code in {302, 303}
        assert response.headers.get("Location", "").endswith("/alpha/onboarding")


def test_student_home_skips_onboarding_gate_once_completed(
    app, client, ctx, user
):
    """Counterpart to the gate test — an onboarded student reaches Home
    directly, with no redirect loop back into onboarding."""
    assert user.alpha_onboarding_completed is True
    login_student(client)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        with patch(
            "app.presentation.student.routes.load_page",
            return_value=_fake_home_page(),
        ):
            response = client.get("/student/", follow_redirects=False)
            assert response.status_code == 200


def test_login_gates_onboarding_before_study_plan_wizard(app, client, ctx, user):
    """B8 (PX-003): "exactly one onboarding decision... regardless of entry
    path." A brand-new student with neither onboarding completed nor an
    active study plan previously landed on ``/study-plan/wizard/1`` straight
    from login — bypassing onboarding entirely until the wizard finished (or
    was abandoned). Login must now offer onboarding first, before the
    study-plan-wizard branch, so the very first screen is orientation, not a
    multi-step form."""
    user.alpha_onboarding_completed = False
    user.alpha_onboarding_skipped = False
    from app.extensions import db

    db.session.commit()
    response = client.post(
        "/auth/login",
        data={"email": "test@kwalitec.example", "password": "password123"},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert response.headers.get("Location", "").endswith("/alpha/onboarding")


def test_login_sends_onboarded_student_without_plan_to_wizard(app, client, ctx, user):
    """Counterpart: once onboarding is done, a student with no active plan
    still reaches the study-plan wizard from login (existing behaviour is
    preserved for the onboarding-complete case)."""
    assert user.alpha_onboarding_completed is True
    response = client.post(
        "/auth/login",
        data={"email": "test@kwalitec.example", "password": "password123"},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "/study-plan/wizard/1" in response.headers.get("Location", "")


def test_session_complete_returns_to_student_home():
    """Canonical completion lands on the single home endpoint."""
    # Contract: session finish destination is student.home (not dashboard).
    from app.presentation.session import routes as session_routes

    source = Path(session_routes.__file__).read_text(encoding="utf-8")
    assert "student.home" in source
    assert CANONICAL_HOME_ENDPOINT == "student.home"


def test_duration_consistency_across_legacy_and_canonical():
    """Same plan → same minutes on legacy StudySessionService and resolver."""
    plan = SimpleNamespace(
        preferred_session_minutes=45,
        weekday_study_minutes=90,
        weekend_study_minutes=120,
    )
    mission = SimpleNamespace(mission_date=date(2026, 7, 26))
    legacy = StudySessionService.estimated_minutes_for_mission(mission, plan)
    canonical = resolve_planned_session_minutes(
        plan, mission_date=mission.mission_date
    )
    assert legacy == canonical == 45


# ---------------------------------------------------------------------------
# Backwards compatibility (dual-run when sole runtime OFF)
# ---------------------------------------------------------------------------


def test_dual_run_preserves_dashboard_home_when_sole_off(app, client, ctx, user):
    login_student(client)
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=False),
    ), patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=False),
    ):
        response = client.get("/", follow_redirects=False)
        assert response.status_code in {302, 303}
        loc = response.headers.get("Location", "")
        assert "/dashboard" in loc
        # Legacy dashboard still renders (no forced sole redirect).
        dash = client.get("/dashboard/", follow_redirects=False)
        assert dash.status_code == 200 or dash.status_code in {302, 303}
        if dash.status_code in {302, 303}:
            # May redirect to onboarding — not to student solely because of flag.
            assert "/student" not in dash.headers.get("Location", "")


def test_login_lands_on_dashboard_under_dual_run(app, client, ctx, user, study_plan):
    del study_plan
    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=False),
    ):
        response = client.post(
            "/auth/login",
            data={"email": user.email, "password": "password123"},
            follow_redirects=False,
        )
        assert response.status_code in {302, 303}
        assert "/dashboard" in response.headers.get("Location", "")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fake_home_page():
    shell = MagicMock()
    shell.page_title = "Home"
    page = MagicMock()
    page.shell = shell
    page.home = None
    return page
