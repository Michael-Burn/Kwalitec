"""Session workspace — operational context for one Learning Session.

Owns presentation / navigation context only.
Never owns learner state, readiness, evidence, or educational decisions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class SessionSurface(StrEnum):
    """Linear Learning Session surfaces (workflow only — no branching)."""

    OVERVIEW = "overview"
    ACTIVITY = "activity"
    REFLECTION = "reflection"
    SUMMARY = "summary"
    COMPLETE = "complete"


class SessionWorkspaceStatus(StrEnum):
    """Lifecycle posture of a session experience workspace."""

    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"


CANONICAL_SURFACES: tuple[SessionSurface, ...] = (
    SessionSurface.OVERVIEW,
    SessionSurface.ACTIVITY,
    SessionSurface.REFLECTION,
    SessionSurface.SUMMARY,
    SessionSurface.COMPLETE,
)

SURFACE_LABELS: dict[SessionSurface, str] = {
    SessionSurface.OVERVIEW: "Session Overview",
    SessionSurface.ACTIVITY: "Learning Activity",
    SessionSurface.REFLECTION: "Reflection",
    SessionSurface.SUMMARY: "Session Summary",
    SessionSurface.COMPLETE: "Complete",
}


@dataclass(frozen=True)
class SessionWorkspace:
    """Focused study environment for one Learning Session.

    Owns presentation, workflow, projection, and navigation only.
    """

    workspace_id: str
    student_id: str
    session_id: str
    status: SessionWorkspaceStatus = SessionWorkspaceStatus.ACTIVE
    active_surface: SessionSurface = SessionSurface.OVERVIEW
    topic_title: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        workspace_id: str,
        student_id: str,
        session_id: str,
        *,
        status: SessionWorkspaceStatus | str = SessionWorkspaceStatus.ACTIVE,
        active_surface: SessionSurface | str = SessionSurface.OVERVIEW,
        topic_title: str = "",
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
    ) -> SessionWorkspace:
        """Construct a session workspace after validating identities."""
        return cls(
            workspace_id=_require_non_empty(workspace_id, "workspace_id"),
            student_id=_require_non_empty(student_id, "student_id"),
            session_id=_require_non_empty(session_id, "session_id"),
            status=_resolve_status(status),
            active_surface=_resolve_surface(active_surface),
            topic_title=(topic_title or "").strip(),
            metadata=tuple(metadata or ()),
        )

    def navigate_to(self, surface: SessionSurface | str) -> SessionWorkspace:
        """Return a copy focused on a different session surface."""
        resolved = _resolve_surface(surface)
        return SessionWorkspace(
            workspace_id=self.workspace_id,
            student_id=self.student_id,
            session_id=self.session_id,
            status=self.status,
            active_surface=resolved,
            topic_title=self.topic_title,
            metadata=self.metadata,
        )

    def with_status(
        self, status: SessionWorkspaceStatus | str
    ) -> SessionWorkspace:
        """Return a copy with updated workspace status."""
        return SessionWorkspace(
            workspace_id=self.workspace_id,
            student_id=self.student_id,
            session_id=self.session_id,
            status=_resolve_status(status),
            active_surface=self.active_surface,
            topic_title=self.topic_title,
            metadata=self.metadata,
        )

    def with_topic(self, topic_title: str) -> SessionWorkspace:
        """Return a copy with an updated topic title."""
        return SessionWorkspace(
            workspace_id=self.workspace_id,
            student_id=self.student_id,
            session_id=self.session_id,
            status=self.status,
            active_surface=self.active_surface,
            topic_title=(topic_title or "").strip(),
            metadata=self.metadata,
        )

    @property
    def active_surface_label(self) -> str:
        """Human label for the active surface."""
        return SURFACE_LABELS[self.active_surface]

    def is_on(self, surface: SessionSurface | str) -> bool:
        """True when the workspace is currently on ``surface``."""
        return self.active_surface is _resolve_surface(surface)


def resolve_surface(value: SessionSurface | str) -> SessionSurface:
    """Public resolver for session surfaces."""
    return _resolve_surface(value)


def surface_index(surface: SessionSurface | str) -> int:
    """Index of ``surface`` in the canonical linear flow order."""
    resolved = _resolve_surface(surface)
    return CANONICAL_SURFACES.index(resolved)


def is_canonical_surface(surface: SessionSurface | str) -> bool:
    """True when ``surface`` is one of the Learning Session surfaces."""
    try:
        _resolve_surface(surface)
        return True
    except ValueError:
        return False


def _resolve_surface(value: SessionSurface | str) -> SessionSurface:
    if isinstance(value, SessionSurface):
        return value
    key = str(value).strip().lower()
    try:
        return SessionSurface(key)
    except ValueError as exc:
        raise ValueError(f"unknown session surface: {value!r}") from exc


def _resolve_status(
    value: SessionWorkspaceStatus | str,
) -> SessionWorkspaceStatus:
    if isinstance(value, SessionWorkspaceStatus):
        return value
    return SessionWorkspaceStatus(str(value).strip().lower())


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
