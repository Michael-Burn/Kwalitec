"""Login Flask adapter package."""

from __future__ import annotations

from adapters.flask.login.routes import login_bp, register_login

__all__ = [
    "login_bp",
    "register_login",
]
