"""Mission plan — ordered educational intent for one day."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.adaptive_mission.mission_objective import MissionObjective
from app.domain.adaptive_mission.mission_step import MissionStep


@dataclass(frozen=True)
class MissionPlan:
    """Structured plan of objectives and steps for one adaptive mission.

    Not a timetable — a single-day educational action plan.
    """

    plan_id: str
    objective: MissionObjective
    steps: tuple[MissionStep, ...]
    concepts_covered: tuple[str, ...]
    estimated_duration_minutes: int

    def __post_init__(self) -> None:
        if not (self.plan_id or "").strip():
            raise ValueError("plan_id is required")
        object.__setattr__(self, "steps", tuple(self.steps or ()))
        object.__setattr__(
            self, "concepts_covered", tuple(self.concepts_covered or ())
        )
        object.__setattr__(
            self,
            "estimated_duration_minutes",
            max(1, int(self.estimated_duration_minutes)),
        )
