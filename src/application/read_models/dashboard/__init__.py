"""Dashboard read models and projection builders."""

from __future__ import annotations

from application.read_models.dashboard.dashboard_read_model import DashboardReadModel
from application.read_models.dashboard.projection_builder import (
    DashboardProjectionBuilder,
)

__all__ = [
    "DashboardProjectionBuilder",
    "DashboardReadModel",
]
