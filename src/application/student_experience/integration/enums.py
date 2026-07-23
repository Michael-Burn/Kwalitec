"""Experience Integration enumerations (PX-002).

Presentation / workflow vocabulary only. Never mastery bands,
recommendation categories, or educational reasoning codes.
"""

from __future__ import annotations

from enum import StrEnum


class JourneySurface(StrEnum):
    """Surfaces in the continuous student learning journey."""

    HOME = "home"
    WORKSPACE = "workspace"
    REFLECTION = "reflection"
    JOURNEY = "journey"
    READINESS = "readiness"
    COACH = "coach"


class IntegrationTrigger(StrEnum):
    """Why an experience refresh cascade was requested."""

    HOME_VIEW = "home_view"
    MISSION_COMPLETE = "mission_complete"
    REFLECTION_SUBMITTED = "reflection_submitted"
    SESSION_RESUMED = "session_resumed"
    MANUAL_REFRESH = "manual_refresh"


class CascadeStep(StrEnum):
    """Ordered steps in the post-mission continuous refresh cascade."""

    WORKSPACE = "workspace"
    REFLECTION = "reflection"
    EVIDENCE = "evidence"
    JOURNEY_REFRESH = "journey_refresh"
    READINESS_REFRESH = "readiness_refresh"
    COACH_CELEBRATION = "coach_celebration"
    HOME_REFRESH = "home_refresh"
