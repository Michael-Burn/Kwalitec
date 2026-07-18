"""Event dispatcher — routes learner events into the pipeline engine.

Validates event types and builds orchestration requests. Does not own
educational state or perform educational reasoning.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.application.learning_orchestrator.dto.orchestration_response import (
    OrchestrationResponse,
)
from app.application.learning_orchestrator.exceptions import (
    EventDispatchError,
    OrchestrationError,
)
from app.application.learning_orchestrator.pipeline_engine import PipelineEngine
from app.application.learning_orchestrator.policies.orchestration_policy import (
    OrchestrationPolicy,
)
from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEvent,
    OrchestrationEventType,
)


class EventDispatcher:
    """Dispatch supported learner events to the PipelineEngine."""

    def __init__(
        self,
        engine: PipelineEngine,
        *,
        clock=None,
        id_factory=None,
    ) -> None:
        self._engine = engine
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (
            lambda: f"evt-{int(self._clock().timestamp() * 1000)}"
        )

    @property
    def engine(self) -> PipelineEngine:
        """Underlying pipeline engine."""
        return self._engine

    def dispatch(
        self,
        event: OrchestrationEvent | OrchestrationRequest,
    ) -> OrchestrationResponse:
        """Dispatch ``event`` through the live-learner pipeline.

        Raises:
            EventDispatchError: When the event type is unknown or invalid.
        """
        try:
            if isinstance(event, OrchestrationRequest):
                if not OrchestrationPolicy.is_known_event(event.event_type):
                    raise EventDispatchError(
                        f"Unknown event type: {event.event_type!r}"
                    )
                return self._engine.run(event)

            if not isinstance(event.event_type, OrchestrationEventType):
                raise EventDispatchError(
                    f"Invalid event type: {event.event_type!r}"
                )
            request = self.request_from_event(event)
            return self._engine.run(request, event=event)
        except OrchestrationError as exc:
            raise EventDispatchError(str(exc)) from exc

    def dispatch_type(
        self,
        event_type: str | OrchestrationEventType,
        *,
        learner_id: str,
        event_id: str | None = None,
        occurred_at: datetime | None = None,
        **kwargs,
    ) -> OrchestrationResponse:
        """Convenience dispatcher from event type + identity fields."""
        token = (
            event_type.value
            if isinstance(event_type, OrchestrationEventType)
            else event_type
        )
        if not OrchestrationPolicy.is_known_event(token):
            raise EventDispatchError(f"Unknown event type: {token!r}")
        request = OrchestrationRequest(
            event_type=token,
            learner_id=learner_id,
            event_id=event_id or self._id_factory(),
            occurred_at=occurred_at or self._clock(),
            subject_id=kwargs.get("subject_id"),
            topic_id=kwargs.get("topic_id"),
            journey_id=kwargs.get("journey_id"),
            session_id=kwargs.get("session_id"),
            activity_id=kwargs.get("activity_id"),
            mission_id=kwargs.get("mission_id"),
            evidence_id=kwargs.get("evidence_id"),
            correlation_id=kwargs.get("correlation_id"),
            orchestration_id=kwargs.get("orchestration_id"),
            payload=kwargs.get("payload"),
            metadata=kwargs.get("metadata"),
        )
        return self.dispatch(request)

    @staticmethod
    def request_from_event(event: OrchestrationEvent) -> OrchestrationRequest:
        """Project a domain event into an orchestration request DTO."""
        return OrchestrationRequest(
            event_type=event.event_type.value,
            learner_id=event.learner_id,
            event_id=event.event_id,
            occurred_at=event.occurred_at,
            subject_id=event.subject_id,
            topic_id=event.topic_id,
            journey_id=event.journey_id,
            session_id=event.session_id,
            activity_id=event.activity_id,
            mission_id=event.mission_id,
            evidence_id=event.evidence_id,
            correlation_id=event.correlation_id,
            payload=dict(event.payload or {}),
        )

    @staticmethod
    def supported_events() -> frozenset[str]:
        """Return the set of dispatchable event type tokens."""
        return OrchestrationPolicy.known_event_types()
