"""Application bootstrap tests (WEB-001)."""

from __future__ import annotations

from flask import Flask

from application.composition import ApplicationContainer
from web.app import WebConfig, create_app


def test_create_app_returns_flask_application(container) -> None:
    app = create_app(WebConfig(testing=True), container=container)

    assert isinstance(app, Flask)
    assert app.config["TESTING"] is True


def test_composition_root_is_loaded_on_startup(container) -> None:
    app = create_app(WebConfig(testing=True), container=container)

    assert "container" in app.extensions
    assert app.extensions["container"] is container
    assert isinstance(app.extensions["container"], ApplicationContainer)


def test_health_endpoint_reports_composition_root(container, client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["composition_root"] is True
    assert "version" in payload


def test_readiness_endpoint_reports_configuration(container, client) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ready"
    assert payload["composition_root"] is True
    assert payload["configuration_ok"] is True
    assert "pipeline_metrics" in payload


def test_register_blueprints_exposes_health_route(app) -> None:
    rules = {rule.rule for rule in app.url_map.iter_rules()}

    assert "/health" in rules
    assert "/health/ready" in rules


def test_create_app_loads_configuration_from_mapping(container) -> None:
    app = create_app(
        {
            "database_url": "sqlite+pysqlite:///:memory:",
            "secret_key": "mapped-secret",
            "testing": True,
        },
        container=container,
    )

    assert app.config["SECRET_KEY"] == "mapped-secret"
    assert app.config["TESTING"] is True
