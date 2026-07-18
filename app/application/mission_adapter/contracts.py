"""Engine contracts for the Mission Adapter.

The adapter depends only on these ports. It never instantiates Mission
Engine V1 or Mission Engine V2 directly — callers inject implementations.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot


@runtime_checkable
class MissionEnginePort(Protocol):
    """Structural contract every mission engine must satisfy.

    Implementations wrap Version 1 ``MissionService`` shapes or Mission
    Engine 2.0 facades. Educational reasoning stays inside those engines —
    this port only exposes lifecycle operations the adapter may route.
    """

    @property
    def engine_id(self) -> str:
        """Stable engine identity (e.g. ``v1``, ``v2``)."""

    @property
    def engine_version(self) -> str:
        """Version string for audit / comparison metadata."""

    def generate_mission(self, request: AdapterRequest) -> MissionSnapshot:
        """Generate a mission commitment from the request context."""

    def resume_mission(self, request: AdapterRequest) -> MissionSnapshot:
        """Resume a paused / in-progress mission."""

    def pause_mission(self, request: AdapterRequest) -> MissionSnapshot:
        """Pause an active mission without completing it."""

    def skip_mission(self, request: AdapterRequest) -> MissionSnapshot:
        """Skip a mission without completing its session."""

    def archive_mission(self, request: AdapterRequest) -> MissionSnapshot:
        """Archive a completed (or complete-and-archive) mission."""

    def is_available(self) -> bool:
        """True when the engine can accept work (health probe only)."""
