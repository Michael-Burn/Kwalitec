"""Version 1 coexistence adapter for Mission Engine 2.0.

Parallel operation only. Does **not** replace ``MissionService``, does not
mutate Version 1 ORM rows, and must not be wired into production routes until
a dedicated migration milestone.

Translates structural fields between Version 1 mission shapes and Mission
Engine 2.0 DTOs so dual-run / reconciliation designs can compare artefacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from types import MappingProxyType

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.dto.mission_summary import MissionSummary
from app.application.mission_engine.mission_state import (
    DeliveryAction,
    MissionSlot,
    MissionState,
)
from app.application.mission_engine.policies.delivery_policy import DeliveryPolicy

# Version 1 Mission.status vocabulary (ORM string column).
V1_STATUS_PENDING = "Pending"
V1_STATUS_IN_PROGRESS = "In Progress"
V1_STATUS_COMPLETED = "Completed"


@dataclass(frozen=True)
class V1MissionView:
    """Framework-free structural view of a Version 1 mission.

    Mirrors the fields needed for dual-run comparison without importing
    SQLAlchemy models (keeps Mission Engine 2.0 framework-independent).
    """

    mission_id: str
    user_id: str
    subject_id: str
    mission_date: date
    title: str
    status: str
    study_plan_id: str | None = None
    task_count: int = 0
    completed_task_count: int = 0


class V1MissionAdapter:
    """Adapter between Version 1 mission views and Mission Engine 2.0 DTOs.

    Explicit non-responsibilities:
    - No ``MissionService`` calls
    - No ORM / Flask imports
    - No educational re-planning
    - No cutover / feature-flag activation
    """

    CUTOVER_STATUS = "parallel_only"
    ADAPTER_VERSION = "v1-mission-adapter-1"

    @staticmethod
    def cutover_status() -> str:
        """Documented coexistence mode (always parallel until migration)."""
        return V1MissionAdapter.CUTOVER_STATUS

    @staticmethod
    def map_v1_status_to_state(status: str) -> MissionState:
        """Map Version 1 status strings onto MissionState."""
        normalised = (status or "").strip().lower()
        if normalised in {"completed", "complete"}:
            return MissionState.COMPLETED
        if normalised in {"in progress", "in_progress", "active"}:
            return MissionState.IN_PROGRESS
        if normalised in {"skipped", "skip"}:
            return MissionState.SKIPPED
        return MissionState.SCHEDULED

    @staticmethod
    def map_state_to_v1_status(state: MissionState) -> str:
        """Map MissionState onto Version 1 status vocabulary."""
        if state in {MissionState.COMPLETED, MissionState.ARCHIVED}:
            return V1_STATUS_COMPLETED
        if state in {MissionState.ACTIVE, MissionState.IN_PROGRESS}:
            return V1_STATUS_IN_PROGRESS
        return V1_STATUS_PENDING

    def to_summary(
        self,
        view: V1MissionView,
        *,
        journey_id: str = "",
        session_id: str = "",
        topic_id: str = "",
        as_of_date: date | None = None,
    ) -> MissionSummary:
        """Project a Version 1 view into a MissionSummary for comparison.

        Missing journey/session/topic ids are left empty — callers that have
        dual-run correlation ids should supply them.
        """
        state = self.map_v1_status_to_state(view.status)
        day = as_of_date or view.mission_date
        slot = MissionSlot.TODAY if view.mission_date == day else MissionSlot.DEFERRED
        # Synthetic DailyMission for delivery policy reuse.
        synthetic = DailyMission(
            mission_id=f"v1-{view.mission_id}",
            learner_id=view.user_id,
            journey_id=journey_id or f"v1-journey-{view.study_plan_id or 'none'}",
            session_id=session_id or f"v1-session-{view.mission_id}",
            topic_id=topic_id or f"v1-subject-{view.subject_id}",
            curriculum_id="v1",
            scheduled_date=view.mission_date,
            slot=slot,
            state=state,
            objective_id=None,
            effort="medium",
            title=view.title,
            sequence_index=0,
            is_resume=state == MissionState.IN_PROGRESS,
            is_revision=False,
            created_at=datetime.now(tz=UTC),
        )
        action = DeliveryPolicy.decide(synthetic)
        return MissionSummary(
            mission_id=synthetic.mission_id,
            learner_id=synthetic.learner_id,
            journey_id=synthetic.journey_id,
            session_id=synthetic.session_id,
            topic_id=synthetic.topic_id,
            scheduled_date=synthetic.scheduled_date,
            slot=synthetic.slot,
            state=synthetic.state,
            title=synthetic.title,
            delivery_action=action,
            is_active=state in {MissionState.ACTIVE, MissionState.IN_PROGRESS},
            is_completed=state
            in {MissionState.COMPLETED, MissionState.ARCHIVED},
            is_resume=synthetic.is_resume,
            is_revision=False,
            objective_id=None,
            effort=synthetic.effort,
        )

    def to_v1_view(
        self,
        mission: DailyMission,
        *,
        subject_id: str = "unknown",
        study_plan_id: str | None = None,
    ) -> V1MissionView:
        """Project a DailyMission into a Version 1 structural view."""
        return V1MissionView(
            mission_id=mission.mission_id,
            user_id=mission.learner_id,
            subject_id=subject_id,
            mission_date=mission.scheduled_date,
            title=mission.title,
            status=self.map_state_to_v1_status(mission.state),
            study_plan_id=study_plan_id,
            task_count=1,
            completed_task_count=(
                1
                if mission.state
                in {MissionState.COMPLETED, MissionState.ARCHIVED}
                else 0
            ),
        )

    def reconciliation_payload(
        self,
        *,
        v1: V1MissionView | None,
        v2: DailyMission | None,
    ) -> MappingProxyType:
        """Build a read-only dual-run comparison map (no writes)."""
        data: dict[str, str] = {
            "adapter_version": self.ADAPTER_VERSION,
            "cutover_status": self.cutover_status(),
            "v1_present": "true" if v1 is not None else "false",
            "v2_present": "true" if v2 is not None else "false",
        }
        if v1 is not None:
            data["v1_mission_id"] = v1.mission_id
            data["v1_status"] = v1.status
            data["v1_date"] = v1.mission_date.isoformat()
            data["v1_title"] = v1.title
        if v2 is not None:
            data["v2_mission_id"] = v2.mission_id
            data["v2_state"] = v2.state.value
            data["v2_date"] = v2.scheduled_date.isoformat()
            data["v2_title"] = v2.title
            data["v2_session_id"] = v2.session_id
            data["v2_journey_id"] = v2.journey_id
        if v1 is not None and v2 is not None:
            data["dates_match"] = str(
                v1.mission_date == v2.scheduled_date
            ).lower()
            data["status_aligned"] = str(
                self.map_v1_status_to_state(v1.status) == v2.state
                or self.map_state_to_v1_status(v2.state) == v1.status
            ).lower()
        return MappingProxyType(data)

    @staticmethod
    def default_delivery_action_for_v1(status: str) -> DeliveryAction:
        """Map Version 1 status to a delivery action without UI."""
        state = V1MissionAdapter.map_v1_status_to_state(status)
        if state == MissionState.COMPLETED:
            return DeliveryAction.REVIEW
        if state == MissionState.IN_PROGRESS:
            return DeliveryAction.CONTINUE
        return DeliveryAction.TODAY
