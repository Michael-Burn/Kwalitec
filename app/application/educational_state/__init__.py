"""Canonical Educational State — single learner truth for projections.

Phase 1 consolidation: Dashboard, Journey, Coach, Analytics, Revision, and
Readiness cards must project from the same snapshot. They must not recompute
readiness, mastery, or progress independently.

Educational authority remains in Twin / Adaptive / Journey / Mission ports.
This package only assembles an opaque read model for presentation.

Note: port collaborators are duck-typed to avoid import cycles with
``app.application.student_experience``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EducationalStateSnapshot:
    """Opaque educational facts for one learner at one assembly point.

    All fields are port payloads (dicts / sequences). Projection services
    translate them; they never invent educational scores here.
    """

    student_id: str
    learner_summary: dict[str, Any] = field(default_factory=dict)
    readiness_summary: dict[str, Any] = field(default_factory=dict)
    recommendation: dict[str, Any] = field(default_factory=dict)
    todays_session: dict[str, Any] = field(default_factory=dict)
    journey_progress: dict[str, Any] = field(default_factory=dict)
    journey_topics: tuple[dict[str, Any], ...] = ()
    learning_insights: dict[str, Any] = field(default_factory=dict)
    revision_options: tuple[dict[str, Any], ...] = ()
    twin_available: bool = False
    adaptive_available: bool = False
    mission_available: bool = False
    journey_available: bool = False


class EducationalStateService:
    """Load EducationalStateSnapshot once per learner for Experience surfaces.

    Instance-scoped cache avoids duplicate port reads when DashboardService
    assembles multiple surfaces in one request.
    """

    def __init__(
        self,
        *,
        student_twin: Any | None = None,
        adaptive_decision: Any | None = None,
        mission: Any | None = None,
        learning_journey: Any | None = None,
    ) -> None:
        self._twin = student_twin
        self._adaptive = adaptive_decision
        self._mission = mission
        self._journey = learning_journey
        self._cache: dict[str, EducationalStateSnapshot] = {}

    def load(self, student_id: str) -> EducationalStateSnapshot:
        """Return the educational state for ``student_id`` (cached)."""
        sid = (student_id or "").strip()
        if not sid:
            return EducationalStateSnapshot(student_id="")
        cached = self._cache.get(sid)
        if cached is not None:
            return cached
        snapshot = self._assemble(sid)
        self._cache[sid] = snapshot
        return snapshot

    def clear_cache(self) -> None:
        """Drop cached snapshots (tests / new request boundary)."""
        self._cache.clear()

    def _assemble(self, student_id: str) -> EducationalStateSnapshot:
        twin_ok = self._twin is not None and self._twin.is_available()
        adaptive_ok = (
            self._adaptive is not None and self._adaptive.is_available()
        )
        mission_ok = self._mission is not None and self._mission.is_available()
        journey_ok = (
            self._journey is not None and self._journey.is_available()
        )

        learner: dict[str, Any] = {}
        readiness: dict[str, Any] = {}
        insights: dict[str, Any] = {}
        if twin_ok and self._twin is not None:
            learner = dict(self._twin.get_learner_summary(student_id) or {})
            readiness = dict(self._twin.get_readiness_summary(student_id) or {})
            insights = dict(self._twin.get_learning_insights(student_id) or {})

        recommendation: dict[str, Any] = {}
        revision_options: tuple[dict[str, Any], ...] = ()
        if adaptive_ok and self._adaptive is not None:
            recommendation = dict(
                self._adaptive.get_todays_recommendation(student_id) or {}
            )
            raw_options = self._adaptive.get_revision_options(student_id) or ()
            revision_options = tuple(dict(o) for o in raw_options)

        session: dict[str, Any] = {}
        if mission_ok and self._mission is not None:
            session = dict(self._mission.get_todays_session(student_id) or {})

        progress: dict[str, Any] = {}
        topics: tuple[dict[str, Any], ...] = ()
        if journey_ok and self._journey is not None:
            progress = dict(self._journey.get_journey_progress(student_id) or {})
            topics = tuple(
                dict(t) for t in (self._journey.get_topic_list(student_id) or ())
            )

        return EducationalStateSnapshot(
            student_id=student_id,
            learner_summary=learner,
            readiness_summary=readiness,
            recommendation=recommendation,
            todays_session=session,
            journey_progress=progress,
            journey_topics=topics,
            learning_insights=insights,
            revision_options=revision_options,
            twin_available=twin_ok,
            adaptive_available=adaptive_ok,
            mission_available=mission_ok,
            journey_available=journey_ok,
        )


__all__ = [
    "EducationalStateService",
    "EducationalStateSnapshot",
]
