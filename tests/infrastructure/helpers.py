"""Shared helpers for infrastructure tests."""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.infrastructure.events.types import EVENT_TYPES

NOW = datetime(2026, 7, 18, 20, 0, tzinfo=UTC)

EVENT_TYPE_LIST = list(EVENT_TYPES)

LEARNERS = tuple(f"L{i}" for i in range(1, 6))
SUBJECTS = tuple(f"S{i}" for i in range(1, 5))
AGGREGATES = (
    "DigitalTwin",
    "DailyMission",
    "SubjectVersion",
    "LearningJourney",
    "IngestionJob",
)


def make_request(
    *,
    event_type: str = "learning_activity_completed",
    learner_id: str = "learner-1",
    subject_id: str = "SUBJ",
    event_id: str = "evt-1",
    correlation_id: str = "corr-1",
) -> OrchestrationRequest:
    return OrchestrationRequest(
        event_type=event_type,
        learner_id=learner_id,
        event_id=event_id,
        occurred_at=NOW,
        subject_id=subject_id,
        correlation_id=correlation_id,
        payload=MappingProxyType({}),
        metadata=MappingProxyType({}),
    )
