"""Domain representation of a Learning Event.

A Learning Event is a discrete occurrence in the learning journey that is a
candidate to become Learning Evidence. It is not Twin state and is not a
persisted evidence row — those concerns belong to later capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_events.event_metadata import EventMetadata
from app.domain.learning_events.event_source import EventSource
from app.domain.learning_events.event_types import LearningEventType


@dataclass(frozen=True)
class LearningEvent:
    """Pure domain object describing an evidence-producing learning occurrence.

    Attributes:
        event_type: Recognised type from the Learning Event catalogue.
        source: Subsystem or channel that produced the event.
        metadata: Contextual attributes (time, curriculum, session, etc.).
        event_id: Optional stable identity for correlation; not a DB primary key.
    """

    event_type: LearningEventType
    source: EventSource
    metadata: EventMetadata
    event_id: str | None = None

    @classmethod
    def create(
        cls,
        event_type: LearningEventType,
        source: EventSource,
        metadata: EventMetadata,
        *,
        event_id: str | None = None,
    ) -> LearningEvent:
        """Construct a Learning Event.

        Args:
            event_type: Catalogue type for the occurrence.
            source: Provenance of the event.
            metadata: Contextual metadata (must include a timestamp).
            event_id: Optional correlation identity.

        Returns:
            A frozen LearningEvent instance.
        """
        return cls(
            event_type=event_type,
            source=source,
            metadata=metadata,
            event_id=event_id,
        )
