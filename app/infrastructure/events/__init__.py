"""Version 2 integration event model.

Operational and educational-integration events only. No educational scoring.
"""

from __future__ import annotations

from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.serialization import EventSerializer
from app.infrastructure.events.versioning import EventVersionPolicy

__all__ = [
    "EventRegistry",
    "EventSerializer",
    "EventVersionPolicy",
    "IntegrationEvent",
]
