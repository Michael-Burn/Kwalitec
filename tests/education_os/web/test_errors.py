"""HTTP error mapping tests (WEB-001)."""

from __future__ import annotations

import pytest
from flask import Flask

from application.errors import ApplicationError, ConflictError, NotFoundError
from domain.education.foundation.errors import (
    EducationalDomainError,
    EducationalInvariantViolation,
)
from web.app import WebConfig, create_app


@pytest.fixture
def error_app(container) -> Flask:
    app = create_app(WebConfig(testing=True), container=container)

    @app.get("/_test/not-found")
    def trigger_not_found() -> None:
        raise NotFoundError("LearningEpisode", "episode-001")

    @app.get("/_test/conflict")
    def trigger_conflict() -> None:
        raise ConflictError("episode is not planned")

    @app.get("/_test/application")
    def trigger_application_error() -> None:
        raise ApplicationError("unsupported command")

    @app.get("/_test/domain")
    def trigger_domain_error() -> None:
        raise EducationalDomainError("invalid educational state")

    @app.get("/_test/invariant")
    def trigger_invariant_violation() -> None:
        raise EducationalInvariantViolation(
            "episode cannot start",
            invariant="episode_atomicity",
        )

    @app.get("/_test/unexpected")
    def trigger_unexpected_error() -> None:
        raise RuntimeError("boom")

    return app


@pytest.fixture
def error_client(error_app: Flask):
    return error_app.test_client()


@pytest.mark.parametrize(
    ("path", "status", "message"),
    [
        ("/_test/not-found", 404, "LearningEpisode not found: episode-001"),
        ("/_test/conflict", 409, "episode is not planned"),
        ("/_test/application", 400, "unsupported command"),
        ("/_test/domain", 422, "invalid educational state"),
        ("/_test/invariant", 422, "episode cannot start"),
    ],
)
def test_maps_known_errors_to_http_responses(
    error_client,
    path: str,
    status: int,
    message: str,
) -> None:
    response = error_client.get(path)

    assert response.status_code == status
    assert response.get_json() == {"error": message}


def test_maps_unexpected_errors_to_generic_internal_response(error_client) -> None:
    response = error_client.get("/_test/unexpected")

    assert response.status_code == 500
    assert response.get_json() == {"error": "internal server error"}
