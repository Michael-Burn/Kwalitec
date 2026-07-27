"""Graph node — one curriculum concept on a learner-specific Learning Graph."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class PrerequisiteStatus(StrEnum):
    """Whether prerequisites for this concept appear met on the learner graph."""

    MET = "met"
    UNMET = "unmet"
    PARTIAL = "partial"
    UNKNOWN = "unknown"
    NONE = "none"  # no prerequisite edges


@dataclass(frozen=True)
class GraphNode:
    """One curriculum concept node.

    Mastery / confidence / evidence fields are *projections* resolved from the
    Student Digital Twin at sync time. Persistence stores structure + mastery
    link only — Twin mastery rows remain the source of truth.
    """

    node_id: str
    graph_id: str
    concept_id: str
    concept_title: str = ""
    mastery_link_id: str = ""
    mastery_score: float = 0.0
    confidence: float = 0.0
    evidence_count: int = 0
    last_interaction: datetime | None = None
    trend: str = "unknown"
    prerequisite_status: PrerequisiteStatus = PrerequisiteStatus.UNKNOWN

    def __post_init__(self) -> None:
        if not (self.node_id or "").strip():
            raise ValueError("node_id is required")
        if not (self.concept_id or "").strip():
            raise ValueError("concept_id is required")
        object.__setattr__(self, "mastery_score", _clamp(self.mastery_score))
        object.__setattr__(self, "confidence", _clamp(self.confidence))
        status = self.prerequisite_status
        if not isinstance(status, PrerequisiteStatus):
            object.__setattr__(
                self, "prerequisite_status", PrerequisiteStatus(str(status))
            )
        when = self.last_interaction
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "last_interaction", when.astimezone(UTC).replace(tzinfo=None)
            )


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
