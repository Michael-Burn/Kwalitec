"""SessionPort — Learning Session Runtime contract for composition."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.generated_session import GeneratedSession


@runtime_checkable
class SessionPort(Protocol):
    """Structural contract for Learning Session Runtime coordination.

    The composition layer may plan session structures. Session lifecycle
    completion and reflection remain inside the runtime.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``session``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def plan_sessions(
        self,
        request: EducationRequest,
        *,
        journey_id: str,
        count: int = 1,
    ) -> tuple[GeneratedSession, ...]:
        """Return deterministic session plans for the journey context."""

    def is_available(self) -> bool:
        """True when the session port can accept work."""
