"""Experience surface controllers — thin HTTP orchestration over the gateway."""

from __future__ import annotations

from adapters.flask.dashboard.dependency_provider import AdapterDependencies
from adapters.flask.experience.surface_presenter import (
    ExperienceSurfacePresenter,
    ExperienceSurfaceView,
)
from application.student_experience.integration.enums import JourneySurface
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
)
from presentation.dashboard import DashboardPresenter, DashboardViewModel
from presentation.mission_workspace import (
    MissionWorkspaceViewModel,
    WorkspacePresenter,
)


class ExperienceSurfaceController:
    """Present dedicated Home / Journey / Readiness / Coach surfaces."""

    def __init__(self, dependencies: AdapterDependencies) -> None:
        self._dependencies = dependencies

    def show_surface(
        self,
        surface: JourneySurface | str,
        student_id: str | None = None,
    ) -> tuple[ExperienceSurfaceView, ExperienceJourneyViewModel | None]:
        """Load the request-scoped experience and project one surface."""
        resolved = self._resolve_student_id(student_id)
        experience = self._dependencies.experience_gateway.get(resolved)
        result = self._dependencies.load_pipeline_result(resolved)
        view = ExperienceSurfacePresenter.present(
            experience, surface, result=result
        )
        return view, experience

    def show_home(
        self, student_id: str | None = None
    ) -> tuple[DashboardViewModel, ExperienceJourneyViewModel | None]:
        """Home surface — decision screen driven by the live experience."""
        resolved = self._resolve_student_id(student_id)
        experience = self._dependencies.experience_gateway.get(resolved)
        result = self._dependencies.load_pipeline_result(resolved)
        view = DashboardPresenter.present(result, experience=experience)
        return view, experience

    def show_workspace(
        self, student_id: str | None = None
    ) -> tuple[MissionWorkspaceViewModel, ExperienceJourneyViewModel | None]:
        """Workspace surface — mission page with shared experience snapshot."""
        resolved = self._resolve_student_id(student_id)
        experience = self._dependencies.experience_gateway.get(resolved)
        result = self._dependencies.load_pipeline_result(resolved)
        view = WorkspacePresenter.present(result, experience=experience)
        return view, experience

    def _resolve_student_id(self, student_id: str | None) -> str:
        resolved = (student_id or "").strip()
        if not resolved:
            resolved = self._dependencies.student_id_resolver()
        return resolved
