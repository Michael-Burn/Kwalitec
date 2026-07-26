"""Mission Start Adapter — write path to Runtime A (ensure today + start).

Experience → MissionStartAdapter → PlanningService / StudySessionService → SQL.

Translator only: no mission selection math, no recommendation, no demo fallback.
"""

from __future__ import annotations

import logging
import time
from datetime import date
from typing import Any

from app.infrastructure.adapters.educational_runtime_bridge.contracts import (
    FORBIDDEN,
    INVALID_STATE,
    NO_ACTIVE_PLAN,
    NOT_FOUND,
    OUTSIDE_PLAN_WINDOW,
    UNAVAILABLE,
    BridgeResult,
)
from app.infrastructure.adapters.educational_runtime_bridge.mission_mapper import (
    map_mission_to_start_result,
)
from app.infrastructure.adapters.educational_runtime_bridge.start_telemetry import (
    emit_failure,
    emit_latency,
    emit_requested,
    emit_success,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.events.registry import EventRegistry

logger = logging.getLogger(__name__)


class MissionStartAdapter:
    """Bridge adapter: initiate today's study session via Runtime A.

    Controlled by ``ENABLE_MISSION_START_BRIDGE``. Combines PlanningBridge
    ensure-today with MissionLifecycleBridge start_session in one translator.
    Never creates fallback / demo sessions.
    """

    ADAPTER_ID = "mission_start_adapter"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        planning_service: Any | None = None,
        study_session_service: Any | None = None,
        study_plan_service: Any | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._planning_service = planning_service
        self._study_session_service = study_session_service
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

    def start_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
        as_of_date: date | None = None,
    ) -> BridgeResult:
        """Ensure today's mission exists and start it through Runtime A.

        Calls ``PlanningService.generate_today_mission`` when no mission_id is
        supplied (idempotent ensure). Starts via
        ``StudySessionService.start_session``. Does not invent missions.
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

            mission_date = as_of_date or date.today()
            mission = self._resolve_mission(
                user_id,
                mission_id=mission_id,
                mission_date=mission_date,
            )
            if isinstance(mission, BridgeResult):
                self._finish(sid, mission, started, failure=not mission.ok)
                return mission

            session_svc = self._resolve_study_session_service()
            try:
                started_mission = session_svc.start_session(
                    int(mission.id), int(user_id)
                )
            except ValueError as exc:
                code = self._translate_start_value_error(exc)
                result = BridgeResult(
                    ok=False,
                    error_code=code,
                    message=str(exc)[:256],
                )
                self._finish(sid, result, started, failure=True)
                return result

            if int(started_mission.user_id) != int(user_id):
                result = BridgeResult(
                    ok=False,
                    error_code=FORBIDDEN,
                    message="mission ownership mismatch after start",
                )
                self._finish(sid, result, started, failure=True)
                return result

            # B3 (PX-003): pass the resolved calendar day so weekday/weekend
            # selection agrees with every other duration call path.
            estimated = self._estimated_minutes(user_id, mission_date=mission_date)
            projection = map_mission_to_start_result(
                started_mission,
                student_id=sid,
                session_id=session_id or str(started_mission.id),
                estimated_minutes=estimated,
            )
            result = BridgeResult(ok=True, value=projection, fallback_used=False)
            self._finish(
                sid,
                result,
                started,
                failure=False,
                mission_id=str(started_mission.id),
            )
            return result
        except Exception as exc:  # noqa: BLE001 — bridge must fail closed
            logger.exception(
                "MissionStartAdapter unavailable for student_id=%s", sid
            )
            result = BridgeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message=str(exc)[:256],
            )
            self._finish(sid, result, started, failure=True)
            return result

    def _resolve_mission(
        self,
        user_id: int,
        *,
        mission_id: str | None,
        mission_date: date,
    ) -> Any | BridgeResult:
        """Resolve the SQL Mission to start — ensure-today or owned lookup."""
        if mission_id is not None and str(mission_id).strip():
            return self._load_owned_mission(user_id, str(mission_id).strip())

        planning = self._resolve_planning_service()
        mission = planning.generate_today_mission(user_id, today=mission_date)
        if mission is None:
            code, message = self._absence_code(user_id, mission_date)
            return BridgeResult(
                ok=True,
                value=None,
                error_code=code,
                message=message,
                fallback_used=False,
            )
        if int(mission.user_id) != int(user_id):
            return BridgeResult(
                ok=False,
                error_code=FORBIDDEN,
                message="mission ownership mismatch",
            )
        return mission

    def _load_owned_mission(
        self, user_id: int, mission_id: str
    ) -> Any | BridgeResult:
        try:
            mid = int(mission_id)
        except (TypeError, ValueError):
            return BridgeResult(
                ok=False,
                error_code=NOT_FOUND,
                message="mission_id must be a SQL Mission id",
            )
        session_svc = self._resolve_study_session_service()
        try:
            mission = session_svc.get_owned_mission(mid, user_id)
        except ValueError as exc:
            message = str(exc)
            if "does not belong" in message.lower():
                return BridgeResult(
                    ok=False,
                    error_code=FORBIDDEN,
                    message=message[:256],
                )
            return BridgeResult(
                ok=False,
                error_code=NOT_FOUND,
                message=message[:256],
            )
        if mission is None:
            return BridgeResult(
                ok=True,
                value=None,
                error_code=NOT_FOUND,
                message="mission not found",
                fallback_used=False,
            )
        return mission

    @staticmethod
    def _translate_start_value_error(exc: ValueError) -> str:
        message = str(exc).lower()
        if "already been recorded" in message or "completed" in message:
            return INVALID_STATE
        if "does not belong" in message:
            return FORBIDDEN
        if "not found" in message:
            return NOT_FOUND
        return INVALID_STATE

    def _finish(
        self,
        student_id: str,
        result: BridgeResult,
        started: float,
        *,
        failure: bool,
        mission_id: str | None = None,
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
            resolved_mission_id = mission_id
            if resolved_mission_id is None and result.value is not None:
                resolved_mission_id = str(result.value.get("mission_id"))
            emit_success(
                self._events,
                student_id=student_id,
                mission_id=resolved_mission_id,
                error_code=result.error_code,
            )
        emit_latency(
            self._events,
            student_id=student_id,
            latency_ms=latency_ms,
            ok=not failure,
        )

    def _absence_code(
        self, user_id: int, mission_date: date
    ) -> tuple[str, str]:
        """Classify why Runtime A could not ensure a mission."""
        plan_svc = self._resolve_study_plan_service()
        active_plan = plan_svc.get_user_active_plan(user_id)
        if active_plan is None:
            return NO_ACTIVE_PLAN, "no active study plan"
        current_week = plan_svc.get_current_week_plan(active_plan)
        if current_week is None:
            return (
                OUTSIDE_PLAN_WINDOW,
                f"date {mission_date.isoformat()} outside study plan window",
            )
        return NOT_FOUND, "no mission for date"

    def _estimated_minutes(
        self, user_id: int, *, mission_date: date | None = None
    ) -> int | None:
        """Project canonical planned session minutes (EP-007.1) — no invention.

        ``mission_date`` must match the resolved calendar day (B3, PX-003
        release blockers) so weekday/weekend selection never diverges from
        other duration call paths.
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

    def _resolve_planning_service(self) -> Any:
        if self._planning_service is not None:
            return self._planning_service
        from app.services.planning_service import PlanningService

        return PlanningService

    def _resolve_study_session_service(self) -> Any:
        if self._study_session_service is not None:
            return self._study_session_service
        from app.services.study_session_service import StudySessionService

        return StudySessionService

    def _resolve_study_plan_service(self) -> Any:
        if self._study_plan_service is not None:
            return self._study_plan_service
        from app.services.study_plan_service import StudyPlanService

        return StudyPlanService
