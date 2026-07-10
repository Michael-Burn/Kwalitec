"""Learning Events domain package.

Pure conceptual objects for evidence-producing occurrences. See README.md.
"""

from __future__ import annotations

from app.domain.learning_events.event_metadata import EventMetadata
from app.domain.learning_events.event_source import EventSource
from app.domain.learning_events.event_types import LearningEventType
from app.domain.learning_events.learning_event import LearningEvent

__all__ = [
    "EventMetadata",
    "EventSource",
    "LearningEvent",
    "LearningEventType",
]
