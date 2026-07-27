"""Prediction scaffolding — framework only for SDT-001.

Algorithms evolve in future milestones; this module defines the contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class PredictionKind(StrEnum):
    """Supported prediction kinds (framework)."""

    ESTIMATED_READINESS = "estimated_readiness"
    LIKELIHOOD_OF_GOAL_COMPLETION = "likelihood_of_goal_completion"
    EXPECTED_MASTERY_GROWTH = "expected_mastery_growth"


@dataclass(frozen=True)
class Prediction:
    """One prediction scaffold attached to a Twin.

    SDT-001 persists the structure; prediction algorithms remain minimal
    deterministic placeholders until later milestones.
    """

    prediction_id: str
    twin_id: str
    kind: PredictionKind
    value: float = 0.0
    confidence: float = 0.0
    horizon_days: int = 0
    supporting_evidence: tuple[str, ...] = ()
    reason: str = "framework_scaffold"
    created_at: datetime | None = None
    algorithm_version: str = "sdt001.scaffold_v1"

    def __post_init__(self) -> None:
        if not (self.prediction_id or "").strip():
            raise ValueError("prediction_id is required")
        kind = (
            self.kind
            if isinstance(self.kind, PredictionKind)
            else PredictionKind(str(self.kind))
        )
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "value", _clamp(self.value))
        object.__setattr__(self, "confidence", _clamp(self.confidence))
        when = self.created_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(
            self, "supporting_evidence", tuple(self.supporting_evidence or ())
        )


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
