"""EducationPlatformAdapter — implements EducationPlatformPort."""

from __future__ import annotations

from typing import Any

from app.application.education_platform.platform import EducationPlatform
from app.infrastructure._opaque import opaque_dict
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics


class EducationPlatformAdapter:
    """Production adapter for EducationPlatformPort.

    Studio/Foundation consumers probe health and optional student-surface
    projections. Never publishes curriculum. Never invents next actions.
    """

    ADAPTER_ID = "education_platform"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        platform: EducationPlatform | None = None,
        *,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        student_surfaces: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self._platform = platform or EducationPlatform.create()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._surfaces = dict(student_surfaces or {})
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    def health(self) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        status = self._platform.health_status()
        return opaque_dict(status)

    def student_surface(
        self,
        *,
        subject_code: str,
        version_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Return a display-only student surface projection when registered."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        key = subject_code.strip().upper()
        surface = self._surfaces.get(key)
        if surface is None:
            return None
        payload = dict(surface)
        if version_id is not None:
            payload["version_id"] = version_id
        payload["subject_code"] = key
        payload["display_only"] = True
        return payload

    def register_student_surface(
        self, subject_code: str, surface: dict[str, Any]
    ) -> None:
        """Register a display-only surface (integration / test helper)."""
        self._surfaces[subject_code.strip().upper()] = dict(surface)
