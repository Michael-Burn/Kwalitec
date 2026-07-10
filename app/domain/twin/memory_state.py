"""Memory domain state for the Student Digital Twin.

Represents learning retention structure. Structural slots only — no decay
algorithms, spaced-repetition scheduling, or retention forecasts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class RetentionRecord:
    """Structural retention slot for one curriculum topic.

    Belief values are stored when supplied by later update pipelines; this
    record does not compute decay or reinforcement.

    Attributes:
        topic_id: Canonical curriculum topic identity.
        retention_belief: Optional stored retention belief (not computed here).
        last_reinforced: Optional last-reinforcement timestamp.
    """

    topic_id: str
    retention_belief: float | None = None
    last_reinforced: datetime | None = None

    @classmethod
    def create(
        cls,
        topic_id: str,
        *,
        retention_belief: float | None = None,
        last_reinforced: datetime | None = None,
    ) -> RetentionRecord:
        """Construct a RetentionRecord.

        Args:
            topic_id: Non-empty canonical topic identity.
            retention_belief: Optional stored retention belief.
            last_reinforced: Optional reinforcement timestamp.

        Returns:
            A frozen RetentionRecord.

        Raises:
            ValueError: If ``topic_id`` is empty or blank.
        """
        normalized = topic_id.strip() if isinstance(topic_id, str) else ""
        if not normalized:
            raise ValueError("topic_id must be a non-empty string")
        return cls(
            topic_id=normalized,
            retention_belief=retention_belief,
            last_reinforced=last_reinforced,
        )


@dataclass(frozen=True)
class MemoryState:
    """Current retention structure for the learner.

    Attributes:
        retention: Collection of per-topic retention slots.
        revision_ids: Revision / review evidence references.
        last_updated: When this memory snapshot was last materialised.
    """

    retention: tuple[RetentionRecord, ...] = ()
    revision_ids: tuple[str, ...] = field(default_factory=tuple)
    last_updated: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        retention: list[RetentionRecord] | tuple[RetentionRecord, ...] | None = None,
        revision_ids: list[str] | tuple[str, ...] | None = None,
        last_updated: datetime | None = None,
    ) -> MemoryState:
        """Construct a MemoryState.

        Args:
            retention: Optional retention collection.
            revision_ids: Optional revision reference collection.
            last_updated: Optional materialisation timestamp.

        Returns:
            A frozen MemoryState instance.
        """
        return cls(
            retention=tuple(retention or ()),
            revision_ids=tuple(revision_ids or ()),
            last_updated=last_updated,
        )
