"""Request-scoped dependency lifecycle for the web layer."""

from __future__ import annotations

from types import TracebackType

from flask import Flask, g, has_request_context

from application.composition import (
    ApplicationContainer,
    RequestScope,
    create_request_scope,
)
from application.ports.unit_of_work import UnitOfWork
from infrastructure.composition.factories import ApplicationServices

REQUEST_SCOPE_KEY = "education_os_request_scope"


def open_request_scope(container: ApplicationContainer) -> RequestScope:
    """Create a request-scoped unit of work and application services."""
    return create_request_scope(container)


def dispose_unit_of_work(
    unit_of_work: UnitOfWork,
    exc_type: type[BaseException] | None = None,
    exc: BaseException | None = None,
    tb: TracebackType | None = None,
) -> None:
    """Release resources held by a request-scoped unit of work."""
    unit_of_work.__exit__(exc_type, exc, tb)


def bind_request_scope(scope: RequestScope) -> None:
    """Attach the request scope to the active Flask request context."""
    setattr(g, REQUEST_SCOPE_KEY, scope)


def clear_request_scope(
    exc: BaseException | None = None,
) -> RequestScope | None:
    """Remove and return the active request scope, if present."""
    scope = getattr(g, REQUEST_SCOPE_KEY, None)
    if scope is not None:
        delattr(g, REQUEST_SCOPE_KEY)
    return scope


def get_request_scope() -> RequestScope:
    """Return the active request scope or raise when outside a request."""
    if not has_request_context():
        raise RuntimeError("request scope is only available inside a request")
    scope = getattr(g, REQUEST_SCOPE_KEY, None)
    if scope is None:
        raise RuntimeError("request scope has not been initialised")
    return scope


def get_services() -> ApplicationServices:
    """Return application services for the active request."""
    return get_request_scope().services


def get_unit_of_work() -> UnitOfWork:
    """Return the unit of work for the active request."""
    return get_request_scope().unit_of_work


def register_request_lifecycle(app: Flask) -> None:
    """Open and dispose request-scoped dependencies around each HTTP request."""

    @app.before_request
    def _open_request_scope() -> None:
        container: ApplicationContainer = app.extensions["container"]
        bind_request_scope(open_request_scope(container))

    @app.teardown_request
    def _close_request_scope(exc: BaseException | None) -> None:
        scope = clear_request_scope(exc)
        if scope is None:
            return
        exc_type = type(exc) if exc is not None else None
        dispose_unit_of_work(scope.unit_of_work, exc_type, exc, None)
