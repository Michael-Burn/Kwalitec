"""BlueprintPort — instructional structure reads for the composition layer."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.application.education_platform.dto.education_request import EducationRequest


@runtime_checkable
class BlueprintPort(Protocol):
    """Structural contract for Instructional Blueprint Engine reads.

    The composition layer may select / compile structural blueprints.
    It must never generate questions, explanations, or study prose.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``blueprint``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def select_blueprint_id(self, request: EducationRequest) -> str:
        """Return the selected blueprint id for the request context."""

    def estimate_session_count(self, request: EducationRequest) -> int:
        """Return expected session skeleton count (structural only)."""

    def is_available(self) -> bool:
        """True when the blueprint port can accept work."""
