"""Contextual metadata associated with a Learning Event.

Implementation-independent attributes that situate an event in curriculum,
session, and learner context. Persistence and transport shapes are out of scope.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class EventMetadata:
    """Contextual information carried with a Learning Event.

    Attributes:
        timestamp: When the event occurred (timezone-aware preferred by callers).
        topic_id: Canonical curriculum topic identity when topic-scoped.
        curriculum_id: Canonical curriculum identity when curriculum-scoped.
        session_id: Study or practice session correlation id when applicable.
        duration_seconds: Effort or block duration when known.
        difficulty: Difficulty band or label when known (e.g. exam-standard).
        confidence: Explicit self-report confidence when the event carries one.
        source: Optional provenance mirror; primary source lives on LearningEvent.
        tags: Free-form classification tags (e.g. ``self_report``).
        attributes: Extensible key/value bag for producer-specific context.
    """

    timestamp: datetime
    topic_id: str | None = None
    curriculum_id: str | None = None
    session_id: str | None = None
    duration_seconds: int | None = None
    difficulty: str | None = None
    confidence: float | None = None
    source: str | None = None
    tags: tuple[str, ...] = ()
    attributes: dict[str, Any] = field(default_factory=dict)

    def has_tag(self, tag: str) -> bool:
        """Return True if ``tag`` is present in ``tags``."""
        return tag in self.tags

    def with_tags(self, *extra_tags: str) -> EventMetadata:
        """Return a copy with additional tags (deduplicated, order-preserving)."""
        merged: list[str] = list(self.tags)
        for tag in extra_tags:
            if tag not in merged:
                merged.append(tag)
        return EventMetadata(
            timestamp=self.timestamp,
            topic_id=self.topic_id,
            curriculum_id=self.curriculum_id,
            session_id=self.session_id,
            duration_seconds=self.duration_seconds,
            difficulty=self.difficulty,
            confidence=self.confidence,
            source=self.source,
            tags=tuple(merged),
            attributes=dict(self.attributes),
        )
