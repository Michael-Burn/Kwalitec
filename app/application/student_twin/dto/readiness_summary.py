"""Immutable readiness summary DTO."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.readiness_state import ReadinessState


@dataclass(frozen=True)
class ReadinessSummary:
    """Readiness projection for consumers."""

    readiness_score: float = 0.0
    confidence: str = "very_low"
    is_ready: bool = False
    supporting_topic_ids: tuple[str, ...] = field(default_factory=tuple)
    limiting_topic_ids: tuple[str, ...] = field(default_factory=tuple)
    rationale: str = "insufficient_evidence"

    @classmethod
    def from_domain(cls, state: ReadinessState) -> ReadinessSummary:
        """Project ReadinessState to a DTO."""
        return cls(
            readiness_score=state.readiness_score,
            confidence=state.confidence.value,
            is_ready=state.is_ready,
            supporting_topic_ids=state.supporting_topic_ids,
            limiting_topic_ids=state.limiting_topic_ids,
            rationale=state.rationale,
        )
