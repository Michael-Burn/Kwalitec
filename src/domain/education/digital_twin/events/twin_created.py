"""Domain event: Educational Digital Twin was created.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    TwinCreated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.enums import TwinStatus
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DigitalTwinId


@dataclass(frozen=True, slots=True)
class TwinCreated(EducationalValueObject):
    """Immutable record that an EducationalDigitalTwin was created."""

    twin_id: DigitalTwinId
    student_id: str
    status: TwinStatus
    learner_state_id: str

    def _validate(self) -> None:
        if not isinstance(self.twin_id, DigitalTwinId):
            raise EducationalInvariantViolation(
                "twin_id must be a DigitalTwinId",
                invariant="TwinCreated.twin_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.status, TwinStatus):
            raise EducationalInvariantViolation(
                "status must be a TwinStatus",
                invariant="TwinCreated.status.type",
            )
        if self.status is not TwinStatus.ACTIVE:
            raise EducationalInvariantViolation(
                "newly created twin must be ACTIVE",
                invariant="TwinCreated.status.active",
            )
        object.__setattr__(
            self,
            "learner_state_id",
            require_identity_value(self.learner_state_id, "learner_state_id"),
        )
