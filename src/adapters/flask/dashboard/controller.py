"""DashboardController — HTTP orchestration for Student Dashboard 2.0.

Thin application-adapter controller. Resolves display cargo, invokes the
dashboard presenter, and returns a view model. No educational decisions,
persistence, or AI.
"""

from __future__ import annotations

from adapters.flask.dashboard.dependency_provider import AdapterDependencies
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
)
from presentation.dashboard import DashboardPresenter, DashboardViewModel


class DashboardController:
    """Present the student command centre for one HTTP request."""

    def __init__(self, dependencies: AdapterDependencies) -> None:
        self._dependencies = dependencies

    def show(
        self,
        student_id: str | None = None,
        *,
        experience: ExperienceJourneyViewModel | object | None = None,
    ) -> DashboardViewModel:
        """Load pipeline display cargo and present the dashboard view model.

        Args:
            student_id: Optional learner identity. When omitted, uses the
                dependency-provided student_id_resolver.
            experience: Optional already-composed XP experience / snapshot
                bundle. When omitted, loads the request-scoped live experience
                via ``ExperienceGateway`` (composed at most once per request).

        Returns:
            Immutable ``DashboardViewModel`` ready for template mapping.
        """
        resolved_id = (student_id or "").strip()
        if not resolved_id:
            resolved_id = self._dependencies.student_id_resolver()
        result = self._dependencies.load_pipeline_result(resolved_id)
        resolved_experience = experience
        if resolved_experience is None:
            resolved_experience = self._dependencies.experience_gateway.get(
                resolved_id
            )
        return DashboardPresenter.present(result, experience=resolved_experience)

    def current_experience(
        self, student_id: str | None = None
    ) -> ExperienceJourneyViewModel | None:
        """Expose the request-scoped experience snapshot for page chrome."""
        resolved_id = (student_id or "").strip()
        if not resolved_id:
            resolved_id = self._dependencies.student_id_resolver()
        return self._dependencies.experience_gateway.get(resolved_id)
