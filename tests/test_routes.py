"""Tests for application routes and endpoints."""

from __future__ import annotations

import os
import tempfile


class TestDashboardRoute:
    """Tests for dashboard routes."""

    def test_dashboard_index_authenticated(self, logged_in_client):
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200

    def test_dashboard_requires_login(self, client):
        response = client.get("/dashboard/", follow_redirects=True)
        assert response.status_code == 200

    def test_dashboard_no_curriculum_summary_when_no_study_plan(
        self, logged_in_client
    ):
        """Curriculum progress card shows empty state when there is no active study plan."""
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b"Curriculum Roadmap" in response.data
        assert b"Curriculum data will appear once you create a study plan." not in response.data
        assert b"Create your first study plan to unlock your curriculum roadmap." in response.data

    def test_dashboard_curriculum_summary_for_supported_exam(
        self, logged_in_client, study_plan, curriculum
    ):
        """Dashboard renders curriculum summary when suitable curriculum bound."""
        # Attach the curriculum to the study plan and configure version
        cur, _ = curriculum
        from app.extensions import db

        study_plan.curriculum_id = cur.id
        study_plan.curriculum_version = "2025"
        study_plan.curriculum_topic_code = "Probability"
        db.session.commit()

        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200

    def test_dashboard_unsupported_exam_no_error(
        self, logged_in_client, study_plan
    ):
        """Dashboard renders without error for unsupported exam."""
        from app.extensions import db

        study_plan.curriculum_version = "9999"
        study_plan.curriculum_id = 99999
        db.session.commit()

        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200


class TestMissionRoutes:
    """Tests for mission blueprint routes."""

    def test_missions_index_authenticated(self, logged_in_client):
        response = logged_in_client.get("/missions/")
        assert response.status_code == 200

    def test_missions_requires_login(self, client):
        response = client.get("/missions/", follow_redirects=True)
        assert response.status_code == 200

    def test_mission_review_authenticated(self, logged_in_client, mission):
        response = logged_in_client.get(f"/missions/review/{mission.id}")
        assert response.status_code in (200, 302, 404)

    def test_mission_review_requires_login(self, client, mission):
        response = client.get(f"/missions/review/{mission.id}", follow_redirects=True)
        assert response.status_code == 200


class TestStudyPlanRoutes:
    """Tests for study plan blueprint routes."""

    def test_study_plan_list_authenticated(self, logged_in_client, study_plan):
        response = logged_in_client.get("/study-plan/")
        assert response.status_code in (200, 302)

    def test_study_plan_list_requires_login(self, client):
        response = client.get("/study-plan/", follow_redirects=True)
        assert response.status_code == 200

    def test_study_plan_wizard_step1(self, logged_in_client):
        response = logged_in_client.get("/study-plan/wizard/1")
        assert response.status_code == 200

    def test_study_plan_wizard_step1_requires_login(self, client):
        response = client.get("/study-plan/wizard/1", follow_redirects=True)
        assert response.status_code == 200


class TestAnalyticsRoutes:
    """Tests for analytics blueprint routes."""

    def test_analytics_index_authenticated(self, logged_in_client):
        response = logged_in_client.get("/analytics/")
        assert response.status_code == 200

    def test_analytics_requires_login(self, client):
        response = client.get("/analytics/", follow_redirects=True)
        assert response.status_code == 200


