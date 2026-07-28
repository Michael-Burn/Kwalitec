"""DecisionResult — immutable output of observation→decision generation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.reasoning.decisions.context import DecisionContext
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet


@dataclass(frozen=True, slots=True)
class DecisionResult:
    """Complete decision outcome ready for Twin validation and application."""

    context: DecisionContext
    decision_set: EducationalDecisionSet
    decided_at: datetime

    def __post_init__(self) -> None:
        if self.context.reasoning_request_id != (
            self.decision_set.context.reasoning_request_id
        ):
            raise ValueError("reasoning_request_id mismatch")
        if self.context.evidence_bundle_id != (
            self.decision_set.context.evidence_bundle_id
        ):
            raise ValueError("evidence_bundle_id mismatch")
        if self.context.decision_version != self.decision_set.decision_version:
            raise ValueError("decision_version mismatch")

    @property
    def decision_ids(self) -> tuple[str, ...]:
        return self.decision_set.decision_ids

    @property
    def decision_count(self) -> int:
        return len(self.decision_set)
