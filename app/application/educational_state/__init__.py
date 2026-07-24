"""Canonical Educational State — single learner truth for projections.

Phase 1 consolidation: Dashboard, Journey, Coach, Analytics, Revision, and
Readiness cards must project from the same snapshot. They must not recompute
readiness, mastery, or progress independently.

Educational authority remains in Twin / Adaptive / Journey / Mission ports.
This package only assembles an opaque read model for presentation.

PRD-001 Phase D: after a fresh assembly, analytics may observe a
``educational_state.snapshot`` event (hash + metadata only) when the
content hash changes. Analytics never derives or stores Educational State.

Note: port collaborators are duck-typed to avoid import cycles with
``app.application.student_experience``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)

# Process-scoped last-emitted content hash per student (material-change gate).
# Not cleared by ``clear_cache`` — request-boundary cache must not re-emit
# identical Educational State on every page view.
_last_emitted_content_hash: dict[str, str] = {}


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
        # Analytics observes assembly success only — never before, never derives.
        EducationalStateService._observe_snapshot_if_material(snapshot)
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

    @staticmethod
    def _observe_snapshot_if_material(snapshot: EducationalStateSnapshot) -> None:
        """Emit ``educational_state.snapshot`` on material content-hash change.

        Fail-open: analytics errors never affect Educational State assembly.
        Hash + metadata only — Educational State payload is never passed to
        analytics.
        """
        try:
            sid = (snapshot.student_id or "").strip()
            if not sid:
                return
            try:
                user_id = int(sid)
            except (TypeError, ValueError):
                # Analytics identity is opaque integer user id only.
                return

            from app.application.educational_state.content_hash import (
                compute_educational_state_content_hash,
            )

            content_hash = compute_educational_state_content_hash(snapshot)
            previous = _last_emitted_content_hash.get(sid)
            if previous == content_hash:
                return

            snapshot_id = uuid4().hex
            from app.infrastructure.analytics.dispatcher import DispatchStatus
            from app.infrastructure.analytics.educational_state_events import (
                emit_educational_state_snapshot,
            )

            result = emit_educational_state_snapshot(
                user_id=user_id,
                snapshot_id=snapshot_id,
                content_hash=content_hash,
            )
            # Gate only after intentional outcomes — FAILED/REJECTED may retry.
            if result.status in (
                DispatchStatus.ENQUEUED,
                DispatchStatus.DUPLICATE,
                DispatchStatus.DISABLED,
            ):
                _last_emitted_content_hash[sid] = content_hash
        except Exception:  # noqa: BLE001 — analytics must never break learning
            logger.exception(
                "analytics.emit_failed educational_state.snapshot student=%s",
                getattr(snapshot, "student_id", ""),
            )


def reset_snapshot_observation_state() -> None:
    """Clear process-scoped material-change memory (tests only)."""
    _last_emitted_content_hash.clear()


__all__ = [
    "EducationalStateService",
    "EducationalStateSnapshot",
    "reset_snapshot_observation_state",
]
