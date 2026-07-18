"""Immutable mastery summary DTO."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.mastery_state import MasteryState


@dataclass(frozen=True)
class TopicMasteryDTO:
    """Per-topic mastery projection."""

    topic_id: str
    mastery_score: float
    confidence: str


@dataclass(frozen=True)
class MasterySummary:
    """Aggregate mastery projection."""

    overall_score: float = 0.0
    overall_confidence: str = "very_low"
    topic_count: int = 0
    topics: tuple[TopicMasteryDTO, ...] = field(default_factory=tuple)

    @classmethod
    def from_domain(cls, state: MasteryState) -> MasterySummary:
        """Project MasteryState to a DTO."""
        topics = tuple(
            TopicMasteryDTO(
                topic_id=r.topic_id,
                mastery_score=r.mastery_score,
                confidence=r.confidence.value,
            )
            for r in state.topic_records
        )
        return cls(
            overall_score=state.overall_score,
            overall_confidence=state.overall_confidence.value,
            topic_count=state.topic_count,
            topics=topics,
        )
