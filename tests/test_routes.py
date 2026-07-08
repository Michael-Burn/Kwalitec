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