"""Episode step — one educational stage within a Learning Episode.

Architecture Source
    LEARNING_EPISODE_LIFECYCLE.md
Concept
    Episode Step
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode.enums import EpisodeStepStatus
from domain.education.learning_episode.value_objects.episode_sequence import (
    EpisodeStepId,
    EpisodeStepKind,
)


@dataclass(frozen=True, slots=True, eq=False)
class EpisodeStep(EducationalEntity):
    """Ordered educational stage inside a Learning Episode.

    Step kinds are extensible — pedagogies are not hard-coded. Required steps
    must be completed in sequence before episode completion.
    """

    step_id: EpisodeStepId
    kind: EpisodeStepKind
    sequence_index: int
    label: str
    required: bool = True
    status: EpisodeStepStatus = EpisodeStepStatus.PENDING

    @property
    def entity_id(self) -> EpisodeStepId:
        return self.step_id

    def _validate(self) -> None:
        if not isinstance(self.step_id, EpisodeStepId):
            raise EducationalInvariantViolation(
                "step_id must be an EpisodeStepId",
                invariant="EpisodeStep.step_id.type",
            )
        if not isinstance(self.kind, EpisodeStepKind):
            raise EducationalInvariantViolation(
                "kind must be an EpisodeStepKind",
                invariant="EpisodeStep.kind.type",
            )
        if not isinstance(self.sequence_index, int) or self.sequence_index < 0:
            raise EducationalInvariantViolation(
                "sequence_index must be a non-negative integer",
                invariant="EpisodeStep.sequence_index.non_negative",
            )
        object.__setattr__(
            self,
            "label",
            require_non_empty_text(self.label, "label"),
        )
        if not isinstance(self.required, bool):
            raise EducationalInvariantViolation(
                "required must be a bool",
                invariant="EpisodeStep.required.type",
            )
        if not isinstance(self.status, EpisodeStepStatus):
            raise EducationalInvariantViolation(
                "status must be an EpisodeStepStatus",
                invariant="EpisodeStep.status.type",
            )

    def is_pending(self) -> bool:
        return self.status is EpisodeStepStatus.PENDING

    def is_active(self) -> bool:
        return self.status is EpisodeStepStatus.ACTIVE

    def is_completed(self) -> bool:
        return self.status is EpisodeStepStatus.COMPLETED

    def activate(self) -> EpisodeStep:
        """Return this step marked ACTIVE."""
        if self.status is EpisodeStepStatus.COMPLETED:
            raise EducationalInvariantViolation(
                "cannot activate a completed episode step",
                invariant="EpisodeStep.activate.completed",
            )
        if self.status is EpisodeStepStatus.ACTIVE:
            return self
        return EpisodeStep(
            step_id=self.step_id,
            kind=self.kind,
            sequence_index=self.sequence_index,
            label=self.label,
            required=self.required,
            status=EpisodeStepStatus.ACTIVE,
        )

    def complete(self) -> EpisodeStep:
        """Return this step marked COMPLETED."""
        if self.status is EpisodeStepStatus.COMPLETED:
            raise EducationalInvariantViolation(
                "episode step is already completed",
                invariant="EpisodeStep.complete.already",
            )
        if self.status is not EpisodeStepStatus.ACTIVE:
            raise EducationalInvariantViolation(
                "only an active episode step can be completed",
                invariant="EpisodeStep.complete.not_active",
            )
        return EpisodeStep(
            step_id=self.step_id,
            kind=self.kind,
            sequence_index=self.sequence_index,
            label=self.label,
            required=self.required,
            status=EpisodeStepStatus.COMPLETED,
        )
