"""MissionSnapshot — immutable mirror of a MissionPlan."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_generation.errors import MissionInvariantViolation
from application.education.mission_generation.ids import MissionPlanId
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_constraint import (
    MissionConstraint,
)
from application.education.mission_generation.models.mission_summary import (
    MissionSummary,
)


@dataclass(frozen=True, slots=True)
class MissionSnapshot:
    """Immutable, accurate capture of a MissionPlan.

    A snapshot is a read model. It does not re-generate or recompute — it
    faithfully mirrors the plan at the moment it was produced.
    """

    plan_id: MissionPlanId
    student_id: str
    source_recommendation_set_id: str
    generated_at: datetime
    missions: tuple[Mission, ...]
    constraints: tuple[MissionConstraint, ...]
    summary: MissionSummary

    def __post_init__(self) -> None:
        if not isinstance(self.plan_id, MissionPlanId):
            raise MissionInvariantViolation(
                "plan_id must be a MissionPlanId",
                invariant="MissionSnapshot.plan_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise MissionInvariantViolation(
                "student_id must be a non-empty string",
                invariant="MissionSnapshot.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        source_id = (self.source_recommendation_set_id or "").strip()
        if not source_id:
            raise MissionInvariantViolation(
                "source_recommendation_set_id must be a non-empty string",
                invariant="MissionSnapshot.source_recommendation_set_id.required",
            )
        object.__setattr__(self, "source_recommendation_set_id", source_id)
        if not isinstance(self.generated_at, datetime):
            raise MissionInvariantViolation(
                "generated_at must be a datetime",
                invariant="MissionSnapshot.generated_at.type",
            )
        object.__setattr__(self, "missions", tuple(self.missions))
        for mission in self.missions:
            if not isinstance(mission, Mission):
                raise MissionInvariantViolation(
                    "missions must contain Mission values",
                    invariant="MissionSnapshot.missions.type",
                )
        object.__setattr__(self, "constraints", tuple(self.constraints))
        for constraint in self.constraints:
            if not isinstance(constraint, MissionConstraint):
                raise MissionInvariantViolation(
                    "constraints must contain MissionConstraint values",
                    invariant="MissionSnapshot.constraints.type",
                )
        if not isinstance(self.summary, MissionSummary):
            raise MissionInvariantViolation(
                "summary must be a MissionSummary",
                invariant="MissionSnapshot.summary.type",
            )

    def mission_count(self) -> int:
        return len(self.missions)

    def highest_priority(self) -> Mission | None:
        if not self.missions:
            return None
        return self.missions[0]
