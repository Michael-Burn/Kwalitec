"""ExplanationResult — immutable output of Tutor explainability (AP-002D6)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.intelligent_tutor.explainability.context import ExplanationContext
from app.domain.intelligent_tutor.explainability.events import (
    TutorExplanationGenerated,
    TutorExplanationRequested,
    TutorExplanationUnavailable,
)
from app.domain.intelligent_tutor.explainability.explanation import TutorExplanation

ExplanationEvent = (
    TutorExplanationRequested
    | TutorExplanationGenerated
    | TutorExplanationUnavailable
)


@dataclass(frozen=True, slots=True)
class ExplanationResult:
    """Complete explanation outcome ready for Tutor presentation / replay."""

    context: ExplanationContext
    explanation: TutorExplanation
    explained_at: datetime
    events: tuple[ExplanationEvent, ...] = ()

    def __post_init__(self) -> None:
        if self.context.reasoning_request_id != (
            self.explanation.context.reasoning_request_id
        ):
            raise ValueError("reasoning_request_id mismatch")
        if self.context.evidence_bundle_id != (
            self.explanation.context.evidence_bundle_id
        ):
            raise ValueError("evidence_bundle_id mismatch")
        if self.context.explanation_version != self.explanation.explanation_version:
            raise ValueError("explanation_version mismatch")
        if self.explanation.twin_id != self.context.twin_id:
            raise ValueError("explanation twin_id mismatch")
        object.__setattr__(self, "events", tuple(self.events or ()))

    @property
    def explanation_id(self) -> str:
        return self.explanation.explanation_id

    @property
    def section_ids(self) -> tuple[str, ...]:
        return self.explanation.section_ids

    @property
    def section_count(self) -> int:
        return len(self.explanation)

    @property
    def generated_count(self) -> int:
        return sum(1 for e in self.events if isinstance(e, TutorExplanationGenerated))

    @property
    def unavailable_count(self) -> int:
        return sum(
            1 for e in self.events if isinstance(e, TutorExplanationUnavailable)
        )

    @property
    def available(self) -> bool:
        return self.explanation.available
