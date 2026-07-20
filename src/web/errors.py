"""HTTP error mapping for application and domain failures."""

from __future__ import annotations

from typing import Any

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from application.errors import ApplicationError, ConflictError, NotFoundError
from domain.education.foundation.errors import (
    EducationalDomainError,
    EducationalInvariantViolation,
)


def _json_error(message: str, *, status: int) -> tuple[Any, int]:
    return jsonify({"error": message}), status


def register_error_handlers(app: Flask) -> None:
    """Map application and domain errors to HTTP responses."""

    @app.errorhandler(NotFoundError)
    def handle_not_found(exc: NotFoundError) -> tuple[Any, int]:
        return _json_error(str(exc), status=404)

    @app.errorhandler(ConflictError)
    def handle_conflict(exc: ConflictError) -> tuple[Any, int]:
        return _json_error(str(exc), status=409)

    @app.errorhandler(ApplicationError)
    def handle_application_error(exc: ApplicationError) -> tuple[Any, int]:
        return _json_error(str(exc), status=400)

    @app.errorhandler(EducationalInvariantViolation)
    def handle_invariant_violation(
        exc: EducationalInvariantViolation,
    ) -> tuple[Any, int]:
        return _json_error(str(exc), status=422)

    @app.errorhandler(EducationalDomainError)
    def handle_domain_error(exc: EducationalDomainError) -> tuple[Any, int]:
        return _json_error(str(exc), status=422)

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException) -> tuple[Any, int]:
        message = exc.description or "request failed"
        return _json_error(message, status=exc.code or 500)

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception) -> tuple[Any, int]:
        app.logger.exception("unhandled request error")
        return _json_error("internal server error", status=500)
