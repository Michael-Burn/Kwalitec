"""Mission priority bands and deterministic scoring."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class MissionPriority(StrEnum):
    """Priority band for a daily adaptive mission."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class MissionPriorityScore:
    """Explainable priority score derived from educational decisions.

    Higher ``score`` means higher educational impact for today's session.
    Factors are normalised contributions; they do not invent new educational
    inferences — they only rank decisions already present on the Twin / Graph.
    """

    score: float
    priority: MissionPriority
    gap_severity_points: float = 0.0
    recommendation_points: float = 0.0
    readiness_points: float = 0.0
    momentum_points: float = 0.0
    confidence_points: float = 0.0
    recovery_path_points: float = 0.0
    recent_history_points: float = 0.0
    explanation: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "score", float(self.score))
        priority = (
            self.priority
            if isinstance(self.priority, MissionPriority)
            else MissionPriority(str(self.priority))
        )
        object.__setattr__(self, "priority", priority)


def priority_from_score(score: float) -> MissionPriority:
    """Map a deterministic numeric score to a priority band."""
    if score >= 80.0:
        return MissionPriority.CRITICAL
    if score >= 60.0:
        return MissionPriority.HIGH
    if score >= 40.0:
        return MissionPriority.MEDIUM
    return MissionPriority.LOW


PRIORITY_RANK: dict[MissionPriority, int] = {
    MissionPriority.CRITICAL: 4,
    MissionPriority.HIGH: 3,
    MissionPriority.MEDIUM: 2,
    MissionPriority.LOW: 1,
}
