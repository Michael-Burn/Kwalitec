"""GA-001 WS4 — security review assertions (RBAC, session, CSRF, headers, secrets)."""

from __future__ import annotations

import pytest

from app.config import BaseConfig, ProductionConfig, TestingConfig
from app.security.capabilities import Capability
from app.security.permissions import Permission, permissions_for_roles
from app.security.roles import Role
from tests.ga.helpers import login_as, make_founder, make_student


class TestRbacAndPortalSeparation:
    def test_role_permission_matrix_least_privilege(self) -> None:
        student = permissions_for_roles({Role.STUDENT})
        assert student == frozenset({Permission.STUDENT_PORTAL})
        assert Permission.CONSOLE_ACCESS not in student

        support = permissions_for_roles({Role.SUPPORT})
        assert Permission.CONSOLE_ACCESS in support
        assert Permission.USERS_MANAGE not in support

        founder = permissions_for_roles({Role.FOUNDER})
        assert Permission.CONSOLE_ACCESS in founder
        assert Permission.USERS_MANAGE in founder

    def test_student_portal_vs_console(self, client, ctx, app) -> None:
        make_student("ga-sec-student@kwalitec.example")
        app.config["FOUNDER_EMAILS"] = ""
        login_as(client, "ga-sec-student@kwalitec.example")
        assert client.get("/student/").status_code in {200, 302}
        assert client.get("/console/").status_code == 403

    def test_founder_console_capability(self, client, ctx, app) -> None:
        user = make_founder("ga-sec-founder@kwalitec.example")
        assert Capability.CONSOLE in user.get_capabilities()
        app.config["FOUNDER_EMAILS"] = ""
        login_as(client, "ga-sec-founder@kwalitec.example")
        assert client.get("/console/").status_code == 200


class TestSessionAndCookies:
    def test_base_cookie_flags(self) -> None:
        assert BaseConfig.SESSION_COOKIE_HTTPONLY is True
        assert BaseConfig.SESSION_COOKIE_SAMESITE == "Lax"
        assert BaseConfig.WTF_CSRF_ENABLED is True

    def test_production_cookie_hardening(self) -> None:
        assert ProductionConfig.SESSION_COOKIE_SECURE is True
        assert ProductionConfig.SESSION_COOKIE_HTTPONLY is True
        assert ProductionConfig.SESSION_COOKIE_SAMESITE == "Lax"

    def test_testing_disables_csrf_only_in_tests(self) -> None:
        assert TestingConfig.WTF_CSRF_ENABLED is False
        assert BaseConfig.WTF_CSRF_ENABLED is True


class TestSecurityHeaders:
    def test_security_headers_present(self, client) -> None:
        response = client.get("/health/live")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("Referrer-Policy") == (
            "strict-origin-when-cross-origin"
        )
        assert "Content-Security-Policy" in response.headers
        csp = response.headers["Content-Security-Policy"]
        assert "default-src 'self'" in csp
        # Documented residual risk: unsafe-inline still required for legacy templates.
        assert "'unsafe-inline'" in csp


class TestSecretsAndInputValidation:
    def test_production_rejects_insecure_secret(self, monkeypatch) -> None:
        monkeypatch.setenv("SECRET_KEY", "change-this-secret-key")
        monkeypatch.setenv(
            "DATABASE_URL", "postgresql+psycopg://u:p@localhost:5432/kwalitec"
        )
        from app import _validate_env_vars

        with pytest.raises(RuntimeError, match="SECRET_KEY"):
            _validate_env_vars(ProductionConfig)

    def test_login_rejects_unknown_user(self, client) -> None:
        response = client.post(
            "/auth/login",
            data={
                "email": "nobody@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        html = response.get_data(as_text=True).lower()
        assert "invalid" in html or "incorrect" in html or "login" in html

    def test_open_redirect_not_accepted(self, client, ctx) -> None:
        make_student("ga-redirect@kwalitec.example")
        response = client.post(
            "/auth/login?next=https://evil.example/phish",
            data={
                "email": "ga-redirect@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=False,
        )
        assert response.status_code in {200, 302, 303}
        location = response.headers.get("Location", "")
        assert "evil.example" not in location
        if location:
            assert location.startswith("/") or "localhost" in location
