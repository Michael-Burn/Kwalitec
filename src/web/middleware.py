"""HTTP middleware registration for the Education OS web layer."""

from __future__ import annotations

from flask import Flask

from web.errors import register_error_handlers
from web.lifecycle import register_request_lifecycle


def register_middleware(app: Flask) -> None:
    """Wire cross-cutting request behaviour for the Flask application."""
    register_request_lifecycle(app)
    register_error_handlers(app)
