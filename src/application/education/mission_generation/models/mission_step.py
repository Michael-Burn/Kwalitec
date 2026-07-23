"""MissionStep — one executable unit within a mission."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import MissionStepAction
from application.education.mission_generation.errors import MissionInvariantViolation
from application.education.mission_generation.ids import MissionStepId


@dataclass(frozen=True, slots=True)
class MissionStep:
    """Immutable executable step inside a mission.

    Steps are ordered work units with structured action codes. They never
    estimate mastery or invent educational recommendations.
    """

    step_id: MissionStepId
    action: MissionStepAction
    order: int
    estimated_minutes: int
    subject_id: str | None = None
    competency_id: str | None = None
    action_detail: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.step_id, MissionStepId):
            raise MissionInvariantViolation(
                "step_id must be a MissionStepId",
                invariant="MissionStep.step_id.type",
            )
        if not isinstance(self.action, MissionStepAction):
            raise MissionInvariantViolation(
                "action must be a MissionStepAction",
                invariant="MissionStep.action.type",
            )
        if isinstance(self.order, bool) or not isinstance(self.order, int):
            raise MissionInvariantViolation(
                "order must be an integer",
                invariant="MissionStep.order.type",
            )
        if self.order < 1:
            raise MissionInvariantViolation(
                "order must be a positive 1-based integer",
                invariant="MissionStep.order.positive",
            )
        if isinstance(self.estimated_minutes, bool) or not isinstance(
            self.estimated_minutes, int
        ):
            raise MissionInvariantViolation(
                "estimated_minutes must be an integer",
                invariant="MissionStep.estimated_minutes.type",
            )
        if self.estimated_minutes < 1:
            raise MissionInvariantViolation(
                "estimated_minutes must be >= 1",
                invariant="MissionStep.estimated_minutes.positive",
            )
        subject_id = (self.subject_id or "").strip() or None
        object.__setattr__(self, "subject_id", subject_id)
        competency_id = (self.competency_id or "").strip() or None
        object.__setattr__(self, "competency_id", competency_id)
        detail = (self.action_detail or "").strip() or None
        object.__setattr__(self, "action_detail", detail)
