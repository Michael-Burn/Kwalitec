"""Journey Read Adapter — JourneyBridge read path to Runtime A.

Experience → JourneyAdapter → StudyPlan / Mission / StudyAttempt /
TopicProgress / Lifecycle / Readiness → SQL.

Translator only: no educational calculations, no writes, no demo fallback.
"""

from __future__ import annotations

import logging
import time
from datetime import date, datetime
from typing import Any

from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.events.registry import EventRegistry

from .canonical_event_stream import project_canonical_timeline_from_missions
from .contracts import (
    FORBIDDEN,
    NO_ACTIVE_PLAN,
    UNAVAILABLE,
    BridgeResult,
)
from .journey_mapper import (
    NOT_APPLICABLE_RECOMMENDATION,
    UNAVAILABLE_RECOMMENDATION,
    build_trace_ref,
    empty_authentic_journey,
    map_journey_to_projection,
    map_topic_card,
    map_topic_status,
)
from .journey_telemetry import (
    emit_failure,
    emit_latency,
    emit_requested,
    emit_success,
)

logger = logging.getLogger(__name__)

_DEFAULT_TIMELINE_LIMIT = 20
_COMPLETED_RECENT_LIMIT = 5


class JourneyAdapter:
    """Bridge adapter: project the learner Journey exclusively from Runtime A.

    Controlled by ``ENABLE_JOURNEY_BRIDGE``. Read-only translator — never
    calculates mastery/readiness formulas, never writes SQL educational state,
    and never falls back to ``seeded_demo_journey``.
    """

    ADAPTER_ID = "journey_adapter"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        study_plan_service: Any | None = None,
        mission_service: Any | None = None,
        curriculum_service: Any | None = None,
        readiness_service: Any | None = None,
        curriculum_engine_service: Any | None = None,
        learning_lifecycle_service: Any | None = None,
        recommendation_service: Any | None = None,
        mission_model: Any | None = None,
        study_attempt_model: Any | None = None,
        topic_progress_model: Any | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._study_plan_service = study_plan_service
        self._mission_service = mission_service
        self._curriculum_service = curriculum_service
        self._readiness_service = readiness_service
        self._curriculum_engine_service = curriculum_engine_service
        self._lifecycle_service = learning_lifecycle_service
        self._recommendation_service = recommendation_service
        self._mission_model = mission_model
        self._study_attempt_model = study_attempt_model
        self._topic_progress_model = topic_progress_model
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

    def project_journey(
        self,
        student_id: str,
        *,
        as_of_date: date | None = None,
        include_timeline: bool = True,
        timeline_limit: int = _DEFAULT_TIMELINE_LIMIT,
    ) -> BridgeResult:
        """Project Journey from Runtime A into an Experience-compatible DTO.

        Read-only: does not alter evidence, missions, progress, or recommendations.
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

            as_of = as_of_date or date.today()
            plan = self._resolve_study_plan_service().get_user_active_plan(user_id)
            if plan is None:
                projection = empty_authentic_journey(
                    student_id=sid,
                    error_code=NO_ACTIVE_PLAN,
                )
                result = BridgeResult(
                    ok=True,
                    value=projection,
                    error_code=NO_ACTIVE_PLAN,
                    message="no active study plan",
                    fallback_used=False,
                )
                self._finish(
                    sid, result, started, failure=False, has_journey=False
                )
                return result

            if int(getattr(plan, "user_id", user_id)) != int(user_id):
                result = BridgeResult(
                    ok=False,
                    error_code=FORBIDDEN,
                    message="study plan ownership mismatch",
                )
                self._finish(sid, result, started, failure=True)
                return result

            fallback_used = False
            lifecycle_stage = self._lifecycle_stage(user_id, as_of, plan=plan)
            ratio, completion_label, readiness_fallback = self._progress_ratio(
                user_id, plan
            )
            fallback_used = fallback_used or readiness_fallback

            today_mission = self._today_mission(user_id, as_of)
            topics, current_id, current_title = self._project_topics(
                user_id,
                plan,
                today_mission=today_mission,
            )
            if not current_id and today_mission is not None:
                current_title = str(getattr(today_mission, "title", "") or "")
                current_id = str(getattr(today_mission, "id", "") or "")

            active_missions = self._active_missions(
                user_id, as_of, lifecycle_stage=lifecycle_stage
            )
            completed_summary = self._completed_sessions_summary(user_id)
            timeline: list[dict[str, Any]] = []
            if include_timeline:
                timeline = self._project_timeline(
                    user_id,
                    sid,
                    lifecycle_stage=lifecycle_stage,
                    limit=max(0, int(timeline_limit)),
                )

            recommendation_focus = self._recommendation_focus(
                user_id, today_mission=today_mission
            )
            # Recommendation history is not durable without schema — explicit null.
            recommendation_history = None

            examination_label = str(
                getattr(plan, "exam_name", "")
                or getattr(plan, "exam_sitting", "")
                or ""
            )

            projection = map_journey_to_projection(
                student_id=sid,
                has_journey=True,
                overall_progress_ratio=ratio,
                estimated_completion_label=completion_label,
                examination_label=examination_label,
                current_topic_id=current_id,
                current_topic_title=current_title,
                lifecycle_stage=lifecycle_stage,
                topics=topics,
                active_missions=active_missions,
                completed_sessions_summary=completed_summary,
                timeline=timeline,
                recommendation_focus=recommendation_focus,
                recommendation_history=recommendation_history,
                fallback_used=fallback_used,
            )
            result = BridgeResult(
                ok=True,
                value=projection,
                fallback_used=fallback_used,
            )
            self._finish(sid, result, started, failure=False, has_journey=True)
            return result
        except Exception as exc:  # noqa: BLE001 — bridge must fail closed
            logger.exception("JourneyAdapter unavailable for student_id=%s", sid)
            projection = empty_authentic_journey(
                student_id=sid,
                error_code=UNAVAILABLE,
                fallback_used=True,
            )
            result = BridgeResult(
                ok=False,
                value=projection,
                error_code=UNAVAILABLE,
                message=str(exc)[:256],
                fallback_used=True,
            )
            self._finish(sid, result, started, failure=True, has_journey=False)
            return result

    def get_journey_progress_opaque(
        self, student_id: str
    ) -> dict[str, Any] | None:
        """Opaque-engine compatible entry used by ExperienceJourneyAdapter."""
        result = self.project_journey(student_id)
        if not result.ok:
            return result.value
        return result.value

    def _finish(
        self,
        student_id: str,
        result: BridgeResult,
        started: float,
        *,
        failure: bool,
        has_journey: bool | None = None,
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
            resolved_has = has_journey
            if resolved_has is None and result.value is not None:
                resolved_has = bool(result.value.get("has_journey"))
            emit_success(
                self._events,
                student_id=student_id,
                has_journey=resolved_has,
                error_code=result.error_code,
                fallback_used=result.fallback_used,
            )
        emit_latency(
            self._events,
            student_id=student_id,
            latency_ms=latency_ms,
            ok=not failure,
        )

    def _progress_ratio(
        self, user_id: int, plan: Any
    ) -> tuple[float, str, bool]:
        """Project progress ratio from Runtime A Readiness / curriculum coverage.

        Never invents a formula in the adapter — delegates to Runtime A services.
        """
        # Prefer weighted readiness from curriculum summary when available.
        try:
            engine = self._resolve_curriculum_engine_service()
            summary = engine.build_student_curriculum(plan)
            readiness_svc = self._resolve_readiness_service()
            readiness = readiness_svc.calculate_readiness(summary)
            if readiness is not None:
                return (
                    float(readiness.readiness_percentage),
                    str(getattr(readiness, "explanation", "") or ""),
                    False,
                )
        except Exception:  # noqa: BLE001
            logger.debug(
                "weighted readiness unavailable for user_id=%s",
                user_id,
                exc_info=True,
            )

        # Fallback: CurriculumService plan coverage (still Runtime A).
        try:
            curriculum_id = getattr(plan, "curriculum_id", None)
            if curriculum_id:
                curriculum_svc = self._resolve_curriculum_service()
                curriculum = curriculum_svc.get_curriculum_by_id(curriculum_id)
                if curriculum is not None:
                    progress = curriculum_svc.get_curriculum_progress(
                        user_id, curriculum
                    )
                    pct = float(progress.get("completion_percentage") or 0.0)
                    return pct / 100.0, "", True
        except Exception:  # noqa: BLE001
            logger.debug(
                "curriculum progress unavailable for user_id=%s",
                user_id,
                exc_info=True,
            )
        return 0.0, "", True

    def _project_topics(
        self,
        user_id: int,
        plan: Any,
        *,
        today_mission: Any | None,
    ) -> tuple[list[dict[str, Any]], str, str]:
        """Project curriculum-ordered topic cards from TopicProgress."""
        curriculum_id = getattr(plan, "curriculum_id", None)
        if not curriculum_id:
            return [], "", ""

        try:
            curriculum_svc = self._resolve_curriculum_service()
            curriculum = curriculum_svc.get_curriculum_by_id(curriculum_id)
            if curriculum is None:
                return [], "", ""
            ordered = curriculum_svc.get_ordered_topics(curriculum)
            leaf_topics = [t for t in ordered if t.is_leaf_topic()]
        except Exception:  # noqa: BLE001
            logger.exception("curriculum topics unavailable for user_id=%s", user_id)
            return [], "", ""

        progress_map = self._topic_progress_map(
            user_id, [int(t.id) for t in leaf_topics]
        )
        current_mission_title = ""
        if today_mission is not None:
            current_mission_title = str(
                getattr(today_mission, "title", "") or ""
            ).strip().lower()

        # Prefer CurriculumService next incomplete when no mission title match.
        next_incomplete = None
        try:
            next_incomplete = curriculum_svc.get_next_incomplete_topic(
                user_id, curriculum
            )
        except Exception:  # noqa: BLE001
            next_incomplete = None

        cards: list[dict[str, Any]] = []
        current_id = ""
        current_title = ""
        for topic in leaf_topics:
            tp = progress_map.get(int(topic.id))
            completed = bool(tp is not None and getattr(tp, "completed", False))
            stage = None if tp is None else getattr(tp, "current_stage", None)
            title = str(getattr(topic, "name", "") or "")
            is_current = False
            if current_mission_title and title.strip().lower() in (
                current_mission_title,
                f"study {title.strip().lower()}",
            ):
                is_current = True
            elif (
                not current_mission_title
                and next_incomplete is not None
                and int(next_incomplete.id) == int(topic.id)
                and not completed
            ):
                is_current = True
            # Mission titles often look like "Study Probability".
            if (
                not is_current
                and current_mission_title
                and title.strip().lower()
                and title.strip().lower() in current_mission_title
            ):
                is_current = True

            status = map_topic_status(
                completed=completed, is_current=is_current, stage=stage
            )
            if status == "current":
                current_id = str(topic.id)
                current_title = title
            cards.append(
                map_topic_card(
                    topic_id=str(topic.id),
                    title=title,
                    status=status,
                )
            )
        return cards, current_id, current_title

    def _topic_progress_map(
        self, user_id: int, topic_ids: list[int]
    ) -> dict[int, Any]:
        if not topic_ids:
            return {}
        try:
            model = self._resolve_topic_progress_model()
            rows = model.query.filter(
                model.user_id == user_id,
                model.topic_id.in_(topic_ids),
            ).all()
            return {int(row.topic_id): row for row in rows}
        except Exception:  # noqa: BLE001
            logger.debug(
                "TopicProgress read failed for user_id=%s", user_id, exc_info=True
            )
            return {}

    def _today_mission(self, user_id: int, as_of: date) -> Any | None:
        try:
            mission = self._resolve_mission_service().get_today_mission(
                user_id, mission_date=as_of
            )
            if mission is None:
                return None
            if int(getattr(mission, "user_id", user_id)) != int(user_id):
                return None
            return mission
        except Exception:  # noqa: BLE001
            logger.debug(
                "today mission unavailable for user_id=%s", user_id, exc_info=True
            )
            return None

    def _active_missions(
        self,
        user_id: int,
        as_of: date,
        *,
        lifecycle_stage: str,
    ) -> list[dict[str, Any]]:
        """Project today / In Progress missions — read only."""
        mission_cls = self._resolve_mission_model()
        try:
            rows = (
                mission_cls.query.filter(
                    mission_cls.user_id == user_id,
                    mission_cls.status.in_(("Pending", "In Progress")),
                )
                .order_by(mission_cls.mission_date.desc(), mission_cls.id.desc())
                .limit(10)
                .all()
            )
        except Exception:  # noqa: BLE001
            logger.debug(
                "active missions unavailable for user_id=%s",
                user_id,
                exc_info=True,
            )
            return []

        active: list[dict[str, Any]] = []
        for mission in rows:
            mission_date = getattr(mission, "mission_date", None)
            # Prefer today's Pending and any In Progress.
            status = str(getattr(mission, "status", "") or "")
            is_today = mission_date == as_of
            if status == "In Progress" or (status == "Pending" and is_today):
                active.append(
                    {
                        "mission_id": str(mission.id),
                        "session_id": str(mission.id),
                        "topic_title": str(mission.title or ""),
                        "status": status,
                        "mission_date": (
                            None
                            if mission_date is None
                            else (
                                mission_date.isoformat()
                                if hasattr(mission_date, "isoformat")
                                else str(mission_date)
                            )
                        ),
                        "lifecycle_stage": lifecycle_stage,
                        "trace": build_trace_ref(
                            what=f"Active mission: {mission.title}",
                            why_summary="Projected from Runtime A Mission row",
                            reason_codes=["mission_active"],
                            evidence_refs=[
                                {"kind": "mission", "id": str(mission.id)}
                            ],
                            recommendation=dict(NOT_APPLICABLE_RECOMMENDATION),
                        ),
                    }
                )
        return active

    def _completed_sessions_summary(self, user_id: int) -> dict[str, Any]:
        mission_cls = self._resolve_mission_model()
        attempt_cls = self._resolve_study_attempt_model()
        try:
            completed = (
                mission_cls.query.filter(
                    mission_cls.user_id == user_id,
                    mission_cls.status == "Completed",
                )
                .order_by(mission_cls.mission_date.desc(), mission_cls.id.desc())
                .all()
            )
        except Exception:  # noqa: BLE001
            return {"count": 0, "recent": []}

        recent: list[dict[str, Any]] = []
        for mission in completed[:_COMPLETED_RECENT_LIMIT]:
            minutes = None
            try:
                attempts = attempt_cls.query.filter_by(
                    user_id=user_id, mission_id=mission.id
                ).all()
                if attempts:
                    total = sum(
                        int(a.duration_minutes or 0)
                        for a in attempts
                        if a.duration_minutes is not None
                    )
                    minutes = total if total > 0 else None
            except Exception:  # noqa: BLE001
                minutes = None
            completed_at = getattr(mission, "mission_date", None)
            recent.append(
                {
                    "mission_id": str(mission.id),
                    "topic_title": str(mission.title or ""),
                    "completed_at": (
                        None
                        if completed_at is None
                        else (
                            completed_at.isoformat()
                            if hasattr(completed_at, "isoformat")
                            else str(completed_at)
                        )
                    ),
                    "study_minutes": minutes,
                }
            )
        return {"count": len(completed), "recent": recent}

    def _project_timeline(
        self,
        user_id: int,
        student_id: str,
        *,
        lifecycle_stage: str,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Project recent EducationalTimelineEvents from Missions + Attempts.

        Uses the shared canonical event stream so History stays consistent.
        """
        if limit <= 0:
            return []

        mission_cls = self._resolve_mission_model()
        attempt_cls = self._resolve_study_attempt_model()

        try:
            missions = (
                mission_cls.query.filter(mission_cls.user_id == user_id)
                .order_by(mission_cls.mission_date.desc(), mission_cls.id.desc())
                .limit(limit)
                .all()
            )
        except Exception:  # noqa: BLE001
            missions = []

        attempts_by_mission: dict[Any, list[Any]] = {}
        for mission in missions:
            try:
                attempts_by_mission[mission.id] = list(
                    attempt_cls.query.filter_by(
                        user_id=user_id, mission_id=mission.id
                    ).all()
                )
            except Exception:  # noqa: BLE001
                attempts_by_mission[mission.id] = []

        return project_canonical_timeline_from_missions(
            student_id=student_id,
            missions=missions,
            attempts_by_mission=attempts_by_mission,
            lifecycle_stage=lifecycle_stage,
            limit=limit,
        )

    def _recommendation_focus(
        self, user_id: int, *, today_mission: Any | None
    ) -> dict[str, Any] | None:
        """Optional current recommendation focus — never fabricates history."""
        if today_mission is not None:
            title = str(getattr(today_mission, "title", "") or "").strip()
            if title:
                return {
                    "topic_title": title,
                    "reason_codes": ["mission_aligned"],
                    "mission_aligned": True,
                    "authority": "recommendation_bridge",
                    "recommendation": dict(UNAVAILABLE_RECOMMENDATION),
                }
        try:
            rec_svc = self._resolve_recommendation_service()
            raw = rec_svc.generate_recommendations(user_id, limit=1)
            if raw:
                primary = dict(raw[0])
                label = str(primary.get("title") or "").strip()
                if label:
                    return {
                        "topic_title": label,
                        "reason_codes": ["recommendation_service"],
                        "mission_aligned": False,
                        "authority": "recommendation_service",
                        "recommendation": dict(UNAVAILABLE_RECOMMENDATION),
                    }
        except Exception:  # noqa: BLE001
            logger.debug(
                "recommendation focus unavailable for user_id=%s",
                user_id,
                exc_info=True,
            )
        return None

    def _lifecycle_stage(
        self, user_id: int, as_of: date, *, plan: Any | None = None
    ) -> str:
        try:
            lifecycle_svc = self._resolve_lifecycle_service()
            resolved = lifecycle_svc.resolve(
                user_id, study_plan=plan, today=as_of
            )
            return str(getattr(resolved, "stage", "") or "")
        except Exception:  # noqa: BLE001
            logger.debug(
                "lifecycle stage unavailable for user_id=%s",
                user_id,
                exc_info=True,
            )
            return ""

    @staticmethod
    def _iso_date(value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date().isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return str(value)

    @staticmethod
    def _parse_user_id(student_id: str) -> int | None:
        if not student_id:
            return None
        try:
            return int(student_id)
        except (TypeError, ValueError):
            return None

    def _resolve_study_plan_service(self) -> Any:
        if self._study_plan_service is not None:
            return self._study_plan_service
        from app.services.study_plan_service import StudyPlanService

        return StudyPlanService

    def _resolve_mission_service(self) -> Any:
        if self._mission_service is not None:
            return self._mission_service
        from app.services.mission_service import MissionService

        return MissionService

    def _resolve_curriculum_service(self) -> Any:
        if self._curriculum_service is not None:
            return self._curriculum_service
        from app.services.curriculum_service import CurriculumService

        return CurriculumService

    def _resolve_readiness_service(self) -> Any:
        if self._readiness_service is not None:
            return self._readiness_service
        from app.services.readiness_service import ReadinessService

        return ReadinessService

    def _resolve_curriculum_engine_service(self) -> Any:
        if self._curriculum_engine_service is not None:
            engine = self._curriculum_engine_service
            return engine() if isinstance(engine, type) else engine
        from app.services.curriculum_engine_service import CurriculumEngineService

        return CurriculumEngineService()

    def _resolve_lifecycle_service(self) -> Any:
        if self._lifecycle_service is not None:
            return self._lifecycle_service
        from app.services.learning_lifecycle_service import LearningLifecycleService

        return LearningLifecycleService

    def _resolve_recommendation_service(self) -> Any:
        if self._recommendation_service is not None:
            return self._recommendation_service
        from app.services.recommendation_service import RecommendationService

        return RecommendationService

    def _resolve_mission_model(self) -> Any:
        if self._mission_model is not None:
            return self._mission_model
        from app.models.mission import Mission

        return Mission

    def _resolve_study_attempt_model(self) -> Any:
        if self._study_attempt_model is not None:
            return self._study_attempt_model
        from app.models.learning import StudyAttempt

        return StudyAttempt

    def _resolve_topic_progress_model(self) -> Any:
        if self._topic_progress_model is not None:
            return self._topic_progress_model
        from app.models.topic_progress import TopicProgress

        return TopicProgress
