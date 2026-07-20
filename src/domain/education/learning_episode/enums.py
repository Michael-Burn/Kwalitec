"""Learning Episode enumerations.

Architecture Source
    LEARNING_EPISODE_ARCHITECTURE.md / LEARNING_EPISODE_LIFECYCLE.md
Concept
    Episode Status / Outcome / Step Status
"""

from __future__ import annotations

from enum import StrEnum


class EpisodeStatus(StrEnum):
    """Lifecycle status of a Learning Episode aggregate."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"


class EpisodeStepStatus(StrEnum):
    """Progress status of an individual episode step."""

    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


class EpisodeOutcomeKind(StrEnum):
    """Modest educational outcome of an episode — never mastery.

    Aligns with Learning Episode Architecture evaluation language:
    advanced / partial / interrupted / remediation / follow-up.
    """

    GOAL_ACHIEVED = "goal_achieved"
    GOAL_PARTIALLY_ACHIEVED = "goal_partially_achieved"
    INTERRUPTED = "interrupted"
    REQUIRES_REMEDIATION = "requires_remediation"
    REQUIRES_FOLLOW_UP = "requires_follow_up"


class DurationBand(StrEnum):
    """Illustrative duration bands (Learning Episode Types §2)."""

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
