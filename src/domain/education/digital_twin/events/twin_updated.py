"""Domain event: Educational Digital Twin memory was updated.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    TwinUpdated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.enums import TwinStatus, TwinUpdateKind
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DigitalTwinId


@dataclass(frozen=True, slots=True)
class TwinUpdated(EducationalValueObject):
    """Immutable record that Twin educational memory changed."""

    twin_id: DigitalTwinId
    student_id: str
    status: TwinStatus
    update_kind: TwinUpdateKind
    evidence_count: int
    intervention_count: int
    trajectory_length: int

    def _validate(self) -> None:
        if not isinstance(self.twin_id, DigitalTwinId):
            raise EducationalInvariantViolation(
                "twin_id must be a DigitalTwinId",
                invariant="TwinUpdated.twin_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.status, TwinStatus):
            raise EducationalInvariantViolation(
                "status must be a TwinStatus",
                invariant="TwinUpdated.status.type",
            )
        if not isinstance(self.update_kind, TwinUpdateKind):
            raise EducationalInvariantViolation(
                "update_kind must be a TwinUpdateKind",
                invariant="TwinUpdated.update_kind.type",
            )
        if not isinstance(self.evidence_count, int) or self.evidence_count < 0:
            raise EducationalInvariantViolation(
                "evidence_count must be a non-negative integer",
                invariant="TwinUpdated.evidence_count.non_negative",
            )
        if (
            not isinstance(self.intervention_count, int)
            or self.intervention_count < 0
        ):
            raise EducationalInvariantViolation(
                "intervention_count must be a non-negative integer",
                invariant="TwinUpdated.intervention_count.non_negative",
            )
        if (
            not isinstance(self.trajectory_length, int)
            or self.trajectory_length < 0
        ):
            raise EducationalInvariantViolation(
                "trajectory_length must be a non-negative integer",
                invariant="TwinUpdated.trajectory_length.non_negative",
            )
