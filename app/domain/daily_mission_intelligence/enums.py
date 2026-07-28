"""Daily Mission Intelligence enumerations (ILE-004).

Presentation / educational-memory vocabulary for one primary daily mission.
Never Twin, ranking, or engine labels.
"""

from __future__ import annotations

from enum import StrEnum


class MissionLifecyclePhase(StrEnum):
    """Student-visible mission lifecycle (ILE-004).

    Created → Presented → Accepted → Completed | Deferred →
    Journal → Timeline → Next mission.
    """

    CREATED = "created"
    PRESENTED = "presented"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    JOURNALED = "journaled"
    NEXT_READY = "next_ready"


class MissionOptimisationAxis(StrEnum):
    """Lawful educational optimisation axes for mission selection rationale.

    Missions may cite these as educational reasons. Engagement, screen time,
    streaks, and retention metrics are forbidden axes.
    """

    LEARNING_VALUE = "learning_value"
    MOMENTUM = "momentum"
    KNOWLEDGE_STABILITY = "knowledge_stability"
    RECOVERY = "recovery"
    CONSISTENCY = "consistency"


# Student-safe labels for optimisation axes (Study Sensei voice).
AXIS_LABELS: dict[str, str] = {
    MissionOptimisationAxis.LEARNING_VALUE: "Learning value",
    MissionOptimisationAxis.MOMENTUM: "Learning momentum",
    MissionOptimisationAxis.KNOWLEDGE_STABILITY: "Knowledge stability",
    MissionOptimisationAxis.RECOVERY: "Recovery",
    MissionOptimisationAxis.CONSISTENCY: "Consistency",
}


# Forbidden optimisation language — engagement theatre.
FORBIDDEN_OPTIMISATION_TERMS: tuple[str, ...] = (
    "engagement",
    "screen time",
    "streak",
    "retention metric",
    "daily active",
    "gamification",
    "points for opening",
)
