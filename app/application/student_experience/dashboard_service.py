"""DashboardService — aggregate student dashboard projection."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.student_experience._registry import ExperienceRegistry
from app.application.student_experience.dto.history_snapshot import HistorySnapshot
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.dto.journey_snapshot import JourneySnapshot
from app.application.student_experience.dto.profile_snapshot import ProfileSnapshot
from app.application.student_experience.dto.revision_snapshot import RevisionSnapshot
from app.application.student_experience.exceptions import (
    NavigationError,
    PortUnavailable,
    WorkspaceNotFound,
)
from app.application.student_experience.history_service import HistoryService
from app.application.student_experience.home_service import HomeService
from app.application.student_experience.journey_service import JourneyService
from app.application.student_experience.ports import PORT_NAMES
from app.application.student_experience.profile_service import ProfileService
from app.application.student_experience.revision_service import RevisionService
from app.domain.student_experience.experience_workspace import (
    CANONICAL_SURFACES,
    SURFACE_LABELS,
    ExperienceSurface,
    ExperienceWorkspace,
    resolve_surface,
)


@dataclass(frozen=True)
class NavigationItemSnapshot:
    """One navigation item for the student experience shell."""

    surface: str
    label: str
    active: bool = False


@dataclass(frozen=True)
class DashboardSnapshot:
    """Aggregate student dashboard: home + navigation + surface snapshots."""

    student_id: str
    workspace_id: str
    active_surface: str
    navigation: tuple[NavigationItemSnapshot, ...] = field(default_factory=tuple)
    home: HomeSnapshot | None = None
    journey: JourneySnapshot | None = None
    revision: RevisionSnapshot | None = None
    history: HistorySnapshot | None = None
    profile: ProfileSnapshot | None = None
    port_availability: tuple[tuple[str, bool], ...] = field(default_factory=tuple)
    learning_activity_status: str = ""


class DashboardService:
    """Compose the student dashboard from specialised projection services.

    Owns navigation / workspace presentation only.
    """

    def __init__(
        self,
        registry: ExperienceRegistry,
        *,
        home: HomeService,
        journey: JourneyService,
        revision: RevisionService,
        history: HistoryService,
        profile: ProfileService,
        ports: dict | None = None,
        orchestrator_status_loader=None,
    ) -> None:
        self._registry = registry
        self._home = home
        self._journey = journey
        self._revision = revision
        self._history = history
        self._profile = profile
        self._ports = dict(ports or {})
        self._orchestrator_status_loader = orchestrator_status_loader

    def open_workspace(
        self,
        student_id: str,
        *,
        workspace_id: str | None = None,
        examination_label: str = "",
        display_name: str = "",
    ) -> ExperienceWorkspace:
        """Open or reuse an experience workspace for ``student_id``."""
        existing = self._registry.get_workspace_for_student(student_id)
        if existing is not None and (
            workspace_id is None or existing.workspace_id == workspace_id
        ):
            return existing
        wid = (workspace_id or f"exp-{student_id}").strip()
        workspace = ExperienceWorkspace.create(
            wid,
            student_id,
            examination_label=examination_label,
            display_name=display_name,
        )
        self._registry.put_workspace(workspace)
        return workspace

    def navigate(
        self, workspace_id: str, surface: ExperienceSurface | str
    ) -> ExperienceWorkspace:
        """Navigate a workspace to ``surface``."""
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"workspace {workspace_id!r} not found")
        try:
            updated = workspace.navigate_to(surface)
        except ValueError as exc:
            raise NavigationError(str(exc)) from exc
        self._registry.put_workspace(updated)
        return updated

    def dashboard(
        self,
        student_id: str,
        *,
        workspace_id: str | None = None,
        surface: ExperienceSurface | str | None = None,
        include_all_surfaces: bool = False,
    ) -> DashboardSnapshot:
        """Build an aggregate student dashboard projection."""
        workspace = self.open_workspace(student_id, workspace_id=workspace_id)
        if surface is not None:
            workspace = self.navigate(workspace.workspace_id, surface)

        active = workspace.active_surface
        navigation = tuple(
            NavigationItemSnapshot(
                surface=s.value,
                label=SURFACE_LABELS[s],
                active=s is active,
            )
            for s in CANONICAL_SURFACES
        )

        home_snap = None
        journey_snap = None
        revision_snap = None
        history_snap = None
        profile_snap = None

        def _load(target: ExperienceSurface) -> None:
            nonlocal home_snap, journey_snap, revision_snap, history_snap, profile_snap
            if target is ExperienceSurface.HOME:
                home_snap = self._home.home(student_id)
            elif target is ExperienceSurface.JOURNEY:
                journey_snap = self._journey.journey(student_id)
            elif target is ExperienceSurface.REVISION:
                revision_snap = self._revision.revision(student_id)
            elif target is ExperienceSurface.HISTORY:
                history_snap = self._history.history(student_id)
            elif target is ExperienceSurface.PROFILE:
                profile_snap = self._profile.profile(student_id)

        if include_all_surfaces:
            for s in CANONICAL_SURFACES:
                _load(s)
        else:
            _load(active)

        activity_status = ""
        if self._orchestrator_status_loader is not None:
            try:
                activity_status = str(
                    self._orchestrator_status_loader(student_id) or ""
                )
            except Exception:  # noqa: BLE001 — presentation must not raise
                activity_status = ""

        availability = tuple(
            (name, _port_available(self._ports.get(name))) for name in PORT_NAMES
        )

        return DashboardSnapshot(
            student_id=student_id,
            workspace_id=workspace.workspace_id,
            active_surface=active.value,
            navigation=navigation,
            home=home_snap,
            journey=journey_snap,
            revision=revision_snap,
            history=history_snap,
            profile=profile_snap,
            port_availability=availability,
            learning_activity_status=activity_status,
        )


def _port_available(port: object | None) -> bool:
    if port is None:
        return False
    try:
        return bool(port.is_available())  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        return False


# Re-export resolve_surface for navigation callers.
__all__ = [
    "DashboardService",
    "DashboardSnapshot",
    "NavigationItemSnapshot",
    "PortUnavailable",
    "resolve_surface",
]
