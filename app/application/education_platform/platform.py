"""EducationPlatform — sole public interface to the Educational Core.

Everything outside the Educational Core communicates only with this facade.
Coordinates existing bounded contexts; owns NO educational rules.
"""

from __future__ import annotations

from app.application.education_platform.composition_root import CompositionRoot
from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.diagnostics import DiagnosticReport, Diagnostics
from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.education_response import EducationResponse
from app.application.education_platform.health_service import HealthService
from app.application.education_platform.orchestration_service import (
    OrchestrationService,
)
from app.application.education_platform.platform_validator import PlatformValidator
from app.application.education_platform.policies.orchestration_policy import (
    WORKFLOW_BUILD_PLATFORM_SNAPSHOT,
    WORKFLOW_GENERATE_DAILY_MISSIONS,
    WORKFLOW_GENERATE_JOURNEY,
    WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
    WORKFLOW_GENERATE_LEARNING_SESSIONS,
    WORKFLOW_GENERATE_SUBJECT,
    WORKFLOW_VALIDATE_PLATFORM,
)
from app.application.education_platform.ports.activity_port import ActivityPort
from app.application.education_platform.ports.blueprint_port import BlueprintPort
from app.application.education_platform.ports.curriculum_port import CurriculumPort
from app.application.education_platform.ports.journey_port import JourneyPort
from app.application.education_platform.ports.mission_port import MissionPort
from app.application.education_platform.ports.session_port import SessionPort
from app.application.education_platform.workflow_executor import WorkflowExecutor


