"""MissionTask — one ordered instructional unit within a mission.

Architecture Source
    STRATEGY_COMPOSITION_MODEL.md
    SESSION_ASSEMBLY_MODEL.md
Concept
    Mission Task
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    require_non_empty_text,
)
from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.mission_generation.ids import MissionTaskId


@dataclass(frozen=True, slots=True, eq=False)
class MissionTask(EducationalEntity):
    """Single ordered instructional task in a MissionSequence.

    Tasks project Teaching Strategy composition members into executable
    educational work units. They do not prescribe prompts or UI screens.
    """

    task_id: MissionTaskId
    sequence_index: int
    strategy_type: TeachingStrategyType
    label: str
    estimated_minutes: int
    required: bool = True
    success_hint: str | None = None

    @property
    def entity_id(self) -> MissionTaskId:
        return self.task_id

    def _validate(self) -> None:
        if not isinstance(self.task_id, MissionTaskId):
            raise EducationalInvariantViolation(
                "task_id must be a MissionTaskId",
                invariant="MissionTask.task_id.type",
            )
        if not isinstance(self.sequence_index, int) or isinstance(
            self.sequence_index, bool
        ):
            raise EducationalInvariantViolation(
                "sequence_index must be an integer",
                invariant="MissionTask.sequence_index.type",
            )
        if self.sequence_index < 1:
            raise EducationalInvariantViolation(
                "sequence_index must be a positive integer",
                invariant="MissionTask.sequence_index.positive",
            )
        if not isinstance(self.strategy_type, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "strategy_type must be a TeachingStrategyType",
                invariant="MissionTask.strategy_type.type",
            )
        object.__setattr__(
            self,
            "label",
            require_non_empty_text(self.label, "label"),
        )
        if not isinstance(self.estimated_minutes, int) or isinstance(
            self.estimated_minutes, bool
        ):
            raise EducationalInvariantViolation(
                "estimated_minutes must be an integer",
                invariant="MissionTask.estimated_minutes.type",
            )
        if self.estimated_minutes <= 0:
            raise EducationalInvariantViolation(
                "estimated_minutes must be positive",
                invariant="MissionTask.estimated_minutes.positive",
            )
        if not isinstance(self.required, bool):
            raise EducationalInvariantViolation(
                "required must be a boolean",
                invariant="MissionTask.required.type",
            )
        if self.success_hint is not None:
            object.__setattr__(
                self,
                "success_hint",
                require_non_empty_text(self.success_hint, "success_hint"),
            )
