"""Stateless orchestration rules — event → pipeline stage order.

Defines lawful stage sequences only. No educational reasoning.
"""

from __future__ import annotations

from app.application.learning_orchestrator.exceptions import OrchestrationError
from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEventType,
)
from app.domain.learning_orchestrator.pipeline_stage import (
    CANONICAL_PIPELINE,
    PipelineStageName,
)

# Canonical live-learner dependency chain (composition order).
DEPENDENCY_CHAIN: tuple[str, ...] = tuple(s.value for s in CANONICAL_PIPELINE)

PORT_NAMES: tuple[str, ...] = (
    "evidence",
    "twin",
    "adaptive_learning",
    "mission",
    "analytics",
)

# Full pipeline for all supported live events (deterministic order).
_FULL_PIPELINE: tuple[PipelineStageName, ...] = CANONICAL_PIPELINE

# Event → stage sequence. Future event types extend this table only.
_EVENT_STAGES: dict[str, tuple[PipelineStageName, ...]] = {
    OrchestrationEventType.LEARNING_ACTIVITY_COMPLETED.value: _FULL_PIPELINE,
    OrchestrationEventType.KNOWLEDGE_CHECK_COMPLETED.value: _FULL_PIPELINE,
    OrchestrationEventType.REFLECTION_SUBMITTED.value: _FULL_PIPELINE,
    OrchestrationEventType.SESSION_COMPLETED.value: _FULL_PIPELINE,
    OrchestrationEventType.MISSION_COMPLETED.value: _FULL_PIPELINE,
    OrchestrationEventType.MANUAL_CONFIDENCE_UPDATE.value: (
        PipelineStageName.EVIDENCE,
        PipelineStageName.TWIN,
        PipelineStageName.DECISION,
        PipelineStageName.ANALYTICS,
    ),
}


class OrchestrationPolicy:
    """Deterministic event → stage ordering (stateless)."""

    @staticmethod
    def known_event_types() -> frozenset[str]:
        """Return the set of supported event type tokens."""
        return frozenset(_EVENT_STAGES)

    @staticmethod
    def is_known_event(event_type: str) -> bool:
        """True when ``event_type`` is a supported orchestration event."""
        return event_type in _EVENT_STAGES

    @staticmethod
    def stages_for(event_type: str) -> tuple[PipelineStageName, ...]:
        """Return ordered pipeline stages for ``event_type``.

        Raises:
            OrchestrationError: When the event type is unknown.
        """
        try:
            return _EVENT_STAGES[event_type]
        except KeyError as exc:
            raise OrchestrationError(
                f"Unknown orchestration event type: {event_type!r}"
            ) from exc

    @staticmethod
    def required_ports(event_type: str) -> frozenset[str]:
        """Return port names required by ``event_type``."""
        from app.domain.learning_orchestrator.pipeline_stage import (
            STAGE_PORT_NAMES,
        )

        stages = OrchestrationPolicy.stages_for(event_type)
        return frozenset(STAGE_PORT_NAMES[s] for s in stages)

    @staticmethod
    def dependency_chain() -> tuple[str, ...]:
        """Return the canonical live-learner pipeline order."""
        return DEPENDENCY_CHAIN

    @staticmethod
    def port_names() -> tuple[str, ...]:
        """Return all known port names in canonical order."""
        return PORT_NAMES

    @staticmethod
    def event_ready(
        event_type: str,
        *,
        registered: frozenset[str] | set[str],
    ) -> bool:
        """True when every required port for ``event_type`` is registered."""
        if not OrchestrationPolicy.is_known_event(event_type):
            return False
        required = OrchestrationPolicy.required_ports(event_type)
        return required.issubset(registered)

    @staticmethod
    def register_event_stages(
        event_type: str,
        stages: tuple[PipelineStageName, ...],
    ) -> None:
        """Extension hook for tests / future event types (mutates table).

        Production callers should prefer adding members to
        ``OrchestrationEventType`` and updating the static table at
        module load. This method exists for controlled extension tests.
        """
        if not stages:
            raise OrchestrationError(
                f"Cannot register empty stages for {event_type!r}"
            )
        _EVENT_STAGES[event_type] = stages
