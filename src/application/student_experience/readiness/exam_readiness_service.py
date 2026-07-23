"""ExamReadinessService — compose Education OS outputs into Exam Readiness.

Projection only. Never estimates mastery, generates recommendations,
generates missions, schedules work, persists data, forecasts exams, or
invokes AI.
"""

from __future__ import annotations

from application.student_experience.readiness.ids import (
    ReadinessId,
    ReadinessSnapshotId,
)
from application.student_experience.readiness.models.action_plan_card import (
    ActionPlanCard,
)
from application.student_experience.readiness.models.exam_readiness_view_model import (
    ExamReadinessViewModel,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)
from application.student_experience.readiness.models.risk_card import RiskCard
from application.student_experience.readiness.models.strength_card import StrengthCard
from application.student_experience.readiness.ports.readiness_export_provider import (
    ReadinessExportProvider,
)
from application.student_experience.readiness.ports.readiness_publisher import (
    ReadinessPublisher,
)
from application.student_experience.readiness.readiness_composer import (
    compose_action_plan,
    compose_readiness,
    compose_snapshot,
    summarise_risks,
    summarise_strengths,
)
from application.student_experience.readiness.readiness_inputs import ReadinessInputs


class ExamReadinessService:
    """Application service composing the Exam Readiness Experience.

    Consumes Education OS artefacts and optional presentation ports.
    Returns immutable view models suitable for UI binding.
    """

    def __init__(
        self,
        *,
        readiness_publisher: ReadinessPublisher | None = None,
        readiness_export_provider: ReadinessExportProvider | None = None,
    ) -> None:
        self._publisher = readiness_publisher
        self._export = readiness_export_provider

    def build_readiness(
        self,
        inputs: ReadinessInputs,
        *,
        readiness_id: ReadinessId | str | None = None,
    ) -> ExamReadinessViewModel:
        """Compose the full Exam Readiness view model.

        Args:
            inputs: Caller-supplied Education OS artefacts and ``as_of`` time.
            readiness_id: Optional identity for the composed readiness view.
                Defaults to a deterministic id derived from student and time.

        Returns:
            Immutable ``ExamReadinessViewModel``.
        """
        resolved_id = self._resolve_readiness_id(inputs, readiness_id)
        return compose_readiness(inputs, readiness_id=resolved_id)

    def summarise_strengths(self, inputs: ReadinessInputs) -> StrengthCard:
        """Summarise strengths from existing assessment and execution signals.

        Args:
            inputs: Caller-supplied Education OS artefacts.

        Returns:
            Immutable ``StrengthCard``.
        """
        return summarise_strengths(inputs)

    def summarise_risks(self, inputs: ReadinessInputs) -> RiskCard:
        """Summarise risks from existing gaps, schedule, and recommendations.

        Args:
            inputs: Caller-supplied Education OS artefacts.

        Returns:
            Immutable ``RiskCard``.
        """
        return summarise_risks(inputs)

    def compose_action_plan(self, inputs: ReadinessInputs) -> ActionPlanCard:
        """Compose deterministic guidance from existing recommendations.

        Args:
            inputs: Caller-supplied Education OS artefacts.

        Returns:
            Immutable ``ActionPlanCard``.
        """
        return compose_action_plan(inputs)

    def build_snapshot(
        self,
        readiness: ExamReadinessViewModel,
        *,
        snapshot_id: ReadinessSnapshotId | str | None = None,
        home_focus_headline: str | None = None,
        journey_trajectory_message: str | None = None,
    ) -> ReadinessSnapshot:
        """Project a composed readiness view into a compact snapshot.

        Args:
            readiness: Previously composed ``ExamReadinessViewModel``.
            snapshot_id: Optional snapshot identity. Defaults to a
                deterministic id derived from the readiness identity and time.
            home_focus_headline: Optional focus headline from the current home.
            journey_trajectory_message: Optional trajectory message from journey.

        Returns:
            Immutable ``ReadinessSnapshot``.
        """
        resolved = self._resolve_snapshot_id(readiness, snapshot_id)
        return compose_snapshot(
            readiness,
            snapshot_id=resolved,
            home_focus_headline=home_focus_headline,
            journey_trajectory_message=journey_trajectory_message,
        )

    def refresh_readiness(
        self,
        inputs: ReadinessInputs,
        *,
        readiness_id: ReadinessId | str | None = None,
    ) -> ExamReadinessViewModel:
        """Rebuild the readiness view and publish it when a publisher is configured.

        Args:
            inputs: Caller-supplied Education OS artefacts and ``as_of`` time.
            readiness_id: Optional identity for the composed readiness view.

        Returns:
            Freshly composed ``ExamReadinessViewModel``.
        """
        readiness = self.build_readiness(inputs, readiness_id=readiness_id)
        if self._publisher is not None:
            self._publisher.publish_readiness(readiness)
            home_headline = None
            if inputs.home_snapshot is not None:
                home_headline = inputs.home_snapshot.focus_headline
            journey_message = None
            if inputs.journey_snapshot is not None:
                journey_message = inputs.journey_snapshot.trajectory_message
            snapshot = self.build_snapshot(
                readiness,
                home_focus_headline=home_headline,
                journey_trajectory_message=journey_message,
            )
            self._publisher.publish_snapshot(snapshot)
        return readiness

    def export_readiness(self, readiness: ExamReadinessViewModel) -> str | None:
        """Export readiness when an export provider is configured; else ``None``."""
        if self._export is None:
            return None
        return self._export.export_readiness(readiness)

    @staticmethod
    def _resolve_readiness_id(
        inputs: ReadinessInputs, readiness_id: ReadinessId | str | None
    ) -> ReadinessId:
        if isinstance(readiness_id, ReadinessId):
            return readiness_id
        if isinstance(readiness_id, str) and readiness_id.strip():
            return ReadinessId(readiness_id.strip())
        stamp = inputs.as_of.strftime("%Y%m%dT%H%M%S")
        return ReadinessId(f"readiness:{inputs.student_id}:{stamp}")

    @staticmethod
    def _resolve_snapshot_id(
        readiness: ExamReadinessViewModel,
        snapshot_id: ReadinessSnapshotId | str | None,
    ) -> ReadinessSnapshotId:
        if isinstance(snapshot_id, ReadinessSnapshotId):
            return snapshot_id
        if isinstance(snapshot_id, str) and snapshot_id.strip():
            return ReadinessSnapshotId(snapshot_id.strip())
        stamp = readiness.composed_at.strftime("%Y%m%dT%H%M%S")
        return ReadinessSnapshotId(f"rsnap:{readiness.readiness_id.value}:{stamp}")
