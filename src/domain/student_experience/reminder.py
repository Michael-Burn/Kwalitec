"""Reminder — presentation review and session reminder.

Architecture Source
    EXP-001 Student Experience Engine
Concept
    Reminder
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.mission_generation.ids import MissionSpecificationId
from domain.student_experience.enums import ReminderKind
from domain.student_experience.ids import ReminderId


@dataclass(frozen=True, slots=True)
class Reminder(EducationalValueObject):
    """Immutable presentation reminder scheduled from plans and recommendations.

    Reminders surface already-decided review windows and recommendation
    categories. They never invent educational next steps or mutate
    RecommendationSpecification contents.
    """

    reminder_id: ReminderId
    kind: ReminderKind
    day_index: int
    message: str
    sequence: int
    mission_id: MissionSpecificationId | None = None
    source_label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.reminder_id, ReminderId):
            raise EducationalInvariantViolation(
                "reminder_id must be a ReminderId",
                invariant="Reminder.reminder_id.type",
            )
        if not isinstance(self.kind, ReminderKind):
            raise EducationalInvariantViolation(
                "kind must be a ReminderKind",
                invariant="Reminder.kind.type",
            )
        if not isinstance(self.day_index, int) or isinstance(self.day_index, bool):
            raise EducationalInvariantViolation(
                "day_index must be an integer",
                invariant="Reminder.day_index.type",
            )
        if self.day_index < 0:
            raise EducationalInvariantViolation(
                "day_index must be non-negative",
                invariant="Reminder.day_index.non_negative",
            )
        object.__setattr__(
            self,
            "message",
            require_non_empty_text(self.message, "message"),
        )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="Reminder.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="Reminder.sequence.positive",
            )
        if self.mission_id is not None and not isinstance(
            self.mission_id, MissionSpecificationId
        ):
            raise EducationalInvariantViolation(
                "mission_id must be a MissionSpecificationId when provided",
                invariant="Reminder.mission_id.type",
            )
        if self.source_label is not None:
            object.__setattr__(
                self,
                "source_label",
                require_non_empty_text(self.source_label, "source_label"),
            )
