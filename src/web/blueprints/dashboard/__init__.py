"""Dashboard API blueprint — thin HTTP surface over dashboard read models."""

from __future__ import annotations

from web.blueprints.dashboard.routes import dashboard_bp

__all__ = ["dashboard_bp"]
