"""Reference value objects for artefacts owned outside this aggregate.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Current Mission Reference / Current Checkpoint Reference /
    Educational Timeline Reference

These are lightweight, immutable citations. They do not load the referenced
aggregate, persist state, or encode a transport DTO.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state.ids import (
    CheckpointId,
    EducationalTimelineId,
    MissionId,
)


@dataclass(frozen=True, slots=True)
class MissionReference(EducationalValueObject):
    """Citation of the student's current mission."""

    mission_id: MissionId
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.mission_id, MissionId):
            raise EducationalInvariantViolation(
                "mission_id must be a MissionId",
                invariant="MissionReference.mission_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self, "label", require_non_empty_text(self.label, "label")
            )


@dataclass(frozen=True, slots=True)
class CheckpointReference(EducationalValueObject):
    """Citation of the student's current checkpoint."""

    checkpoint_id: CheckpointId
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.checkpoint_id, CheckpointId):
            raise EducationalInvariantViolation(
                "checkpoint_id must be a CheckpointId",
                invariant="CheckpointReference.checkpoint_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self, "label", require_non_empty_text(self.label, "label")
            )


@dataclass(frozen=True, slots=True)
class EducationalTimelineReference(EducationalValueObject):
    """Citation of the student's educational timeline."""

    timeline_id: EducationalTimelineId
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.timeline_id, EducationalTimelineId):
            raise EducationalInvariantViolation(
                "timeline_id must be an EducationalTimelineId",
                invariant="EducationalTimelineReference.timeline_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self, "label", require_non_empty_text(self.label, "label")
            )
