"""Domain representation of an Evidence Candidate.

An Evidence Candidate is a conceptual piece of learning evidence identified
inside a Learning Event. It is not persisted Learning Evidence, not Twin state,
and carries no numerical score.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.domain.evidence.evidence_category import (
    EvidenceCategory,
    EvidenceConfidenceLevel,
)
from app.domain.learning_events.learning_event import LearningEvent


@dataclass(frozen=True)
class EvidenceCandidate:
    """Immutable candidate piece of learning evidence extracted from an event.

    Attributes:
        identifier: Stable correlation id for this candidate (not a DB key).
        category: High-level evidence category from the Evidence Model.
        originating_event: The Learning Event this candidate was derived from.
        timestamp: When the underlying evidence occurred.
        topic_id: Canonical curriculum topic identity when topic-scoped.
        payload: Structured facts describing what was observed (no scores).
        provenance: Attributable producer / source channel for the candidate.
        confidence_level: Qualitative confidence only (High/Medium/Low/Unknown).
        metadata: Extensible contextual attributes for later capabilities.
    """

    identifier: str
    category: EvidenceCategory
    originating_event: LearningEvent
    timestamp: datetime
    topic_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    provenance: str | None = None
    confidence_level: EvidenceConfidenceLevel = EvidenceConfidenceLevel.UNKNOWN
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        identifier: str,
        category: EvidenceCategory,
        originating_event: LearningEvent,
        timestamp: datetime,
        *,
        topic_id: str | None = None,
        payload: dict[str, Any] | None = None,
        provenance: str | None = None,
        confidence_level: EvidenceConfidenceLevel = EvidenceConfidenceLevel.UNKNOWN,
        metadata: dict[str, Any] | None = None,
    ) -> EvidenceCandidate:
        """Construct an Evidence Candidate.

        Args:
            identifier: Correlation identity for this candidate.
            category: Evidence category classification.
            originating_event: Source Learning Event.
            timestamp: Occurrence time for the evidence.
            topic_id: Optional canonical topic reference.
            payload: Optional evidence facts (defaults to empty).
            provenance: Optional producer / source attribution.
            confidence_level: Qualitative confidence (defaults to Unknown).
            metadata: Optional extensible context bag.

        Returns:
            A frozen EvidenceCandidate instance.
        """
        return cls(
            identifier=identifier,
            category=category,
            originating_event=originating_event,
            timestamp=timestamp,
            topic_id=topic_id,
            payload=dict(payload or {}),
            provenance=provenance,
            confidence_level=confidence_level,
            metadata=dict(metadata or {}),
        )
