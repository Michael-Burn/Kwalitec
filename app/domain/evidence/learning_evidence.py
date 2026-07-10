"""Domain representation of Learning Evidence.

Learning Evidence is the canonical, immutable evidence representation consumed
by the Student Digital Twin and future intelligence components. It is produced
by the Evidence Transformation Stage from a validated Evidence Candidate.

This object is not persisted here, carries no numerical score or weight, and
does not update Twin state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.evidence.evidence_type import EvidenceType


@dataclass(frozen=True)
class LearningEvidence:
    """Immutable canonical learning evidence record.

    Attributes:
        evidence_id: Stable correlation id for this evidence (not a DB key).
        evidence_type: Catalogue type from the Learning Evidence Model.
        originating_event_id: Correlation id of the source Learning Event.
        timestamp: When the underlying evidence occurred.
        topic_id: Canonical curriculum topic identity when topic-scoped.
        curriculum_id: Canonical curriculum identity when curriculum-scoped.
        payload: Structured facts describing what was observed (no scores).
        provenance: Attributable producer / source channel for the evidence.
        confidence_level: Qualitative confidence only (High/Medium/Low/Unknown).
        metadata: Extensible contextual attributes for later capabilities.
    """

    evidence_id: str
    evidence_type: EvidenceType
    originating_event_id: str | None
    timestamp: datetime
    topic_id: str | None = None
    curriculum_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    provenance: str | None = None
    confidence_level: EvidenceConfidenceLevel = EvidenceConfidenceLevel.UNKNOWN
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        evidence_id: str,
        evidence_type: EvidenceType,
        originating_event_id: str | None,
        timestamp: datetime,
        *,
        topic_id: str | None = None,
        curriculum_id: str | None = None,
        payload: dict[str, Any] | None = None,
        provenance: str | None = None,
        confidence_level: EvidenceConfidenceLevel = EvidenceConfidenceLevel.UNKNOWN,
        metadata: dict[str, Any] | None = None,
    ) -> LearningEvidence:
        """Construct a Learning Evidence record.

        Args:
            evidence_id: Correlation identity for this evidence.
            evidence_type: Catalogue type classification.
            originating_event_id: Source Learning Event correlation id.
            timestamp: Occurrence time for the evidence.
            topic_id: Optional canonical topic reference.
            curriculum_id: Optional canonical curriculum reference.
            payload: Optional evidence facts (defaults to empty).
            provenance: Optional producer / source attribution.
            confidence_level: Qualitative confidence (defaults to Unknown).
            metadata: Optional extensible context bag.

        Returns:
            A frozen LearningEvidence instance.
        """
        return cls(
            evidence_id=evidence_id,
            evidence_type=evidence_type,
            originating_event_id=originating_event_id,
            timestamp=timestamp,
            topic_id=topic_id,
            curriculum_id=curriculum_id,
            payload=dict(payload or {}),
            provenance=provenance,
            confidence_level=confidence_level,
            metadata=dict(metadata or {}),
        )
