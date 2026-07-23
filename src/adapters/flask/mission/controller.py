"""MissionController — HTTP orchestration for the Mission Workspace.

Thin application-adapter controller. Invokes the workspace presenter only.
No educational decisions, persistence, or AI.
"""

from __future__ import annotations

from adapters.flask.dashboard.dependency_provider import AdapterDependencies
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
)
from presentation.mission_workspace import (
    MissionWorkspaceViewModel,
    WorkspacePresenter,
)


class MissionController:
    """Present the mission workspace for one HTTP request."""

    def __init__(self, dependencies: AdapterDependencies) -> None:
        self._dependencies = dependencies

    def show(
        self,
        student_id: str | None = None,
        *,
        experience: ExperienceJourneyViewModel | object | None = None,
    ) -> MissionWorkspaceViewModel:
        """Load pipeline display cargo and present the mission workspace."""
        resolved_id = (student_id or "").strip()
        if not resolved_id:
            resolved_id = self._dependencies.student_id_resolver()
        result = self._dependencies.load_pipeline_result(resolved_id)
        resolved_experience = experience
        if resolved_experience is None:
            resolved_experience = self._dependencies.experience_gateway.get(
                resolved_id
            )
        return WorkspacePresenter.present(result, experience=resolved_experience)

    def current_experience(
        self, student_id: str | None = None
    ) -> ExperienceJourneyViewModel | None:
        """Expose the request-scoped experience snapshot for page chrome."""
        resolved_id = (student_id or "").strip()
        if not resolved_id:
            resolved_id = self._dependencies.student_id_resolver()
        return self._dependencies.experience_gateway.get(resolved_id)
