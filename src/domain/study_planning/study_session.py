"""StudySession — one scheduled sitting within a StudyPlan.

Architecture Source
    SESSION_ASSEMBLY_MODEL.md
Concept
    Study Session
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.mission_generation.ids import MissionSpecificationId, MissionTaskId
from domain.study_planning.enums import SessionKind
from domain.study_planning.ids import StudySessionId


@dataclass(frozen=True, slots=True, eq=False)
class StudySession(EducationalEntity):
    """Single ordered sitting allocated on a relative planning day.

    Work sessions advance mission tasks. Review and recovery sessions protect
    retention and capacity honesty. Sessions never invoke calendar APIs.
    """

    session_id: StudySessionId
    sequence_index: int
    day_index: int
    kind: SessionKind
    mission_id: MissionSpecificationId
    allocated_minutes: int
    label: str
    mission_task_ids: tuple[MissionTaskId, ...] = ()

    @property
    def entity_id(self) -> StudySessionId:
        return self.session_id

    def _validate(self) -> None:
        if not isinstance(self.session_id, StudySessionId):
            raise EducationalInvariantViolation(
                "session_id must be a StudySessionId",
                invariant="StudySession.session_id.type",
            )
        if not isinstance(self.sequence_index, int) or isinstance(
            self.sequence_index, bool
        ):
            raise EducationalInvariantViolation(
                "sequence_index must be an integer",
                invariant="StudySession.sequence_index.type",
            )
        if self.sequence_index < 1:
            raise EducationalInvariantViolation(
                "sequence_index must be a positive integer",
                invariant="StudySession.sequence_index.positive",
            )
        if not isinstance(self.day_index, int) or isinstance(self.day_index, bool):
            raise EducationalInvariantViolation(
                "day_index must be an integer",
                invariant="StudySession.day_index.type",
            )
        if self.day_index < 0:
            raise EducationalInvariantViolation(
                "day_index must be non-negative",
                invariant="StudySession.day_index.non_negative",
            )
        if not isinstance(self.kind, SessionKind):
            raise EducationalInvariantViolation(
                "kind must be a SessionKind",
                invariant="StudySession.kind.type",
            )
        if not isinstance(self.mission_id, MissionSpecificationId):
            raise EducationalInvariantViolation(
                "mission_id must be a MissionSpecificationId",
                invariant="StudySession.mission_id.type",
            )
        if not isinstance(self.allocated_minutes, int) or isinstance(
            self.allocated_minutes, bool
        ):
            raise EducationalInvariantViolation(
                "allocated_minutes must be an integer",
                invariant="StudySession.allocated_minutes.type",
            )
        if self.allocated_minutes <= 0:
            raise EducationalInvariantViolation(
                "allocated_minutes must be positive",
                invariant="StudySession.allocated_minutes.positive",
            )
        object.__setattr__(
            self,
            "label",
            require_non_empty_text(self.label, "label"),
        )
        if not isinstance(self.mission_task_ids, tuple):
            raise EducationalInvariantViolation(
                "mission_task_ids must be a tuple",
                invariant="StudySession.mission_task_ids.type",
            )
        seen: set[str] = set()
        for task_id in self.mission_task_ids:
            if not isinstance(task_id, MissionTaskId):
                raise EducationalInvariantViolation(
                    "mission_task_ids must contain MissionTaskId values",
                    invariant="StudySession.mission_task_ids.item_type",
                )
            if task_id.value in seen:
                raise EducationalInvariantViolation(
                    "mission_task_ids must be unique within a session",
                    invariant="StudySession.mission_task_ids.unique",
                )
            seen.add(task_id.value)
        if self.kind is SessionKind.WORK and not self.mission_task_ids:
            raise EducationalInvariantViolation(
                "work sessions must claim at least one mission task",
                invariant="StudySession.work.requires_tasks",
            )
        if self.kind is not SessionKind.WORK and self.mission_task_ids:
            raise EducationalInvariantViolation(
                "review and recovery sessions must not claim mission tasks",
                invariant="StudySession.non_work.no_tasks",
            )

    def is_work(self) -> bool:
        return self.kind is SessionKind.WORK

    def is_review(self) -> bool:
        return self.kind is SessionKind.REVIEW

    def is_recovery(self) -> bool:
        return self.kind is SessionKind.RECOVERY
