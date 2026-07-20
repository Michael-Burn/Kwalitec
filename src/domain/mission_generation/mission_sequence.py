"""MissionSequence — ordered task plan for a generated mission.

Architecture Source
    SESSION_ASSEMBLY_MODEL.md
    STRATEGY_COMPOSITION_MODEL.md
Concept
    Mission Sequence
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.mission_generation.ids import MissionTaskId
from domain.mission_generation.mission_task import MissionTask


@dataclass(frozen=True, slots=True)
class MissionSequence(EducationalValueObject):
    """Immutable ordered educational task plan for one mission.

    Ordering is educational law: sequence_index must be strictly increasing
    from 1 without gaps. Required tasks define completion membership.
    """

    tasks: tuple[MissionTask, ...]

    def _validate(self) -> None:
        if not isinstance(self.tasks, tuple):
            raise EducationalInvariantViolation(
                "tasks must be a tuple of MissionTask",
                invariant="MissionSequence.tasks.type",
            )
        if not self.tasks:
            raise EducationalInvariantViolation(
                "mission sequence must contain at least one task",
                invariant="MissionSequence.tasks.min_one",
            )
        seen_ids: set[str] = set()
        for expected_index, task in enumerate(self.tasks, start=1):
            if not isinstance(task, MissionTask):
                raise EducationalInvariantViolation(
                    "tasks must contain MissionTask values",
                    invariant="MissionSequence.tasks.item_type",
                )
            if task.sequence_index != expected_index:
                raise EducationalInvariantViolation(
                    "mission tasks must be ordered with contiguous sequence_index "
                    f"starting at 1 (expected {expected_index}, got "
                    f"{task.sequence_index})",
                    invariant="MissionSequence.tasks.sequence_order",
                )
            if task.task_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "mission sequence must not contain duplicate task identities",
                    invariant="MissionSequence.tasks.unique",
                )
            seen_ids.add(task.task_id.value)
        if not any(task.required for task in self.tasks):
            raise EducationalInvariantViolation(
                "mission sequence must declare at least one required task",
                invariant="MissionSequence.required.min_one",
            )

    @classmethod
    def of(cls, *tasks: MissionTask) -> MissionSequence:
        return cls(tasks=tuple(tasks))

    @property
    def length(self) -> int:
        return len(self.tasks)

    def required_tasks(self) -> tuple[MissionTask, ...]:
        return tuple(task for task in self.tasks if task.required)

    def task_ids(self) -> tuple[MissionTaskId, ...]:
        return tuple(task.task_id for task in self.tasks)

    def index_of(self, task_id: MissionTaskId) -> int:
        for task in self.tasks:
            if task.task_id == task_id:
                return task.sequence_index
        raise EducationalInvariantViolation(
            "task is not part of this mission sequence",
            invariant="MissionSequence.task.not_found",
        )

    def total_estimated_minutes(self) -> int:
        return sum(task.estimated_minutes for task in self.tasks)