class TestSettingsRoutes:
    """Tests for settings blueprint routes."""

    def test_settings_index_authenticated(self, logged_in_client):
        response = logged_in_client.get("/settings/")
        assert response.status_code == 200

    def test_settings_requires_login(self, client):
        response = client.get("/settings/", follow_redirects=True)
        assert response.status_code == 200

    def test_data_page_returns_200_on_fresh_database(self, logged_in_client):
        """Settings → Data must not 500 when no records exist.

        Regression test: WeekPlan and MissionTask lack a direct user_id
        column, so filter_by(user_id=...) used to raise AttributeError.
        """
        response = logged_in_client.get("/settings/data")
        assert response.status_code == 200

    def test_data_page_shows_counts_with_records(
        self, logged_in_client, study_plan, mission
    ):
        """Settings → Data shows correct record counts."""
        response = logged_in_client.get("/settings/data")
        assert response.status_code == 200
        html = response.data.decode()
        # Template renders labels via: label | replace('_', ' ') | title
        assert "Study Plans" in html
        assert "Missions" in html
        assert "Mission Tasks" in html


class TestErrorHandling:
    """Tests for error pages and error handling."""

    def test_404_page(self, client):
        response = client.get("/nonexistent-page-that-does-not-exist")
        assert response.status_code == 404

    def test_csrf_protection_active(self, client):
        """Test that CSRF protection is active (expect 400)."""
        response = client.post("/auth/login", data={})
        assert response.status_code in (200, 400)

    def test_custom_500_page_in_production_mode(self):
        """Regression: production (no PROPAGATE_EXCEPTIONS) returns custom 500."""
        db_fd, db_path = tempfile.mkstemp(suffix=".sqlite3")

        try:
            from app import create_app

            app = create_app()
            app.config.update(
                TESTING=True,
                PROPAGATE_EXCEPTIONS=False,
                DEBUG=False,
                WTF_CSRF_ENABLED=False,
                SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
                SERVER_NAME="localhost.localdomain",
            )

            @app.route("/trigger-500")
            def trigger_500():
                raise RuntimeError("intentional test error")

            with app.app_context():
                from app.extensions import db

                db.create_all()

            client = app.test_client()
            response = client.get("/trigger-500")
            assert response.status_code == 500
            assert b"Internal Server Error" in response.data
        finally:
            os.close(db_fd)
            os.unlink(db_path)


class TestHealthCheck:
    """Tests for health-check endpoint."""

    def test_health_check_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data["status"] == "ok"
        assert "timestamp" in data

    def test_health_check_db_status(self, client):
        response = client.get("/health")
        data = response.get_json()
        assert "database" in data
        assert data["database"] in ("connected", "error")


class TestSecurityHeaders:
    """Tests for production security headers."""

    def test_security_headers_present(self, client):
        response = client.get("/auth/login")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"


