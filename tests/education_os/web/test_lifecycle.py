"""Request lifecycle tests (WEB-001)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from application.composition import RequestScope
from application.services.learning_application_service import LearningApplicationService
from infrastructure.composition.factories import ApplicationServices
from web.app import WebConfig, create_app
from web.lifecycle import (
    dispose_unit_of_work,
    get_request_scope,
    get_services,
    get_unit_of_work,
    open_request_scope,
)


def test_request_scope_exposes_application_services(container, client) -> None:
    observed: list[type] = []

    @client.application.get("/_test/services")
    def probe_services() -> dict[str, str]:
        services = get_services()
        observed.append(type(services.learning))
        return {"service": type(services.learning).__name__}

    response = client.get("/_test/services")

    assert response.status_code == 200
    assert observed == [LearningApplicationService]


def test_request_scope_provides_unit_of_work(container, client) -> None:
    observed: list[bool] = []

    @client.application.get("/_test/uow")
    def probe_uow() -> dict[str, bool]:
        uow = get_unit_of_work()
        observed.append(uow is get_request_scope().unit_of_work)
        return {"same_scope": observed[-1]}

    response = client.get("/_test/uow")

    assert response.status_code == 200
    assert observed == [True]


def test_open_request_scope_builds_services(container) -> None:
    scope = open_request_scope(container)

    assert isinstance(scope, RequestScope)
    assert isinstance(scope.services, ApplicationServices)
    assert scope.unit_of_work is not None


def test_get_request_scope_outside_request_raises(container) -> None:
    app = create_app(WebConfig(testing=True), container=container)

    with app.app_context():
        with pytest.raises(RuntimeError, match="only available inside a request"):
            get_request_scope()


def test_unit_of_work_is_disposed_after_request(container) -> None:
    disposed: list[str] = []
    original_open = open_request_scope

    def tracking_open(active_container):
        scope = original_open(active_container)
        original_exit = scope.unit_of_work.__exit__

        def tracking_exit(*args, **kwargs):
            disposed.append("disposed")
            return original_exit(*args, **kwargs)

        scope.unit_of_work.__exit__ = tracking_exit  # type: ignore[method-assign]
        return scope

    app = create_app(WebConfig(testing=True), container=container)

    with patch("web.lifecycle.open_request_scope", tracking_open):
        client = app.test_client()
        response = client.get("/health")

    assert response.status_code == 200
    assert disposed == ["disposed"]


def test_dispose_unit_of_work_rolls_back_active_unit(container) -> None:
    scope = open_request_scope(container)
    scope.unit_of_work.begin()

    dispose_unit_of_work(scope.unit_of_work)

    assert scope.unit_of_work.is_active is False


def test_root_route_resolves_services_per_request(container, client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "service": "LearningApplicationService",
    }
