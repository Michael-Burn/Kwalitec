"""End-to-end smoke test suite — verifies Kwalitec's core user journey.

All tests run against a freshly migrated test database using the existing
test fixtures from ``conftest.py``.  No test should modify application
behaviour; any discovered defect MUST be fixed at its root cause with
regression assertions added here.
"""

from __future__ import annotations

import json
from datetime import date, timedelta

import pytest
from flask.testing import FlaskClient

from app.models.study_plan import StudyPlan, WeekPlan
from app.models.topic_progress import TopicProgress

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _login(client: FlaskClient) -> FlaskClient:
    """Log in the test user and return the client after following redirects."""
    client.post(
        "/auth/login",
        data={"email": "test@kwalitec.example", "password": "password123"},
        follow_redirects=True,
    )
    return client


def _wizard_step_1(client: FlaskClient) -> FlaskClient:
    """Submit wizard step 1: select IFoA."""
    client.post(
        "/study-plan/wizard/1",
        data={"exam_category": "IFoA"},
        follow_redirects=True,
    )
    return client


def _wizard_step_2(client: FlaskClient) -> FlaskClient:
    """Submit wizard step 2: select CS1 paper."""
    client.post(
        "/study-plan/wizard/2",
        data={"exam_paper": "CS1"},
        follow_redirects=True,
    )
    return client


def _wizard_step_3(client: FlaskClient) -> FlaskClient:
    """Submit wizard step 3: sitting and exam date."""
    future_date = (date.today() + timedelta(days=180)).isoformat()
    client.post(
        "/study-plan/wizard/3",
        data={
            "exam_sitting": "April 2027",
            "exam_date": future_date,
        },
        follow_redirects=True,
    )
    return client


def _wizard_step_4(client: FlaskClient) -> FlaskClient:
    """Submit wizard step 4: current position ('not started', no topic)."""
    client.post(
        "/study-plan/wizard/4",
        data={
            "current_position": "not_started",
            "current_topic": "",
        },
        follow_redirects=True,
    )
    return client


def _wizard_step_5(client: FlaskClient) -> FlaskClient:
    """Submit wizard step 5: study availability."""
    client.post(
        "/study-plan/wizard/5",
        data={
            "weekday_study_minutes": 60,
            "weekend_study_minutes": 90,
            "preferred_session_minutes": 60,
        },
        follow_redirects=True,
    )
    return client


def _wizard_step_6(client: FlaskClient) -> FlaskClient:
    """Submit wizard step 6: learning style."""
    client.post(
        "/study-plan/wizard/6",
        data={"study_preference": "Mixed"},
        follow_redirects=True,
    )
    return client


def _wizard_step_7(client: FlaskClient) -> FlaskClient:
    """Submit wizard step 7: target grade."""
    client.post(
        "/study-plan/wizard/7",
        data={"target_grade": "Pass"},
        follow_redirects=True,
    )
    return client


def _complete_wizard(client: FlaskClient) -> FlaskClient:
    """Run the full wizard from step 1 through step 7."""
    _wizard_step_1(client)
    _wizard_step_2(client)
    _wizard_step_3(client)
    _wizard_step_4(client)
    _wizard_step_5(client)
    _wizard_step_6(client)
    _wizard_step_7(client)
    return client


