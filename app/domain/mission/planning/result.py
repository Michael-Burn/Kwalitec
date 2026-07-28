"""PlanningResult — immutable output of Twin→Mission planning."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.mission.planning.batch import PlanningBatch
from app.domain.mission.planning.context import PlanningContext
from app.domain.mission.planning.events import (
    MissionGenerated,
    MissionPlanningCompleted,
    MissionPlanningSkipped,
    MissionPlanningStarted,
)
from app.domain.mission.planning.plan import StudyMissionPlan

PlanningEvent = (
    MissionPlanningStarted
    | MissionGenerated
    | MissionPlanningSkipped
    | MissionPlanningCompleted
)


@dataclass(frozen=True, slots=True)
class PlanningResult:
    """Complete planning outcome ready for Mission persistence / replay."""

    context: PlanningContext
    batch: PlanningBatch
    study_mission_plan: StudyMissionPlan
    planned_at: datetime
    events: tuple[PlanningEvent, ...] = ()

    def __post_init__(self) -> None:
        if self.context.reasoning_request_id != self.batch.context.reasoning_request_id:
            raise ValueError("reasoning_request_id mismatch")
        if self.context.evidence_bundle_id != self.batch.context.evidence_bundle_id:
            raise ValueError("evidence_bundle_id mismatch")
        if self.context.planning_version != self.batch.planning_version:
            raise ValueError("planning_version mismatch")
        if self.study_mission_plan.twin_id != self.context.twin_id:
            raise ValueError("study_mission_plan twin_id mismatch")
        object.__setattr__(self, "events", tuple(self.events or ()))

    @property
    def candidate_ids(self) -> tuple[str, ...]:
        return self.batch.candidate_ids

    @property
    def candidate_count(self) -> int:
        return len(self.batch)

    @property
    def generated_count(self) -> int:
        return sum(1 for e in self.events if isinstance(e, MissionGenerated))

    @property
    def skipped_count(self) -> int:
        return sum(1 for e in self.events if isinstance(e, MissionPlanningSkipped))

    @property
    def mission_id(self) -> str:
        return self.study_mission_plan.mission_id

    @property
    def plan_id(self) -> str:
        return self.study_mission_plan.plan_id
