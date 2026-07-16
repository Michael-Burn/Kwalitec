"""QS-001 / PTP-005 Version 1 Cohesion regression tests."""

from __future__ import annotations

from app.services.internal_alpha_status_service import InternalAlphaStatusService
from app.version import APP_VERSION, PRODUCT_TAGLINE


class TestVersionIdentity:
    def test_single_app_version_in_settings(self, logged_in_client):
        response = logged_in_client.get("/settings/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert APP_VERSION in body
        assert "v1.1" not in body

    def test_auth_footer_matches_app_version(self, client):
        response = client.get("/auth/login")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert f"Kwalitec v{APP_VERSION}" in body

    def test_authenticated_footer_matches_app_version(self, logged_in_client):
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert f"Kwalitec v{APP_VERSION}" in body

    def test_health_check_version(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json()["version"] == APP_VERSION

    def test_internal_alpha_status_uses_same_app_version(self, db, user):
        status = InternalAlphaStatusService.build_status(user.id)
        assert status.app_version == APP_VERSION


class TestStudySessionTerminology:
    def test_sidebar_and_mission_page_align(self, logged_in_client):
        dash = logged_in_client.get("/dashboard/")
        assert b"Study Session" in dash.data
        assert b"Resume Mission" not in dash.data
        assert b"Open Today&#39;s Mission" not in dash.data

        mission = logged_in_client.get("/missions/")
        assert mission.status_code == 200
        body = mission.get_data(as_text=True)
        assert "Today's Study Session" in body
        assert "Daily Mission" not in body
        assert "Study Coach" not in body

    def test_analytics_heading_matches_nav(self, logged_in_client):
        response = logged_in_client.get("/analytics/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Analytics" in body
        assert 'class="section-title">Insights<' not in body


class TestProductIdentity:
    def test_login_uses_unified_tagline(self, client):
        response = client.get("/auth/login")
        body = response.get_data(as_text=True)
        assert PRODUCT_TAGLINE in body
        assert "Intelligent Exam Preparation" not in body
        assert "Burnout Monitoring" not in body
        assert "Adaptive Learning" not in body


class TestOnboardingDedup:
    def test_wizard_step4_does_not_collect_completed_topics(self, logged_in_client):
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CS1",
                "exam_sitting": "April 2027",
                "exam_date": "2027-04-15",
            }
        get_resp = logged_in_client.get("/study-plan/wizard/4")
        html = get_resp.get_data(as_text=True)
        assert "Which topics have you already completed" not in html

        post_resp = logged_in_client.post(
            "/study-plan/wizard/4",
            data={"current_position": "learning"},
            follow_redirects=True,
        )
        assert post_resp.status_code == 200
        with logged_in_client.session_transaction() as sess:
            wizard_data = sess["wizard_data"]
            assert wizard_data["current_position"] == "learning"
            assert "completed_curriculum_topics" not in wizard_data
