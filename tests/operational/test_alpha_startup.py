"""Startup, health, logging, blueprint registration, and sole-runtime gate."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from tests.operational.helpers import (
    ALPHA_HTTP_ROUTES,
    REQUIRED_BLUEPRINTS,
    SESSION_SURFACE_ROUTES,
    alpha_flags,
)


def test_app_factory_creates_app(app):
    assert app is not None
    assert app.config["TESTING"] is True


def test_required_blueprints_registered(app):
    missing = [n for n in REQUIRED_BLUEPRINTS if n not in app.blueprints]
    assert missing == []


def test_alpha_routes_registered(app):
    rules = {r.rule for r in app.url_map.iter_rules()}
    missing = [rule for rule in ALPHA_HTTP_ROUTES if rule not in rules]
    assert missing == []


def test_session_surface_routes_registered(app):
    rules = {r.rule for r in app.url_map.iter_rules()}
    missing = [rule for rule in SESSION_SURFACE_ROUTES if rule not in rules]
    assert missing == []


def test_health_endpoint_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["database"] == "connected"
    assert "version" in payload
    assert "timestamp" in payload


def test_index_redirects_to_dashboard_without_sole_runtime(client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=alpha_flags(SOLE_RUNTIME=False),
    ):
        response = client.get("/")
    assert response.status_code in {302, 303}
    assert "/dashboard" in response.headers["Location"]


def test_index_redirects_to_student_when_sole_runtime(client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=alpha_flags(SOLE_RUNTIME=True),
    ):
        response = client.get("/")
    assert response.status_code in {302, 303}
    assert "/student" in response.headers["Location"]


def test_error_handlers_registered(app):
    assert 403 in app.error_handler_spec[None]
    assert 404 in app.error_handler_spec[None]


def test_logging_handlers_configured():
    import logging

    root = logging.getLogger()
    assert root.handlers


def test_security_headers_on_health(client):
    response = client.get("/health")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert "Content-Security-Policy" in response.headers


def test_static_asset_version_configured(app):
    assert app.config.get("STATIC_ASSET_VERSION")


def test_migrate_extension_present(app):
    assert "migrate" in app.extensions


def test_production_rejects_insecure_secret(monkeypatch):
    from app import create_app
    from app.config import ProductionConfig

    monkeypatch.setenv("SECRET_KEY", "change-me")
    monkeypatch.setenv("APP_ENV", "production")
    with pytest.raises(RuntimeError, match="Configuration validation failed"):
        create_app(ProductionConfig)
