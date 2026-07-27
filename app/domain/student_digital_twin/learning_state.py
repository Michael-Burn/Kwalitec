"""Multi-dimensional learning state — not a single percentage."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class LearningState:
    """Educational state independent of UI presentation.

    Dimensions are normalised 0.0–1.0 and must be reproducible from
    observations via StudentReasoningService.
    """

    knowledge: float = 0.0
    confidence: float = 0.0
    retention: float = 0.0
    consistency: float = 0.0
    momentum: float = 0.0
    exam_readiness: float = 0.0
    snapshot_id: str = ""
    computed_at: datetime | None = None
    evidence_count: int = 0
    reason: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "knowledge", _clamp(self.knowledge))
        object.__setattr__(self, "confidence", _clamp(self.confidence))
        object.__setattr__(self, "retention", _clamp(self.retention))
        object.__setattr__(self, "consistency", _clamp(self.consistency))
        object.__setattr__(self, "momentum", _clamp(self.momentum))
        object.__setattr__(self, "exam_readiness", _clamp(self.exam_readiness))
        when = self.computed_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "computed_at", when.astimezone(UTC).replace(tzinfo=None)
            )

    @classmethod
    def empty(
        cls, *, snapshot_id: str = "", computed_at: datetime | None = None
    ) -> LearningState:
        return cls(
            snapshot_id=snapshot_id,
            computed_at=computed_at or datetime.now(UTC).replace(tzinfo=None),
            reason="initial_empty_state",
        )

    def as_dict(self) -> dict[str, float]:
        return {
            "knowledge": self.knowledge,
            "confidence": self.confidence,
            "retention": self.retention,
            "consistency": self.consistency,
            "momentum": self.momentum,
            "exam_readiness": self.exam_readiness,
        }


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
