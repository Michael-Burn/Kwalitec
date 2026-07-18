"""Curriculum Navigation port consumed by Mission Engine 2.0."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class CurriculumNavigationPort(Protocol):
    """Structural contract for Curriculum Navigation Service reads.

    Mission Engine 2.0 may confirm a topic exists in the curriculum order.
    It must never select the next topic or invent sequencing.
    """

    def topic_available(self, topic_id: str) -> bool:
        """True when ``topic_id`` is present in the navigation order."""

    def ordered_topic_ids(self) -> tuple[str, ...]:
        """Canonical hierarchy order of topic ids."""
