"""Student Experience integration event types (V2-018).

LearningSessionCompleted shares the V2-017 catalogued type name.
New experience-surface events are additive.
"""

from __future__ import annotations

from app.infrastructure.events.base import IntegrationEvent

STUDENT_HOME_VIEWED = "StudentHomeViewed"
LEARNING_SESSION_STARTED = "LearningSessionStarted"
LEARNING_SESSION_COMPLETED = "LearningSessionCompleted"
RECOMMENDATION_ACCEPTED = "RecommendationAccepted"
RECOMMENDATION_DISMISSED = "RecommendationDismissed"
JOURNEY_VIEWED = "JourneyViewed"
REVISION_STARTED = "RevisionStarted"
HISTORY_VIEWED = "HistoryViewed"
PROFILE_UPDATED = "ProfileUpdated"

EXPERIENCE_EVENT_TYPES: tuple[str, ...] = (
    STUDENT_HOME_VIEWED,
    LEARNING_SESSION_STARTED,
    LEARNING_SESSION_COMPLETED,
    RECOMMENDATION_ACCEPTED,
    RECOMMENDATION_DISMISSED,
    JOURNEY_VIEWED,
    REVISION_STARTED,
    HISTORY_VIEWED,
    PROFILE_UPDATED,
)


def student_home_viewed(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a StudentHomeViewed event."""
    return IntegrationEvent.create(STUDENT_HOME_VIEWED, payload, **kwargs)


def learning_session_started(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a LearningSessionStarted event."""
    return IntegrationEvent.create(LEARNING_SESSION_STARTED, payload, **kwargs)


def recommendation_accepted(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a RecommendationAccepted event."""
    return IntegrationEvent.create(RECOMMENDATION_ACCEPTED, payload, **kwargs)


def recommendation_dismissed(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a RecommendationDismissed event."""
    return IntegrationEvent.create(RECOMMENDATION_DISMISSED, payload, **kwargs)


def journey_viewed(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a JourneyViewed event."""
    return IntegrationEvent.create(JOURNEY_VIEWED, payload, **kwargs)


def revision_started(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a RevisionStarted event."""
    return IntegrationEvent.create(REVISION_STARTED, payload, **kwargs)


def history_viewed(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a HistoryViewed event."""
    return IntegrationEvent.create(HISTORY_VIEWED, payload, **kwargs)


def profile_updated(payload: dict, **kwargs) -> IntegrationEvent:
    """Build a ProfileUpdated event."""
    return IntegrationEvent.create(PROFILE_UPDATED, payload, **kwargs)
