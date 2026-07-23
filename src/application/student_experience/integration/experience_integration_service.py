"""ExperienceIntegrationService — continuous Student Experience journey (PX-002).

Orchestrates existing XP modules into one learning journey. Projection /
workflow only. Never estimates mastery, generates recommendations, generates
missions, schedules work, persists data, or invokes AI.
"""

from __future__ import annotations

from application.student_experience.coach.learning_coach_service import (
    LearningCoachService,
)
from application.student_experience.home.home_inputs import HomeInputs
from application.student_experience.home.models.primary_focus import PrimaryFocus
from application.student_experience.home.student_home_service import StudentHomeService
from application.student_experience.integration.enums import IntegrationTrigger
from application.student_experience.integration.ids import ExperienceBundleId
from application.student_experience.integration.integration_composer import (
    aligned_module_inputs,
    compose_experience,
)
from application.student_experience.integration.integration_inputs import (
    IntegrationInputs,
)
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
    ExperienceSnapshotBundle,
    IntegratedNextAction,
)
from application.student_experience.integration.navigation import (
    action_key_for_focus,
    next_action_from_focus,
)
from application.student_experience.integration.ports import (
    ExperienceIntegrationPublisher,
)
from application.student_experience.progress.learning_journey_service import (
    LearningJourneyService,
)
from application.student_experience.readiness.exam_readiness_service import (
    ExamReadinessService,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)
from application.student_experience.workspace.study_workspace_service import (
    StudyWorkspaceService,
)


