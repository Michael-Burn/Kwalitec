"""LearningJourneyService — compose Education OS histories into Learning Journey.

Projection only. Never estimates mastery, generates recommendations,
generates missions, schedules work, persists data, or invokes AI.
"""

from __future__ import annotations

from application.student_experience.progress.ids import JourneyId, JourneySnapshotId
from application.student_experience.progress.journey_composer import (
    build_timeline,
    compose_journey,
    compose_snapshot,
    summarise_consistency,
    summarise_growth,
    summarise_habits,
)
from application.student_experience.progress.journey_inputs import JourneyInputs
from application.student_experience.progress.models.consistency_card import (
    ConsistencyCard,
)
from application.student_experience.progress.models.growth_card import GrowthCard
from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.progress.models.learning_journey_view_model import (
    LearningJourneyViewModel,
)
from application.student_experience.progress.models.study_habits_card import (
    StudyHabitsCard,
)
from application.student_experience.progress.models.timeline_card import TimelineCard
from application.student_experience.progress.ports.journey_export_provider import (
    JourneyExportProvider,
)
from application.student_experience.progress.ports.journey_publisher import (
    JourneyPublisher,
)
from application.student_experience.progress.ports.milestone_provider import (
    MilestoneProvider,
    ProvidedMilestone,
)


class LearningJourneyService:
    """Application service composing the Learning Journey Experience.

    Consumes Education OS history artefacts and optional presentation ports.
    Returns immutable view models suitable for UI binding.
    """

    def __init__(
        self,
        *,
        milestone_provider: MilestoneProvider | None = None,
        journey_publisher: JourneyPublisher | None = None,
        journey_export_provider: JourneyExportProvider | None = None,
    ) -> None:
        self._milestones = milestone_provider
        self._publisher = journey_publisher
        self._export = journey_export_provider

    def build_journey(
        self,
        inputs: JourneyInputs,
        *,
        journey_id: JourneyId | str | None = None,
    ) -> LearningJourneyViewModel:
        """Compose the full Learning Journey view model.

        Args:
            inputs: Caller-supplied Education OS histories and ``as_of`` time.
            journey_id: Optional identity for the composed journey. Defaults to
                a deterministic id derived from student and composition time.

        Returns:
            Immutable ``LearningJourneyViewModel``.
        """
        resolved_id = self._resolve_journey_id(inputs, journey_id)
        milestones = self._load_milestones(inputs.student_id)
        return compose_journey(
            inputs,
            journey_id=resolved_id,
            provided_milestones=milestones,
        )

    def build_timeline(self, inputs: JourneyInputs) -> TimelineCard:
        """Compose chronological educational events.

        Args:
            inputs: Caller-supplied Education OS histories.

        Returns:
            Immutable ``TimelineCard``.
        """
        return build_timeline(inputs)

    def summarise_growth(self, inputs: JourneyInputs) -> GrowthCard:
        """Summarise weekly and monthly growth from history.

        Args:
            inputs: Caller-supplied Education OS histories.

        Returns:
            Immutable ``GrowthCard``.
        """
        return summarise_growth(inputs)

    def summarise_habits(self, inputs: JourneyInputs) -> StudyHabitsCard:
        """Summarise deterministic study habits from history.

        Args:
            inputs: Caller-supplied Education OS histories.

        Returns:
            Immutable ``StudyHabitsCard``.
        """
        return summarise_habits(inputs)

    def summarise_consistency(self, inputs: JourneyInputs) -> ConsistencyCard:
        """Summarise streak and study consistency from history.

        Args:
            inputs: Caller-supplied Education OS histories.

        Returns:
            Immutable ``ConsistencyCard``.
        """
        return summarise_consistency(inputs)

    def build_snapshot(
        self,
        journey: LearningJourneyViewModel,
        *,
        snapshot_id: JourneySnapshotId | str | None = None,
        home_focus_headline: str | None = None,
    ) -> JourneySnapshot:
        """Project a composed journey into a compact snapshot.

        Args:
            journey: Previously composed ``LearningJourneyViewModel``.
            snapshot_id: Optional snapshot identity. Defaults to a
                deterministic id derived from the journey identity and time.
            home_focus_headline: Optional focus headline from the current home.

        Returns:
            Immutable ``JourneySnapshot``.
        """
        resolved = self._resolve_snapshot_id(journey, snapshot_id)
        return compose_snapshot(
            journey,
            snapshot_id=resolved,
            home_focus_headline=home_focus_headline,
        )

    def refresh_journey(
        self,
        inputs: JourneyInputs,
        *,
        journey_id: JourneyId | str | None = None,
    ) -> LearningJourneyViewModel:
        """Rebuild the journey view and publish it when a publisher is configured.

        Args:
            inputs: Caller-supplied Education OS histories and ``as_of`` time.
            journey_id: Optional identity for the composed journey.

        Returns:
            Freshly composed ``LearningJourneyViewModel``.
        """
        journey = self.build_journey(inputs, journey_id=journey_id)
        if self._publisher is not None:
            self._publisher.publish_journey(journey)
            home_headline = None
            if inputs.home_snapshot is not None:
                home_headline = inputs.home_snapshot.focus_headline
            snapshot = self.build_snapshot(
                journey,
                home_focus_headline=home_headline,
            )
            self._publisher.publish_snapshot(snapshot)
        return journey

    def export_journey(self, journey: LearningJourneyViewModel) -> str | None:
        """Export a journey when an export provider is configured; else ``None``."""
        if self._export is None:
            return None
        return self._export.export_journey(journey)

    def _load_milestones(self, student_id: str) -> tuple[ProvidedMilestone, ...]:
        if self._milestones is None:
            return ()
        return self._milestones.list_milestones(student_id)

    @staticmethod
    def _resolve_journey_id(
        inputs: JourneyInputs, journey_id: JourneyId | str | None
    ) -> JourneyId:
        if isinstance(journey_id, JourneyId):
            return journey_id
        if isinstance(journey_id, str) and journey_id.strip():
            return JourneyId(journey_id.strip())
        stamp = inputs.as_of.strftime("%Y%m%dT%H%M%S")
        return JourneyId(f"journey:{inputs.student_id}:{stamp}")

    @staticmethod
    def _resolve_snapshot_id(
        journey: LearningJourneyViewModel,
        snapshot_id: JourneySnapshotId | str | None,
    ) -> JourneySnapshotId:
        if isinstance(snapshot_id, JourneySnapshotId):
            return snapshot_id
        if isinstance(snapshot_id, str) and snapshot_id.strip():
            return JourneySnapshotId(snapshot_id.strip())
        stamp = journey.composed_at.strftime("%Y%m%dT%H%M%S")
        return JourneySnapshotId(f"jsnap:{journey.journey_id.value}:{stamp}")
