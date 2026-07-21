"""Dashboard Flask adapter package."""

from __future__ import annotations

from adapters.flask.dashboard.controller import DashboardController
from adapters.flask.dashboard.dependency_provider import (
    AdapterDependencies,
    FlaskDependencyProvider,
    get_dependencies,
)
from adapters.flask.dashboard.routes import dashboard_bp, register_dashboard

__all__ = [
    "AdapterDependencies",
    "DashboardController",
    "FlaskDependencyProvider",
    "dashboard_bp",
    "get_dependencies",
    "register_dashboard",
]