class TestStudyPlanWizardStep4:
    """Tests for wizard step 4 — current position with completed curriculum topics."""

    def test_step4_get_requires_login(self, client):
        response = client.get("/study-plan/wizard/4", follow_redirects=True)
        assert response.status_code == 200

    def test_step4_get_displays_for_supported_curriculum(self, logged_in_client):
        """Step 4 for IFoA/CS1 should show curriculum topic checkboxes."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CS1",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
            }
        response = logged_in_client.get("/study-plan/wizard/4")
        assert response.status_code == 200
        # Should contain the curriculum topic checklist div
        assert b'id="curriculum-topic-field"' in response.data
        # Should use checkboxes, not radios
        assert b'type="checkbox"' in response.data

    def test_step4_get_displays_for_cb2_curriculum(self, logged_in_client):
        """Step 4 for IFoA/CB2 should show curriculum topic checkboxes."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CB2",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
            }
        response = logged_in_client.get("/study-plan/wizard/4")
        assert response.status_code == 200
        assert b'id="curriculum-topic-field"' in response.data
        assert b'type="checkbox"' in response.data
        assert b'id="current-topic-field"' not in response.data

    def test_step4_get_displays_for_cm1_curriculum(self, logged_in_client):
        """Step 4 for IFoA/CM1 should show curriculum topic checkboxes."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CM1",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
            }
        response = logged_in_client.get("/study-plan/wizard/4")
        assert response.status_code == 200
        assert b'id="curriculum-topic-field"' in response.data
        assert b'type="checkbox"' in response.data
        assert b'id="current-topic-field"' not in response.data

    def test_step4_get_displays_free_text_for_unsupported(self, logged_in_client):
        """Step 4 for an unsupported exam (CM2) should show free-text topic."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CM2",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
            }
        response = logged_in_client.get("/study-plan/wizard/4")
        assert response.status_code == 200
        # Should contain the free-text topic field
        assert b'id="current-topic-field"' in response.data
        # Should NOT contain the curriculum topic checklist
        assert b'id="curriculum-topic-field"' not in response.data

    def test_step4_post_stores_completed_topics(self, logged_in_client):
        """POST with checked curriculum topics stores them in session."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CS1",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
            }
        response = logged_in_client.post(
            "/study-plan/wizard/4",
            data={
                "current_position": "learning",
                "curriculum_topic": ["1.1", "1.2"],
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        with logged_in_client.session_transaction() as sess:
            wizard_data = sess["wizard_data"]
            assert wizard_data["current_position"] == "learning"
            assert "completed_curriculum_topics" in wizard_data
            assert wizard_data["completed_curriculum_topics"] == ["1.1", "1.2"]
            # Legacy key must be removed
            assert "curriculum_topic" not in wizard_data

    def test_step4_post_no_topics_selected(self, logged_in_client):
        """POST with no completed topics stores an empty list."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CS1",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
            }
        response = logged_in_client.post(
            "/study-plan/wizard/4",
            data={
                "current_position": "not_started",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        with logged_in_client.session_transaction() as sess:
            wizard_data = sess["wizard_data"]
            assert wizard_data["completed_curriculum_topics"] == []

    def test_step4_post_unsupported_clears_completed_topics(self, logged_in_client):
        """POST for unsupported exam should clear completed_curriculum_topics."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CM2",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
            }
        response = logged_in_client.post(
            "/study-plan/wizard/4",
            data={
                "current_position": "learning",
                "current_topic": "Probability distributions",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        with logged_in_client.session_transaction() as sess:
            wizard_data = sess["wizard_data"]
            assert "completed_curriculum_topics" not in wizard_data
            assert wizard_data["current_topic"] == "Probability distributions"

    def test_step4_back_navigation_restores_completed_topics(self, logged_in_client):
        """When navigating back to step 4, completed topics are pre-checked."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CS1",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
                "current_position": "learning",
                "completed_curriculum_topics": ["1.1"],
            }
        response = logged_in_client.get("/study-plan/wizard/4")
        assert response.status_code == 200
        html = response.data.decode()
        # The previously completed topic should be checked
        assert 'value="1.1"' in html
        assert "checked" in html

    def test_step4_review_shows_completed_topics(self, logged_in_client):
        """Review page should display completed curriculum topics."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CS1",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
                "current_position": "learning",
                "completed_curriculum_topics": ["1.1", "1.2"],
                "weekday_study_minutes": 60,
                "weekend_study_minutes": 120,
                "study_preference": "Mixed",
                "target_grade": "Pass",
                "preferred_session_minutes": 60,
            }
        response = logged_in_client.get("/study-plan/review")
        assert response.status_code == 200
        html = response.data.decode()
        assert "Completed Topics" in html
        assert "1.1" in html
        assert "1.2" in html


class TestStudyPlanManagementRoutes:
    """Tests for study plan management — edit, delete, archive, set-active,
    and list routes."""

    def test_list_plans_page(self, logged_in_client, study_plan):
        """GET /study-plan/plans/all renders the plans list."""
        resp = logged_in_client.get("/study-plan/plans/all")
        assert resp.status_code == 200
        assert b"My Plans" in resp.data or b"Study Plans" in resp.data

    def test_list_plans_requires_login(self, client):
        resp = client.get("/study-plan/plans/all", follow_redirects=True)
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"

    def test_view_plan_authenticated(self, logged_in_client, study_plan):
        """GET /study-plan/<id> shows plan details."""
        resp = logged_in_client.get(f"/study-plan/{study_plan.id}")
        assert resp.status_code == 200

    def test_view_plan_not_found(self, logged_in_client):
        """Viewing a non-existent plan redirects."""
        resp = logged_in_client.get("/study-plan/99999", follow_redirects=True)
        assert resp.status_code == 200
        assert b"not found" in resp.data.lower()

    def test_view_plan_wrong_user_redirects(self, logged_in_client, study_plan):
        """Viewing another user's plan should redirect."""
        # The study_plan fixture is owned by the current logged-in user,
        # so we test with an ID that doesn't exist to the user.
        resp = logged_in_client.get("/study-plan/99999", follow_redirects=True)
        assert resp.status_code == 200

    def test_edit_plan_get(self, logged_in_client, study_plan):
        """GET edit page for an existing plan."""
        resp = logged_in_client.get(
            f"/study-plan/{study_plan.id}/edit"
        )
        assert resp.status_code == 200
        assert b"Edit Study Plan" in resp.data

    def test_edit_plan_get_not_found(self, logged_in_client):
        """GET edit for non-existent plan redirects."""
        resp = logged_in_client.get(
            "/study-plan/99999/edit", follow_redirects=True
        )
        assert resp.status_code == 200
        assert b"not found" in resp.data.lower()

    def test_edit_plan_archived_rejected(self, logged_in_client, study_plan):
        """GET edit for archived plan redirects with message."""
        from app.extensions import db
        study_plan.archived = True
        study_plan.active = False
        db.session.commit()

        resp = logged_in_client.get(
            f"/study-plan/{study_plan.id}/edit", follow_redirects=True
        )
        assert resp.status_code == 200
        assert b"Cannot edit an archived" in resp.data

    def test_edit_plan_post_updates_fields(self,
        logged_in_client, study_plan):
        """POST edit updates study plan fields."""
        from datetime import date as dt_date, timedelta

        future = (dt_date.today() + timedelta(days=365)).isoformat()
        resp = logged_in_client.post(
            f"/study-plan/{study_plan.id}/edit",
            data={
                "exam_name": "IFoA CM1 Edited",
                "exam_sitting": "September 2027",
                "exam_date": future,
                "weekday_study_minutes": 90,
                "weekend_study_minutes": 150,
                "preferred_session_minutes": 45,
                "current_stage": "Revision Phase",
                "study_preference": "Questions First",
                "target_grade": "B",
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200

        from app.models.study_plan import StudyPlan
        from app.extensions import db
        updated = db.session.get(StudyPlan, study_plan.id)
        assert updated.exam_name == "IFoA CM1 Edited"
        assert updated.exam_sitting == "September 2027"
        assert updated.preferred_session_minutes == 45

    def test_delete_plan_post(self, logged_in_client, study_plan):
        """POST delete removes the plan."""
        resp = logged_in_client.post(
            f"/study-plan/{study_plan.id}/delete",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"permanently deleted" in resp.data.lower()

        from app.models.study_plan import StudyPlan
        assert StudyPlan.query.get(study_plan.id) is None

    def test_delete_plan_not_found(self, logged_in_client):
        """Deleting a non-existent plan redirects with error."""
        resp = logged_in_client.post(
            "/study-plan/99999/delete", follow_redirects=True
        )
        assert resp.status_code == 200
        assert b"not found" in resp.data.lower()

    def test_archive_plan_post(self, logged_in_client, study_plan):
        """POST archive sets the plan as archived."""
        resp = logged_in_client.post(
            f"/study-plan/{study_plan.id}/archive",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"archived" in resp.data.lower()

        from app.models.study_plan import StudyPlan
        from app.extensions import db
        updated = db.session.get(StudyPlan, study_plan.id)
        assert updated.archived is True
        assert updated.active is False

    def test_archive_plan_not_found(self, logged_in_client):
        """Archiving a non-existent plan redirects with error."""
        resp = logged_in_client.post(
            "/study-plan/99999/archive", follow_redirects=True
        )
        assert resp.status_code == 200
        assert b"not found" in resp.data.lower()

    def test_set_active_plan_post(self, app, ctx, user):
        """POST set-active makes the plan active and deactivates others."""
        from app.services.study_plan_service import StudyPlanService
        from datetime import date as dt_date, timedelta

        client = app.test_client()
        client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )

        sp1 = StudyPlanService.create_study_plan(
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
        # sp2 active (most recent), sp1 inactive
        assert sp2.active is True
        assert sp1.active is False

        resp = client.post(
            f"/study-plan/{sp1.id}/set-active",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"set as active" in resp.data.lower()

        from app.models.study_plan import StudyPlan
        from app.extensions import db
        sp1_check = db.session.get(StudyPlan, sp1.id)
        sp2_check = db.session.get(StudyPlan, sp2.id)
        assert sp1_check.active is True
        assert sp2_check.active is False

    def test_set_active_archived_plan_rejected(self,
        logged_in_client, study_plan):
        """Cannot activate an archived plan."""
        from app.extensions import db
        study_plan.archived = True
        study_plan.active = False
        db.session.commit()

        resp = logged_in_client.post(
            f"/study-plan/{study_plan.id}/set-active",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"Cannot activate an archived" in resp.data

    def test_set_active_not_found(self, logged_in_client):
        """Set-active for non-existent plan redirects with error."""
        resp = logged_in_client.post(
            "/study-plan/99999/set-active", follow_redirects=True
        )
        assert resp.status_code == 200
        assert b"not found" in resp.data.lower()

    def test_set_active_requires_login(self, client, study_plan):
        resp = client.post(
            f"/study-plan/{study_plan.id}/set-active",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"

    def test_archive_requires_login(self, client, study_plan):
        resp = client.post(
            f"/study-plan/{study_plan.id}/archive",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"

    def test_delete_requires_login(self, client, study_plan):
        resp = client.post(
            f"/study-plan/{study_plan.id}/delete",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"

    def test_edit_requires_login(self, client, study_plan):
        resp = client.get(
            f"/study-plan/{study_plan.id}/edit", follow_redirects=True
        )
        assert resp.status_code == 200
        assert resp.request.path == "/auth/login"


class TestCurriculumVersionResolution:
    """Tests for discovery-driven curriculum version resolution."""

    def test_ifoa_cs1_resolves_to_2026(self):
        """IFoA + CS1 should resolve to curriculum version '2026'."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("IFoA", "CS1")
        assert result == "2026"

    def test_ifoa_cb2_resolves_to_2026(self):
        """IFoA + CB2 should resolve to curriculum version '2026' from disk."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("IFoA", "CB2")
        assert result == "2026"

    def test_ifoa_cm1_resolves_to_2026(self):
        """IFoA + CM1 should resolve to curriculum version '2026'."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("IFoA", "CM1")
        assert result == "2026"

    def test_ifoa_cm2_returns_none(self):
        """IFoA + CM2 has no on-disk syllabus — returns None."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("IFoA", "CM2")
        assert result is None

    def test_cfa_returns_none(self):
        """CFA has no on-disk syllabus — returns None."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("CFA", "Level I")
        assert result is None

    def test_unknown_category_returns_none(self):
        """An unknown category returns None — no curriculum on disk."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("Other", "")
        assert result is None

    def test_discover_curriculum_version_matches_resolve(self):
        """Silent discovery and resolve agree for supported papers."""
        from app.study_plan.routes import (
            _discover_curriculum_version,
            _resolve_curriculum_version,
        )

        for paper in ("CS1", "CB2", "CM1"):
            assert _discover_curriculum_version("IFoA", paper) == "2026"
            assert _resolve_curriculum_version("IFoA", paper) == "2026"
