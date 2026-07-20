"""SessionExperienceService — public facade for Learning Session Experience."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar

from app.application.session_experience._registry import SessionExperienceRegistry
from app.application.session_experience.activity_service import ActivityService
from app.application.session_experience.completion_service import CompletionService
from app.application.session_experience.diagnostics import (
    DiagnosticReport,
    Diagnostics,
)
from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
)
from app.application.session_experience.dto.overview_snapshot import OverviewSnapshot
from app.application.session_experience.dto.progress_snapshot import ProgressSnapshot
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.application.session_experience.exceptions import (
    NavigationError,
    WorkspaceNotFound,
)
from app.application.session_experience.ports.activity_engine_port import (
    ActivityEnginePort,
)
from app.application.session_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.session_experience.ports.mission_port import MissionPort
from app.application.session_experience.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.application.session_experience.ports.student_twin_port import StudentTwinPort
from app.application.session_experience.progress_service import ProgressService
from app.application.session_experience.reflection_service import ReflectionService
from app.application.session_experience.session_service import SessionService
from app.domain.session_experience.session_navigation import (
    assert_linear_advance,
    next_surface,
)
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    SessionWorkspace,
)


@dataclass(frozen=True)
class SessionFlowSnapshot:
    """Composite snapshot for the active Learning Session surface."""

    workspace: SessionWorkspace
    surface: str
    overview: OverviewSnapshot | None = None
    activity: ActivitySnapshot | None = None
    progress: ProgressSnapshot | None = None
    reflection: ReflectionSnapshot | None = None
    completion: CompletionSnapshot | None = None
    next_surface: str | None = None


class SessionExperienceService:
    """Sole public application facade for Learning Session Experience.

    Owns workflow, navigation, presentation projections, and session state.
    Does not own learning decisions, evidence, readiness, missions,
    recommendations, or journey calculations.

    Production adapters are configured via :meth:`create` / the registered
    production builder (presentation / infrastructure composition root).
    Test doubles remain injectable through the constructor or ``create``.
    """

    _production_builder: ClassVar[
        Callable[[], SessionExperienceService] | None
    ] = None

    def __init__(
        self,
        *,
        session_runtime: SessionRuntimePort | None = None,
        activity_engine: ActivityEnginePort | None = None,
        mission: MissionPort | None = None,
        student_twin: StudentTwinPort | None = None,
        adaptive_decision: AdaptiveDecisionPort | None = None,
        registry: SessionExperienceRegistry | None = None,
    ) -> None:
        self._registry = registry or SessionExperienceRegistry()
        self._ports = {
            "session_runtime": session_runtime,
            "activity_engine": activity_engine,
            "mission": mission,
            "student_twin": student_twin,
            "adaptive_decision": adaptive_decision,
        }
        self._session = SessionService(
            session_runtime=session_runtime,
            mission=mission,
            registry=self._registry,
        )
        self._activity = ActivityService(
            activity_engine=activity_engine,
            session_runtime=session_runtime,
            registry=self._registry,
        )
        self._progress = ProgressService(
            session_runtime=session_runtime,
            activity_engine=activity_engine,
        )
        self._reflection = ReflectionService(
            session_runtime=session_runtime,
            registry=self._registry,
        )
        self._completion = CompletionService(
            session_runtime=session_runtime,
            student_twin=student_twin,
            adaptive_decision=adaptive_decision,
            registry=self._registry,
        )
        self._diagnostics = Diagnostics(
            registry=self._registry, ports=self._ports
        )

    @classmethod
    def set_production_builder(
        cls,
        builder: Callable[[], SessionExperienceService] | None,
    ) -> None:
        """Register the production composition builder (infrastructure / factory).

        Keeps the application package free of infrastructure imports while
        allowing ``create(use_production_adapters=True)`` during normal runs.
        """
        cls._production_builder = builder

    @classmethod
    def create(
        cls,
        *,
        session_runtime: SessionRuntimePort | None = None,
        activity_engine: ActivityEnginePort | None = None,
        mission: MissionPort | None = None,
        student_twin: StudentTwinPort | None = None,
        adaptive_decision: AdaptiveDecisionPort | None = None,
        registry: SessionExperienceRegistry | None = None,
        use_production_adapters: bool = True,
    ) -> SessionExperienceService:
        """Construct a facade with explicit ports or production adapters.

        Explicit port overrides always win. When no ports are provided and
        ``use_production_adapters`` is True, the registered production builder
        is used. Tests may pass ``use_production_adapters=False`` or inject
        doubles directly.
        """
        if any(
            port is not None
            for port in (
                session_runtime,
                activity_engine,
                mission,
                student_twin,
                adaptive_decision,
            )
        ):
            return cls(
                session_runtime=session_runtime,
                activity_engine=activity_engine,
                mission=mission,
                student_twin=student_twin,
                adaptive_decision=adaptive_decision,
                registry=registry,
            )
        if use_production_adapters and cls._production_builder is not None:
            return cls._production_builder()
        return cls(registry=registry)

    @property
    def session(self) -> SessionService:
        return self._session

    @property
    def activity(self) -> ActivityService:
        return self._activity

    @property
    def progress(self) -> ProgressService:
        return self._progress

    @property
    def reflection(self) -> ReflectionService:
        return self._reflection

    @property
    def completion(self) -> CompletionService:
        return self._completion

    @property
    def registry(self) -> SessionExperienceRegistry:
        return self._registry

    def open_session(
        self,
        student_id: str,
        *,
        session_id: str | None = None,
        mission_id: str | None = None,
    ) -> OverviewSnapshot:
        """Open Session Overview for today's Learning Session."""
        return self._session.open_session(
            student_id, session_id=session_id, mission_id=mission_id
        )

    def get_overview(
        self, student_id: str, *, session_id: str
    ) -> OverviewSnapshot:
        return self._session.overview(student_id, session_id=session_id)

    def begin_session(
        self, student_id: str, *, session_id: str
    ) -> OverviewSnapshot:
        return self._session.begin(student_id, session_id=session_id)

    def get_activity(
        self, student_id: str, *, session_id: str
    ) -> ActivitySnapshot:
        return self._activity.current(student_id, session_id=session_id)

    def submit_response(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> ActivitySnapshot:
        return self._activity.submit_response(
            student_id,
            session_id=session_id,
            activity_id=activity_id,
            response=response,
        )

    def advance_activity(
        self, student_id: str, *, session_id: str
    ) -> ActivitySnapshot | None:
        return self._activity.advance(student_id, session_id=session_id)

    def get_progress(
        self, student_id: str, *, session_id: str
    ) -> ProgressSnapshot:
        return self._progress.progress(student_id, session_id=session_id)

    def get_reflection(
        self, student_id: str, *, session_id: str
    ) -> ReflectionSnapshot:
        return self._reflection.reflection(student_id, session_id=session_id)

    def continue_from_reflection(
        self, student_id: str, *, session_id: str
    ) -> ReflectionSnapshot:
        return self._reflection.continue_to_summary(
            student_id, session_id=session_id
        )

    def get_summary(
        self, student_id: str, *, session_id: str
    ) -> CompletionSnapshot:
        return self._completion.summary(student_id, session_id=session_id)

    def complete_session(
        self, student_id: str, *, session_id: str
    ) -> CompletionSnapshot:
        return self._completion.complete(student_id, session_id=session_id)

    def navigate(
        self, session_id: str, surface: SessionSurface | str
    ) -> SessionWorkspace:
        """Advance one linear step to ``surface`` (no branching)."""
        workspace = self._registry.get_workspace_for_session(session_id)
        if workspace is None:
            raise WorkspaceNotFound(f"workspace not found for session {session_id}")
        try:
            assert_linear_advance(workspace.active_surface, surface)
        except ValueError as exc:
            raise NavigationError(str(exc)) from exc
        updated = workspace.navigate_to(surface)
        self._registry.put_workspace(updated)
        return updated

    def get_flow(
        self,
        student_id: str,
        *,
        session_id: str,
        surface: SessionSurface | str | None = None,
    ) -> SessionFlowSnapshot:
        """Assemble the active surface projection for presentation."""
        workspace = self._registry.get_workspace_for_session(session_id)
        if workspace is None:
            self.open_session(student_id, session_id=session_id)
            workspace = self._registry.get_workspace_for_session(session_id)
        if workspace is None:
            raise WorkspaceNotFound(f"workspace not found for session {session_id}")
        if surface is not None:
            target = SessionSurface(str(surface).strip().lower())
            if workspace.active_surface is not target:
                # get_flow renders the active workflow surface only.
                pass
        active = workspace.active_surface
        overview = activity = progress = reflection = completion = None
        if active is SessionSurface.OVERVIEW:
            overview = self.get_overview(student_id, session_id=session_id)
        elif active is SessionSurface.ACTIVITY:
            activity = self.get_activity(student_id, session_id=session_id)
            progress = self.get_progress(student_id, session_id=session_id)
        elif active is SessionSurface.REFLECTION:
            reflection = self.get_reflection(student_id, session_id=session_id)
        elif active is SessionSurface.SUMMARY:
            completion = self.get_summary(student_id, session_id=session_id)
        elif active is SessionSurface.COMPLETE:
            completion = self.get_summary(student_id, session_id=session_id)
        nxt = next_surface(active)
        return SessionFlowSnapshot(
            workspace=workspace,
            surface=active.value,
            overview=overview,
            activity=activity,
            progress=progress,
            reflection=reflection,
            completion=completion,
            next_surface=None if nxt is None else nxt.value,
        )

    def diagnostics(self) -> DiagnosticReport:
        """Return an immutable diagnostic report."""
        return self._diagnostics.report()
