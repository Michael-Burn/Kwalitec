"""ActivityPort — Learning Activity Engine contract for composition."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.application.education_platform.dto.education_request import EducationRequest


@runtime_checkable
class ActivityPort(Protocol):
    """Structural contract for Learning Activity Engine coordination.

    The composition layer may request activity id sequences for a session.
    Activity completion and evidence routing remain inside the engine.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``activity``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def plan_activity_ids(
        self,
        request: EducationRequest,
        *,
        session_id: str,
    ) -> tuple[str, ...]:
        """Return deterministic activity ids for the session context."""

    def is_available(self) -> bool:
        """True when the activity port can accept work."""
