"""Mission Resume Adapter — continuity path to Runtime A (active session).

Experience → MissionResumeAdapter → StudySessionService / MissionService → SQL.

Translator only: locates and validates an existing active session. Does not
generate missions, start Pending sessions, or invent educational state.
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
    map_mission_to_resume_result,
)
from app.infrastructure.adapters.educational_runtime_bridge.resume_telemetry import (
    emit_failure,
    emit_latency,
    emit_requested,
    emit_success,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.events.registry import EventRegistry

logger = logging.getLogger(__name__)

_IN_PROGRESS = "in progress"


class MissionResumeAdapter:
    """Bridge adapter: resume an active study session via Runtime A.

    Controlled by ``ENABLE_MISSION_RESUME_BRIDGE``. Locates an In Progress SQL
    Mission, validates ownership and continuity, and returns the canonical
    educational projection. Never creates replacement or demo sessions.
    """

    ADAPTER_ID = "mission_resume_adapter"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        study_session_service: Any | None = None,
        mission_service: Any | None = None,
        study_plan_service: Any | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._study_session_service = study_session_service
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

    def resume_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
        as_of_date: date | None = None,
    ) -> BridgeResult:
        """Locate the student's active session and return canonical state.

        Uses ``StudySessionService.get_owned_mission`` for explicit ids and
        ``MissionService.get_today_mission`` when locating today's active
        session. Does not call start, generate, or invent missions.
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

            resolved_id = self._explicit_mission_key(
                mission_id=mission_id, session_id=session_id
            )
            if resolved_id is not None:
                mission = self._load_owned_mission(user_id, resolved_id)
            else:
                mission = self._locate_active_today(
                    user_id, as_of_date=as_of_date or date.today()
                )

            if isinstance(mission, BridgeResult):
                self._finish(sid, mission, started, failure=not mission.ok)
                return mission

            continuity = self._validate_continuity(mission, user_id=user_id)
            if continuity is not None:
                self._finish(sid, continuity, started, failure=not continuity.ok)
                return continuity

            # B3 (PX-003): pass the resumed mission's own date so
            # weekday/weekend selection agrees with every other duration
            # call path.
            estimated = self._estimated_minutes(
                user_id, mission_date=getattr(mission, "mission_date", None)
            )
            projection = map_mission_to_resume_result(
                mission,
                student_id=sid,
                session_id=session_id or str(mission.id),
                estimated_minutes=estimated,
            )
            result = BridgeResult(ok=True, value=projection, fallback_used=False)
            self._finish(
                sid,
                result,
                started,
                failure=False,
                mission_id=str(mission.id),
                session_id=str(projection.get("session_id") or mission.id),
            )
            return result
        except Exception as exc:  # noqa: BLE001 — bridge must fail closed
            logger.exception(
                "MissionResumeAdapter unavailable for student_id=%s", sid
            )
            result = BridgeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message=str(exc)[:256],
            )
            self._finish(sid, result, started, failure=True)
            return result

    def get_session_status(
        self,
        student_id: str,
        *,
        session_id: str,
    ) -> BridgeResult:
        """Resume-support status lookup keyed by Experience session_id."""
        return self.resume_session(student_id, session_id=session_id)

    @staticmethod
    def _explicit_mission_key(
        *,
        mission_id: str | None,
        session_id: str | None,
    ) -> str | None:
        for candidate in (mission_id, session_id):
            if candidate is not None and str(candidate).strip():
                return str(candidate).strip()
        return None

    def _locate_active_today(
        self, user_id: int, *, as_of_date: date
    ) -> Any | BridgeResult:
        """Read today's mission without generate/start — locate only."""
        mission_svc = self._resolve_mission_service()
        mission = mission_svc.get_today_mission(user_id, mission_date=as_of_date)
        if mission is None:
            code, message = self._absence_code(user_id, as_of_date)
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
                message="session_id / mission_id must be a SQL Mission id",
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
    def _validate_continuity(mission: Any, *, user_id: int) -> BridgeResult | None:
        """Fail closed when educational continuity cannot be preserved."""
        if int(mission.user_id) != int(user_id):
            return BridgeResult(
                ok=False,
                error_code=FORBIDDEN,
                message="mission ownership mismatch",
            )
        status = str(getattr(mission, "status", "") or "").strip().lower()
        if status == _IN_PROGRESS:
            return None
        if status == "completed":
            return BridgeResult(
                ok=False,
                error_code=INVALID_STATE,
                message="session is completed and cannot be resumed",
            )
        if status == "pending":
            return BridgeResult(
                ok=False,
                error_code=INVALID_STATE,
                message="session has not been started; resume requires In Progress",
            )
        return BridgeResult(
            ok=False,
            error_code=INVALID_STATE,
            message=f"session status {status!r} is not resumable",
        )

    def _finish(
        self,
        student_id: str,
        result: BridgeResult,
        started: float,
        *,
        failure: bool,
        mission_id: str | None = None,
        session_id: str | None = None,
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
            resolved_session_id = session_id
            if result.value is not None:
                if resolved_mission_id is None:
                    resolved_mission_id = str(result.value.get("mission_id"))
                if resolved_session_id is None:
                    resolved_session_id = str(result.value.get("session_id"))
            emit_success(
                self._events,
                student_id=student_id,
                mission_id=resolved_mission_id,
                session_id=resolved_session_id,
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
        """Classify why Runtime A has no active session to resume."""
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
        return NOT_FOUND, "no active in-progress session to resume"

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

    def _resolve_study_session_service(self) -> Any:
        if self._study_session_service is not None:
            return self._study_session_service
        from app.services.study_session_service import StudySessionService

        return StudySessionService

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
