"""Validate mission integrity rules for Mission Engine 2.0.

Ensures: exactly one active mission, valid session reference, valid journey
state, and curriculum topic availability. No educational reasoning.
"""

from __future__ import annotations

from app.application.learning_journey.dto.journey_snapshot import JourneySnapshot
from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.exceptions import (
    ActiveMissionExists,
    DuplicateMission,
    InvalidJourneyReference,
    InvalidSessionReference,
    TopicUnavailable,
)
from app.application.mission_engine_v2.lifecycle import MissionState
from app.application.mission_engine_v2.policies.workload_policy import WorkloadPolicy
from app.application.mission_engine_v2.ports.curriculum_navigation_port import (
    CurriculumNavigationPort,
)
from app.domain.learning_journey.value_objects.journey_state import JourneyState


class MissionValidator:
    """Mission integrity checks (stateless helpers + instance methods)."""

    VALID_JOURNEY_STATES = frozenset(
        {
            JourneyState.NOT_STARTED,
            JourneyState.ACTIVE,
            JourneyState.PAUSED,
            JourneyState.RESUMED,
            JourneyState.DEFERRED,
            JourneyState.READY_FOR_COMPLETION,
        }
    )

    def __init__(
        self,
        *,
        navigation: CurriculumNavigationPort | None = None,
    ) -> None:
        self._navigation = navigation

    def validate_no_duplicate(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        candidate: DailyMission,
    ) -> None:
        """Reject when learner+date+session already has an open mission."""
        for existing in missions:
            if existing.mission_id == candidate.mission_id:
                continue
            if existing.state in {MissionState.COMPLETED, MissionState.ARCHIVED}:
                continue
            if (
                existing.learner_id == candidate.learner_id
                and existing.scheduled_date == candidate.scheduled_date
                and existing.session_id == candidate.session_id
            ):
                raise DuplicateMission(
                    f"Duplicate mission for learner {candidate.learner_id} "
                    f"date {candidate.scheduled_date} session {candidate.session_id}"
                )

    def validate_one_active(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        activating_mission_id: str | None = None,
    ) -> None:
        """Reject when more than one ACTIVE/PAUSED mission would exist."""
        if not WorkloadPolicy.can_activate(
            missions,
            excluding_mission_id=activating_mission_id,
        ):
            raise ActiveMissionExists("Learner already has an active mission")

    def validate_session_reference(
        self,
        mission: DailyMission,
        snapshot: JourneySnapshot | None = None,
    ) -> None:
        """Ensure session_id is non-empty and consistent with snapshot when given."""
        if not mission.session_id or not mission.session_id.strip():
            raise InvalidSessionReference("Mission session_id is required")
        if snapshot is None:
            return
        if mission.journey_id != snapshot.journey_id:
            raise InvalidSessionReference(
                f"Mission journey {mission.journey_id} does not match "
                f"snapshot journey {snapshot.journey_id}"
            )
        known = {s.session_id for s in snapshot.sessions}
        if known and mission.session_id not in known:
            # Allow planned-but-not-yet-attached session ids from SessionPlan.
            if not mission.session_id.startswith("sess-"):
                raise InvalidSessionReference(
                    f"Session {mission.session_id} not found on journey "
                    f"{snapshot.journey_id}"
                )

    def validate_journey_state(
        self,
        snapshot: JourneySnapshot,
        *,
        allow_deferred: bool = True,
    ) -> None:
        """Ensure journey state permits mission scheduling."""
        if snapshot.state not in self.VALID_JOURNEY_STATES:
            raise InvalidJourneyReference(
                f"Journey {snapshot.journey_id} state {snapshot.state.value} "
                "cannot accept missions"
            )
        if not allow_deferred and snapshot.state == JourneyState.DEFERRED:
            raise InvalidJourneyReference(
                f"Journey {snapshot.journey_id} is deferred"
            )

    def validate_topic_available(self, topic_id: str) -> None:
        """Ensure curriculum topic is present when navigation is injected."""
        if self._navigation is None:
            return
        if not self._navigation.topic_available(topic_id):
            raise TopicUnavailable(
                f"Topic {topic_id} is not available in curriculum navigation"
            )

    def validate_mission_identity(self, mission: DailyMission) -> None:
        """Ensure required identity fields are present."""
        if not mission.mission_id:
            raise InvalidSessionReference("mission_id is required")
        if not mission.learner_id:
            raise InvalidJourneyReference("learner_id is required")
        if not mission.journey_id:
            raise InvalidJourneyReference("journey_id is required")
        if not mission.topic_id:
            raise InvalidJourneyReference("topic_id is required")

    def validate_new_mission(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        candidate: DailyMission,
        snapshot: JourneySnapshot | None = None,
    ) -> None:
        """Full validation gate before adding a mission to the ledger."""
        self.validate_mission_identity(candidate)
        self.validate_no_duplicate(missions, candidate)
        self.validate_topic_available(candidate.topic_id)
        if candidate.state in {MissionState.ACTIVE, MissionState.PAUSED}:
            self.validate_one_active(
                missions,
                activating_mission_id=candidate.mission_id,
            )
        if snapshot is not None:
            self.validate_journey_state(snapshot)
            self.validate_session_reference(candidate, snapshot)
