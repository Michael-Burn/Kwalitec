"""Production custom-domain / public URL readiness tests."""

from __future__ import annotations

import logging


class TestPublicUrlHelpers:
    def test_normalize_strips_path_and_slash(self) -> None:
        from app.public_url import normalize_app_url

        assert (
            normalize_app_url("https://app.example.com/path/")
            == "https://app.example.com"
        )
        assert normalize_app_url("app.example.com") == "https://app.example.com"
        assert normalize_app_url("") == ""
        assert normalize_app_url("   ") == ""

    def test_absolute_public_url_prefers_app_url(self, app) -> None:
        from app.public_url import absolute_public_url

        app.config["APP_URL"] = "https://learn.example.com"
        with app.test_request_context(
            "/",
            base_url="https://kwalitec.onrender.com/",
        ):
            assert absolute_public_url("/auth/login") == (
                "https://learn.example.com/auth/login"
            )

    def test_public_base_url_falls_back_to_request(self, app) -> None:
        from app.public_url import public_base_url

        app.config["APP_URL"] = ""
        with app.test_request_context(
            "/",
            base_url="https://kwalitec.onrender.com/",
        ):
            assert public_base_url() == "https://kwalitec.onrender.com"


class TestProductionDomainConfig:
    def test_production_cookie_and_static_defaults(self) -> None:
        from app.config import ProductionConfig

        assert ProductionConfig.SESSION_COOKIE_SECURE is True
        assert ProductionConfig.SESSION_COOKIE_HTTPONLY is True
        assert ProductionConfig.SESSION_COOKIE_SAMESITE == "Lax"
        assert ProductionConfig.REMEMBER_COOKIE_SECURE is True
        assert ProductionConfig.SEND_FILE_MAX_AGE_DEFAULT == 31_536_000
        assert ProductionConfig.PREFERRED_URL_SCHEME == "https"
        assert ProductionConfig.TRUSTED_PROXY_HOPS >= 1

    def test_normalize_and_scheme_helpers(self, monkeypatch) -> None:
        from app.config import _normalize_app_url, _preferred_url_scheme

        assert _normalize_app_url("https://app.example.com/") == (
            "https://app.example.com"
        )
        monkeypatch.setenv("APP_URL", "https://app.example.com")
        monkeypatch.delenv("PREFERRED_URL_SCHEME", raising=False)
        assert _preferred_url_scheme("http") == "https"

    def test_optional_cookie_domain_helper(self, monkeypatch) -> None:
        from app.config import _env_optional_str

        monkeypatch.setenv("SESSION_COOKIE_DOMAIN", ".example.com")
        assert _env_optional_str("SESSION_COOKIE_DOMAIN") == ".example.com"
        monkeypatch.setenv("SESSION_COOKIE_DOMAIN", "  ")
        assert _env_optional_str("SESSION_COOKIE_DOMAIN") is None


class TestRobotsAndSitemap:
    def test_robots_and_sitemap_use_app_url(self, app, client) -> None:
        app.config["APP_URL"] = "https://app.example.com"
        robots = client.get("/robots.txt")
        assert robots.status_code == 200
        body = robots.get_data(as_text=True)
        assert "Sitemap: https://app.example.com/sitemap.xml" in body
        assert "Disallow: /console/" in body

        sitemap = client.get("/sitemap.xml")
        assert sitemap.status_code == 200
        xml = sitemap.get_data(as_text=True)
        assert "<loc>https://app.example.com/</loc>" in xml
        assert "<loc>https://app.example.com/auth/login</loc>" in xml

    def test_login_metadata_uses_app_url(self, app, client) -> None:
        app.config["APP_URL"] = "https://app.example.com"
        response = client.get("/auth/login")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'rel="canonical" href="https://app.example.com/auth/login"' in html
        assert 'property="og:url" content="https://app.example.com/auth/login"' in html
        assert "https://app.example.com/static/branding/social-preview.png" in html
        assert "favicon" in html


class TestExternalUrlGenerationUnderProxy:
    def test_url_for_external_uses_request_host(self, app) -> None:
        """When the request Host is the custom domain, absolute urls match it.

        On Render, ProxyFix copies ``X-Forwarded-Host`` into the WSGI host so
        ``url_for(..., _external=True)`` tracks the custom domain without
        setting Flask ``SERVER_NAME``.
        """
        app.config["PREFERRED_URL_SCHEME"] = "https"
        app.config["SERVER_NAME"] = None
        from flask import url_for

        with app.test_request_context(
            "/auth/login",
            base_url="https://app.example.com/",
        ):
            login = url_for("auth.login", _external=True)
            assert login.startswith("https://app.example.com/")


class TestAppUrlProductionWarning:
    def test_missing_app_url_warns_in_production(
        self, monkeypatch, caplog
    ) -> None:
        monkeypatch.setenv("SECRET_KEY", "a" * 32)
        monkeypatch.setenv(
            "DATABASE_URL", "postgresql+psycopg://u:p@localhost:5432/kwalitec"
        )
        monkeypatch.delenv("APP_URL", raising=False)

        from app import _validate_env_vars
        from app.config import ProductionConfig

        with caplog.at_level(logging.WARNING, logger="app"):
            _validate_env_vars(ProductionConfig)
        assert any("APP_URL is unset" in r.message for r in caplog.records)