class EducationPlatform:
    """Single public API for the composed Educational Core.

    Deterministic workflows only. No AI. No content generation.
    Framework-independent: no Flask, SQLAlchemy, or persistence.
    """

    PLATFORM_VERSION = "education-platform-1"

    def __init__(
        self,
        *,
        registry: DependencyRegistry,
        orchestration: OrchestrationService | None = None,
        validator: PlatformValidator | None = None,
        health: HealthService | None = None,
        diagnostics: Diagnostics | None = None,
        clock=None,
    ) -> None:
        self._registry = registry
        self._validator = validator or PlatformValidator()
        self._executor = WorkflowExecutor(validator=self._validator)
        self._orchestration = orchestration or OrchestrationService(
            registry=registry,
            executor=self._executor,
            validator=self._validator,
        )
        self._health = health or HealthService(
            registry=registry,
            platform_version=self.PLATFORM_VERSION,
            clock=clock,
        )
        self._diagnostics = diagnostics or Diagnostics(
            registry=registry,
            platform_version=self.PLATFORM_VERSION,
            validator=self._validator,
            clock=clock,
        )

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_registry(
        cls,
        registry: DependencyRegistry,
        *,
        clock=None,
    ) -> EducationPlatform:
        """Build a platform from an already-populated registry."""
        return cls(registry=registry, clock=clock)

    @classmethod
    def create(
        cls,
        *,
        curriculum: CurriculumPort | None = None,
        blueprint: BlueprintPort | None = None,
        journey: JourneyPort | None = None,
        session: SessionPort | None = None,
        activity: ActivityPort | None = None,
        mission: MissionPort | None = None,
        require_complete: bool = False,
        clock=None,
    ) -> EducationPlatform:
        """Assemble via CompositionRoot (dependency injection only)."""
        return CompositionRoot.assemble(
            curriculum=curriculum,
            blueprint=blueprint,
            journey=journey,
            session=session,
            activity=activity,
            mission=mission,
            require_complete=require_complete,
            clock=clock,
        )

    # ------------------------------------------------------------------
    # Registry access (for replacement / inspection)
    # ------------------------------------------------------------------

    @property
    def registry(self) -> DependencyRegistry:
        """Underlying dependency registry (ports only)."""
        return self._registry

    def replace_port(self, name: str, port: object) -> object | None:
        """Replace a registered port implementation; return previous."""
        return self._registry.replace(name, port)

    # ------------------------------------------------------------------
    # Workflows
    # ------------------------------------------------------------------

    def generate_subject(self, request: EducationRequest) -> EducationResponse:
        """Resolve a subject plan via the curriculum port."""
        return self._run(
            EducationRequest(
                workflow=WORKFLOW_GENERATE_SUBJECT,
                learner_id=request.learner_id,
                curriculum_id=request.curriculum_id,
                subject_id=request.subject_id,
                topic_id=request.topic_id,
                journey_id=request.journey_id,
                session_id=request.session_id,
                mission_id=request.mission_id,
                organisation_id=request.organisation_id,
                correlation_id=request.correlation_id,
                context=request.context,
            )
        )

    def generate_journey(self, request: EducationRequest) -> EducationResponse:
        """Coordinate curriculum → blueprint → journey creation."""
        return self._run(
            EducationRequest(
                workflow=WORKFLOW_GENERATE_JOURNEY,
                learner_id=request.learner_id,
                curriculum_id=request.curriculum_id,
                subject_id=request.subject_id,
                topic_id=request.topic_id,
                journey_id=request.journey_id,
                session_id=request.session_id,
                mission_id=request.mission_id,
                organisation_id=request.organisation_id,
                correlation_id=request.correlation_id,
                context=request.context,
            )
        )

    def generate_learning_sessions(
        self, request: EducationRequest
    ) -> EducationResponse:
        """Coordinate through session planning."""
        return self._run(
            EducationRequest(
                workflow=WORKFLOW_GENERATE_LEARNING_SESSIONS,
                learner_id=request.learner_id,
                curriculum_id=request.curriculum_id,
                subject_id=request.subject_id,
                topic_id=request.topic_id,
                journey_id=request.journey_id,
                session_id=request.session_id,
                mission_id=request.mission_id,
                organisation_id=request.organisation_id,
                correlation_id=request.correlation_id,
                context=request.context,
            )
        )

    def generate_learning_activities(
        self, request: EducationRequest
    ) -> EducationResponse:
        """Coordinate through activity planning inside sessions."""
        return self._run(
            EducationRequest(
                workflow=WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
                learner_id=request.learner_id,
                curriculum_id=request.curriculum_id,
                subject_id=request.subject_id,
                topic_id=request.topic_id,
                journey_id=request.journey_id,
                session_id=request.session_id,
                mission_id=request.mission_id,
                organisation_id=request.organisation_id,
                correlation_id=request.correlation_id,
                context=request.context,
            )
        )

    def generate_daily_missions(
        self, request: EducationRequest
    ) -> EducationResponse:
        """Coordinate the full Educational Core chain through missions."""
        return self._run(
            EducationRequest(
                workflow=WORKFLOW_GENERATE_DAILY_MISSIONS,
                learner_id=request.learner_id,
                curriculum_id=request.curriculum_id,
                subject_id=request.subject_id,
                topic_id=request.topic_id,
                journey_id=request.journey_id,
                session_id=request.session_id,
                mission_id=request.mission_id,
                organisation_id=request.organisation_id,
                correlation_id=request.correlation_id,
                context=request.context,
            )
        )

    def build_platform_snapshot(
        self, request: EducationRequest
    ) -> EducationResponse:
        """Build a read-only platform snapshot via full chain coordination."""
        return self._run(
            EducationRequest(
                workflow=WORKFLOW_BUILD_PLATFORM_SNAPSHOT,
                learner_id=request.learner_id,
                curriculum_id=request.curriculum_id,
                subject_id=request.subject_id,
                topic_id=request.topic_id,
                journey_id=request.journey_id,
                session_id=request.session_id,
                mission_id=request.mission_id,
                organisation_id=request.organisation_id,
                correlation_id=request.correlation_id,
                context=request.context,
            )
        )

    def validate_platform(
        self, request: EducationRequest | None = None
    ) -> EducationResponse:
        """Validate composition integrity (no educational reasoning)."""
        learner_id = request.learner_id if request else "system"
        correlation_id = request.correlation_id if request else None
        return self._run(
            EducationRequest(
                workflow=WORKFLOW_VALIDATE_PLATFORM,
                learner_id=learner_id,
                correlation_id=correlation_id,
            )
        )

    # ------------------------------------------------------------------
    # Health / diagnostics
    # ------------------------------------------------------------------

    def health_status(self) -> dict[str, object]:
        """Return read-only health (never mutates composition)."""
        return self._health.status()

    def diagnostics(self) -> DiagnosticReport:
        """Return an immutable diagnostic report."""
        return self._diagnostics.report()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _run(self, request: EducationRequest) -> EducationResponse:
        from app.application.education_platform.dto.workflow_result import (
            WorkflowResult,
        )
        from app.application.education_platform.exceptions import (
            EducationPlatformError,
        )

        try:
            response = self._orchestration.execute(request)
        except EducationPlatformError as exc:
            response = EducationResponse(
                workflow=request.workflow,
                success=False,
                request_correlation_id=request.correlation_id,
                workflow_result=WorkflowResult(
                    workflow=request.workflow,
                    success=False,
                    error=f"{type(exc).__name__}: {exc}",
                ),
                error=f"{type(exc).__name__}: {exc}",
            )
        if response.workflow_result is not None:
            self._diagnostics.record_workflow_timing(response.workflow_result)
        return response
