"""Orchestration events — discrete learner occurrences to coordinate.

Events are coordination signals only. They are not Twin state, curriculum
mutations, or persisted evidence rows.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType


class OrchestrationEventType(StrEnum):
    """Supported live-learner event types (extensible catalogue)."""

    LEARNING_ACTIVITY_COMPLETED = "learning_activity_completed"
    KNOWLEDGE_CHECK_COMPLETED = "knowledge_check_completed"
    REFLECTION_SUBMITTED = "reflection_submitted"
    SESSION_COMPLETED = "session_completed"
    MISSION_COMPLETED = "mission_completed"
    MANUAL_CONFIDENCE_UPDATE = "manual_confidence_update"

    @classmethod
    def resolve(cls, value: str) -> OrchestrationEventType:
        """Resolve a catalogue token; unknown values raise ValueError.

        Future event types should be added as members. Callers that need
        soft-fail behaviour should catch ValueError rather than inventing
        aliases here.
        """
        try:
            return cls(value)
        except ValueError as exc:
            raise ValueError(f"Unknown orchestration event type: {value!r}") from exc


@dataclass(frozen=True)
class OrchestrationEvent:
    """Immutable learner event accepted by the Learning Orchestrator.

    Attributes:
        event_type: Catalogue type for the occurrence.
        learner_id: Stable learner identity (not a DB key requirement).
        event_id: Correlation identity for this occurrence.
        occurred_at: When the event happened (timezone-aware preferred).
        subject_id: Optional subject scope.
        topic_id: Optional topic scope.
        journey_id: Optional journey scope.
        session_id: Optional session scope.
        activity_id: Optional activity scope.
        mission_id: Optional mission scope.
        evidence_id: Optional evidence correlation id.
        payload: Opaque structural attributes from the caller.
        correlation_id: Optional cross-system correlation token.
    """

    event_type: OrchestrationEventType
    learner_id: str
    event_id: str
    occurred_at: datetime
    subject_id: str | None = None
    topic_id: str | None = None
    journey_id: str | None = None
    session_id: str | None = None
    activity_id: str | None = None
    mission_id: str | None = None
    evidence_id: str | None = None
    payload: MappingProxyType | None = None
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        if not self.learner_id:
            raise ValueError("learner_id is required")
        if not self.event_id:
            raise ValueError("event_id is required")
        if self.payload is None:
            object.__setattr__(self, "payload", MappingProxyType({}))
        elif not isinstance(self.payload, MappingProxyType):
            object.__setattr__(
                self, "payload", MappingProxyType(dict(self.payload))
            )

    @classmethod
    def create(
        cls,
        *,
        event_type: OrchestrationEventType | str,
        learner_id: str,
        event_id: str,
        occurred_at: datetime,
        subject_id: str | None = None,
        topic_id: str | None = None,
        journey_id: str | None = None,
        session_id: str | None = None,
        activity_id: str | None = None,
        mission_id: str | None = None,
        evidence_id: str | None = None,
        payload: dict | MappingProxyType | None = None,
        correlation_id: str | None = None,
    ) -> OrchestrationEvent:
        """Construct a validated orchestration event."""
        resolved = (
            event_type
            if isinstance(event_type, OrchestrationEventType)
            else OrchestrationEventType.resolve(event_type)
        )
        return cls(
            event_type=resolved,
            learner_id=learner_id,
            event_id=event_id,
            occurred_at=occurred_at,
            subject_id=subject_id,
            topic_id=topic_id,
            journey_id=journey_id,
            session_id=session_id,
            activity_id=activity_id,
            mission_id=mission_id,
            evidence_id=evidence_id,
            payload=payload,  # type: ignore[arg-type]
            correlation_id=correlation_id,
        )
