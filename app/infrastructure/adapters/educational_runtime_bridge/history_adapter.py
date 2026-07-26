"""History Read Adapter — HistoryBridge read path to Runtime A.

Experience → HistoryAdapter → StudyAttempt / Mission / TopicProgress /
Lifecycle → SQL.

Translator only: no educational calculations, no writes, no demo fallback.
Shares the canonical Mission/Attempt event stream with JourneyAdapter.
"""

from __future__ import annotations

import base64
import logging
import time
from datetime import date
from typing import Any

from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.events.registry import EventRegistry

from .canonical_event_stream import iso_date
from .contracts import (
    FORBIDDEN,
    NOT_FOUND,
    UNAVAILABLE,
    BridgeResult,
)
from .history_mapper import (
    HARD_MAX_PAGE_LIMIT,
    clamp_limit,
    empty_authentic_history,
    map_achievement,
    map_completed_session,
    map_history_to_projection,
    map_page_meta,
    session_trace_for_mission,
)
from .history_telemetry import (
    emit_failure,
    emit_latency,
    emit_requested,
    emit_success,
)

logger = logging.getLogger(__name__)

_FORBIDDEN_RAW_KEYS = frozenset({"events", "raw_events", "event_log"})


class HistoryAdapter:
    """Bridge adapter: project learner History exclusively from Runtime A.

    Controlled by ``ENABLE_HISTORY_BRIDGE``. Read-only translator — never
    calculates mastery/readiness formulas, never writes SQL educational state,
    and never falls back to Twin demo insights.
    """

    ADAPTER_ID = "history_adapter"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        study_plan_service: Any | None = None,
        adaptive_learning_service: Any | None = None,
        learning_lifecycle_service: Any | None = None,
        mission_model: Any | None = None,
        study_attempt_model: Any | None = None,
        topic_progress_model: Any | None = None,
        topic_model: Any | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._study_plan_service = study_plan_service
        self._adaptive_learning_service = adaptive_learning_service
        self._lifecycle_service = learning_lifecycle_service
        self._mission_model = mission_model
        self._study_attempt_model = study_attempt_model
        self._topic_progress_model = topic_progress_model
        self._topic_model = topic_model
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
        """Project History from Runtime A into an Experience-compatible DTO.

        Read-only: does not alter evidence, missions, progress, or recommendations.
        """
        sid = (student_id or "").strip()
        page_limit = clamp_limit(limit)
        page_offset = max(0, int(offset or 0))
        self._diagnostics.record_call(self.ADAPTER_ID)
        emit_requested(self._events, student_id=sid, method="project_history")
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

            cursor_before = self._decode_cursor(cursor)
            lifecycle = self._lifecycle_stage(user_id)
            completed = self._list_completed_missions(
                user_id,
                from_date=from_date,
                to_date=to_date,
                before=cursor_before,
            )

            # Optional lifecycle_stage filter (learning | revision).
            stage_filter = (lifecycle_stage or "").strip().lower()
            if stage_filter in {"learning", "revision"}:
                # Without durable per-mission stage history, apply current stage.
                if lifecycle.strip().lower() != stage_filter:
                    completed = []

            # event_types filter: History list emphasises completed sessions.
            type_filter = {
                str(t).strip() for t in (event_types or ()) if str(t).strip()
            }
            if type_filter and "SessionCompleted" not in type_filter:
                completed = []

            # topic_code filter against mission title (no fabricated mapping).
            code = (topic_code or "").strip().lower()
            if code:
                completed = [
                    m
                    for m in completed
                    if code in str(getattr(m, "title", "") or "").lower()
                ]

            total_for_page = completed
            page_rows = total_for_page[page_offset : page_offset + page_limit]
            has_more = (page_offset + page_limit) < len(total_for_page)
            next_offset = (page_offset + page_limit) if has_more else None
            next_cursor = None
            if has_more and page_rows:
                last = page_rows[-1]
                next_cursor = self._encode_cursor(
                    getattr(last, "mission_date", None),
                    getattr(last, "id", None),
                )

            sessions: list[dict[str, Any]] = []
            total_minutes = 0
            for mission in page_rows:
                attempts = self._attempts_for_mission(user_id, mission.id)
                minutes = self._sum_minutes(attempts)
                total_minutes += minutes
                mid = str(mission.id)
                title = str(mission.title or "") or "Session"
                completed_at = iso_date(getattr(mission, "mission_date", None)) or ""
                attempt_ids = [str(a.id) for a in attempts]
                sessions.append(
                    map_completed_session(
                        session_id=mid,
                        mission_id=mid,
                        topic_title=title,
                        completed_at=completed_at,
                        study_minutes=minutes,
                        lifecycle_stage=lifecycle or None,
                        trace=session_trace_for_mission(
                            topic_title=title,
                            mission_id=mid,
                            attempt_ids=attempt_ids,
                        ),
                    )
                )

            # Total study minutes across all matching completed missions (not
            # just the page) — still Runtime A aggregates, not invented.
            if page_offset == 0 and not has_more:
                page_total_minutes = total_minutes
            else:
                page_total_minutes = 0
                for mission in total_for_page:
                    page_total_minutes += self._sum_minutes(
                        self._attempts_for_mission(user_id, mission.id)
                    )

            mastered = self._mastered_topic_labels(user_id)
            achievements = self._recent_achievements(user_id)
            revision_labels = self._revision_history_labels(
                user_id, lifecycle_stage=lifecycle, missions=total_for_page
            )

            # Durable readiness time-series is not available without schema —
            # explicit null contract (never fabricate progression points).
            readiness_progression = None
            # Recommendation history is not durable — explicit null.
            recommendation_history = None

            projection = map_history_to_projection(
                student_id=sid,
                completed_sessions=sessions,
                total_study_minutes=page_total_minutes,
                readiness_progression=readiness_progression,
                readiness_unavailable_reason="unavailable",
                mastered_topics=mastered,
                revision_history=revision_labels,
                recent_achievements=achievements,
                recommendation_history=recommendation_history,
                page=map_page_meta(
                    limit=page_limit,
                    offset=page_offset,
                    has_more=has_more,
                    next_offset=next_offset,
                    cursor=cursor,
                    next_cursor=next_cursor,
                ),
                fallback_used=False,
            )
            projection = self._strip_raw_event_keys(projection)
            result = BridgeResult(ok=True, value=projection, fallback_used=False)
            self._finish(
                sid,
                result,
                started,
                failure=False,
                session_count=len(sessions),
            )
            return result
        except Exception as exc:  # noqa: BLE001 — bridge must fail closed
            logger.exception("HistoryAdapter unavailable for student_id=%s", sid)
            projection = empty_authentic_history(
                student_id=sid,
                error_code=UNAVAILABLE,
                fallback_used=True,
                limit=page_limit,
                offset=page_offset,
            )
            result = BridgeResult(
                ok=False,
                value=projection,
                error_code=UNAVAILABLE,
                message=str(exc)[:256],
                fallback_used=True,
            )
            self._finish(sid, result, started, failure=True, session_count=0)
            return result

    def get_evidence_summary(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        attempt_id: str | None = None,
    ) -> BridgeResult:
        """Read-only evidence inspect — never re-commits evidence."""
        sid = (student_id or "").strip()
        self._diagnostics.record_call(self.ADAPTER_ID)
        emit_requested(
            self._events, student_id=sid, method="get_evidence_summary"
        )
        started = time.perf_counter()

        try:
            user_id = self._parse_user_id(sid)
            if user_id is None:
                result = BridgeResult(
                    ok=False,
                    error_code=FORBIDDEN,
                    message="student_id must map to an authenticated user id",
                )
                self._finish(
                    sid, result, started, failure=True, method="get_evidence_summary"
                )
                return result

            mission = None
            attempts: list[Any] = []
            attempt_cls = self._resolve_study_attempt_model()
            mission_cls = self._resolve_mission_model()

            if attempt_id:
                try:
                    aid = int(str(attempt_id).strip())
                except (TypeError, ValueError):
                    result = BridgeResult(
                        ok=False,
                        error_code=NOT_FOUND,
                        message="attempt_id not found",
                    )
                    self._finish(
                        sid,
                        result,
                        started,
                        failure=True,
                        method="get_evidence_summary",
                    )
                    return result
                attempt = attempt_cls.query.filter_by(id=aid).first()
                if attempt is None:
                    result = BridgeResult(
                        ok=False,
                        error_code=NOT_FOUND,
                        message="attempt not found",
                    )
                    self._finish(
                        sid,
                        result,
                        started,
                        failure=True,
                        method="get_evidence_summary",
                    )
                    return result
                if int(getattr(attempt, "user_id", -1)) != int(user_id):
                    result = BridgeResult(
                        ok=False,
                        error_code=FORBIDDEN,
                        message="attempt ownership mismatch",
                    )
                    self._finish(
                        sid,
                        result,
                        started,
                        failure=True,
                        method="get_evidence_summary",
                    )
                    return result
                attempts = [attempt]
                mission = mission_cls.query.filter_by(
                    id=attempt.mission_id, user_id=user_id
                ).first()
            elif mission_id:
                try:
                    mid = int(str(mission_id).strip())
                except (TypeError, ValueError):
                    result = BridgeResult(
                        ok=False,
                        error_code=NOT_FOUND,
                        message="mission_id not found",
                    )
                    self._finish(
                        sid,
                        result,
                        started,
                        failure=True,
                        method="get_evidence_summary",
                    )
                    return result
                mission = mission_cls.query.filter_by(
                    id=mid, user_id=user_id
                ).first()
                if mission is None:
                    result = BridgeResult(
                        ok=False,
                        error_code=NOT_FOUND,
                        message="mission not found",
                    )
                    self._finish(
                        sid,
                        result,
                        started,
                        failure=True,
                        method="get_evidence_summary",
                    )
                    return result
                attempts = self._attempts_for_mission(user_id, mission.id)
            else:
                result = BridgeResult(
                    ok=False,
                    error_code=NOT_FOUND,
                    message="mission_id or attempt_id required",
                )
                self._finish(
                    sid, result, started, failure=True, method="get_evidence_summary"
                )
                return result

            topic_title = str(getattr(mission, "title", "") or "") if mission else ""
            study_date = None
            questions = None
            duration = None
            if attempts:
                primary = attempts[0]
                study_date = iso_date(getattr(primary, "study_date", None))
                questions = getattr(primary, "questions_attempted", None)
                duration = self._sum_minutes(attempts) or None
            elif mission is not None:
                study_date = iso_date(getattr(mission, "mission_date", None))

            outcome_labels: list[str] = []
            for attempt in attempts:
                before = getattr(attempt, "confidence_before", None)
                after = getattr(attempt, "confidence_after", None)
                if before or after:
                    outcome_labels.append(
                        f"Confidence {before or '?'} → {after or '?'}"
                    )

            summary = {
                "student_id": sid,
                "mission_id": (
                    None if mission is None else str(mission.id)
                ),
                "attempt_ids": [str(a.id) for a in attempts],
                "summary": {
                    "topic_title": topic_title,
                    "study_date": study_date,
                    "outcome_labels": outcome_labels,
                    # Evidence acceptance / mastery flags are not durable on
                    # StudyAttempt without schema — explicit nulls.
                    "evidence_accepted": None,
                    "mastery_updated": None,
                    "questions_attempted": questions,
                    "duration_minutes": duration,
                },
                "why": {
                    "reason_codes": ["evidence_inspect"],
                    "summary": "Projected from Runtime A StudyAttempt / Mission",
                },
                "recommendation_delta_ref": None,
                "recommendation_delta_meta": {
                    "unavailable_reason": "unavailable",
                },
                "authority": "history_bridge",
            }
            summary = self._strip_raw_event_keys(summary)
            result = BridgeResult(ok=True, value=summary, fallback_used=False)
            self._finish(
                sid,
                result,
                started,
                failure=False,
                session_count=1 if mission is not None else 0,
                method="get_evidence_summary",
            )
            return result
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "HistoryAdapter evidence summary unavailable for student_id=%s",
                sid,
            )
            result = BridgeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message=str(exc)[:256],
                fallback_used=True,
            )
            self._finish(
                sid, result, started, failure=True, method="get_evidence_summary"
            )
            return result

    def _finish(
        self,
        student_id: str,
        result: BridgeResult,
        started: float,
        *,
        failure: bool,
        session_count: int | None = None,
        method: str = "project_history",
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
            resolved_count = session_count
            if resolved_count is None and result.value is not None:
                resolved_count = int(result.value.get("session_count") or 0)
            emit_success(
                self._events,
                student_id=student_id,
                session_count=resolved_count,
                error_code=result.error_code,
                fallback_used=result.fallback_used,
            )
        emit_latency(
            self._events,
            student_id=student_id,
            latency_ms=latency_ms,
            ok=not failure,
            method=method,
        )

    def _list_completed_missions(
        self,
        user_id: int,
        *,
        from_date: date | None,
        to_date: date | None,
        before: tuple[date, int] | None,
    ) -> list[Any]:
        mission_cls = self._resolve_mission_model()
        try:
            query = mission_cls.query.filter(
                mission_cls.user_id == user_id,
                mission_cls.status == "Completed",
            )
            if from_date is not None:
                query = query.filter(mission_cls.mission_date >= from_date)
            if to_date is not None:
                query = query.filter(mission_cls.mission_date <= to_date)
            if before is not None:
                before_date, before_id = before
                # Cursor: rows strictly before (date, id) in reverse chrono order.
                query = query.filter(
                    (mission_cls.mission_date < before_date)
                    | (
                        (mission_cls.mission_date == before_date)
                        & (mission_cls.id < before_id)
                    )
                )
            return (
                query.order_by(
                    mission_cls.mission_date.desc(), mission_cls.id.desc()
                )
                .limit(HARD_MAX_PAGE_LIMIT * 5)
                .all()
            )
        except Exception:  # noqa: BLE001
            logger.debug(
                "completed missions unavailable for user_id=%s",
                user_id,
                exc_info=True,
            )
            return []

    def _attempts_for_mission(self, user_id: int, mission_id: Any) -> list[Any]:
        try:
            attempt_cls = self._resolve_study_attempt_model()
            return list(
                attempt_cls.query.filter_by(
                    user_id=user_id, mission_id=mission_id
                ).all()
            )
        except Exception:  # noqa: BLE001
            return []

    @staticmethod
    def _sum_minutes(attempts: list[Any]) -> int:
        total = 0
        for attempt in attempts:
            minutes = getattr(attempt, "duration_minutes", None)
            if minutes is not None:
                total += int(minutes)
        return max(0, total)

    def _mastered_topic_labels(self, user_id: int) -> list[str]:
        try:
            adaptive = self._resolve_adaptive_learning_service()
            rows = adaptive.get_mastered_topics(user_id)
        except Exception:  # noqa: BLE001
            logger.debug(
                "mastered topics unavailable for user_id=%s",
                user_id,
                exc_info=True,
            )
            rows = []

        labels: list[str] = []
        topic_cls = None
        try:
            topic_cls = self._resolve_topic_model()
        except Exception:  # noqa: BLE001
            topic_cls = None

        for row in rows:
            topic_id = getattr(row, "topic_id", None)
            title = ""
            if topic_cls is not None and topic_id is not None:
                try:
                    topic = topic_cls.query.filter_by(id=topic_id).first()
                    if topic is not None:
                        title = str(getattr(topic, "name", "") or "")
                except Exception:  # noqa: BLE001
                    title = ""
            if not title:
                title = f"Topic {topic_id}" if topic_id is not None else ""
            if title:
                labels.append(title)
        return labels

    def _recent_achievements(self, user_id: int) -> list[dict[str, Any]]:
        """Project completed/mastered TopicProgress rows as achievement cards."""
        try:
            from sqlalchemy import or_ as db_or_

            model = self._resolve_topic_progress_model()
            rows = (
                model.query.filter(
                    model.user_id == user_id,
                    db_or_(
                        model.completed.is_(True),
                        model.current_stage.in_(("Mastered", "Completed")),
                    ),
                )
                .order_by(model.id.desc())
                .limit(10)
                .all()
            )
        except Exception:  # noqa: BLE001
            return []

        topic_cls = None
        try:
            topic_cls = self._resolve_topic_model()
        except Exception:  # noqa: BLE001
            topic_cls = None

        cards: list[dict[str, Any]] = []
        for row in rows:
            topic_id = getattr(row, "topic_id", None)
            title = ""
            if topic_cls is not None and topic_id is not None:
                try:
                    topic = topic_cls.query.filter_by(id=topic_id).first()
                    if topic is not None:
                        title = str(getattr(topic, "name", "") or "")
                except Exception:  # noqa: BLE001
                    title = ""
            if not title:
                title = f"Topic {topic_id}" if topic_id is not None else "Topic"
            earned = iso_date(getattr(row, "updated_at", None)) or ""
            stage = str(getattr(row, "current_stage", "") or "")
            cards.append(
                map_achievement(
                    achievement_id=f"topic-progress-{row.id}",
                    title=title,
                    earned_at=earned,
                    description=f"Progress stage: {stage}" if stage else "",
                )
            )
        return cards

    def _revision_history_labels(
        self,
        user_id: int,
        *,
        lifecycle_stage: str,
        missions: list[Any],
    ) -> list[str]:
        """Labels from revision-stage activity — never invents revision math."""
        stage = (lifecycle_stage or "").strip().lower()
        if stage != "revision":
            return []
        labels: list[str] = []
        for mission in missions[:10]:
            title = str(getattr(mission, "title", "") or "").strip()
            when = iso_date(getattr(mission, "mission_date", None)) or ""
            if title:
                labels.append(
                    f"Revision activity: {title}"
                    + (f" ({when})" if when else "")
                )
        return labels

    def _lifecycle_stage(self, user_id: int) -> str:
        try:
            plan = None
            try:
                plan = self._resolve_study_plan_service().get_user_active_plan(
                    user_id
                )
            except Exception:  # noqa: BLE001
                plan = None
            lifecycle_svc = self._resolve_lifecycle_service()
            resolved = lifecycle_svc.resolve(
                user_id, study_plan=plan, today=date.today()
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
    def _encode_cursor(mission_date: Any, mission_id: Any) -> str | None:
        iso = iso_date(mission_date)
        if iso is None or mission_id is None:
            return None
        raw = f"{iso}:{mission_id}"
        return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("ascii")

    @staticmethod
    def _decode_cursor(cursor: str | None) -> tuple[date, int] | None:
        if not cursor or not str(cursor).strip():
            return None
        try:
            raw = base64.urlsafe_b64decode(str(cursor).strip().encode("ascii"))
            text = raw.decode("utf-8")
            date_part, id_part = text.rsplit(":", 1)
            return date.fromisoformat(date_part), int(id_part)
        except Exception:  # noqa: BLE001
            return None

    @staticmethod
    def _strip_raw_event_keys(payload: dict[str, Any]) -> dict[str, Any]:
        return {
            k: v for k, v in payload.items() if k not in _FORBIDDEN_RAW_KEYS
        }

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

    def _resolve_adaptive_learning_service(self) -> Any:
        if self._adaptive_learning_service is not None:
            return self._adaptive_learning_service
        from app.services.adaptive_learning_service import AdaptiveLearningService

        return AdaptiveLearningService

    def _resolve_lifecycle_service(self) -> Any:
        if self._lifecycle_service is not None:
            return self._lifecycle_service
        from app.services.learning_lifecycle_service import LearningLifecycleService

        return LearningLifecycleService

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

    def _resolve_topic_model(self) -> Any:
        if self._topic_model is not None:
            return self._topic_model
        from app.models.curriculum import Topic

        return Topic
