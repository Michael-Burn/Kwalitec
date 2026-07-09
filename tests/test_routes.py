"""Tests for application routes and endpoints."""

from __future__ import annotations


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
        assert b"Curriculum Progress" in response.data
        assert b"Curriculum data will appear once you create a study plan." in response.data

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

    def test_step4_get_displays_free_text_for_unsupported(self, logged_in_client):
        """Step 4 for an unsupported exam (CM1) should show free-text topic."""
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CM1",
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
                "curriculum_topic": ["CS1-A", "CS1-B"],
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        with logged_in_client.session_transaction() as sess:
            wizard_data = sess["wizard_data"]
            assert wizard_data["current_position"] == "learning"
            assert "completed_curriculum_topics" in wizard_data
            assert wizard_data["completed_curriculum_topics"] == ["CS1-A", "CS1-B"]
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
                "exam_paper": "CM1",
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
                "completed_curriculum_topics": ["CS1-A"],
            }
        response = logged_in_client.get("/study-plan/wizard/4")
        assert response.status_code == 200
        html = response.data.decode()
        # The previously completed topic should be checked
        assert 'value="CS1-A"' in html
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
                "completed_curriculum_topics": ["CS1-A", "CS1-B"],
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
        assert "CS1-A" in html
        assert "CS1-B" in html


class TestCurriculumVersionResolution:
    """Tests for _resolve_curriculum_version helper."""

    def test_ifoa_cs1_resolves_to_2026(self):
        """IFoA + CS1 should resolve to curriculum version '2026'."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("IFoA", "CS1")
        assert result == "2026"

    def test_ifoa_cm1_returns_none(self):
        """IFoA + CM1 is not yet mapped — returns None (no curriculum)."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("IFoA", "CM1")
        assert result is None

    def test_cfa_returns_none(self):
        """CFA is not mapped — returns None (no curriculum)."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("CFA", "Level I")
        assert result is None

    def test_unknown_category_returns_none(self):
        """An unknown category returns None — no curriculum mapping."""
        from app.study_plan.routes import _resolve_curriculum_version

        result = _resolve_curriculum_version("Other", "")
        assert result is None