class ExperienceIntegrationService:
    """Application service integrating XP modules into one continuous journey.

    Responsibilities
        Chain Home → Workspace → Reflection → Journey → Readiness → Coach → Home.
        Resolve state-aware primary CTAs.
        Refresh CoachContext automatically after mission completion.
        Surface readiness changes and empty/success states.

    Non-responsibilities
        Educational reasoning, domain capability changes, Education OS mutation.
    """

    def __init__(
        self,
        *,
        home_service: StudentHomeService | None = None,
        journey_service: LearningJourneyService | None = None,
        readiness_service: ExamReadinessService | None = None,
        workspace_service: StudyWorkspaceService | None = None,
        coach_service: LearningCoachService | None = None,
        publisher: ExperienceIntegrationPublisher | None = None,
    ) -> None:
        self._home = home_service or StudentHomeService()
        self._journey = journey_service or LearningJourneyService()
        self._readiness = readiness_service or ExamReadinessService()
        self._workspace = workspace_service or StudyWorkspaceService()
        self._coach = coach_service or LearningCoachService()
        self._publisher = publisher

    def build_experience(
        self,
        inputs: IntegrationInputs,
        *,
        bundle_id: ExperienceBundleId | str | None = None,
        trigger: IntegrationTrigger = IntegrationTrigger.HOME_VIEW,
    ) -> ExperienceJourneyViewModel:
        """Compose the continuous experience without publishing."""
        return compose_experience(
            inputs,
            bundle_id=self._resolve_bundle_id(inputs, bundle_id),
            trigger=trigger,
            home_service=self._home,
            journey_service=self._journey,
            readiness_service=self._readiness,
            workspace_service=self._workspace,
            coach_service=self._coach,
            publish=False,
        )

    def refresh_experience(
        self,
        inputs: IntegrationInputs,
        *,
        bundle_id: ExperienceBundleId | str | None = None,
        trigger: IntegrationTrigger = IntegrationTrigger.MANUAL_REFRESH,
    ) -> ExperienceJourneyViewModel:
        """Rebuild and publish the continuous experience when configured."""
        journey = compose_experience(
            inputs,
            bundle_id=self._resolve_bundle_id(inputs, bundle_id),
            trigger=trigger,
            home_service=self._home,
            journey_service=self._journey,
            readiness_service=self._readiness,
            workspace_service=self._workspace,
            coach_service=self._coach,
            publish=True,
        )
        self._publish(journey)
        return journey

    def refresh_after_mission_complete(
        self,
        inputs: IntegrationInputs,
        *,
        bundle_id: ExperienceBundleId | str | None = None,
        evidence_recorded: bool = True,
    ) -> ExperienceJourneyViewModel:
        """Run the post-mission continuous cascade.

        Workspace → Reflection → Evidence → Journey refresh → Readiness
        refresh → Coach celebration → Home refresh.

        Evidence capture remains the caller's responsibility; this method
        only projects and refreshes experience surfaces from supplied inputs.
        """
        cascade_inputs = IntegrationInputs(
            home=inputs.home,
            journey=inputs.journey,
            readiness=inputs.readiness,
            workspace=inputs.workspace,
            evaluation=inputs.evaluation,
            mission_plan=inputs.mission_plan,
            schedule=inputs.schedule,
            mission_execution=inputs.mission_execution,
            prior_readiness_snapshot=inputs.prior_readiness_snapshot,
            evidence_recorded=evidence_recorded or inputs.evidence_recorded,
        )
        return self.refresh_experience(
            cascade_inputs,
            bundle_id=bundle_id,
            trigger=IntegrationTrigger.MISSION_COMPLETE,
        )

    def refresh_after_reflection(
        self,
        inputs: IntegrationInputs,
        *,
        bundle_id: ExperienceBundleId | str | None = None,
    ) -> ExperienceJourneyViewModel:
        """Refresh the journey after reflection evidence is recorded."""
        cascade_inputs = IntegrationInputs(
            home=inputs.home,
            journey=inputs.journey,
            readiness=inputs.readiness,
            workspace=inputs.workspace,
            evaluation=inputs.evaluation,
            mission_plan=inputs.mission_plan,
            schedule=inputs.schedule,
            mission_execution=inputs.mission_execution,
            prior_readiness_snapshot=inputs.prior_readiness_snapshot,
            evidence_recorded=True,
        )
        return self.refresh_experience(
            cascade_inputs,
            bundle_id=bundle_id,
            trigger=IntegrationTrigger.REFLECTION_SUBMITTED,
        )

    def present_home(
        self,
        home_inputs: HomeInputs,
        *,
        prior_readiness_snapshot: ReadinessSnapshot | None = None,
        bundle_id: ExperienceBundleId | str | None = None,
    ) -> ExperienceJourneyViewModel:
        """Compose the continuous journey from HomeInputs (sibling inputs aligned)."""
        journey, readiness, workspace = aligned_module_inputs(home_inputs)
        inputs = IntegrationInputs(
            home=home_inputs,
            journey=journey,
            readiness=readiness,
            workspace=workspace,
            prior_readiness_snapshot=prior_readiness_snapshot,
        )
        return self.build_experience(
            inputs,
            bundle_id=bundle_id,
            trigger=IntegrationTrigger.HOME_VIEW,
        )

    def resolve_next_action(self, home_inputs: HomeInputs) -> IntegratedNextAction:
        """Resolve the state-aware primary CTA for the continuous journey."""
        focus = self._home.determine_primary_focus(home_inputs)
        return next_action_from_focus(focus)

    def resolve_primary_focus(self, home_inputs: HomeInputs) -> PrimaryFocus:
        """Expose PrimaryFocus for adapters that already consume home focus."""
        return self._home.determine_primary_focus(home_inputs)

    def action_key(self, home_inputs: HomeInputs) -> str:
        """Adapter navigation action key for the current primary CTA."""
        focus = self.resolve_primary_focus(home_inputs)
        return action_key_for_focus(focus.action_kind)

    def build_snapshot_bundle(
        self,
        journey: ExperienceJourneyViewModel,
    ) -> ExperienceSnapshotBundle:
        """Project a journey view model into a compact snapshot bundle."""
        return journey.to_snapshot_bundle()

    def _publish(self, journey: ExperienceJourneyViewModel) -> None:
        if self._publisher is None:
            return
        self._publisher.publish_journey(journey)
        self._publisher.publish_bundle(journey.to_snapshot_bundle())

    @staticmethod
    def _resolve_bundle_id(
        inputs: IntegrationInputs,
        bundle_id: ExperienceBundleId | str | None,
    ) -> ExperienceBundleId:
        if isinstance(bundle_id, ExperienceBundleId):
            return bundle_id
        if isinstance(bundle_id, str) and bundle_id.strip():
            return ExperienceBundleId(bundle_id.strip())
        stamp = inputs.as_of.strftime("%Y%m%dT%H%M%S")
        return ExperienceBundleId(f"xp-bundle:{inputs.student_id}:{stamp}")