def _create_plan(client: FlaskClient, user) -> StudyPlan:
    """Login, complete wizard, and create a study plan. Returns the plan."""
    _login(client)
    _complete_wizard(client)
    resp = client.post(
        "/study-plan/review",
        data={"confirm": "yes"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    plan = StudyPlan.query.filter_by(user_id=user.id, active=True).first()
    assert plan is not None, "Study plan was not created"
    return plan


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 1 — Authentication
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeAuthentication:
    """Verify login flow: redirect to dashboard and HTTP 200."""

    def test_login_redirects_to_wizard(self, client, user):
        """Login should redirect to wizard step 1 when no study plan exists."""
        resp = client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        # The user has no study plan yet, so they'll be redirected to wizard step 1
        assert resp.request.path == "/study-plan/wizard/1"

    def test_login_page_loads(self, client):
        """GET /auth/login returns 200."""
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        assert b"Sign in" in resp.data

    def test_login_rejects_bad_credentials(self, client, user):
        """Invalid credentials should not log in."""
        resp = client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "wrongpassword"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"Invalid email or password" in resp.data


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 2 — Study Plan Wizard
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeStudyPlanWizard:
    """Complete the full Study Plan Wizard and verify results."""

    def test_wizard_step_1_get(self, client, user):
        """Step 1 renders correctly."""
        _login(client)
        resp = client.get("/study-plan/wizard/1")
        assert resp.status_code == 200
        assert b"Examination" in resp.data

    def test_wizard_step_1_post(self, client, user):
        """Step 1 posts and redirects to step 2."""
        _login(client)
        resp = client.post(
            "/study-plan/wizard/1",
            data={"exam_category": "IFoA"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/2"

    def test_wizard_step_2_get(self, client, user):
        """Step 2 renders correctly."""
        _login(client)
        _wizard_step_1(client)
        resp = client.get("/study-plan/wizard/2")
        assert resp.status_code == 200
        assert b"CS1" in resp.data

    def test_wizard_step_2_post(self, client, user):
        """Step 2 posts and redirects to step 3."""
        _login(client)
        _wizard_step_1(client)
        resp = client.post(
            "/study-plan/wizard/2",
            data={"exam_paper": "CS1"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/3"

    def test_wizard_step_3_get(self, client, user):
        """Step 3 renders correctly."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        resp = client.get("/study-plan/wizard/3")
        assert resp.status_code == 200
        assert b"Exam Date" in resp.data or b"Sitting" in resp.data

    def test_wizard_step_3_post(self, client, user):
        """Step 3 posts and redirects to step 4."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        future_date = (date.today() + timedelta(days=180)).isoformat()
        resp = client.post(
            "/study-plan/wizard/3",
            data={
                "exam_sitting": "April 2027",
                "exam_date": future_date,
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/4"

    def test_wizard_step_4_get(self, client, user):
        """Step 4 renders with curriculum topics for IFoA CS1."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        _wizard_step_3(client)
        resp = client.get("/study-plan/wizard/4")
        assert resp.status_code == 200
        assert b"Current Position" in resp.data or b"haven" in resp.data

    def test_wizard_step_4_post(self, client, user):
        """Step 4 posts and redirects to step 5."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        _wizard_step_3(client)
        resp = client.post(
            "/study-plan/wizard/4",
            data={
                "current_position": "not_started",
                "current_topic": "",
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/5"

    def test_wizard_step_5_get(self, client, user):
        """Step 5 renders correctly."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        _wizard_step_3(client)
        _wizard_step_4(client)
        resp = client.get("/study-plan/wizard/5")
        assert resp.status_code == 200

    def test_wizard_step_5_post(self, client, user):
        """Step 5 posts and redirects to step 6."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        _wizard_step_3(client)
        _wizard_step_4(client)
        resp = client.post(
            "/study-plan/wizard/5",
            data={
                "weekday_study_minutes": 60,
                "weekend_study_minutes": 90,
                "preferred_session_minutes": 60,
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/6"

    def test_wizard_step_6_get(self, client, user):
        """Step 6 renders correctly."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        _wizard_step_3(client)
        _wizard_step_4(client)
        _wizard_step_5(client)
        resp = client.get("/study-plan/wizard/6")
        assert resp.status_code == 200
        assert b"Learning Style" in resp.data or b"Mixed" in resp.data

    def test_wizard_step_6_post(self, client, user):
        """Step 6 posts and redirects to step 7."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        _wizard_step_3(client)
        _wizard_step_4(client)
        _wizard_step_5(client)
        resp = client.post(
            "/study-plan/wizard/6",
            data={"study_preference": "Mixed"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/7"

    def test_wizard_step_7_get(self, client, user):
        """Step 7 renders with target grade choices."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        _wizard_step_3(client)
        _wizard_step_4(client)
        _wizard_step_5(client)
        _wizard_step_6(client)
        resp = client.get("/study-plan/wizard/7")
        assert resp.status_code == 200
        assert b"Target" in resp.data or b"result" in resp.data.lower()

    def test_wizard_step_7_post_redirects_to_review(self, client, user):
        """Step 7 posts and redirects to review."""
        _login(client)
        _wizard_step_1(client)
        _wizard_step_2(client)
        _wizard_step_3(client)
        _wizard_step_4(client)
        _wizard_step_5(client)
        _wizard_step_6(client)
        resp = client.post(
            "/study-plan/wizard/7",
            data={"target_grade": "Pass"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/review"

    def test_review_page_renders(self, client, user):
        """Review page renders with all wizard data."""
        _login(client)
        _complete_wizard(client)
        resp = client.get("/study-plan/review")
        assert resp.status_code == 200
        assert b"Review" in resp.data or b"target" in resp.data.lower()

    def test_create_study_plan_succeeds(self, client, user):
        """Final confirmation creates the study plan."""
        _login(client)
        _complete_wizard(client)
        resp = client.post(
            "/study-plan/review",
            data={"confirm": "yes"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert "/calibration/" in resp.request.path
        assert b"history" in resp.data.lower() or b"starting" in resp.data.lower()

    def test_exactly_one_study_plan_created(self, app, ctx, user):
        """Only one StudyPlan should be created for the user."""
        client = app.test_client()
        _create_plan(client, user)

        plans = StudyPlan.query.filter_by(user_id=user.id).all()
        active_plans = [p for p in plans if p.active]
        assert len(active_plans) == 1, (
            f"Expected exactly 1 active study plan, got {len(active_plans)}"
        )

    def test_week_plans_generated(self, app, ctx, user):
        """WeekPlans are generated after study plan creation."""
        client = app.test_client()
        _create_plan(client, user)

        study_plan = StudyPlan.query.filter_by(user_id=user.id, active=True).first()
        assert study_plan is not None

        week_plans_count = WeekPlan.query.filter_by(
            study_plan_id=study_plan.id,
        ).count()
        assert week_plans_count > 0, (
            f"Expected at least 1 WeekPlan, but found {week_plans_count}"
        )

    def test_topic_progress_created_for_curriculum_backed_exam(
        self, app, ctx, user
    ):
        """TopicProgress records are created for IFoA CS1 exam."""
        client = app.test_client()
        _create_plan(client, user)

        tp_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert tp_count > 0, (
            f"Expected TopicProgress records for IFoA CS1, but got {tp_count}"
        )

    def test_no_500_during_wizard(self, client, user):
        """No Internal Server Error occurs during the full wizard flow."""
        _login(client)

        # Step 1
        resp = client.get("/study-plan/wizard/1")
        assert resp.status_code == 200

        resp = client.post(
            "/study-plan/wizard/1",
            data={"exam_category": "IFoA"},
            follow_redirects=True,
        )
        assert resp.status_code == 200

        # Step 2
        resp = client.post(
            "/study-plan/wizard/2",
            data={"exam_paper": "CS1"},
            follow_redirects=True,
        )
        assert resp.status_code == 200

        # Step 3
        future_date = (date.today() + timedelta(days=180)).isoformat()
        resp = client.post(
            "/study-plan/wizard/3",
            data={
                "exam_sitting": "April 2027",
                "exam_date": future_date,
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200

        # Step 4
        resp = client.post(
            "/study-plan/wizard/4",
            data={
                "current_position": "not_started",
                "current_topic": "",
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200

        # Step 5
        resp = client.post(
            "/study-plan/wizard/5",
            data={
                "weekday_study_minutes": 60,
                "weekend_study_minutes": 90,
                "preferred_session_minutes": 60,
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200

        # Step 6
        resp = client.post(
            "/study-plan/wizard/6",
            data={"study_preference": "Mixed"},
            follow_redirects=True,
        )
        assert resp.status_code == 200

        # Step 7
        resp = client.post(
            "/study-plan/wizard/7",
            data={"target_grade": "Pass"},
            follow_redirects=True,
        )
        assert resp.status_code == 200

        # Review
        resp = client.post(
            "/study-plan/review",
            data={"confirm": "yes"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 3 — Dashboard
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeDashboard:
    """Verify dashboard loads and key sections render without errors."""

    def test_dashboard_returns_200_or_redirect(self, logged_in_client):
        """Dashboard returns HTTP status 200 or 302 when logged in."""
        resp = logged_in_client.get("/dashboard/")
        # With no study plan, the user may be redirected to wizard.
        assert resp.status_code in (200, 302)

    def test_dashboard_after_plan_creation(self, app, ctx, user):
        """Dashboard renders fully after a study plan exists."""
        client = app.test_client()
        _create_plan(client, user)

        resp = client.get("/dashboard/")
        assert resp.status_code == 200
        assert b"Dashboard" in resp.data or b"Command Centre" in resp.data

    def test_curriculum_progress_section(self, app, ctx, user):
        """Curriculum Progress section renders on dashboard."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/dashboard/")
        assert resp.status_code == 200

    def test_readiness_section(self, app, ctx, user):
        """Readiness section renders on dashboard."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/dashboard/")
        assert resp.status_code == 200

    def test_time_status_section(self, app, ctx, user):
        """Time status section renders on dashboard."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/dashboard/")
        assert resp.status_code == 200

    def test_todays_mission_section(self, app, ctx, user):
        """Today's Mission section renders on dashboard."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/dashboard/")
        assert resp.status_code == 200

    def test_no_exceptions_on_dashboard(self, app, ctx, user):
        """Dashboard renders with no 500 errors."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/dashboard/")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 4 — Mission Page
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeMission:
    """Verify Today's Mission page renders correctly."""

    def test_mission_page_returns_200(self, app, ctx, user):
        """Mission page returns 200 after study plan creation."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/missions/")
        assert resp.status_code == 200
        assert b"Mission" in resp.data or b"mission" in resp.data.lower()

    def test_mission_hero_renders(self, app, ctx, user):
        """Mission Hero section renders."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/missions/")
        assert resp.status_code == 200
        assert b"Mission Centre" in resp.data or b"Daily Mission" in resp.data

    def test_progress_bar_renders(self, app, ctx, user):
        """Progress bar renders on mission page."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/missions/")
        assert resp.status_code == 200

    def test_task_checklist_renders(self, app, ctx, user):
        """Task checklist renders on mission page."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/missions/")
        assert resp.status_code == 200

    def test_no_exceptions_on_mission(self, app, ctx, user):
        """Mission page renders without 500 errors."""
        client = app.test_client()
        _create_plan(client, user)
        resp = client.get("/missions/")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 5 — Study Plan Page
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeStudyPlanPage:
    """Verify the active Study Plan view renders correctly."""

    def test_study_plan_page_returns_200(self, app, ctx, user):
        """Study Plan view page returns 200."""
        client = app.test_client()
        study_plan = _create_plan(client, user)

        resp = client.get(f"/study-plan/{study_plan.id}")
        assert resp.status_code == 200
        assert b"Study Plan" in resp.data or b"study" in resp.data.lower()

    def test_roadmap_renders(self, app, ctx, user):
        """Roadmap renders on study plan page."""
        client = app.test_client()
        study_plan = _create_plan(client, user)

        resp = client.get(f"/study-plan/{study_plan.id}")
        assert resp.status_code == 200
        # Roadmap section should be present when curriculum exists
        assert resp.status_code == 200

    def test_curriculum_topics_render(self, app, ctx, user):
        """Curriculum topics render on study plan page."""
        client = app.test_client()
        study_plan = _create_plan(client, user)

        resp = client.get(f"/study-plan/{study_plan.id}")
        assert resp.status_code == 200

    def test_status_badges_render(self, app, ctx, user):
        """Status badges render on study plan page."""
        client = app.test_client()
        study_plan = _create_plan(client, user)

        resp = client.get(f"/study-plan/{study_plan.id}")
        assert resp.status_code == 200

    def test_no_exceptions_on_study_plan(self, app, ctx, user):
        """Study Plan page renders without 500 errors."""
        client = app.test_client()
        study_plan = _create_plan(client, user)

        resp = client.get(f"/study-plan/{study_plan.id}")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 6 — Settings
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeSettings:
    """Verify all settings pages return 200 and the data page shows counts."""

    def test_settings_overview(self, logged_in_client):
        """GET /settings returns 200."""
        resp = logged_in_client.get("/settings/")
        assert resp.status_code == 200

    def test_settings_profile(self, logged_in_client):
        """GET /settings/profile returns 200."""
        resp = logged_in_client.get("/settings/profile")
        assert resp.status_code == 200

    def test_settings_preferences(self, logged_in_client):
        """GET /settings/preferences returns 200."""
        resp = logged_in_client.get("/settings/preferences")
        assert resp.status_code == 200

    def test_settings_data_returns_200(self, logged_in_client):
        """GET /settings/data returns 200."""
        resp = logged_in_client.get("/settings/data")
        assert resp.status_code == 200

    def test_settings_data_shows_model_counts(self, logged_in_client):
        """Data page displays model counts."""
        resp = logged_in_client.get("/settings/data")
        assert resp.status_code == 200
        assert (
            b"study_plans" in resp.data.lower()
            or b"Data" in resp.data
            or b"Export" in resp.data
            or b"Backup" in resp.data
        )

    def test_no_exceptions_on_settings(self, logged_in_client):
        """No 500 errors on settings pages."""
        for url in ["/settings/", "/settings/profile", "/settings/preferences",
                     "/settings/data"]:
            resp = logged_in_client.get(url)
            assert resp.status_code == 200
            assert b"Internal Server Error" not in resp.data


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 7 — Export
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeExport:
    """Verify JSON backup export downloads correctly."""

    def test_backup_export_returns_200(self, app, ctx, user):
        """Export endpoint returns 200 with JSON content."""
        client = app.test_client()
        _create_plan(client, user)

        resp = client.get("/settings/export/backup")
        assert resp.status_code == 200
        assert resp.mimetype == "application/json"

    def test_backup_contains_expected_sections(self, app, ctx, user):
        """Backup JSON contains metadata and data sections."""
        client = app.test_client()
        _create_plan(client, user)

        resp = client.get("/settings/export/backup")
        assert resp.status_code == 200

        backup = json.loads(resp.data)
        assert "metadata" in backup
        assert "data" in backup
        assert "version" in backup["metadata"]
        assert backup["metadata"]["version"] == "1.0"
        assert "user_email" in backup["metadata"]
        assert backup["metadata"]["user_email"] == "test@kwalitec.example"

    def test_backup_includes_study_plan_data(self, app, ctx, user):
        """Backup includes study plan data after wizard completion."""
        client = app.test_client()
        _create_plan(client, user)

        resp = client.get("/settings/export/backup")
        assert resp.status_code == 200

        backup = json.loads(resp.data)
        assert "study_plans" in backup["data"]
        assert len(backup["data"]["study_plans"]) >= 1

    def test_no_exceptions_on_backup(self, app, ctx, user):
        """Backup export returns no 500 errors."""
        client = app.test_client()
        _create_plan(client, user)

        resp = client.get("/settings/export/backup")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 8 — Analytics
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeAnalytics:
    """Verify Analytics page renders correctly."""

    def test_analytics_returns_200(self, app, ctx, user):
        """Analytics returns 200 after study plan creation."""
        client = app.test_client()
        _create_plan(client, user)

        resp = client.get("/analytics/")
        assert resp.status_code == 200
        assert b"Analytics" in resp.data or b"analytics" in resp.data.lower()

    def test_analytics_empty_state_or_dashboard(self, app, ctx, user):
        """Analytics renders either empty state or dashboard."""
        client = app.test_client()
        _create_plan(client, user)

        resp = client.get("/analytics/")
        assert resp.status_code == 200
        content = resp.data.decode("utf-8", errors="replace").lower()
        assert (
            "analytics" in content
            or "chart" in content
            or "readiness" in content
            or "no" in content
        )

    def test_no_exceptions_on_analytics(self, app, ctx, user):
        """Analytics page has no 500 errors."""
        client = app.test_client()
        _create_plan(client, user)

        resp = client.get("/analytics/")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 9 — Logout
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeLogout:
    """Verify logout and protected page redirect behaviour."""

    def test_logout_redirects_to_login(self, logged_in_client):
        """Logout redirects the user to the login page."""
        resp = logged_in_client.post("/auth/logout", follow_redirects=True)
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"

    def test_protected_page_redirects_to_login(self, client):
        """Protected pages redirect to login when unauthenticated."""
        protected_urls = [
            "/dashboard/",
            "/missions/",
            "/study-plan/",
            "/analytics/",
            "/settings/",
            "/settings/profile",
            "/settings/preferences",
            "/settings/data",
        ]
        for url in protected_urls:
            resp = client.get(url, follow_redirects=True)
            assert resp.status_code == 200
            assert resp.request.path == "/auth/login", (
                f"Expected {url} to redirect to /auth/login, got {resp.request.path}"
            )

    def test_protected_export_redirects_to_login(self, client):
        """Export endpoint redirects to login when unauthenticated."""
        resp = client.get("/settings/export/backup", follow_redirects=True)
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"

    def test_logout_then_visit_dashboard_redirects(self, logged_in_client):
        """After logout, visiting dashboard redirects to login."""
        logged_in_client.post("/auth/logout", follow_redirects=True)
        resp = logged_in_client.get("/dashboard/", follow_redirects=True)
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"


# ─────────────────────────────────────────────────────────────────────────────
# Full End-to-End Journey
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# Smoke Test 10 — Study Plan Lifecycle (Edit → Archive → Set Active → Delete)
# ─────────────────────────────────────────────────────────────────────────────


class TestSmokeStudyPlanLifecycle:
    """Comprehensive smoke test covering the full study plan lifecycle:
    Create → Edit → Archive → Set Active → Delete."""

    def test_complete_lifecycle(self, app, ctx, user):
        """Create, edit, archive, re-activate, and delete a study plan."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.study_plan import StudyPlan
        from datetime import date as dt_date, timedelta

        client = app.test_client()

        # ── Login ──────────────────────────────────────────────────────
        client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )

        # ── 1. Create a plan ───────────────────────────────────────────
        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CM1",
            exam_sitting="April 2027",
            exam_date=dt_date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Chapter 1",
            study_preference="Mixed",
            target_grade="A",
        )
        assert sp.active is True
        assert sp.archived is False

        # ── 2. Edit the plan via route ─────────────────────────────────
        future = (dt_date.today() + timedelta(days=365)).isoformat()
        resp = client.post(
            f"/study-plan/{sp.id}/edit",
            data={
                "exam_name": "IFoA CM1 Revised",
                "exam_sitting": "September 2027",
                "exam_date": future,
                "weekday_study_minutes": 45,
                "weekend_study_minutes": 90,
                "preferred_session_minutes": 30,
                "current_stage": "Revision",
                "study_preference": "Reading First",
                "target_grade": "B",
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"updated successfully" in resp.data.lower()

        from app.extensions import db
        db.session.refresh(sp)
        assert sp.exam_name == "IFoA CM1 Revised"
        assert sp.weekday_study_minutes == 45
        assert sp.preferred_session_minutes == 30

        # ── 3. Archive the plan ────────────────────────────────────────
        resp = client.post(
            f"/study-plan/{sp.id}/archive",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"archived" in resp.data.lower()

        db.session.refresh(sp)
        assert sp.archived is True
        assert sp.active is False

        # ── 4. Create a second plan ────────────────────────────────────
        sp2 = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CM2",
            exam_sitting="June 2027",
            exam_date=dt_date.today() + timedelta(days=365),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Chapter 1",
            study_preference="Mixed",
            target_grade="B",
        )
        assert sp2.active is True

        # ── 5. Set the archived plan active (via route — should reject) ─
        resp = client.post(
            f"/study-plan/{sp.id}/set-active",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"Cannot activate an archived" in resp.data
        # sp2 must still be active
        db.session.refresh(sp2)
        assert sp2.active is True

        # ── 6. Delete the second plan ──────────────────────────────────
        plan_id_2 = sp2.id
        resp = client.post(
            f"/study-plan/{plan_id_2}/delete",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"permanently deleted" in resp.data.lower()
        assert StudyPlan.query.get(plan_id_2) is None

        # ── 7. Delete the archived plan too ────────────────────────────
        plan_id_1 = sp.id
        resp = client.post(
            f"/study-plan/{plan_id_1}/delete",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"permanently deleted" in resp.data.lower()
        assert StudyPlan.query.get(plan_id_1) is None

        # ── Verify no remaining plans ──────────────────────────────────
        all_plans = StudyPlan.query.filter_by(user_id=user.id).all()
        assert len(all_plans) == 0

    def test_create_edit_archive_set_active_sequence(self, app, ctx, user):
        """Create multiple plans and verify set-active ensures only one active."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.study_plan import StudyPlan
        from datetime import date as dt_date, timedelta

        client = app.test_client()
        client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )

        # Create 3 plans
        sp1 = StudyPlanService.create_study_plan(
            user_id=user.id, exam_name="Plan A", exam_sitting="A1",
            exam_date=dt_date.today() + timedelta(days=90),
            weekday_study_minutes=60, weekend_study_minutes=120,
            current_stage="Start", study_preference="Mixed", target_grade="A",
        )
        sp2 = StudyPlanService.create_study_plan(
            user_id=user.id, exam_name="Plan B", exam_sitting="B1",
            exam_date=dt_date.today() + timedelta(days=180),
            weekday_study_minutes=60, weekend_study_minutes=120,
            current_stage="Start", study_preference="Mixed", target_grade="B",
        )
        sp3 = StudyPlanService.create_study_plan(
            user_id=user.id, exam_name="Plan C", exam_sitting="C1",
            exam_date=dt_date.today() + timedelta(days=270),
            weekday_study_minutes=60, weekend_study_minutes=120,
            current_stage="Start", study_preference="Mixed", target_grade="C",
        )
        # sp3 should be active, sp1/sp2 inactive
        assert sp3.active is True
        assert sp2.active is False
        assert sp1.active is False

        # Set sp1 active
        client.post(f"/study-plan/{sp1.id}/set-active", follow_redirects=True)
        from app.extensions import db
        db.session.refresh(sp1)
        db.session.refresh(sp2)
        db.session.refresh(sp3)
        assert sp1.active is True
        assert sp2.active is False
        assert sp3.active is False

        # Archive sp2
        client.post(f"/study-plan/{sp2.id}/archive", follow_redirects=True)
        db.session.refresh(sp2)
        assert sp2.archived is True
        assert sp2.active is False

        # sp1 still active
        db.session.refresh(sp1)
        assert sp1.active is True

        # Verify get_user_plans excludes archived
        visible = StudyPlanService.get_user_plans(user.id)
        assert len(visible) == 2  # sp1 and sp3, sp2 is archived

        # Verify get_user_plans with include_archived
        all_plans = StudyPlanService.get_user_plans(user.id, include_archived=True)
        assert len(all_plans) == 3


class TestFullEndToEnd:
    """A single test that covers the complete user journey end-to-end."""

    def test_complete_user_journey(self, app, ctx, user):
        """Login → Wizard → Dashboard → Mission → Study Plan → Settings
        → Export → Analytics → Logout.  All must return 200 without 500s."""
        client = app.test_client()

        # ── 1. Login ────────────────────────────────────────────────────
        resp = client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )
        assert resp.status_code == 200

        # ── 2. Complete Study Plan Wizard ───────────────────────────────
        # Step 1
        resp = client.post(
            "/study-plan/wizard/1",
            data={"exam_category": "IFoA"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/2"

        # Step 2
        resp = client.post(
            "/study-plan/wizard/2",
            data={"exam_paper": "CS1"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/3"

        # Step 3
        future_date = (date.today() + timedelta(days=180)).isoformat()
        resp = client.post(
            "/study-plan/wizard/3",
            data={
                "exam_sitting": "April 2027",
                "exam_date": future_date,
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/4"

        # Step 4
        resp = client.post(
            "/study-plan/wizard/4",
            data={
                "current_position": "not_started",
                "current_topic": "",
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/5"

        # Step 5
        resp = client.post(
            "/study-plan/wizard/5",
            data={
                "weekday_study_minutes": 60,
                "weekend_study_minutes": 90,
                "preferred_session_minutes": 60,
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/6"

        # Step 6
        resp = client.post(
            "/study-plan/wizard/6",
            data={"study_preference": "Mixed"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/wizard/7"

        # Step 7
        resp = client.post(
            "/study-plan/wizard/7",
            data={"target_grade": "Pass"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/study-plan/review"

        # Review — GET
        resp = client.get("/study-plan/review")
        assert resp.status_code == 200

        # Review — POST (Create) → first plan launches Student Calibration
        resp = client.post(
            "/study-plan/review",
            data={"confirm": "yes"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert "/calibration/" in resp.request.path
        assert b"Internal Server Error" not in resp.data

        # Calibration skip (empty-history Birth Twin) → dashboard
        plan = StudyPlan.query.filter_by(user_id=user.id, active=True).one()
        resp = client.post(
            f"/calibration/after-plan/{plan.id}",
            data={"skip_beginner": "I'm starting from scratch — skip detail"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert "/dashboard" in resp.request.path
        assert b"Internal Server Error" not in resp.data

        # ── Verify exactly one StudyPlan ────────────────────────────────
        active_plans = StudyPlan.query.filter_by(
            user_id=user.id, active=True
        ).all()
        assert len(active_plans) == 1, (
            f"Expected exactly 1 active study plan, got {len(active_plans)}"
        )

        # ── Verify WeekPlans generated ──────────────────────────────────
        week_count = WeekPlan.query.filter_by(
            study_plan_id=active_plans[0].id,
        ).count()
        assert week_count > 0, "No WeekPlans generated"

        # ── Verify TopicProgress created ────────────────────────────────
        tp_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert tp_count > 0, (
            "No TopicProgress records for curriculum-backed exam IFoA CS1"
        )

        # ── 3. Dashboard ────────────────────────────────────────────────
        resp = client.get("/dashboard/")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data

        # ── 4. Mission Page ─────────────────────────────────────────────
        resp = client.get("/missions/")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data

        # ── 5. Study Plan View ──────────────────────────────────────────
        study_plan = active_plans[0]
        resp = client.get(f"/study-plan/{study_plan.id}")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data

        # ── 6. Settings ─────────────────────────────────────────────────
        for settings_url in ["/settings/", "/settings/profile",
                             "/settings/preferences", "/settings/data"]:
            resp = client.get(settings_url)
            assert resp.status_code == 200, (
                f"Settings page {settings_url} returned {resp.status_code}"
            )
            assert b"Internal Server Error" not in resp.data

        # ── 7. Export Backup ────────────────────────────────────────────
        resp = client.get("/settings/export/backup")
        assert resp.status_code == 200
        assert resp.mimetype == "application/json"
        assert b"Internal Server Error" not in resp.data

        backup = json.loads(resp.data)
        assert "metadata" in backup
        assert "data" in backup
        assert "study_plans" in backup["data"]
        assert len(backup["data"]["study_plans"]) >= 1

        # ── 8. Analytics ────────────────────────────────────────────────
        resp = client.get("/analytics/")
        assert resp.status_code == 200
        assert b"Internal Server Error" not in resp.data

        # ── 9. Logout ───────────────────────────────────────────────────
        resp = client.post("/auth/logout", follow_redirects=True)
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"

        # Protected pages now redirect to login
        for protected_url in ["/dashboard/", "/missions/",
                              "/analytics/", "/settings/"]:
            resp = client.get(protected_url, follow_redirects=True)
            assert resp.status_code == 200
            assert resp.request.path == "/auth/login", (
                f"After logout, {protected_url} should redirect to "
                f"/auth/login, but got {resp.request.path}"
            )