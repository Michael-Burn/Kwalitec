"""Port resolution helpers for Curriculum Studio services."""

from __future__ import annotations

from typing import Any

from app.application.curriculum_studio.exceptions import PortUnavailable
from app.application.curriculum_studio.ports.curriculum_ingestion_port import (
    CurriculumIngestionPort,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.application.curriculum_studio.ports.education_platform_port import (
    EducationPlatformPort,
)


def require_management(
    port: CurriculumManagementPort | None,
    *,
    action: str = "operation",
) -> CurriculumManagementPort:
    """Return Management port or raise PortUnavailable."""
    if port is None:
        raise PortUnavailable(
            f"Curriculum Management port required for {action}"
        )
    if not port.is_available():
        raise PortUnavailable(
            f"Curriculum Management port unavailable for {action}"
        )
    return port


def require_ingestion(
    port: CurriculumIngestionPort | None,
    *,
    action: str = "operation",
) -> CurriculumIngestionPort:
    """Return Ingestion port or raise PortUnavailable."""
    if port is None:
        raise PortUnavailable(
            f"Curriculum Ingestion port required for {action}"
        )
    if not port.is_available():
        raise PortUnavailable(
            f"Curriculum Ingestion port unavailable for {action}"
        )
    return port


def optional_platform(
    port: EducationPlatformPort | None,
) -> EducationPlatformPort | None:
    """Return platform port when injected and available, else None."""
    if port is None:
        return None
    try:
        if not port.is_available():
            return None
    except Exception:  # noqa: BLE001 — optional probe must not raise
        return None
    return port


def as_str(value: Any, default: str = "") -> str:
    """Coerce opaque port value to string."""
    if value is None:
        return default
    return str(value)


def as_bool(value: Any, default: bool = False) -> bool:
    """Coerce opaque port value to bool."""
    if value is None:
        return default
    return bool(value)
