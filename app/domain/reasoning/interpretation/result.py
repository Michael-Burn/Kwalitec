"""InterpretationResult — immutable output of evidence interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.reasoning.interpretation.context import InterpretationContext
from app.domain.reasoning.observations.observation_set import EducationalObservationSet


@dataclass(frozen=True, slots=True)
class InterpretationResult:
    """Complete interpretation outcome ready for Twin consumption (not applied)."""

    context: InterpretationContext
    observation_set: EducationalObservationSet
    interpreted_at: datetime

    def __post_init__(self) -> None:
        if self.context.reasoning_request_id != (
            self.observation_set.reasoning_request_id
        ):
            raise ValueError("reasoning_request_id mismatch between context and set")
        if self.context.evidence_bundle_id != self.observation_set.evidence_bundle_id:
            raise ValueError("evidence_bundle_id mismatch between context and set")
        if (
            self.context.interpreter_version
            != self.observation_set.interpretation_version
        ):
            raise ValueError("interpretation_version mismatch between context and set")

    @property
    def observation_ids(self) -> tuple[str, ...]:
        return self.observation_set.observation_ids

    @property
    def observation_count(self) -> int:
        return len(self.observation_set)
