"""Learner state — owned learner posture within an Educational Digital Twin.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Learner State
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.enums import LearnerActivityStatus
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class LearnerStateId(EducationalValueObject):
    """Identity of a LearnerState entity within a Twin."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "LearnerStateId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class LearnerState(EducationalEntity):
    """Remembered learner posture owned by an EducationalDigitalTwin.

    LearnerState holds activity posture only. It does not diagnose, prioritize,
    or orchestrate learning.
    """

    learner_state_id: LearnerStateId
    student_id: str
    activity_status: LearnerActivityStatus = LearnerActivityStatus.ENGAGED

    @property
    def entity_id(self) -> LearnerStateId:
        return self.learner_state_id

    def _validate(self) -> None:
        if not isinstance(self.learner_state_id, LearnerStateId):
            raise EducationalInvariantViolation(
                "learner_state_id must be a LearnerStateId",
                invariant="LearnerState.learner_state_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.activity_status, LearnerActivityStatus):
            raise EducationalInvariantViolation(
                "activity_status must be a LearnerActivityStatus",
                invariant="LearnerState.activity_status.type",
            )

    def with_activity_status(
        self, activity_status: LearnerActivityStatus
    ) -> LearnerState:
        """Return a copy with an amended activity posture."""
        return LearnerState(
            learner_state_id=self.learner_state_id,
            student_id=self.student_id,
            activity_status=activity_status,
        )
