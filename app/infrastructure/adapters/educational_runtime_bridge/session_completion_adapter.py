"""Session Completion Adapter — Evidence Before Completion path to Runtime A.

Experience → SessionCompletionAdapter → StudySessionService → MissionService
→ Evidence Authority → SQL.

Translator only: validates, commits educational evidence, then marks complete.
Does not generate recommendations, invent completion state, or bypass evidence.
"""

from __future__ import annotations

import logging
import time
from datetime import UTC, date, datetime
from typing import Any

from app.infrastructure.adapters.educational_runtime_bridge.contracts import (
    EVIDENCE_REJECTED,
    FORBIDDEN,
    INVALID_STATE,
    NOT_FOUND,
    UNAVAILABLE,
    BridgeResult,
)
from app.infrastructure.adapters.educational_runtime_bridge.mission_mapper import (
    map_mission_to_completion_result,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.events.registry import EventRegistry

from .completion_telemetry import (
    emit_failure,
    emit_latency,
    emit_requested,
    emit_success,
)

logger = logging.getLogger(__name__)

_IN_PROGRESS = "in progress"


class SessionCompletionAdapter:
    """Bridge adapter: complete an active study session via Runtime A.

    Controlled by ``ENABLE_SESSION_COMPLETION_BRIDGE``. Enforces Evidence
    Before Completion: validate → commit evidence → mark complete → project.
    Never invents demo educational state.
    """

    ADAPTER_ID = "session_completion_adapter"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        study_session_service: Any | None = None,
        mission_service: Any | None = None,
        learning_service: Any | None = None,
        study_plan_service: Any | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._study_session_service = study_session_service
        self._mission_service = mission_service
        self._learning_service = learning_service
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
        """Validate, commit evidence, then complete through Runtime A.

        Order (Evidence Before Completion):
        1. Validate session ownership and In Progress status.
        2. Commit educational evidence when practice outcome is present.
        3. Mark session complete via MissionService.
        4. Return canonical educational completion state.

        If evidence cannot be committed, the session remains active and
        completion fails cleanly with no partial educational completion.
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
            if resolved_id is None:
                result = BridgeResult(
                    ok=False,
                    error_code=NOT_FOUND,
                    message="session_id or mission_id is required to complete",
                )
                self._finish(sid, result, started, failure=True)
                return result

            mission = self._load_owned_mission(user_id, resolved_id)
            if isinstance(mission, BridgeResult):
                self._finish(sid, mission, started, failure=not mission.ok)
                return mission

            validation = self._validate_completable(mission, user_id=user_id)
            if validation is not None:
                self._finish(sid, validation, started, failure=not validation.ok)
                return validation

            practice = self._practice_fields(outcome)
            if practice is not None:
                evidence = self._commit_practice_evidence(
                    mission,
                    user_id=user_id,
                    practice=practice,
                )
                if isinstance(evidence, BridgeResult):
                    self._finish(sid, evidence, started, failure=True)
                    return evidence
                _attempt, evidence_accepted, mastery_updated = evidence
                completed = self._mark_session_complete(mission, user_id=user_id)
                if isinstance(completed, BridgeResult):
                    self._finish(sid, completed, started, failure=True)
                    return completed
                mission = completed
                self._observe_completed(
                    user_id=user_id,
                    mission_id=int(mission.id),
                    topic_id=practice.get("topic_id"),
                    duration_minutes=practice.get("duration_minutes"),
                )
            else:
                finish = self._finish_without_practice(
                    mission,
                    user_id=user_id,
                    outcome=outcome,
                )
                if isinstance(finish, BridgeResult):
                    self._finish(sid, finish, started, failure=True)
                    return finish
                mission, evidence_accepted, mastery_updated = finish

            # B3 (PX-003): pass the completed mission's own date so
            # weekday/weekend selection agrees with every other duration
            # call path.
            estimated = (
                estimated_minutes
                if estimated_minutes is not None
                else self._estimated_minutes(
                    user_id, mission_date=getattr(mission, "mission_date", None)
                )
            )
            completed_at = datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
            projection = map_mission_to_completion_result(
                mission,
                student_id=sid,
                session_id=session_id or str(mission.id),
                topic_title=topic_title or str(mission.title or ""),
                estimated_minutes=estimated,
                completed_at=completed_at,
                evidence_accepted=evidence_accepted,
                mastery_updated=mastery_updated,
            )
            result = BridgeResult(ok=True, value=projection, fallback_used=False)
            self._finish(
                sid,
                result,
                started,
                failure=False,
                mission_id=str(mission.id),
                session_id=str(projection.get("session_id") or mission.id),
                evidence_accepted=evidence_accepted,
            )
            return result
        except Exception as exc:  # noqa: BLE001 — bridge must fail closed
            logger.exception(
                "SessionCompletionAdapter unavailable for student_id=%s", sid
            )
            result = BridgeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message=str(exc)[:256],
            )
            self._finish(sid, result, started, failure=True)
            return result

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
                ok=False,
                error_code=NOT_FOUND,
                message="mission not found",
            )
        return mission

    @staticmethod
    def _validate_completable(mission: Any, *, user_id: int) -> BridgeResult | None:
        """Fail closed when the session cannot lawfully be completed."""
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
                message="session has already been recorded",
            )
        if status == "pending":
            return BridgeResult(
                ok=False,
                error_code=INVALID_STATE,
                message="session has not been started; complete requires In Progress",
            )
        return BridgeResult(
            ok=False,
            error_code=INVALID_STATE,
            message=f"session status {status!r} is not completable",
        )

    @staticmethod
    def _practice_fields(outcome: dict[str, Any] | None) -> dict[str, Any] | None:
        """Extract practice outcome fields when present; else None."""
        if not outcome:
            return None
        attempted = outcome.get("questions_attempted")
        correct = outcome.get("questions_correct")
        if attempted is None and correct is None:
            return None
        topic_id = outcome.get("topic_id")
        try:
            resolved_topic = None if topic_id is None else int(topic_id)
        except (TypeError, ValueError):
            resolved_topic = None
        duration = outcome.get("duration_minutes")
        try:
            resolved_duration = None if duration is None else int(duration)
        except (TypeError, ValueError):
            resolved_duration = None
        notes = outcome.get("notes")
        return {
            "questions_attempted": attempted,
            "questions_correct": correct,
            "duration_minutes": resolved_duration,
            "notes": None if notes is None else str(notes),
            "topic_id": resolved_topic,
        }

    def _commit_practice_evidence(
        self,
        mission: Any,
        *,
        user_id: int,
        practice: dict[str, Any],
    ) -> tuple[Any, bool, bool] | BridgeResult:
        """Commit educational evidence before marking the session complete.

        On failure the mission must remain In Progress (caller does not mark
        complete). Translates Runtime A validation / authority errors.
        """
        session_svc = self._resolve_study_session_service()
        try:
            session_svc.validate_practice_outcome(
                practice["questions_attempted"],
                practice["questions_correct"],
            )
        except ValueError as exc:
            return BridgeResult(
                ok=False,
                error_code=INVALID_STATE,
                message=str(exc)[:256],
            )
        if (
            practice.get("duration_minutes") is not None
            and int(practice["duration_minutes"]) <= 0
        ):
            return BridgeResult(
                ok=False,
                error_code=INVALID_STATE,
                message="Time spent must be a positive number of minutes.",
            )

        learning = self._resolve_learning_service()
        try:
            study_attempt = learning.create_study_attempt(
                user_id=user_id,
                mission_id=int(mission.id),
                topic_id=practice.get("topic_id"),
                study_date=date.today(),
                duration_minutes=practice.get("duration_minutes"),
                questions_attempted=int(practice["questions_attempted"]),
                questions_correct=int(practice["questions_correct"]),
                notes=practice.get("notes"),
            )
        except ValueError as exc:
            return BridgeResult(
                ok=False,
                error_code=EVIDENCE_REJECTED,
                message=str(exc)[:256],
            )
        except Exception as exc:  # noqa: BLE001 — evidence fail closed
            logger.exception(
                "evidence commit failed mission=%s user=%s", mission.id, user_id
            )
            return BridgeResult(
                ok=False,
                error_code=EVIDENCE_REJECTED,
                message=str(exc)[:256],
            )

        from app.services.educational_evidence_authority import (
            EducationalEvidenceAuthority,
        )

        evidence_accepted = (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results(
                study_attempt
            )
        )
        mastery_updated = bool(
            evidence_accepted and practice.get("topic_id") is not None
        )
        return study_attempt, evidence_accepted, mastery_updated

    def _mark_session_complete(
        self, mission: Any, *, user_id: int
    ) -> Any | BridgeResult:
        """Mark tasks done and complete the mission after evidence commit."""
        session_svc = self._resolve_study_session_service()
        mission_svc = self._resolve_mission_service()
        try:
            session_svc.mark_all_tasks_complete(mission)
            # Re-load after task commit so MissionService sees completed tasks.
            refreshed = session_svc.get_owned_mission(int(mission.id), user_id)
            completed = mission_svc.complete_mission(int(refreshed.id), user_id)
        except ValueError as exc:
            return BridgeResult(
                ok=False,
                error_code=self._translate_complete_value_error(exc),
                message=str(exc)[:256],
            )
        return completed

    def _finish_without_practice(
        self,
        mission: Any,
        *,
        user_id: int,
        outcome: dict[str, Any] | None,
    ) -> tuple[Any, bool, bool] | BridgeResult:
        """Complete engagement without structured practice via finish_session."""
        from app.services.study_session_service import COMPLETION_YES

        session_svc = self._resolve_study_session_service()
        completion_status = COMPLETION_YES
        notes = "No practice questions recorded today."
        topic_id = None
        if outcome:
            status = outcome.get("completion_status")
            if status is not None and str(status).strip():
                completion_status = str(status).strip().lower()
            if outcome.get("notes") is not None:
                notes = str(outcome.get("notes"))
            raw_topic = outcome.get("topic_id")
            try:
                topic_id = None if raw_topic is None else int(raw_topic)
            except (TypeError, ValueError):
                topic_id = None
        try:
            result = session_svc.finish_session(
                mission_id=int(mission.id),
                user_id=user_id,
                completion_status=completion_status,
                notes=notes,
                topic_id=topic_id,
            )
        except ValueError as exc:
            return BridgeResult(
                ok=False,
                error_code=self._translate_complete_value_error(exc),
                message=str(exc)[:256],
            )
        # finish_session without structured questions is engagement close only —
        # not authorised Educational Evidence of understanding.
        return result.mission, False, False

    def _observe_completed(
        self,
        *,
        user_id: int,
        mission_id: int,
        topic_id: int | None,
        duration_minutes: int | None,
    ) -> None:
        session_svc = self._resolve_study_session_service()
        from app.services.study_session_service import COMPLETION_YES

        observe = getattr(session_svc, "_observe_session_completed", None)
        if observe is None:
            return
        try:
            observe(
                user_id=user_id,
                mission_id=mission_id,
                session_completion=COMPLETION_YES,
                topic_id=topic_id,
                duration_minutes=duration_minutes,
            )
        except Exception:  # noqa: BLE001 — analytics must never break learning
            logger.exception(
                "completion observe failed mission=%s user=%s",
                mission_id,
                user_id,
            )

    @staticmethod
    def _translate_complete_value_error(exc: ValueError) -> str:
        message = str(exc).lower()
        if "already been recorded" in message or "already" in message:
            return INVALID_STATE
        if "does not belong" in message:
            return FORBIDDEN
        if "not found" in message:
            return NOT_FOUND
        if "complete all mission" in message:
            return INVALID_STATE
        return INVALID_STATE

    def _finish(
        self,
        student_id: str,
        result: BridgeResult,
        started: float,
        *,
        failure: bool,
        mission_id: str | None = None,
        session_id: str | None = None,
        evidence_accepted: bool | None = None,
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
            accepted = evidence_accepted
            if result.value is not None:
                if resolved_mission_id is None:
                    resolved_mission_id = str(result.value.get("mission_id"))
                if resolved_session_id is None:
                    resolved_session_id = str(result.value.get("session_id"))
                if accepted is None:
                    accepted = bool(result.value.get("evidence_accepted"))
            emit_success(
                self._events,
                student_id=student_id,
                mission_id=resolved_mission_id,
                session_id=resolved_session_id,
                error_code=result.error_code,
                evidence_accepted=accepted,
            )
        emit_latency(
            self._events,
            student_id=student_id,
            latency_ms=latency_ms,
            ok=not failure,
        )

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

    def _resolve_learning_service(self) -> Any:
        if self._learning_service is not None:
            return self._learning_service
        from app.services.learning_service import LearningService

        return LearningService

    def _resolve_study_plan_service(self) -> Any:
        if self._study_plan_service is not None:
            return self._study_plan_service
        from app.services.study_plan_service import StudyPlanService

        return StudyPlanService
