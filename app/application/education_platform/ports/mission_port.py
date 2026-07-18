"""MissionPort — Mission Engine / Adapter contract for composition."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.generated_mission import GeneratedMission


@runtime_checkable
class MissionPort(Protocol):
    """Structural contract for Mission Engine / Mission Adapter coordination.

    The composition layer may request daily mission structures. Educational
    reasoning and V1/V2 routing remain inside the mission bounded contexts.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``mission``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def generate_missions(
        self,
        request: EducationRequest,
        *,
        journey_id: str,
        session_id: str,
        topic_id: str,
    ) -> tuple[GeneratedMission, ...]:
        """Return deterministic mission structures for the request context."""

    def is_available(self) -> bool:
        """True when the mission port can accept work."""
