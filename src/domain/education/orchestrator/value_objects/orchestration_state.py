"""Orchestration state — current coordination posture.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    Orchestration State
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator.entities.orchestration_stage import (
    OrchestrationStageId,
)
from domain.education.orchestrator.enums import OrchestrationStatus


@dataclass(frozen=True, slots=True)
class OrchestrationState(EducationalValueObject):
    """Immutable snapshot of orchestration lifecycle posture.

    State tracks coordination status only. It does not encode diagnosis,
    priority, or strategy selection.
    """

    status: OrchestrationStatus
    current_stage_id: OrchestrationStageId | None = None
    pause_reason: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.status, OrchestrationStatus):
            raise EducationalInvariantViolation(
                "status must be an OrchestrationStatus",
                invariant="OrchestrationState.status.type",
            )
        if self.current_stage_id is not None and not isinstance(
            self.current_stage_id, OrchestrationStageId
        ):
            raise EducationalInvariantViolation(
                "current_stage_id must be an OrchestrationStageId when provided",
                invariant="OrchestrationState.current_stage_id.type",
            )
        if self.pause_reason is not None:
            object.__setattr__(
                self,
                "pause_reason",
                require_non_empty_text(self.pause_reason, "pause_reason"),
            )
        if self.status is OrchestrationStatus.PLANNED:
            if self.current_stage_id is not None:
                raise EducationalInvariantViolation(
                    "planned orchestration must not have an active stage",
                    invariant="OrchestrationState.planned.no_active_stage",
                )
            if self.pause_reason is not None:
                raise EducationalInvariantViolation(
                    "planned orchestration must not carry a pause reason",
                    invariant="OrchestrationState.planned.no_pause_reason",
                )
        if self.status is OrchestrationStatus.PAUSED and self.pause_reason is None:
            raise EducationalInvariantViolation(
                "paused orchestration must declare a pause reason",
                invariant="OrchestrationState.paused.reason.required",
            )
        if (
            self.status is not OrchestrationStatus.PAUSED
            and self.pause_reason is not None
        ):
            raise EducationalInvariantViolation(
                "pause reason is only lawful while paused",
                invariant="OrchestrationState.pause_reason.only_when_paused",
            )
        if self.status is OrchestrationStatus.COMPLETED:
            if self.current_stage_id is not None:
                raise EducationalInvariantViolation(
                    "completed orchestration must not retain an active stage",
                    invariant="OrchestrationState.completed.no_active_stage",
                )

    def is_planned(self) -> bool:
        return self.status is OrchestrationStatus.PLANNED

    def is_active(self) -> bool:
        return self.status is OrchestrationStatus.ACTIVE

    def is_paused(self) -> bool:
        return self.status is OrchestrationStatus.PAUSED

    def is_completed(self) -> bool:
        return self.status is OrchestrationStatus.COMPLETED

    def is_terminal(self) -> bool:
        return self.status is OrchestrationStatus.COMPLETED

    @classmethod
    def planned(cls) -> OrchestrationState:
        return cls(status=OrchestrationStatus.PLANNED)

    @classmethod
    def active(cls, current_stage_id: OrchestrationStageId) -> OrchestrationState:
        return cls(
            status=OrchestrationStatus.ACTIVE,
            current_stage_id=current_stage_id,
        )

    @classmethod
    def paused(
        cls,
        reason: str,
        *,
        current_stage_id: OrchestrationStageId | None = None,
    ) -> OrchestrationState:
        return cls(
            status=OrchestrationStatus.PAUSED,
            current_stage_id=current_stage_id,
            pause_reason=reason,
        )

    @classmethod
    def completed(cls) -> OrchestrationState:
        return cls(status=OrchestrationStatus.COMPLETED)
