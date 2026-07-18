"""Journey-attributed learning evidence.

Specialises the Learning Evidence Model by attaching journey / session /
objective attribution. Does not fork evidence catalogue semantics, invent
mastery maths, or duplicate Version 1 evidence stores.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.evidence.evidence_type import EvidenceType


@dataclass(frozen=True)
class JourneyEvidence:
    """Evidence observation attributed to a Learning Journey.

    Attributes:
        journey_evidence_id: Journey-scoped attribution identity.
        evidence_id: Correlation id of the canonical LearningEvidence record.
        journey_id: Parent Learning Journey identity.
        evidence_type: Catalogue type from the Learning Evidence Model.
        confidence_level: Qualitative confidence (not a numeric weight).
        recorded_at: When the attribution was recorded on the journey.
        session_id: Optional Learning Session that produced the evidence.
        objective_id: Optional LearningObjective citation.
        topic_id: Optional canonical topic (should match journey topic).
    """

    journey_evidence_id: str
    evidence_id: str
    journey_id: str
    evidence_type: EvidenceType
    confidence_level: EvidenceConfidenceLevel
    recorded_at: datetime
    session_id: str | None = None
    objective_id: str | None = None
    topic_id: str | None = None

    @classmethod
    def create(
        cls,
        journey_evidence_id: str,
        evidence_id: str,
        journey_id: str,
        evidence_type: EvidenceType | str,
        recorded_at: datetime,
        *,
        confidence_level: EvidenceConfidenceLevel
        | str = EvidenceConfidenceLevel.UNKNOWN,
        session_id: str | None = None,
        objective_id: str | None = None,
        topic_id: str | None = None,
    ) -> JourneyEvidence:
        """Construct JourneyEvidence after validating attribution invariants.

        Raises:
            ValueError: When required identities are empty.
        """
        jeid = _require_non_empty(journey_evidence_id, "journey_evidence_id")
        eid = _require_non_empty(evidence_id, "evidence_id")
        jid = _require_non_empty(journey_id, "journey_id")
        etype = (
            evidence_type
            if isinstance(evidence_type, EvidenceType)
            else EvidenceType(evidence_type)
        )
        conf = (
            confidence_level
            if isinstance(confidence_level, EvidenceConfidenceLevel)
            else EvidenceConfidenceLevel(confidence_level)
        )
        return cls(
            journey_evidence_id=jeid,
            evidence_id=eid,
            journey_id=jid,
            evidence_type=etype,
            confidence_level=conf,
            recorded_at=recorded_at,
            session_id=_optional_id(session_id),
            objective_id=_optional_id(objective_id),
            topic_id=_optional_id(topic_id),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _optional_id(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
