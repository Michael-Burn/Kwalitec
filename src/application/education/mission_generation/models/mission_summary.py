"""MissionSummary — compact read model over a MissionPlan."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import MissionType
from application.education.mission_generation.errors import MissionInvariantViolation


@dataclass(frozen=True, slots=True)
class MissionSummary:
    """Immutable summary projection of a generated mission plan."""

    mission_count: int
    total_duration_minutes: int
    prerequisite_mission_count: int
    maintenance_mission_count: int
    type_counts: tuple[tuple[MissionType, int], ...] = ()
    highest_priority_mission_id: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "mission_count",
            "total_duration_minutes",
            "prerequisite_mission_count",
            "maintenance_mission_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise MissionInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"MissionSummary.{name}.type",
                )
            if value < 0:
                raise MissionInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"MissionSummary.{name}.non_negative",
                )
        counts = tuple(self.type_counts)
        for entry in counts:
            if (
                not isinstance(entry, tuple)
                or len(entry) != 2
                or not isinstance(entry[0], MissionType)
                or isinstance(entry[1], bool)
                or not isinstance(entry[1], int)
                or entry[1] < 0
            ):
                raise MissionInvariantViolation(
                    "type_counts must be (MissionType, non-negative int) pairs",
                    invariant="MissionSummary.type_counts.type",
                )
        object.__setattr__(self, "type_counts", counts)
        highest = (self.highest_priority_mission_id or "").strip() or None
        object.__setattr__(self, "highest_priority_mission_id", highest)

    def is_empty(self) -> bool:
        return self.mission_count == 0
