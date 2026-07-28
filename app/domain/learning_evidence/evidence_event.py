"""Immutable Learning Evidence event value object (EI-005)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class EvidenceEvent:
    """Append-only educational observation against a curriculum node.

    Does not carry mastery, confidence, recommendations, or mission intents.
    """

    evidence_id: str
    instance_id: str
    node_stable_id: str
    evidence_type: str
    occurred_at: datetime
    source: str
    recorded_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
    corrects_evidence_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "instance_id": self.instance_id,
            "node_stable_id": self.node_stable_id,
            "evidence_type": self.evidence_type,
            "occurred_at": self.occurred_at.isoformat(),
            "source": self.source,
            "recorded_at": self.recorded_at.isoformat(),
            "metadata": dict(self.metadata),
            "corrects_evidence_id": self.corrects_evidence_id,
        }
