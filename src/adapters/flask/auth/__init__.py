"""Flask authentication adapter — production identity surface.

Thin HTTP adapters over framework-independent authentication services.
"""

from __future__ import annotations

from adapters.flask.auth.controller import AuthController
from adapters.flask.auth.dependency_provider import (
    AUTH_SESSION_KEY,
    AuthAdapterDependencies,
    AuthDependencyProvider,
    get_auth_dependencies,
)
from adapters.flask.auth.factory import build_authentication_service
from adapters.flask.auth.secure_cookies import apply_secure_cookie_config

# Routes are imported lazily by register_auth / wiring to avoid circular imports
# with adapters.flask package initialisation.


def __getattr__(name: str):
    if name in {"auth_bp", "register_auth"}:
        from adapters.flask.auth.routes import auth_bp, register_auth

        if name == "auth_bp":
            return auth_bp
        return register_auth
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "AUTH_SESSION_KEY",
    "AuthAdapterDependencies",
    "AuthController",
    "AuthDependencyProvider",
    "apply_secure_cookie_config",
    "auth_bp",
    "build_authentication_service",
    "get_auth_dependencies",
    "register_auth",
]
