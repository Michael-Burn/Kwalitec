"""ExecutionHistory — caller-supplied mission execution outcomes for planning.

Summarises MissionExecution history without mutating MissionPlan or
StudentEducationalState. Completed missions are removed from future
schedules; abandoned missions are re-placed per AbandonmentPolicy.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_generation.ids import MissionId
from application.education.revision_planner.errors import ScheduleInvariantViolation


@dataclass(frozen=True, slots=True)
class ExecutionHistory:
    """Immutable summary of mission execution outcomes for scheduling."""

    completed_mission_ids: tuple[MissionId, ...] = ()
    abandoned_mission_ids: tuple[MissionId, ...] = ()
    in_progress_mission_ids: tuple[MissionId, ...] = ()
    expired_mission_ids: tuple[MissionId, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "completed_mission_ids",
            self._normalise_ids(self.completed_mission_ids, "completed_mission_ids"),
        )
        object.__setattr__(
            self,
            "abandoned_mission_ids",
            self._normalise_ids(self.abandoned_mission_ids, "abandoned_mission_ids"),
        )
        object.__setattr__(
            self,
            "in_progress_mission_ids",
            self._normalise_ids(
                self.in_progress_mission_ids, "in_progress_mission_ids"
            ),
        )
        object.__setattr__(
            self,
            "expired_mission_ids",
            self._normalise_ids(self.expired_mission_ids, "expired_mission_ids"),
        )

    @staticmethod
    def _normalise_ids(
        values: tuple[MissionId, ...] | Sequence[MissionId],
        field_name: str,
    ) -> tuple[MissionId, ...]:
        seen: set[str] = set()
        ordered: list[MissionId] = []
        for mission_id in values:
            if not isinstance(mission_id, MissionId):
                raise ScheduleInvariantViolation(
                    f"{field_name} must contain MissionId values",
                    invariant=f"ExecutionHistory.{field_name}.type",
                )
            if mission_id.value in seen:
                continue
            seen.add(mission_id.value)
            ordered.append(mission_id)
        return tuple(ordered)

    @classmethod
    def from_executions(
        cls, executions: Sequence[MissionExecution]
    ) -> ExecutionHistory:
        """Derive history from MissionExecution aggregates."""
        completed: list[MissionId] = []
        abandoned: list[MissionId] = []
        in_progress: list[MissionId] = []
        expired: list[MissionId] = []
        for execution in executions:
            if not isinstance(execution, MissionExecution):
                raise ScheduleInvariantViolation(
                    "executions must contain MissionExecution values",
                    invariant="ExecutionHistory.from_executions.type",
                )
            if execution.status is ExecutionStatus.COMPLETED:
                completed.append(execution.mission_id)
            elif execution.status is ExecutionStatus.ABANDONED:
                abandoned.append(execution.mission_id)
            elif execution.status is ExecutionStatus.EXPIRED:
                expired.append(execution.mission_id)
            elif execution.status in (
                ExecutionStatus.STARTED,
                ExecutionStatus.PAUSED,
                ExecutionStatus.RESUMED,
            ):
                in_progress.append(execution.mission_id)
        return cls(
            completed_mission_ids=tuple(completed),
            abandoned_mission_ids=tuple(abandoned),
            in_progress_mission_ids=tuple(in_progress),
            expired_mission_ids=tuple(expired),
        )

    def is_completed(self, mission_id: MissionId) -> bool:
        return mission_id in self.completed_mission_ids

    def is_abandoned(self, mission_id: MissionId) -> bool:
        return mission_id in self.abandoned_mission_ids

    def exclude_from_future(self) -> frozenset[MissionId]:
        """Mission ids that must not appear in future schedule slots."""
        return frozenset(self.completed_mission_ids)
