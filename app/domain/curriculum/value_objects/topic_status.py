"""Learner-facing availability posture for a curriculum topic.

Status is derived from graph eligibility and learner progress inputs —
it is not stored copyrighted content and does not claim mastery.
"""

from __future__ import annotations

from enum import StrEnum


class TopicStatus(StrEnum):
    """Availability / lifecycle posture of a topic for a learner."""

    LOCKED = "locked"
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


def is_studyable_status(status: TopicStatus) -> bool:
    """True when the learner may begin or continue study on the topic."""
    return status in {TopicStatus.AVAILABLE, TopicStatus.ACTIVE}


def is_terminal_topic_status(status: TopicStatus) -> bool:
    """True when the topic posture no longer invites new educational work."""
    return status in {TopicStatus.COMPLETED, TopicStatus.ARCHIVED}
