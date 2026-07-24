"""StudentExperienceService — public facade for learner experience projections."""

from __future__ import annotations

from app.application.educational_state import EducationalStateService
from app.application.student_experience._registry import ExperienceRegistry
from app.application.student_experience.dashboard_service import (
    DashboardService,
    DashboardSnapshot,
)
from app.application.student_experience.diagnostics import (
    DiagnosticReport,
    Diagnostics,
)
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.history_snapshot import HistorySnapshot
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.dto.journey_snapshot import JourneySnapshot
from app.application.student_experience.dto.profile_snapshot import ProfileSnapshot
from app.application.student_experience.dto.revision_snapshot import RevisionSnapshot
from app.application.student_experience.exceptions import PortUnavailable
from app.application.student_experience.explanation_service import (
    ExplanationService,
)
from app.application.student_experience.history_service import HistoryService
from app.application.student_experience.home_service import HomeService
from app.application.student_experience.journey_service import JourneyService
from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.student_experience.ports.learning_journey_port import (
    LearningJourneyPort,
)
from app.application.student_experience.ports.learning_orchestrator_port import (
    LearningOrchestratorPort,
)
from app.application.student_experience.ports.mission_port import MissionPort
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.application.student_experience.profile_service import ProfileService
from app.application.student_experience.revision_service import RevisionService
from app.domain.student_experience.experience_session import (
    ExperienceSession,
    ExperienceSessionStatus,
)
from app.domain.student_experience.experience_workspace import (
    ExperienceSurface,
    ExperienceWorkspace,
)
from app.domain.student_experience.recommendation_explanation import (
    translate_to_student_language,
)


class StudentExperienceService:
    """Sole public application facade for Student Experience projections.

    Wires optional ports into specialised projection services.
    Framework-independent. No Flask, UI, or persistence.
    """

    def __init__(
        self,
        *,
        student_twin: StudentTwinPort | None = None,
        adaptive_decision: AdaptiveDecisionPort | None = None,
        mission: MissionPort | None = None,
        learning_journey: LearningJourneyPort | None = None,
        learning_orchestrator: LearningOrchestratorPort | None = None,
        registry: ExperienceRegistry | None = None,
    ) -> None:
        self._registry = registry or ExperienceRegistry()
        self._ports = {
            "student_twin": student_twin,
            "adaptive_decision": adaptive_decision,
            "mission": mission,
            "learning_journey": learning_journey,
            "learning_orchestrator": learning_orchestrator,
        }
        self._explanation = ExplanationService(
            adaptive_decision=adaptive_decision
        )
        self._educational_state = EducationalStateService(
            student_twin=student_twin,
            adaptive_decision=adaptive_decision,
            mission=mission,
            learning_journey=learning_journey,
        )
        self._home = HomeService(
            student_twin=student_twin,
            adaptive_decision=adaptive_decision,
            mission=mission,
            explanation=self._explanation,
            educational_state=self._educational_state,
        )
        self._journey = JourneyService(
            learning_journey=learning_journey,
            educational_state=self._educational_state,
        )
        self._revision = RevisionService(
            adaptive_decision=adaptive_decision,
            explanation=self._explanation,
            educational_state=self._educational_state,
        )
        self._history = HistoryService(
            student_twin=student_twin,
            educational_state=self._educational_state,
        )
        self._profile = ProfileService(
            student_twin=student_twin,
            educational_state=self._educational_state,
        )
        self._dashboard = DashboardService(
            self._registry,
            home=self._home,
            journey=self._journey,
            revision=self._revision,
            history=self._history,
            profile=self._profile,
            ports=self._ports,
            orchestrator_status_loader=self._activity_status,
        )
        self._diagnostics = Diagnostics(
            registry=self._registry, ports=self._ports
        )

    @property
    def home(self) -> HomeService:
        return self._home

    @property
    def journey(self) -> JourneyService:
        return self._journey

    @property
    def revision(self) -> RevisionService:
        return self._revision

    @property
    def history(self) -> HistoryService:
        return self._history

    @property
    def profile(self) -> ProfileService:
        return self._profile

    @property
    def explanation(self) -> ExplanationService:
        return self._explanation

    @property
    def dashboard(self) -> DashboardService:
        return self._dashboard

    @property
    def registry(self) -> ExperienceRegistry:
        return self._registry

    def open_workspace(
        self,
        student_id: str,
        *,
        workspace_id: str | None = None,
        examination_label: str = "",
        display_name: str = "",
    ) -> ExperienceWorkspace:
        """Open a student experience workspace."""
        return self._dashboard.open_workspace(
            student_id,
            workspace_id=workspace_id,
            examination_label=examination_label,
            display_name=display_name,
        )

    def navigate(
        self, workspace_id: str, surface: ExperienceSurface | str
    ) -> ExperienceWorkspace:
        """Navigate to an experience surface."""
        return self._dashboard.navigate(workspace_id, surface)

    def get_home(self, student_id: str) -> HomeSnapshot:
        return self._home.home(student_id)

    def get_journey(self, student_id: str) -> JourneySnapshot:
        return self._journey.journey(student_id)

    def get_revision(self, student_id: str) -> RevisionSnapshot:
        return self._revision.revision(student_id)

    def get_history(self, student_id: str) -> HistorySnapshot:
        return self._history.history(student_id)

    def get_profile(self, student_id: str) -> ProfileSnapshot:
        return self._profile.profile(student_id)

    def explain(
        self, student_id: str, *, decision_id: str | None = None
    ) -> ExplanationSnapshot:
        return self._explanation.explain_recommendation(
            student_id, decision_id=decision_id
        )

    def get_dashboard(
        self,
        student_id: str,
        *,
        surface: ExperienceSurface | str | None = None,
        include_all_surfaces: bool = False,
    ) -> DashboardSnapshot:
        return self._dashboard.dashboard(
            student_id,
            surface=surface,
            include_all_surfaces=include_all_surfaces,
        )

    def start_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
    ) -> ExperienceSession:
        """Request Today's Session start via Mission port; return UX handle."""
        mission = self._ports.get("mission")
        if mission is None or not mission.is_available():
            raise PortUnavailable("mission port unavailable")
        result = mission.start_session(
            student_id, mission_id=mission_id, session_id=session_id
        )
        session_key = (
            result.get("experience_session_id")
            or result.get("session_id")
            or f"es-{student_id}"
        )
        handle = ExperienceSession.create(
            str(session_key),
            student_id,
            status=ExperienceSessionStatus.IN_PROGRESS,
            mission_id=(
                None
                if result.get("mission_id") is None
                else str(result.get("mission_id"))
            )
            or mission_id,
            session_id=(
                None
                if result.get("session_id") is None
                else str(result.get("session_id"))
            )
            or session_id,
            topic_title=translate_to_student_language(
                str(result.get("topic_title") or "")
            ),
            estimated_minutes=(
                None
                if result.get("estimated_minutes") is None
                else int(result["estimated_minutes"])
            ),
            started_at=str(result.get("started_at") or ""),
        )
        self._registry.put_session(handle)
        return handle

    def diagnostics(self) -> DiagnosticReport:
        """Return an immutable diagnostic report."""
        return self._diagnostics.report()

    def _activity_status(self, student_id: str) -> str:
        orch = self._ports.get("learning_orchestrator")
        if orch is None or not orch.is_available():
            return ""
        status = orch.get_activity_status(student_id) or {}
        return translate_to_student_language(
            str(status.get("status_label") or status.get("status") or "")
        )
