"""Relative educational difficulty band for a curriculum topic.

Bands inform sequencing and pathway design. They are not mastery scores
and do not encode pass probability.
"""

from __future__ import annotations

from enum import StrEnum


class TopicDifficulty(StrEnum):
    """Relative difficulty posture of a topic within a curriculum."""

    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    CAPSTONE = "capstone"


_DIFFICULTY_RANK: dict[TopicDifficulty, int] = {
    TopicDifficulty.FOUNDATIONAL: 1,
    TopicDifficulty.INTERMEDIATE: 2,
    TopicDifficulty.ADVANCED: 3,
    TopicDifficulty.CAPSTONE: 4,
}


def difficulty_rank(difficulty: TopicDifficulty) -> int:
    """Return a stable ordinal for comparison (1=FOUNDATIONAL … 4=CAPSTONE)."""
    return _DIFFICULTY_RANK[difficulty]


def difficulty_at_least(
    left: TopicDifficulty, right: TopicDifficulty
) -> bool:
    """True when ``left`` is at least as demanding as ``right``."""
    return difficulty_rank(left) >= difficulty_rank(right)
