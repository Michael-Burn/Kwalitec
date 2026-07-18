"""Validate mission integrity rules for Mission Engine 2.0.

Ensures: no duplicates, one active mission, valid session/journey references.
No educational reasoning.
"""

from __future__ import annotations

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.exceptions import (
    ActiveMissionExists,
    DuplicateMission,
    InvalidJourneyReference,
    InvalidSessionReference,
)
from app.application.mission_engine.mission_state import MissionState
from app.application.mission_engine.policies.workload_policy import WorkloadPolicy
from app.domain.learning_journey.entities.learning_journey import LearningJourney
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

    def validate_no_duplicate(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        candidate: DailyMission,
    ) -> None:
        """Reject when learner+date+session already has an open mission."""
        for existing in missions:
            if existing.mission_id == candidate.mission_id:
                continue
            if existing.state in {
                MissionState.SKIPPED,
                MissionState.COMPLETED,
                MissionState.ARCHIVED,
            }:
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
        """Reject when more than one ACTIVE/IN_PROGRESS mission would exist."""
        if not WorkloadPolicy.can_activate(
            missions,
            excluding_mission_id=activating_mission_id,
        ):
            raise ActiveMissionExists(
                "Learner already has an active mission"
            )

    def validate_session_reference(
        self,
        mission: DailyMission,
        journey: LearningJourney | None = None,
    ) -> None:
        """Ensure session_id is non-empty and consistent with journey when given."""
        if not mission.session_id or not mission.session_id.strip():
            raise InvalidSessionReference("Mission session_id is required")
        if journey is None:
            return
        if mission.journey_id != journey.journey_id:
            raise InvalidSessionReference(
                f"Mission journey {mission.journey_id} does not match "
                f"provided journey {journey.journey_id}"
            )
        known = {s.session_id for s in journey.ordered_sessions()}
        if known and mission.session_id not in known:
            # Allow planned-but-not-yet-attached session ids from SessionPlan.
            if not mission.session_id.startswith("sess-"):
                raise InvalidSessionReference(
                    f"Session {mission.session_id} not found on journey "
                    f"{journey.journey_id}"
                )

    def validate_journey_state(
        self,
        journey: LearningJourney,
        *,
        allow_deferred: bool = True,
    ) -> None:
        """Ensure journey state permits mission scheduling."""
        if journey.state not in self.VALID_JOURNEY_STATES:
            raise InvalidJourneyReference(
                f"Journey {journey.journey_id} state {journey.state.value} "
                "cannot accept missions"
            )
        if (
            not allow_deferred
            and journey.state == JourneyState.DEFERRED
        ):
            raise InvalidJourneyReference(
                f"Journey {journey.journey_id} is deferred"
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
        journey: LearningJourney | None = None,
    ) -> None:
        """Full validation gate before adding a mission to the ledger."""
        self.validate_mission_identity(candidate)
        self.validate_no_duplicate(missions, candidate)
        if candidate.state in WorkloadPolicy.ACTIVE_STATES:
            self.validate_one_active(
                missions,
                activating_mission_id=candidate.mission_id,
            )
        if journey is not None:
            self.validate_journey_state(journey)
            self.validate_session_reference(candidate, journey)
