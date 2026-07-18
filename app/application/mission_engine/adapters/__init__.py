"""Adapters for Version 1 coexistence with Mission Engine 2.0.

Parallel operation only until a dedicated migration milestone.
"""

from __future__ import annotations

from app.application.mission_engine.adapters.v1_mission_adapter import (
    V1MissionAdapter,
    V1MissionView,
)

__all__ = [
    "V1MissionAdapter",
    "V1MissionView",
]
