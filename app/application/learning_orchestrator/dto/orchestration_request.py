"""Immutable OrchestrationRequest — input to every Learning Orchestrator run."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType


@dataclass(frozen=True)
class OrchestrationRequest:
    """Caller context for a Learning Orchestrator invocation.

    Contains stable identifiers and opaque event attributes only.
    The orchestrator never performs educational reasoning from these
    fields — it only routes them through the pipeline in order.
    """

    event_type: str
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
    correlation_id: str | None = None
    orchestration_id: str | None = None
    payload: MappingProxyType | None = None
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        if not self.learner_id:
            raise ValueError("learner_id is required")
        if not self.event_id:
            raise ValueError("event_id is required")
        if not self.event_type:
            raise ValueError("event_type is required")
        if self.payload is None:
            object.__setattr__(self, "payload", MappingProxyType({}))
        elif not isinstance(self.payload, MappingProxyType):
            object.__setattr__(
                self, "payload", MappingProxyType(dict(self.payload))
            )
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self, "metadata", MappingProxyType(dict(self.metadata))
            )
