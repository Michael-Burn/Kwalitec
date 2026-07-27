"""Structured learning feedback — educational, not motivational."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.assessment_pipeline.feedback_source import FeedbackSource


def _freeze_metadata(metadata: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(metadata or {}))


@dataclass(frozen=True)
class LearningFeedback:
    """Deterministic educational feedback for one assessed activity.

    Fields remain educational (what happened / what evidence / what next)
    rather than motivational slogans.
    """

    feedback_id: str
    twin_id: str
    event_id: str
    result_id: str
    activity: str
    performance: str
    evidence_generated: tuple[str, ...]
    concepts_covered: tuple[str, ...]
    confidence: float
    suggested_next_action: str
    timestamp: datetime
    source: FeedbackSource = FeedbackSource.ASSESSMENT_PIPELINE
    observation_id: str = ""
    mission_id: str = ""
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.feedback_id or "").strip():
            raise ValueError("feedback_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.event_id or "").strip():
            raise ValueError("event_id is required")
        source = (
            self.source
            if isinstance(self.source, FeedbackSource)
            else FeedbackSource(str(self.source))
        )
        object.__setattr__(self, "source", source)
        when = self.timestamp
        if when.tzinfo is not None:
            object.__setattr__(
                self, "timestamp", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(
            self, "evidence_generated", tuple(self.evidence_generated or ())
        )
        object.__setattr__(
            self, "concepts_covered", tuple(self.concepts_covered or ())
        )
        object.__setattr__(
            self, "confidence", max(0.0, min(1.0, float(self.confidence)))
        )
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))
