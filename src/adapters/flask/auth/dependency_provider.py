"""Auth adapter dependencies — injectable authentication collaborators."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from flask import Flask, current_app, g, has_app_context, has_request_context

from application.auth.auth_service import AuthenticationService

AUTH_DEPS_EXTENSION = "eos_auth_dependencies"
AUTH_DEPS_G_KEY = "eos_auth_dependencies"
AUTH_SESSION_KEY = "eos_auth_session"
AUTH_CSRF_SESSION_KEY = "eos_auth_csrf"


@dataclass(frozen=True, slots=True)
class AuthAdapterDependencies:
    """Collaborators for authentication HTTP handlers."""

    auth_service: AuthenticationService | None = None


class AuthDependencyProvider:
    """Resolve ``AuthAdapterDependencies`` from Flask context or overrides."""

    def __init__(self, dependencies: AuthAdapterDependencies | None = None) -> None:
        self._dependencies = dependencies or AuthAdapterDependencies()

    def override(self, **kwargs: Any) -> AuthAdapterDependencies:
        self._dependencies = replace(self._dependencies, **kwargs)
        return self._dependencies

    def resolve(self) -> AuthAdapterDependencies:
        if has_request_context():
            bound = getattr(g, AUTH_DEPS_G_KEY, None)
            if isinstance(bound, AuthAdapterDependencies):
                return bound
        if has_app_context():
            app_deps = current_app.extensions.get(AUTH_DEPS_EXTENSION)
            if isinstance(app_deps, AuthAdapterDependencies):
                return app_deps
        return self._dependencies

    @staticmethod
    def bind(app: Flask, dependencies: AuthAdapterDependencies) -> None:
        app.extensions[AUTH_DEPS_EXTENSION] = dependencies

    @staticmethod
    def bind_request(dependencies: AuthAdapterDependencies) -> None:
        if not has_request_context():
            raise RuntimeError("bind_request requires an active request context")
        setattr(g, AUTH_DEPS_G_KEY, dependencies)


def get_auth_dependencies() -> AuthAdapterDependencies:
    """Module-level convenience for route handlers."""
    return AuthDependencyProvider().resolve()
