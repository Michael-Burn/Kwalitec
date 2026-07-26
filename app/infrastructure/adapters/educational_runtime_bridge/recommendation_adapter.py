"""Recommendation Read Adapter — RecommendationBridge read path to Runtime A.

Experience → RecommendationAdapter → RecommendationService (+ Mission read)
→ Learning State / Evidence-backed progress → SQL.

Translator only: no recommendation math, no learning-state mutation, no demo
fallback, no caching of authoritative educational state.
"""

from __future__ import annotations

import logging
import time
from datetime import date
from typing import Any

from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.events.registry import EventRegistry

from .contracts import (
    FORBIDDEN,
    NOT_FOUND,
    UNAVAILABLE,
    BridgeResult,
)
from .recommendation_mapper import map_recommendation_to_projection
from .recommendation_telemetry import (
    emit_failure,
    emit_latency,
    emit_requested,
    emit_success,
)

logger = logging.getLogger(__name__)


class RecommendationAdapter:
    """Bridge adapter: project today's Runtime A recommendation for Experience.

    Controlled by ``ENABLE_RECOMMENDATION_BRIDGE``. Retrieves canonical
    recommendations from ``RecommendationService`` and aligns the primary label
    to today's SQL Mission when present. Never calls write APIs
    (``record_decision``, mission generate/start/complete) and never falls back
    to ``seeded_demo_adaptive``.
    """

    ADAPTER_ID = "recommendation_adapter"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        recommendation_service: Any | None = None,
        mission_service: Any | None = None,
        study_plan_service: Any | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._recommendation_service = recommendation_service
        self._mission_service = mission_service
        self._study_plan_service = study_plan_service
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=True,
            version=self.ADAPTER_VERSION,
        )

    @property
    def adapter_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_available(self) -> bool:
        return True

    def get_todays_recommendation(
        self,
        student_id: str,
        *,
        mission_projection: dict[str, Any] | None = None,
        as_of_date: date | None = None,
    ) -> BridgeResult:
        """Read Runtime A recommendation and map to opaque Experience DTO.

        Read-only: does not alter learning state, evidence, or missions.
        Does not invent recommendations independently of Runtime A.
        """
        sid = (student_id or "").strip()
        self._diagnostics.record_call(self.ADAPTER_ID)
        emit_requested(self._events, student_id=sid)
        started = time.perf_counter()

        try:
            user_id = self._parse_user_id(sid)
            if user_id is None:
                result = BridgeResult(
                    ok=False,
                    error_code=FORBIDDEN,
                    message="student_id must map to an authenticated user id",
                )
                self._finish(sid, result, started, failure=True)
                return result

            resolved_date = as_of_date or date.today()
            mission = self._resolve_mission(
                user_id,
                mission_projection=mission_projection,
                as_of_date=as_of_date,
            )
            # B3 (PX-003): pass the same calendar day used to resolve today's
            # mission so weekday/weekend selection agrees with Mission's own
            # duration call path (StudySessionService / session_duration.py) —
            # previously called without a date, only Mission's path knew the
            # day, letting weekend estimates silently diverge from Home's.
            estimated = self._estimated_minutes(user_id, mission_date=resolved_date)
            topic_code = ""
            if isinstance(mission_projection, dict):
                topic_code = str(mission_projection.get("topic_code") or "")

            recs, rec_error = self._fetch_recommendations(user_id)
            fallback_used = False
            primary: dict[str, Any] | None = None
            alternatives: list[dict[str, Any]] = []

            if rec_error is not None and mission is None:
                result = BridgeResult(
                    ok=False,
                    error_code=UNAVAILABLE,
                    message=rec_error,
                )
                self._finish(sid, result, started, failure=True)
                return result

            if rec_error is not None and mission is not None:
                # Spec fallback: mission-only label when RecommendationService fails.
                fallback_used = True
                primary = None
                alternatives = []
            elif recs:
                primary = dict(recs[0])
                alternatives = [dict(r) for r in recs[1:]]
            else:
                primary = None
                alternatives = []

            projection = map_recommendation_to_projection(
                student_id=sid,
                mission=mission,
                primary=primary,
                alternatives=alternatives,
                topic_code=topic_code,
                estimated_minutes=estimated,
                fallback_used=fallback_used,
            )

            if projection is None:
                result = BridgeResult(
                    ok=True,
                    value=None,
                    error_code=NOT_FOUND,
                    message="no recommendation and no mission for projection",
                    fallback_used=False,
                )
                self._finish(sid, result, started, failure=False)
                return result

            result = BridgeResult(
                ok=True,
                value=projection,
                fallback_used=fallback_used,
            )
            self._finish(
                sid,
                result,
                started,
                failure=False,
                decision_id=str(projection.get("decision_id") or "") or None,
                mission_id=projection.get("mission_id"),
                mission_aligned=bool(projection.get("mission_aligned")),
            )
            return result
        except Exception as exc:  # noqa: BLE001 — bridge must fail closed
            logger.exception(
                "RecommendationAdapter unavailable for student_id=%s", sid
            )
            result = BridgeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message=str(exc)[:256],
            )
            self._finish(sid, result, started, failure=True)
            return result

    def get_todays_recommendation_opaque(
        self, student_id: str
    ) -> dict[str, Any] | None:
        """Opaque-engine compatible entry used by ExperienceAdaptiveAdapter."""
        result = self.get_todays_recommendation(student_id)
        if not result.ok:
            return None
        return result.value

    def _finish(
        self,
        student_id: str,
        result: BridgeResult,
        started: float,
        *,
        failure: bool,
        decision_id: str | None = None,
        mission_id: str | None = None,
        mission_aligned: bool | None = None,
    ) -> None:
        latency_ms = (time.perf_counter() - started) * 1000.0
        if failure:
            self._diagnostics.record_call(self.ADAPTER_ID, error=True)
            emit_failure(
                self._events,
                student_id=student_id,
                error_code=result.error_code or UNAVAILABLE,
                message=result.message,
            )
        else:
            resolved_decision_id = decision_id
            resolved_mission_id = mission_id
            resolved_aligned = mission_aligned
            if result.value is not None:
                if resolved_decision_id is None:
                    resolved_decision_id = str(
                        result.value.get("decision_id") or ""
                    ) or None
                if resolved_mission_id is None:
                    mid = result.value.get("mission_id")
                    resolved_mission_id = None if mid is None else str(mid)
                if resolved_aligned is None:
                    resolved_aligned = bool(result.value.get("mission_aligned"))
            emit_success(
                self._events,
                student_id=student_id,
                decision_id=resolved_decision_id,
                mission_id=resolved_mission_id,
                mission_aligned=resolved_aligned,
                error_code=result.error_code,
                fallback_used=result.fallback_used,
            )
        emit_latency(
            self._events,
            student_id=student_id,
            latency_ms=latency_ms,
            ok=not failure,
        )

    def _resolve_mission(
        self,
        user_id: int,
        *,
        mission_projection: dict[str, Any] | None,
        as_of_date: date | None,
    ) -> Any | None:
        """Locate today's mission for alignment — read only."""
        if isinstance(mission_projection, dict):
            title = str(mission_projection.get("topic_title") or "").strip()
            mid = mission_projection.get("mission_id") or mission_projection.get(
                "session_id"
            )
            if title or mid:
                return _MissionProjection(
                    id=mid or "",
                    title=title,
                    user_id=user_id,
                )
        mission_svc = self._resolve_mission_service()
        mission_date = as_of_date or date.today()
        mission = mission_svc.get_today_mission(user_id, mission_date=mission_date)
        if mission is None:
            return None
        if int(getattr(mission, "user_id", user_id)) != int(user_id):
            logger.warning(
                "RecommendationAdapter ignoring mission ownership mismatch "
                "user_id=%s mission_user=%s",
                user_id,
                getattr(mission, "user_id", None),
            )
            return None
        return mission

    def _fetch_recommendations(
        self, user_id: int
    ) -> tuple[list[dict[str, Any]], str | None]:
        """Retrieve canonical recommendations from Runtime A (read-only)."""
        try:
            rec_svc = self._resolve_recommendation_service()
            raw = rec_svc.generate_recommendations(user_id, limit=5)
            if raw is None:
                return [], None
            return [dict(r) for r in raw], None
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "RecommendationService unavailable for user_id=%s", user_id
            )
            return [], str(exc)[:256]

    def _estimated_minutes(
        self, user_id: int, *, mission_date: date | None = None
    ) -> int | None:
        """Project canonical planned session minutes (EP-007.1) — no invention.

        ``mission_date`` must match the day used to resolve today's mission
        (see B3, PX-003 release blockers) so weekday/weekend selection never
        diverges from Mission's own duration call path.
        """
        from app.application.student_experience.session_duration import (
            resolve_planned_session_minutes,
        )

        try:
            plan = self._resolve_study_plan_service().get_user_active_plan(user_id)
            return resolve_planned_session_minutes(plan, mission_date=mission_date)
        except Exception:  # noqa: BLE001
            return None

    @staticmethod
    def _parse_user_id(student_id: str) -> int | None:
        if not student_id:
            return None
        try:
            return int(student_id)
        except (TypeError, ValueError):
            return None

    def _resolve_recommendation_service(self) -> Any:
        if self._recommendation_service is not None:
            return self._recommendation_service
        from app.services.recommendation_service import RecommendationService

        return RecommendationService

    def _resolve_mission_service(self) -> Any:
        if self._mission_service is not None:
            return self._mission_service
        from app.services.mission_service import MissionService

        return MissionService

    def _resolve_study_plan_service(self) -> Any:
        if self._study_plan_service is not None:
            return self._study_plan_service
        from app.services.study_plan_service import StudyPlanService

        return StudyPlanService


class _MissionProjection:
    """Minimal mission-shaped object from an optional facade projection."""

    __slots__ = ("id", "title", "user_id")

    def __init__(self, *, id: str, title: str, user_id: int) -> None:
        self.id = id
        self.title = title
        self.user_id = user_id
