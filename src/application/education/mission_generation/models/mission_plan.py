"""MissionPlan — immutable collection of executable missions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_generation.enums import MissionType
from application.education.mission_generation.errors import MissionInvariantViolation
from application.education.mission_generation.ids import MissionPlanId
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_constraint import (
    MissionConstraint,
)
from application.education.mission_generation.models.mission_snapshot import (
    MissionSnapshot,
)
from application.education.mission_generation.models.mission_summary import (
    MissionSummary,
)


@dataclass(frozen=True, slots=True)
class MissionPlan:
    """Immutable plan of executable learning missions.

    MissionPlan is the Adaptive Mission Generator's product: deterministic
    learning work derived from a RecommendationSet at one caller-supplied
    point in time. It never mutates after construction, never persists,
    never estimates mastery, and never modifies StudentEducationalState.
    """

    plan_id: MissionPlanId
    student_id: str
    source_recommendation_set_id: str
    generated_at: datetime
    missions: tuple[Mission, ...] = ()
    constraints: tuple[MissionConstraint, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.plan_id, MissionPlanId):
            raise MissionInvariantViolation(
                "plan_id must be a MissionPlanId",
                invariant="MissionPlan.plan_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise MissionInvariantViolation(
                "student_id must be a non-empty string",
                invariant="MissionPlan.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        source_id = (self.source_recommendation_set_id or "").strip()
        if not source_id:
            raise MissionInvariantViolation(
                "source_recommendation_set_id must be a non-empty string",
                invariant="MissionPlan.source_recommendation_set_id.required",
            )
        object.__setattr__(self, "source_recommendation_set_id", source_id)
        if not isinstance(self.generated_at, datetime):
            raise MissionInvariantViolation(
                "generated_at must be a datetime",
                invariant="MissionPlan.generated_at.type",
            )
        object.__setattr__(self, "missions", tuple(self.missions))
        for mission in self.missions:
            if not isinstance(mission, Mission):
                raise MissionInvariantViolation(
                    "missions must contain Mission values",
                    invariant="MissionPlan.missions.type",
                )
        object.__setattr__(self, "constraints", tuple(self.constraints))
        for constraint in self.constraints:
            if not isinstance(constraint, MissionConstraint):
                raise MissionInvariantViolation(
                    "constraints must contain MissionConstraint values",
                    invariant="MissionPlan.constraints.type",
                )

    def mission_count(self) -> int:
        return len(self.missions)

    def is_empty(self) -> bool:
        return not self.missions

    def highest_priority(self) -> Mission | None:
        if not self.missions:
            return None
        return self.missions[0]

    def missions_of_type(self, mission_type: MissionType) -> tuple[Mission, ...]:
        return tuple(m for m in self.missions if m.mission_type is mission_type)

    def total_duration_minutes(self) -> int:
        return sum(m.estimate.duration_minutes for m in self.missions)

    def produce_summary(self) -> MissionSummary:
        counts: dict[MissionType, int] = {}
        for mission in self.missions:
            counts[mission.mission_type] = counts.get(mission.mission_type, 0) + 1
        type_counts = tuple(
            sorted(counts.items(), key=lambda item: item[0].value)
        )
        highest = self.highest_priority()
        return MissionSummary(
            mission_count=len(self.missions),
            total_duration_minutes=self.total_duration_minutes(),
            prerequisite_mission_count=sum(
                1 for m in self.missions if m.is_prerequisite()
            ),
            maintenance_mission_count=sum(
                1 for m in self.missions if m.is_lightweight()
            ),
            type_counts=type_counts,
            highest_priority_mission_id=(
                highest.mission_id.value if highest is not None else None
            ),
        )

    def produce_snapshot(self) -> MissionSnapshot:
        return MissionSnapshot(
            plan_id=self.plan_id,
            student_id=self.student_id,
            source_recommendation_set_id=self.source_recommendation_set_id,
            generated_at=self.generated_at,
            missions=self.missions,
            constraints=self.constraints,
            summary=self.produce_summary(),
        )
