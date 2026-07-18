"""JourneyPort — Learning Journey Engine contract for composition."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.application.education_platform.dto.education_request import EducationRequest


@runtime_checkable
class JourneyPort(Protocol):
    """Structural contract for Learning Journey Engine coordination.

    The composition layer may create journey handles and read ids.
    Educational progression / Topic Complete remain inside the engine.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``journey``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def create_journey(self, request: EducationRequest) -> str:
        """Create (or resolve) a journey and return its journey_id."""

    def journey_exists(self, journey_id: str) -> bool:
        """True when ``journey_id`` is known to the engine."""

    def is_available(self) -> bool:
        """True when the journey port can accept work."""
