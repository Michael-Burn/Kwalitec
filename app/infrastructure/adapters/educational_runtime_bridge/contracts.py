"""Educational Runtime Bridge contracts — Mission / Rec / Journey / History.

Translator interfaces only. Educational law stays in Runtime A services.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Protocol, runtime_checkable

# Shared failure codes (BRIDGE_INTERFACE_SPECIFICATION.md).
UNAVAILABLE = "UNAVAILABLE"
NO_ACTIVE_PLAN = "NO_ACTIVE_PLAN"
OUTSIDE_PLAN_WINDOW = "OUTSIDE_PLAN_WINDOW"
NOT_FOUND = "NOT_FOUND"
FORBIDDEN = "FORBIDDEN"
INVALID_STATE = "INVALID_STATE"
EVIDENCE_REJECTED = "EVIDENCE_REJECTED"

BRIDGE_ERROR_CODES = frozenset(
    {
        UNAVAILABLE,
        NO_ACTIVE_PLAN,
        OUTSIDE_PLAN_WINDOW,
        NOT_FOUND,
        FORBIDDEN,
        INVALID_STATE,
        EVIDENCE_REJECTED,
    }
)

AUTHORITY_PLANNING_SERVICE = "planning_service"
AUTHORITY_STUDY_SESSION_SERVICE = "study_session_service"
AUTHORITY_RECOMMENDATION_BRIDGE = "recommendation_bridge"
AUTHORITY_RECOMMENDATION_SERVICE = "recommendation_service"
AUTHORITY_JOURNEY_BRIDGE = "journey_bridge"
AUTHORITY_HISTORY_BRIDGE = "history_bridge"


@dataclass(frozen=True)
class BridgeResult:
    """Result envelope for bridge adapter calls.

    ``ok`` is True when the bridge completed without infrastructure failure.
    Absence of a mission (no plan / outside window / not found) is a successful
    translation with ``value is None`` and an informative ``error_code``.
    """

    ok: bool
    value: dict[str, Any] | None = None
    error_code: str | None = None
    message: str | None = None
    fallback_used: bool = False


@runtime_checkable
class MissionReadBridge(Protocol):
    """PlanningBridge read contract — today's mission projection only.

    Does not start, resume, complete, or generate missions.
    """

    @property
    def adapter_id(self) -> str:
        """Stable bridge adapter identity."""

    def get_todays_session(
        self,
        student_id: str,
        *,
        as_of_date: date | None = None,
    ) -> BridgeResult:
        """Project today's SQL Mission as an Experience opaque session dict."""


@runtime_checkable
class MissionStartBridge(Protocol):
    """Mission Start contract — ensure today + start session write path.

    Translates to PlanningService.generate_today_mission and
    StudySessionService.start_session. Does not resume or complete.
    """

    @property
    def adapter_id(self) -> str:
        """Stable bridge adapter identity."""

    def start_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
        as_of_date: date | None = None,
    ) -> BridgeResult:
        """Ensure today's mission and start it via Runtime A."""


@runtime_checkable
class MissionResumeBridge(Protocol):
    """Mission Resume contract — locate active session continuity path.

    Translates to StudySessionService.get_owned_mission /
    MissionService.get_today_mission. Does not start, generate, or complete.
    """

    @property
    def adapter_id(self) -> str:
        """Stable bridge adapter identity."""

    def resume_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
        as_of_date: date | None = None,
    ) -> BridgeResult:
        """Locate and project the student's active Runtime A session."""


@runtime_checkable
class SessionCompletionBridge(Protocol):
    """Session Completion contract — Evidence Before Completion write path.

    Translates to StudySessionService / MissionService / Evidence Authority.
    Does not generate recommendations or invent completion state.
    """

    @property
    def adapter_id(self) -> str:
        """Stable bridge adapter identity."""

    def complete_session(
        self,
        student_id: str,
        *,
        session_id: str | None = None,
        mission_id: str | None = None,
        outcome: dict[str, Any] | None = None,
        topic_title: str = "",
        estimated_minutes: int | None = None,
    ) -> BridgeResult:
        """Validate, commit evidence, then complete via Runtime A."""


@runtime_checkable
class RecommendationBridge(Protocol):
    """Recommendation read contract — Runtime A recommendation projection.

    Translates to RecommendationService (+ optional Mission alignment).
    Does not write decisions, alter learning state, or invent recommendations.
    """

    @property
    def adapter_id(self) -> str:
        """Stable bridge adapter identity."""

    def get_todays_recommendation(
        self,
        student_id: str,
        *,
        mission_projection: dict[str, Any] | None = None,
        as_of_date: date | None = None,
    ) -> BridgeResult:
        """Project today's Runtime A recommendation as an Experience opaque dict."""


@runtime_checkable
class JourneyBridge(Protocol):
    """Journey read contract — Runtime A learning-journey projection.

    Translates StudyPlan / Mission / StudyAttempt / TopicProgress / Lifecycle
    reads into Experience Journey DTOs. Does not calculate educational state
    or write SQL.
    """

    @property
    def adapter_id(self) -> str:
        """Stable bridge adapter identity."""

    def project_journey(
        self,
        student_id: str,
        *,
        as_of_date: date | None = None,
        include_timeline: bool = True,
        timeline_limit: int = 20,
    ) -> BridgeResult:
        """Project the learner Journey exclusively from Runtime A."""


@runtime_checkable
class HistoryBridge(Protocol):
    """History read contract — Runtime A accomplishment narrative projection.

    Translates Mission / StudyAttempt / TopicProgress / Lifecycle / Readiness
    reads into Experience History DTOs. Does not calculate educational state
    or write SQL.
    """

    @property
    def adapter_id(self) -> str:
        """Stable bridge adapter identity."""

    def project_history(
        self,
        student_id: str,
        *,
        limit: int = 20,
        offset: int = 0,
        cursor: str | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        event_types: list[str] | None = None,
        lifecycle_stage: str | None = None,
        topic_code: str | None = None,
    ) -> BridgeResult:
        """Project History exclusively from Runtime A with stable pagination."""

    def get_evidence_summary(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        attempt_id: str | None = None,
    ) -> BridgeResult:
        """Read-only evidence inspect projection for a History item."""
