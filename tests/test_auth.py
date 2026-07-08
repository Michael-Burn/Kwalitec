"""Tests for authentication routes and functionality."""

from __future__ import annotations


class TestAuthRoutes:
    """Tests for auth blueprint routes."""

    def test_login_page_renders(self, client):
        response = client.get("/auth/login")
        assert response.status_code == 200
        assert b"Sign in" in response.data

    def test_login_redirects_authenticated_user(self, logged_in_client):
        response = logged_in_client.get("/auth/login")
        assert response.status_code == 302

    def test_login_with_valid_credentials(self, client, user):
        response = client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_login_with_invalid_credentials(self, client):
        response = client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "wrongpassword"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Invalid email or password" in response.data

    def test_login_with_nonexistent_user(self, client):
        response = client.post(
            "/auth/login",
            data={"email": "nouser@example.com", "password": "password"},
            follow_redirects=True,
        )
        assert b"Invalid email or password" in response.data

    def test_logout(self, logged_in_client):
        response = logged_in_client.post("/auth/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"You have been signed out" in response.data

    def test_logout_requires_login(self, client):
        response = client.post("/auth/logout", follow_redirects=True)
        assert response.status_code == 200

    def test_login_redirects_to_dashboard_if_authenticated(self, logged_in_client):
        response = logged_in_client.get("/auth/login", follow_redirects=True)
        assert response.status_code == 200

    def test_case_insensitive_email(self, client, user):
        """Verify email is normalized to lowercase."""
        response = client.post(
            "/auth/login",
            data={"email": "TEST@KWALITEC.EXAMPLE", "password": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_trim_whitespace_email(self, client, user):
        """Verify email whitespace is stripped."""
        response = client.post(
            "/auth/login",
            data={"email": "  test@kwalitec.example  ", "password": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200


class TestSafeNextUrl:
    """Tests for the _safe_next_url helper."""

    def test_empty_next(self, app):
        from app.auth.routes import _safe_next_url

        with app.test_request_context("/auth/login"):
            assert _safe_next_url() is None

    def test_relative_next(self, app):
        from app.auth.routes import _safe_next_url

        with app.test_request_context("/auth/login?next=/dashboard/"):
            assert _safe_next_url() == "/dashboard/"

    def test_external_next_rejected(self, app):
        from app.auth.routes import _safe_next_url

        with app.test_request_context("/auth/login?next=https://evil.com"):
            assert _safe_next_url() is None

    def test_absolute_url_rejected(self, app):
        from app.auth.routes import _safe_next_url

        with app.test_request_context("/auth/login?next=http://evil.com/phish"):
            assert _safe_next_url() is None


class TestProtectedRoutes:
    """Tests that protected routes require login."""

    def test_dashboard_requires_login(self, client):
        response = client.get("/dashboard/", follow_redirects=True)
        assert response.status_code == 200

    def test_analytics_requires_login(self, client):
        response = client.get("/analytics/", follow_redirects=True)
        assert response.status_code == 200

    def test_missions_requires_login(self, client):
        response = client.get("/missions/", follow_redirects=True)
        assert response.status_code == 200

    def test_settings_requires_login(self, client):
        response = client.get("/settings/", follow_redirects=True)
        assert response.status_code == 200

    def test_study_plan_requires_login(self, client):
        response = client.get("/study-plan/", follow_redirects=True)
        assert response.status_code == 200

    def test_root_redirects_to_login(self, client):
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200