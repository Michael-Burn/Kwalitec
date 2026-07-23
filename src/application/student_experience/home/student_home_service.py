"""StudentHomeService — compose Education OS outputs into the Student Home.

Projection only. Never estimates mastery, generates recommendations,
generates missions, schedules work, persists data, or invokes AI.
"""

from __future__ import annotations

from application.student_experience.home.home_composer import (
    compose_home,
    compose_snapshot,
    determine_primary_focus,
    summarise_progress,
)
from application.student_experience.home.home_inputs import HomeInputs
from application.student_experience.home.ids import HomeId, SnapshotId
from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.home.models.home_view_model import HomeViewModel
from application.student_experience.home.models.primary_focus import PrimaryFocus
from application.student_experience.home.models.progress_summary import ProgressSummary
from application.student_experience.home.ports.achievement_provider import (
    AchievementProvider,
    HomeAchievement,
)
from application.student_experience.home.ports.home_publisher import HomePublisher
from application.student_experience.home.ports.notification_provider import (
    HomeNotification,
    NotificationProvider,
)


class StudentHomeService:
    """Application service composing the Student Home Experience.

    Consumes existing Education OS artefacts and optional presentation ports.
    Returns immutable view models suitable for UI binding.
    """

    def __init__(
        self,
        *,
        notification_provider: NotificationProvider | None = None,
        achievement_provider: AchievementProvider | None = None,
        home_publisher: HomePublisher | None = None,
    ) -> None:
        self._notifications = notification_provider
        self._achievements = achievement_provider
        self._publisher = home_publisher

    def build_home(
        self,
        inputs: HomeInputs,
        *,
        home_id: HomeId | str | None = None,
    ) -> HomeViewModel:
        """Compose the full Student Home view model.

        Args:
            inputs: Caller-supplied Education OS artefacts and ``as_of`` time.
            home_id: Optional identity for the composed home. Defaults to a
                deterministic id derived from student and composition time.

        Returns:
            Immutable ``HomeViewModel``.
        """
        resolved_id = self._resolve_home_id(inputs, home_id)
        achievements = self._load_achievements(inputs.student_id)
        return compose_home(
            inputs,
            home_id=resolved_id,
            achievements=achievements,
        )

    def refresh_home(
        self,
        inputs: HomeInputs,
        *,
        home_id: HomeId | str | None = None,
    ) -> HomeViewModel:
        """Rebuild the home view and publish it when a publisher is configured.

        Args:
            inputs: Caller-supplied Education OS artefacts and ``as_of`` time.
            home_id: Optional identity for the composed home.

        Returns:
            Freshly composed ``HomeViewModel``.
        """
        home = self.build_home(inputs, home_id=home_id)
        if self._publisher is not None:
            self._publisher.publish_home(home)
            snapshot = self.build_snapshot(home)
            self._publisher.publish_snapshot(snapshot)
        return home

    def build_snapshot(
        self,
        home: HomeViewModel,
        *,
        snapshot_id: SnapshotId | str | None = None,
    ) -> HomeSnapshot:
        """Project a composed home into a compact snapshot.

        Args:
            home: Previously composed ``HomeViewModel``.
            snapshot_id: Optional snapshot identity. Defaults to a
                deterministic id derived from the home identity and time.

        Returns:
            Immutable ``HomeSnapshot``.
        """
        resolved = self._resolve_snapshot_id(home, snapshot_id)
        return compose_snapshot(home, snapshot_id=resolved)

    def summarise_progress(self, inputs: HomeInputs) -> ProgressSummary:
        """Summarise progress from available Education OS outputs.

        Args:
            inputs: Caller-supplied Education OS artefacts.

        Returns:
            Immutable ``ProgressSummary``.
        """
        return summarise_progress(inputs)

    def determine_primary_focus(self, inputs: HomeInputs) -> PrimaryFocus:
        """Determine the single primary focus for the student right now.

        Args:
            inputs: Caller-supplied Education OS artefacts.

        Returns:
            Immutable ``PrimaryFocus``.
        """
        return determine_primary_focus(inputs)

    def list_notifications(
        self, student_id: str, *, limit: int = 5
    ) -> tuple[HomeNotification, ...]:
        """Return notifications when a provider is configured; else empty."""
        if self._notifications is None:
            return ()
        return self._notifications.list_notifications(student_id, limit=limit)

    def _load_achievements(self, student_id: str) -> tuple[HomeAchievement, ...]:
        if self._achievements is None:
            return ()
        return self._achievements.list_achievements(student_id)

    @staticmethod
    def _resolve_home_id(
        inputs: HomeInputs, home_id: HomeId | str | None
    ) -> HomeId:
        if isinstance(home_id, HomeId):
            return home_id
        if isinstance(home_id, str) and home_id.strip():
            return HomeId(home_id.strip())
        stamp = inputs.as_of.strftime("%Y%m%dT%H%M%S")
        return HomeId(f"home:{inputs.student_id}:{stamp}")

    @staticmethod
    def _resolve_snapshot_id(
        home: HomeViewModel, snapshot_id: SnapshotId | str | None
    ) -> SnapshotId:
        if isinstance(snapshot_id, SnapshotId):
            return snapshot_id
        if isinstance(snapshot_id, str) and snapshot_id.strip():
            return SnapshotId(snapshot_id.strip())
        stamp = home.composed_at.strftime("%Y%m%dT%H%M%S")
        return SnapshotId(f"snap:{home.home_id.value}:{stamp}")
