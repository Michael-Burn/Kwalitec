"""Application events — coordination signals, not domain events."""

from __future__ import annotations

from application.events.base import ApplicationEvent
from application.events.evidence import EvidenceRecordedApplicationEvent
from application.events.learning import (
    LearningEpisodeCompletedApplicationEvent,
    LearningSessionStartedApplicationEvent,
)
from application.events.planning import TeachingPlanGeneratedApplicationEvent
from application.events.twin import DigitalTwinUpdatedApplicationEvent

__all__ = [
    "ApplicationEvent",
    "DigitalTwinUpdatedApplicationEvent",
    "EvidenceRecordedApplicationEvent",
    "LearningEpisodeCompletedApplicationEvent",
    "LearningSessionStartedApplicationEvent",
    "TeachingPlanGeneratedApplicationEvent",
]
