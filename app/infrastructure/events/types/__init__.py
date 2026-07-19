"""Named Version 2 integration event types."""

from __future__ import annotations

from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.types.experience import EXPERIENCE_EVENT_TYPES

EVIDENCE_RECORDED = "EvidenceRecorded"
TWIN_UPDATED = "TwinUpdated"
ADAPTIVE_DECISION_GENERATED = "AdaptiveDecisionGenerated"
MISSION_UPDATED = "MissionUpdated"
CURRICULUM_PUBLISHED = "CurriculumPublished"
CURRICULUM_VALIDATED = "CurriculumValidated"
LEARNING_SESSION_COMPLETED = "LearningSessionCompleted"

# Core + Student Experience surface events (V2-017 / V2-018).
EVENT_TYPES: tuple[str, ...] = tuple(
    dict.fromkeys(
        (
            EVIDENCE_RECORDED,
            TWIN_UPDATED,
            ADAPTIVE_DECISION_GENERATED,
            MISSION_UPDATED,
            CURRICULUM_PUBLISHED,
            CURRICULUM_VALIDATED,
            LEARNING_SESSION_COMPLETED,
            *EXPERIENCE_EVENT_TYPES,
        )
    )
)


def evidence_recorded(
    payload: dict,
    **kwargs,
) -> IntegrationEvent:
    """Build an EvidenceRecorded event."""
    return IntegrationEvent.create(EVIDENCE_RECORDED, payload, **kwargs)


def twin_updated(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a TwinUpdated event."""
    return IntegrationEvent.create(TWIN_UPDATED, payload, **kwargs)


def adaptive_decision_generated(payload: dict, **kwargs) -> IntegrationEvent:
    """Build an AdaptiveDecisionGenerated event."""
    return IntegrationEvent.create(
        ADAPTIVE_DECISION_GENERATED, payload, **kwargs
    )


def mission_updated(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a MissionUpdated event."""
    return IntegrationEvent.create(MISSION_UPDATED, payload, **kwargs)


def curriculum_published(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a CurriculumPublished event."""
    return IntegrationEvent.create(CURRICULUM_PUBLISHED, payload, **kwargs)


def curriculum_validated(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a CurriculumValidated event."""
    return IntegrationEvent.create(CURRICULUM_VALIDATED, payload, **kwargs)


def learning_session_completed(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a LearningSessionCompleted event."""
    return IntegrationEvent.create(
        LEARNING_SESSION_COMPLETED, payload, **kwargs
    )
