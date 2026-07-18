"""Experience workspace — student operational context for the learning product.

A workspace is presentation / navigation context only.
It never owns learner state, readiness, or recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ExperienceSurface(StrEnum):
    """Primary student experience surfaces (navigation only)."""

    HOME = "home"
    JOURNEY = "journey"
    REVISION = "revision"
    HISTORY = "history"
    PROFILE = "profile"


class ExperienceWorkspaceStatus(StrEnum):
    """Lifecycle posture of a student experience workspace."""

    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"


CANONICAL_SURFACES: tuple[ExperienceSurface, ...] = (
    ExperienceSurface.HOME,
    ExperienceSurface.JOURNEY,
    ExperienceSurface.REVISION,
    ExperienceSurface.HISTORY,
    ExperienceSurface.PROFILE,
)

SURFACE_LABELS: dict[ExperienceSurface, str] = {
    ExperienceSurface.HOME: "Home",
    ExperienceSurface.JOURNEY: "Journey",
    ExperienceSurface.REVISION: "Revision",
    ExperienceSurface.HISTORY: "History",
    ExperienceSurface.PROFILE: "Profile",
}


@dataclass(frozen=True)
class ExperienceWorkspace:
    """Student-facing operational context for one learning product view.

    Owns presentation, workflow, projection, and navigation only.
    """

    workspace_id: str
    student_id: str
    examination_label: str = ""
    display_name: str = ""
    status: ExperienceWorkspaceStatus = ExperienceWorkspaceStatus.ACTIVE
    active_surface: ExperienceSurface = ExperienceSurface.HOME
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        workspace_id: str,
        student_id: str,
        *,
        examination_label: str = "",
        display_name: str = "",
        status: ExperienceWorkspaceStatus | str = ExperienceWorkspaceStatus.ACTIVE,
        active_surface: ExperienceSurface | str = ExperienceSurface.HOME,
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
    ) -> ExperienceWorkspace:
        """Construct a workspace after validating identities."""
        return cls(
            workspace_id=_require_non_empty(workspace_id, "workspace_id"),
            student_id=_require_non_empty(student_id, "student_id"),
            examination_label=(examination_label or "").strip(),
            display_name=(display_name or "").strip(),
            status=_resolve_status(status),
            active_surface=_resolve_surface(active_surface),
            metadata=tuple(metadata or ()),
        )

    def navigate_to(
        self, surface: ExperienceSurface | str
    ) -> ExperienceWorkspace:
        """Return a copy focused on a different experience surface."""
        resolved = _resolve_surface(surface)
        return ExperienceWorkspace(
            workspace_id=self.workspace_id,
            student_id=self.student_id,
            examination_label=self.examination_label,
            display_name=self.display_name,
            status=self.status,
            active_surface=resolved,
            metadata=self.metadata,
        )

    def with_status(
        self, status: ExperienceWorkspaceStatus | str
    ) -> ExperienceWorkspace:
        """Return a copy with updated workspace status."""
        return ExperienceWorkspace(
            workspace_id=self.workspace_id,
            student_id=self.student_id,
            examination_label=self.examination_label,
            display_name=self.display_name,
            status=_resolve_status(status),
            active_surface=self.active_surface,
            metadata=self.metadata,
        )

    def with_examination(self, examination_label: str) -> ExperienceWorkspace:
        """Return a copy with an updated examination label."""
        return ExperienceWorkspace(
            workspace_id=self.workspace_id,
            student_id=self.student_id,
            examination_label=(examination_label or "").strip(),
            display_name=self.display_name,
            status=self.status,
            active_surface=self.active_surface,
            metadata=self.metadata,
        )

    @property
    def active_surface_label(self) -> str:
        """Human label for the active surface."""
        return SURFACE_LABELS[self.active_surface]

    def is_on(self, surface: ExperienceSurface | str) -> bool:
        """True when the workspace is currently on ``surface``."""
        return self.active_surface is _resolve_surface(surface)


def resolve_surface(value: ExperienceSurface | str) -> ExperienceSurface:
    """Public resolver for experience surfaces."""
    return _resolve_surface(value)


def surface_index(surface: ExperienceSurface | str) -> int:
    """Index of ``surface`` in the canonical navigation order."""
    resolved = _resolve_surface(surface)
    return CANONICAL_SURFACES.index(resolved)


def is_canonical_surface(surface: ExperienceSurface | str) -> bool:
    """True when ``surface`` is one of the primary student surfaces."""
    try:
        _resolve_surface(surface)
        return True
    except ValueError:
        return False


def _resolve_surface(value: ExperienceSurface | str) -> ExperienceSurface:
    if isinstance(value, ExperienceSurface):
        return value
    key = str(value).strip().lower()
    try:
        return ExperienceSurface(key)
    except ValueError as exc:
        raise ValueError(f"unknown experience surface: {value!r}") from exc


def _resolve_status(
    value: ExperienceWorkspaceStatus | str,
) -> ExperienceWorkspaceStatus:
    if isinstance(value, ExperienceWorkspaceStatus):
        return value
    return ExperienceWorkspaceStatus(str(value).strip().lower())


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
