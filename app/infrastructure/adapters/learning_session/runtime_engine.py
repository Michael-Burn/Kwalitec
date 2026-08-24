"""Opaque Learning Session Runtime engine
(SR-002 / LXP-003 / EV-001B / SDT-004 / SR-003).

Session Experience HTTP remains an ADAPTER. This engine elevates
LearningSessionRuntime as AUTHORITY for begin / pause / resume / finish
review / snapshot / complete phase transitions on spine-bound sessions.

P2: pause/resume, finish review, progress recovery.
P3: substance projections.
P4 / EV-001B: candidate observation emission + Evidence Before Completion gate.
P5 / SDT-004: Twin consumes Accepted Educational+ packages when
``SR_TWIN_DAILY_LOOP`` is ON. LearningSessionRuntime FSM unchanged.
P6 / SR-003: Progress Engine authorises coverage advancement when
``SR_PROGRESS_SINGULARITY`` is ON. Twin estimates optional for projections.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.evidence_gate import (
    EvidenceBeforeCompletionGate,
)
from app.application.learning_session.exceptions import (
    EvidenceGateRejected,
    FinishReviewRequired,
    InvalidSessionState,
    SessionAlreadyArchived,
    SessionAlreadyCompleted,
)
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.learning_session.runtime_phase import (
    RuntimePhase,
    product_lifecycle_label,
)
from app.application.progress_engine import ProgressEngine, TwinEstimateInput
from app.application.student_twin.session_evidence_consumer import (
    SessionTwinEvidenceConsumer,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    format_learning_objective_label,
)
from app.infrastructure.adapters.learning_session.persistence import (
    DEFAULT_CHECKLIST,
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.student_twin.daily_loop_persistence import (
    DailyLoopTwinPersistence,
)

logger = logging.getLogger(__name__)


class LearningSessionRuntimeEngine:
    """Opaque runtime_engine compatible with SessionRuntimeAdapter.

    Implements ``*_opaque`` methods so Session Experience never imports
    LearningSessionRuntime packages directly.
    """

    def __init__(
        self,
        *,
        runtime: LearningSessionRuntime | None = None,
        persistence: LearningSessionPersistenceAdapter | None = None,
        require_finish_review: bool | None = None,
        evidence_gate: EvidenceBeforeCompletionGate | None = None,
        mission_completer: Any | None = None,
        twin_consumer: SessionTwinEvidenceConsumer | None = None,
        progress_engine: ProgressEngine | None = None,
    ) -> None:
        self._runtime = runtime or LearningSessionRuntime()
        self._persistence = persistence or LearningSessionPersistenceAdapter()
        self._require_finish_review = require_finish_review
        self._evidence_gate = evidence_gate or EvidenceBeforeCompletionGate()
        self._mission_completer = mission_completer
        if twin_consumer is not None:
            self._twin_consumer = twin_consumer
        else:
            twin_store = DailyLoopTwinPersistence(store=self._persistence.store)
            self._twin_consumer = SessionTwinEvidenceConsumer(store=twin_store)
        self._progress_engine = progress_engine or ProgressEngine()

    @property
    def persistence(self) -> LearningSessionPersistenceAdapter:
        return self._persistence

    def _finish_review_required(self) -> bool:
        if self._require_finish_review is not None:
            return bool(self._require_finish_review)
        return bool(resolve_v2_feature_flags().SR_SESSION_COMPLETION_PRODUCT)

    def _evidence_gate_enabled(self) -> bool:
        return bool(resolve_v2_feature_flags().SR_EVIDENCE_GATE)

    def _maybe_write_sql_evidence_companion(
        self,
        *,
        student_id: str,
        session_id: str,
        record: dict[str, Any],
    ) -> Any | None:
        """Phase 2: aggregate scored practice → companion Mission StudyAttempt."""
        try:
            user_id = int(str(student_id).strip())
        except (TypeError, ValueError):
            return None
        duration = None
        try:
            raw_minutes = record.get("estimated_minutes")
            if raw_minutes is not None and str(raw_minutes).strip() != "":
                duration = int(raw_minutes)
                if duration <= 0:
                    duration = None
        except (TypeError, ValueError):
            duration = None
        from app.application.student_runtime.evidence_write_through import (
            maybe_write_sql_evidence_from_sitting,
        )

        return maybe_write_sql_evidence_from_sitting(
            user_id=user_id,
            session_id=session_id,
            mission_instance_id=str(record.get("mission_instance_id") or ""),
            store=self._persistence.store,
            topic_id=record.get("topic_id"),
            duration_minutes=duration,
        )

    def _persist_educational_memory(
        self,
        *,
        session_id: str,
        package_opaque: dict[str, Any] | None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """KWP-011 — freeze EI outputs onto the Evidence Package (additive)."""
        try:
            from app.application.educational_memory import (
                get_educational_memory_service,
            )

            snapshot = get_educational_memory_service().persist_on_store(
                store=self._persistence.store,
                session_id=session_id,
                package=package_opaque
                if isinstance(package_opaque, dict)
                else None,
                metadata=metadata,
            )
            return snapshot.to_opaque() if snapshot is not None else None
        except Exception:  # noqa: BLE001 — memory must never block complete
            logger.exception(
                "educational_memory_persist_failed session_id=%s", session_id
            )
            return None


    def _rebinding(
        self,
        *,
        student_id: str,
        record: dict[str, Any],
        handle: Any,
        active_surface: str | None = None,
    ) -> None:
        self._persistence.save_binding(
            student_id=student_id,
            mission_instance_id=str(record.get("mission_instance_id") or ""),
            handle=handle,
            topic_title=str(record.get("topic_title") or ""),
            topic_id=str(record.get("topic_id") or ""),
            estimated_minutes=record.get("estimated_minutes"),
            curriculum_identity=str(record.get("curriculum_identity") or ""),
            active_surface=active_surface,
            educational_package_id=str(
                record.get("educational_package_id") or ""
            ),
        )

    def get_session_overview_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        topic = str(record.get("topic_title") or "Today's topic")
        minutes = record.get("estimated_minutes") or 30
        progress = self._persistence.load_progress(session_id=session_id) or {}
        checklist = progress.get("checklist") or list(DEFAULT_CHECKLIST)
        handle = self._persistence.load_handle(session_id=session_id)
        phase = (
            handle.phase.value
            if handle is not None
            else str(record.get("phase") or "planned")
        )
        substance_on = bool(resolve_v2_feature_flags().SR_SESSION_SUBSTANCE)
        learning_objectives, activity_count, substance_status = (
            self._substance_overview_fields(
                student_id=student_id,
                session_id=session_id,
                topic=topic,
                substance_on=substance_on,
            )
        )
        return {
            "objective": f"Strengthen {topic}",
            "learning_goal": topic,
            "why_studying": f"Today's Mission focuses on {topic}.",
            "estimated_minutes": minutes,
            "activity_count": activity_count,
            "topics": (topic,),
            "topic_title": topic,
            "learning_objectives": learning_objectives,
            "educational_flow": (
                "learning_objectives",
                "read",
                "worked_example",
                "practice",
                "reflection",
                "ready_to_finish",
            ),
            "status": "in_progress"
            if record.get("status") == "open"
            else "completed",
            "mission_id": record.get("mission_instance_id"),
            "session_id": session_id,
            "student_id": student_id,
            "authority": "learning_session_runtime",
            "substance": substance_status,
            "phase": phase,
            "lifecycle_label": product_lifecycle_label(RuntimePhase(phase))
            if phase in {p.value for p in RuntimePhase}
            else phase,
            "checklist": checklist,
            "active_surface": progress.get("active_surface") or "overview",
            "paused": bool(progress.get("paused")),
            "finish_review_required": self._finish_review_required(),
            "finish_review": record.get("finish_review"),
        }

    def begin_session_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        handle = self._persistence.load_handle(session_id=session_id)
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        if handle is None:
            return {
                "session_id": session_id,
                "student_id": student_id,
                "status": "in_progress",
                "authority": "learning_session_runtime",
            }
        phase = handle.phase.value
        if phase in {"planned", "ready"}:
            handle = self._runtime.start_session(handle)
        elif phase == "paused":
            handle = self._runtime.resume_session(handle)
        elif phase == "ready_to_finish":
            handle = self._runtime.resume_session(handle)
        self._rebinding(
            student_id=student_id,
            record=record,
            handle=handle,
            active_surface="activity",
        )
        self._emit_candidate(
            RuntimeEvidenceType.SESSION_STARTED,
            student_id=student_id,
            session_id=session_id,
            record=record,
            stage="session",
        )
        if record.get("mission_instance_id"):
            self._emit_candidate(
                RuntimeEvidenceType.MISSION_ACCEPTED,
                student_id=student_id,
                session_id=session_id,
                record=record,
                stage="mission",
            )
        objectives = self._learning_objectives_from_sequence(
            student_id=student_id, session_id=session_id
        )
        if objectives:
            self._emit_candidate(
                RuntimeEvidenceType.LEARNING_OBJECTIVES_PRESENTED,
                student_id=student_id,
                session_id=session_id,
                record=record,
                stage="learning_objectives",
                payload={"count": len(objectives)},
            )
        return {
            "session_id": session_id,
            "student_id": student_id,
            "mission_id": record.get("mission_instance_id"),
            "status": "in_progress",
            "phase": handle.phase.value,
            "lifecycle_label": product_lifecycle_label(handle.phase),
            "authority": "learning_session_runtime",
            "evidence_emitted": self._evidence_gate_enabled(),
        }

    def pause_session_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        handle = self._persistence.load_handle(session_id=session_id)
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        if handle is None:
            return None
        try:
            handle = self._runtime.pause_session(handle)
        except (InvalidSessionState, SessionAlreadyCompleted, SessionAlreadyArchived):
            return {
                "session_id": session_id,
                "student_id": student_id,
                "status": "error",
                "phase": handle.phase.value,
                "authority": "learning_session_runtime",
                "error": "cannot_pause",
            }
        progress = self._persistence.load_progress(session_id=session_id) or {}
        self._rebinding(
            student_id=student_id,
            record=record,
            handle=handle,
            active_surface=str(progress.get("active_surface") or "activity"),
        )
        self._emit_candidate(
            RuntimeEvidenceType.SESSION_PAUSED,
            student_id=student_id,
            session_id=session_id,
            record=record,
            stage="session",
        )
        return {
            "session_id": session_id,
            "student_id": student_id,
            "status": "paused",
            "phase": handle.phase.value,
            "lifecycle_label": product_lifecycle_label(handle.phase),
            "authority": "learning_session_runtime",
        }

    def resume_session_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        handle = self._persistence.load_handle(session_id=session_id)
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        if handle is None:
            return None
        try:
            if handle.phase in {
                RuntimePhase.PAUSED,
                RuntimePhase.READY_TO_FINISH,
            }:
                handle = self._runtime.resume_session(handle)
        except (InvalidSessionState, SessionAlreadyCompleted, SessionAlreadyArchived):
            return {
                "session_id": session_id,
                "student_id": student_id,
                "status": "error",
                "phase": handle.phase.value,
                "authority": "learning_session_runtime",
                "error": "cannot_resume",
            }
        progress = self._persistence.load_progress(session_id=session_id) or {}
        surface = str(progress.get("active_surface") or "activity")
        if surface in {"summary", "complete"}:
            surface = "activity"
        self._rebinding(
            student_id=student_id,
            record=record,
            handle=handle,
            active_surface=surface,
        )
        self._emit_candidate(
            RuntimeEvidenceType.SESSION_RESUMED,
            student_id=student_id,
            session_id=session_id,
            record=record,
            stage="session",
        )
        return {
            "session_id": session_id,
            "student_id": student_id,
            "status": "in_progress",
            "phase": handle.phase.value,
            "lifecycle_label": product_lifecycle_label(handle.phase),
            "active_surface": surface,
            "authority": "learning_session_runtime",
        }

    def request_finish_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Enter Ready to Finish — Finish Review required before close."""
        handle = self._persistence.load_handle(session_id=session_id)
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        if handle is None:
            return None
        try:
            if handle.phase != RuntimePhase.READY_TO_FINISH:
                handle = self._runtime.request_finish(handle)
        except (InvalidSessionState, SessionAlreadyCompleted, SessionAlreadyArchived):
            return {
                "session_id": session_id,
                "student_id": student_id,
                "status": "error",
                "phase": handle.phase.value,
                "authority": "learning_session_runtime",
                "error": "cannot_request_finish",
            }
        self._rebinding(
            student_id=student_id,
            record=record,
            handle=handle,
            active_surface="summary",
        )
        return {
            "session_id": session_id,
            "student_id": student_id,
            "status": "ready_to_finish",
            "phase": handle.phase.value,
            "lifecycle_label": product_lifecycle_label(handle.phase),
            "finish_review_required": True,
            "authority": "learning_session_runtime",
        }

    def get_runtime_snapshot_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        handle = self._persistence.load_handle(session_id=session_id)
        progress = self._persistence.load_progress(session_id=session_id) or {}
        topic = str(record.get("topic_title") or "Today's topic")
        checklist = progress.get("checklist") or list(DEFAULT_CHECKLIST)
        done = sum(1 for item in checklist if item.get("done"))
        total = max(1, len(checklist))
        overall = round(done / total, 4)
        if handle is not None:
            snap = self._runtime.generate_runtime_snapshot(handle)
            return {
                "activities_completed": done,
                "activities_remaining": max(0, total - done),
                "activities_total": total,
                "estimated_remaining_minutes": record.get("estimated_minutes") or 30,
                "current_topic": topic,
                "overall_progress": overall,
                "phase": snap.phase,
                "lifecycle_label": product_lifecycle_label(handle.phase),
                "session_state": snap.session_state.value,
                "checklist": checklist,
                "active_surface": progress.get("active_surface") or "activity",
                "paused": handle.phase == RuntimePhase.PAUSED,
                "finish_review": (
                    handle.finish_review.to_opaque()
                    if handle.finish_review is not None
                    else None
                ),
                "authority": "learning_session_runtime",
            }
        return {
            "activities_completed": done,
            "activities_remaining": max(0, total - done),
            "activities_total": total,
            "estimated_remaining_minutes": record.get("estimated_minutes") or 30,
            "current_topic": topic,
            "overall_progress": overall,
            "phase": record.get("phase"),
            "checklist": checklist,
            "active_surface": progress.get("active_surface") or "overview",
            "paused": bool(progress.get("paused")),
            "authority": "learning_session_runtime",
        }

    def record_response_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
        scored_correct: bool | None = None,
        structured: bool = False,
        score_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        substance_on = bool(resolve_v2_feature_flags().SR_SESSION_SUBSTANCE)
        record = self._persistence.load(session_id=session_id) or {}
        stage = self._stage_for_activity(
            student_id=student_id, session_id=session_id, activity_id=activity_id
        )
        emitted = False
        evidence_type = ""
        if self._evidence_gate_enabled():
            obs = self._evidence_gate.builder.observation_for_stage_response(
                stage=stage,
                student_id=student_id,
                session_id=session_id,
                topic_id=str(record.get("topic_id") or ""),
                mission_instance_id=str(record.get("mission_instance_id") or ""),
                activity_id=activity_id,
                response=response,
                scored_correct=scored_correct,
                structured=bool(structured) and scored_correct is not None,
                score_payload=score_payload,
            )
            self._persistence.append_candidate(
                session_id=session_id, observation=obs.to_opaque()
            )
            emitted = True
            evidence_type = obs.type_id.value
        return {
            "recorded": True,
            "student_id": student_id,
            "session_id": session_id,
            "activity_id": activity_id,
            "authority": "learning_session_runtime",
            "substance": "package" if substance_on else "incomplete",
            "response_length": len((response or "").strip()),
            "evidence_emitted": emitted,
            "evidence_type": evidence_type,
            "scored_correct": scored_correct,
            "twin_updated": False,
            "stage": stage,
        }

    def update_checklist_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        item_id: str,
        done: bool,
    ) -> dict[str, Any] | None:
        progress = self._persistence.update_checklist_item(
            session_id=session_id,
            student_id=student_id,
            item_id=item_id,
            done=done,
        )
        if progress is None:
            return None
        return {
            "session_id": session_id,
            "student_id": student_id,
            "checklist": progress.get("checklist"),
            "authority": "learning_session_runtime",
        }

    def save_surface_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        surface: str,
    ) -> dict[str, Any] | None:
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        handle = self._persistence.load_handle(session_id=session_id)
        progress = self._persistence.load_progress(session_id=session_id) or {}
        saved = self._persistence.save_progress(
            session_id=session_id,
            student_id=student_id,
            active_surface=surface,
            checklist=list(progress.get("checklist") or DEFAULT_CHECKLIST),
            phase=(
                handle.phase.value
                if handle is not None
                else str(record.get("phase") or "")
            ),
            paused=handle.phase == RuntimePhase.PAUSED if handle else False,
            elapsed_active_seconds=progress.get("elapsed_active_seconds"),
        )
        return {
            "session_id": session_id,
            "student_id": student_id,
            "active_surface": saved.get("active_surface"),
            "authority": "learning_session_runtime",
        }

    def complete_session_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        finish_verdict: str | None = None,
        finish_notes: str | None = None,
    ) -> dict[str, Any] | None:
        """Complete LSR session; optionally mission/progress under EV-001B gate.

        When ``SR_SESSION_COMPLETION_PRODUCT`` is ON, ``finish_verdict``
        (yes / partially / no) is required. No silent auto-complete.

        When ``SR_EVIDENCE_GATE`` is ON, EducationalEvidenceAuthority validates
        the sitting Evidence Package before session close may proceed to
        mission completion / progress advancement. Twin remains read-only.
        """
        handle = self._persistence.load_handle(session_id=session_id)
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        require_review = self._finish_review_required()
        gate_on = self._evidence_gate_enabled()

        if handle is not None and handle.phase.value not in {
            "completed",
            "archived",
        }:
            if finish_verdict:
                handle = self._runtime.record_finish_review(
                    handle,
                    verdict=finish_verdict,
                    notes=finish_notes,
                )
                if handle.phase != RuntimePhase.READY_TO_FINISH:
                    handle = self._runtime.request_finish(handle)
                self._emit_finish_review_candidate(
                    student_id=student_id,
                    session_id=session_id,
                    record=record,
                    verdict=finish_verdict,
                    notes=finish_notes,
                )

            evidence_package = None
            if gate_on:
                try:
                    evidence_package = self._run_evidence_gate(
                        student_id=student_id,
                        session_id=session_id,
                        record=record,
                        finish_verdict=(
                            finish_verdict
                            or (
                                handle.finish_review.verdict.value
                                if handle.finish_review is not None
                                else None
                            )
                        ),
                        finish_notes=finish_notes,
                    )
                except EvidenceGateRejected as exc:
                    return {
                        "session_id": session_id,
                        "student_id": student_id,
                        "status": "error",
                        "error": "evidence_gate_rejected",
                        "reason": exc.reason,
                        "message": exc.student_explanation or str(exc),
                        "package_id": exc.package_id,
                        "authority": "educational_evidence_authority",
                        "progress_advanced": False,
                        "mission_completed": False,
                        "twin_updated": False,
                    }

            try:
                handle = self._runtime.complete_session(
                    handle,
                    attach_pending_reflection=True,
                    require_finish_review=require_review,
                )
            except FinishReviewRequired as exc:
                return {
                    "session_id": session_id,
                    "student_id": student_id,
                    "status": "error",
                    "error": "finish_review_required",
                    "message": str(exc),
                    "authority": "learning_session_runtime",
                    "progress_advanced": False,
                    "mission_completed": False,
                    "twin_updated": False,
                }
            self._emit_candidate(
                RuntimeEvidenceType.SESSION_COMPLETED,
                student_id=student_id,
                session_id=session_id,
                record=record,
                stage="session",
            )
            self._rebinding(
                student_id=student_id,
                record=record,
                handle=handle,
                active_surface="complete",
            )
        else:
            evidence_package = None
            if gate_on:
                evidence_package = self._persistence.load_evidence_package(
                    session_id=session_id
                )

        self._persistence.mark_completed(session_id=session_id)
        review = None
        if handle is not None and handle.finish_review is not None:
            review = handle.finish_review.to_opaque()
        elif record.get("finish_review"):
            review = record.get("finish_review")

        mission_completed = False
        progress_advanced = False
        twin_updated = False
        twin_result_opaque = None
        package_opaque = None
        disposition = None
        if gate_on and evidence_package is not None:
            if hasattr(evidence_package, "to_opaque"):
                package_opaque = evidence_package.to_opaque()
                validation = evidence_package.validation
            else:
                package_opaque = evidence_package
                validation = None
                from app.application.learning_session.dto.evidence_package import (
                    EvidenceValidationResult,
                )

                validation = EvidenceValidationResult.from_opaque(
                    evidence_package.get("validation")
                    if isinstance(evidence_package, dict)
                    else None
                )
            if validation is not None:
                disposition = validation.disposition.value
                decision = self._progress_engine.authorise_from_validation(
                    validation,
                    topic_id=str(record.get("topic_id") or "") or None,
                    package_id=(
                        evidence_package.package_id
                        if hasattr(evidence_package, "package_id")
                        else str((package_opaque or {}).get("package_id") or "")
                    ),
                    mission_instance_id=str(
                        record.get("mission_instance_id") or ""
                    )
                    or None,
                )
                if validation.may_complete_mission:
                    mission_completed = self._complete_mission_if_authorised(
                        student_id=student_id,
                        mission_instance_id=str(
                            record.get("mission_instance_id") or ""
                        ),
                        advance_progress=decision.may_advance,
                        package_id=(
                            evidence_package.package_id
                            if hasattr(evidence_package, "package_id")
                            else str(
                                (package_opaque or {}).get("package_id") or ""
                            )
                        ),
                        evidence_disposition=disposition,
                        may_complete_mission=True,
                    )
                    progress_advanced = bool(
                        mission_completed and decision.may_advance
                    )
                twin_result = self._consume_twin_evidence(evidence_package)
                twin_updated = bool(twin_result.get("twin_updated"))
                twin_result_opaque = twin_result
                if twin_updated and hasattr(evidence_package, "with_lifecycle"):
                    from app.application.learning_session.dto.evidence_package import (
                        EvidenceLifecycleState,
                    )

                    consumed = evidence_package.with_lifecycle(
                        EvidenceLifecycleState.CONSUMED
                    )
                    package_opaque = consumed.to_opaque()
                    package_opaque["twin_updated"] = True
                    self._persistence.save_evidence_package(
                        session_id=session_id, package=package_opaque
                    )

        study_progress_opaque = None
        if (
            self._progress_engine.singularity_enabled()
            and gate_on
            and evidence_package is not None
        ):
            study_progress_opaque = self._study_progress_opaque(
                twin_result=twin_result_opaque,
                topic_id=str(record.get("topic_id") or "") or None,
                curriculum_identity=(
                    str(
                        getattr(evidence_package, "curriculum_identity", None)
                        or (package_opaque or {}).get("curriculum_identity")
                        or ""
                    )
                    or None
                ),
            )

        # KWP-005: persist sitting outcome flags for Sitting Report GET.
        self._persistence.save_sitting_outcome(
            session_id=session_id,
            progress_advanced=progress_advanced,
            mission_completed=mission_completed,
            twin_updated=twin_updated,
            evidence_disposition=disposition,
            finish_review=review if isinstance(review, dict) else None,
        )

        # KWP-011: freeze educational intelligence onto the Evidence Package.
        # Persistence only — does not redesign Strategy / Diagnostics /
        # Difficulty / Effectiveness / Evidence / Progress / Twin / Runtime.
        memory_snapshot = self._persist_educational_memory(
            session_id=session_id,
            package_opaque=package_opaque,
            metadata={
                "progress_advanced": progress_advanced,
                "mission_completed": mission_completed,
                "evidence_disposition": disposition or "",
                "twin_updated": twin_updated,
            },
        )
        if memory_snapshot is not None and isinstance(package_opaque, dict):
            package_opaque = {
                **package_opaque,
                "intelligence_snapshot": memory_snapshot,
            }

        # Phase 2 — additive Runtime A StudyAttempt write-through via companion
        # Mission. Does not alter Runtime C gate / Twin / mission-complete flags.
        sql_attempt = self._maybe_write_sql_evidence_companion(
            student_id=student_id,
            session_id=session_id,
            record=record,
        )

        return {
            "session_id": session_id,
            "student_id": student_id,
            "status": "completed",
            "authority": "learning_session_runtime",
            "progress_advanced": progress_advanced,
            "mission_completed": mission_completed,
            "twin_updated": twin_updated,
            "twin_consumption": twin_result_opaque,
            "study_progress": study_progress_opaque,
            "progress_authority": (
                "progress_engine"
                if self._progress_engine.singularity_enabled()
                else None
            ),
            "finish_review": review,
            "evidence_disposition": disposition,
            "evidence_package": package_opaque,
            "intelligence_snapshot": memory_snapshot,
            "evidence_gate": gate_on,
            "sql_evidence_attempt_id": (
                int(sql_attempt.id) if sql_attempt is not None else None
            ),
        }

    def get_reflection_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        topic = str(record.get("topic_title") or "Today's topic")
        substance_on = bool(resolve_v2_feature_flags().SR_SESSION_SUBSTANCE)
        if substance_on:
            # EA-006: prefer certified package reflection when topic matches.
            pack_prompt = ""
            try:
                from app.application.educational_packages.loader import (
                    find_educational_package,
                )

                pack = find_educational_package(topic_title=topic)
                if pack is not None:
                    pack_prompt = pack.reflection_prompt or pack.reflection_framing
            except Exception:  # noqa: BLE001 — reflection must stay resilient
                pack_prompt = ""
            objectives = self._learning_objectives_from_sequence(
                student_id=student_id, session_id=session_id
            )
            lead = objectives[0] if objectives else ""
            insight = (
                f"You worked through reading, examples, and practice on {topic}."
            )
            confidence = (
                f"Growing comfort with {lead}"
                if lead
                else f"Growing comfort with {topic}"
            )
            improvement = (
                f"Revisit the learning objective that still feels unclear in {topic}."
            )
            prompt = pack_prompt or (
                f"After reading, examples, and practice on {topic}, "
                "what still feels unclear — and what will you try next?"
            )
            return {
                "key_insight": insight,
                "concept_confidence": confidence,
                "suggested_improvement": improvement,
                "reflection_prompt": prompt,
                "topic_title": topic,
                "learning_objectives": objectives,
                "skip_available": True,
                "authority": "learning_session_runtime",
                "substance": "educational_package" if pack_prompt else "package",
                "twin_updated": False,
            }
        return {
            "key_insight": "",
            "concept_confidence": "",
            "suggested_improvement": "",
            "reflection_prompt": f"What felt clear about {topic}?",
            "topic_title": topic,
            "authority": "learning_session_runtime",
            "substance": "incomplete",
            "twin_updated": False,
        }

    def get_completion_summary_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        record = self._persistence.load(session_id=session_id)
        if record is None or str(record.get("student_id")) != student_id.strip():
            return None
        topic = str(record.get("topic_title") or "Today's topic")
        review = record.get("finish_review")
        substance_on = bool(resolve_v2_feature_flags().SR_SESSION_SUBSTANCE)
        progress = self._persistence.load_progress(session_id=session_id) or {}
        seq = self._persistence.store.get(
            "activity.sequence", f"{student_id.strip()}::{session_id.strip()}"
        )
        activities_completed = int((seq or {}).get("completed") or 0)
        activity_items = self._activity_items_for_summary(
            seq if isinstance(seq, dict) else None
        )
        objectives = self._learning_objectives_from_sequence(
            student_id=student_id, session_id=session_id
        )
        package = self._persistence.load_evidence_package(session_id=session_id) or {}
        observations = list(package.get("observations") or ())
        observation_type_ids = [
            str(o.get("type_id") or "")
            for o in observations
            if isinstance(o, dict) and o.get("type_id")
        ]
        syllabus_refs: list[str] = []
        for item in activity_items:
            for ref in item.get("syllabus_refs") or ():
                text = str(ref).strip()
                if text and text not in syllabus_refs:
                    syllabus_refs.append(text)
        package_objectives = tuple(
            str(x).strip()
            for x in (package.get("learning_objectives") or ())
            if str(x).strip()
        )
        if not objectives and package_objectives:
            objectives = package_objectives

        progress_advanced = bool(record.get("progress_advanced"))
        mission_completed = bool(record.get("mission_completed"))
        disposition = (
            record.get("evidence_disposition")
            or (package.get("validation") or {}).get("disposition")
        )
        # Presentation-layer insights are refined by Sitting Report builder;
        # keep a calm fallback here for rollback paths.
        if substance_on:
            insights = [
                f"You completed today's study flow for {topic}.",
            ]
        else:
            insights = [
                "Session complete. Learning Insights thicken as you practice.",
            ]
        if isinstance(review, dict) and review.get("verdict"):
            verdict = str(review.get("verdict") or "").lower()
            if verdict == "yes":
                insights.insert(0, "You confirmed today's planned study was complete.")
            elif verdict == "partially":
                insights.insert(0, "You marked today's study as partially complete.")
            elif verdict == "no":
                insights.insert(0, "You recorded that planned study was not complete.")

        return {
            "topics_completed": (topic,) if substance_on else (),
            "time_studied_minutes": record.get("estimated_minutes") or 0,
            "activities_completed": activities_completed,
            "learning_insights": tuple(insights),
            "exam_readiness_change": 0.0,
            "topic_title": topic,
            "authority": "learning_session_runtime",
            "progress_advanced": progress_advanced,
            "mission_completed": mission_completed,
            "finish_review": review,
            "substance": "package" if substance_on else "incomplete",
            "checklist": progress.get("checklist"),
            "learning_objectives": objectives,
            "activities": activity_items,
            "observations": observations,
            "observation_type_ids": observation_type_ids,
            "syllabus_refs": tuple(syllabus_refs),
            "evidence_disposition": disposition,
            "package_learning_objectives": package_objectives,
            "educational_package_id": str(
                record.get("educational_package_id") or ""
            ).strip()
            or _educational_package_id_from_sequence(
                seq if isinstance(seq, dict) else None
            ),
            "subject_id": str(
                (record.get("curriculum_identity") or "").split(":")[0]
            ).strip(),
            "intelligence_snapshot": package.get("intelligence_snapshot"),
            "prior_intervention": (
                (package.get("intelligence_snapshot") or {}).get(
                    "prior_intervention"
                )
                if isinstance(package.get("intelligence_snapshot"), dict)
                else package.get("prior_intervention")
            ),
        }

    def _activity_items_for_summary(
        self, seq: dict[str, Any] | None
    ) -> list[dict[str, Any]]:
        if not isinstance(seq, dict):
            return []
        items: list[dict[str, Any]] = []
        completed_ids = {
            str(x)
            for x in (
                seq.get("completed_activity_ids")
                or seq.get("completed_ids")
                or ()
            )
        }
        completed_count = int(seq.get("completed") or 0)
        for idx, raw in enumerate(seq.get("activities") or ()):
            if not isinstance(raw, dict):
                continue
            activity_id = str(raw.get("activity_id") or raw.get("id") or idx)
            done = (
                activity_id in completed_ids
                or bool(raw.get("completed"))
                or bool(raw.get("done"))
                or idx < completed_count
            )
            items.append(
                {
                    "activity_id": activity_id,
                    "title": str(raw.get("title") or raw.get("label") or ""),
                    "stage": str(raw.get("stage") or raw.get("activity_type") or ""),
                    "completed": done,
                    "syllabus_refs": list(raw.get("syllabus_refs") or ()),
                }
            )
        return items

    def record_reflection_note_opaque(
        self, student_id: str, *, session_id: str, note: str
    ) -> dict[str, Any]:
        record = self._persistence.load(session_id=session_id) or {}
        text = (note or "").strip()
        if text:
            self._emit_candidate(
                RuntimeEvidenceType.REFLECTION_SUBMITTED,
                student_id=student_id,
                session_id=session_id,
                record=record,
                stage="reflection",
                payload={"note_length": len(text)},
            )
        else:
            self._emit_candidate(
                RuntimeEvidenceType.REFLECTION_SKIPPED,
                student_id=student_id,
                session_id=session_id,
                record=record,
                stage="reflection",
            )
        return {
            "recorded": True,
            "student_id": student_id,
            "session_id": session_id,
            "authority": "learning_session_runtime",
            # Structured note stays on the session record — Journal is REF-001.
            "journal_written": False,
            "twin_updated": False,
            "evidence_emitted": self._evidence_gate_enabled(),
        }

    def _substance_overview_fields(
        self,
        *,
        student_id: str,
        session_id: str,
        topic: str,
        substance_on: bool,
    ) -> tuple[tuple[str, ...], int, str]:
        if not substance_on:
            return (), 3, "incomplete"
        objectives = self._learning_objectives_from_sequence(
            student_id=student_id, session_id=session_id
        )
        seq = self._persistence.store.get(
            "activity.sequence", f"{student_id.strip()}::{session_id.strip()}"
        )
        activity_count = 3
        if isinstance(seq, dict) and seq.get("activities"):
            activity_count = max(1, len(seq.get("activities") or ()))
            if not objectives:
                objectives = tuple(
                    str(item.get("text") or "")
                    for item in (seq.get("learning_objectives") or ())
                    if str(item.get("text") or "").strip()
                )
        if not objectives:
            objectives = (f"Strengthen understanding of {topic}",)
        return objectives, activity_count, "package"

    def _learning_objectives_from_sequence(
        self, *, student_id: str, session_id: str
    ) -> tuple[str, ...]:
        seq = self._persistence.store.get(
            "activity.sequence", f"{student_id.strip()}::{session_id.strip()}"
        )
        if not isinstance(seq, dict):
            return ()
        labels: list[str] = []
        for item in seq.get("learning_objectives") or ():
            text = str(item.get("text") or "").strip()
            if not text:
                continue
            code = str(item.get("code") or "").strip()
            labels.append(
                format_learning_objective_label(code=code, text=text)
            )
        return tuple(labels)

    def _emit_candidate(
        self,
        type_id: RuntimeEvidenceType,
        *,
        student_id: str,
        session_id: str,
        record: dict[str, Any],
        stage: str = "",
        activity_id: str = "",
        payload: dict[str, Any] | None = None,
    ) -> CandidateObservation | None:
        """Emit a Generated candidate via LearningSessionRuntime builder."""
        if not self._evidence_gate_enabled():
            return None
        obs = self._evidence_gate.builder.emit(
            type_id=type_id,
            student_id=student_id,
            session_id=session_id,
            topic_id=str(record.get("topic_id") or ""),
            mission_instance_id=str(record.get("mission_instance_id") or ""),
            stage=stage,
            activity_id=activity_id,
            payload=payload,
        )
        self._persistence.append_candidate(
            session_id=session_id, observation=obs.to_opaque()
        )
        return obs

    def _emit_finish_review_candidate(
        self,
        *,
        student_id: str,
        session_id: str,
        record: dict[str, Any],
        verdict: str,
        notes: str | None,
    ) -> None:
        if not self._evidence_gate_enabled():
            return
        obs = self._evidence_gate.builder.observation_for_finish_review(
            verdict=verdict,
            student_id=student_id,
            session_id=session_id,
            topic_id=str(record.get("topic_id") or ""),
            mission_instance_id=str(record.get("mission_instance_id") or ""),
            notes=notes,
        )
        self._persistence.append_candidate(
            session_id=session_id, observation=obs.to_opaque()
        )

    def _stage_for_activity(
        self, *, student_id: str, session_id: str, activity_id: str
    ) -> str:
        seq = self._persistence.store.get(
            "activity.sequence", f"{student_id.strip()}::{session_id.strip()}"
        )
        if isinstance(seq, dict):
            for item in seq.get("activities") or ():
                if str(item.get("activity_id") or "") == activity_id.strip():
                    return str(item.get("stage") or "practice")
            # Fall back to current index stage.
            index = int(seq.get("index") or 1) - 1
            activities = list(seq.get("activities") or ())
            if 0 <= index < len(activities):
                return str(activities[index].get("stage") or "practice")
        # Checklist / legacy fallback by activity id prefix.
        aid = activity_id.strip().lower()
        if "read" in aid:
            return "read"
        if "example" in aid:
            return "worked_example"
        if "reflect" in aid:
            return "reflection"
        return "practice"

    def _run_evidence_gate(
        self,
        *,
        student_id: str,
        session_id: str,
        record: dict[str, Any],
        finish_verdict: str | None,
        finish_notes: str | None,
    ):
        """Build + validate + persist package; raise if session may not close."""
        raw_items = self._persistence.load_candidates(session_id=session_id)
        observations: list[CandidateObservation] = []
        for item in raw_items:
            obs = CandidateObservation.from_opaque(item)
            if obs is not None:
                observations.append(obs)
        objectives = self._learning_objectives_from_sequence(
            student_id=student_id, session_id=session_id
        )
        package = self._evidence_gate.build_and_validate(
            student_id=student_id,
            session_id=session_id,
            observations=observations,
            mission_instance_id=str(record.get("mission_instance_id") or ""),
            topic_id=str(record.get("topic_id") or ""),
            topic_title=str(record.get("topic_title") or ""),
            curriculum_identity=str(record.get("curriculum_identity") or ""),
            learning_objectives=objectives,
            finish_review_verdict=finish_verdict,
            finish_review_notes=finish_notes,
            session_metadata={
                "estimated_minutes": record.get("estimated_minutes"),
                "phase": record.get("phase"),
            },
        )
        package = self._evidence_gate.assert_session_may_complete(package)
        package = self._evidence_gate.mark_persisted(package)
        self._persistence.save_evidence_package(
            session_id=session_id, package=package.to_opaque()
        )
        return package

    def _consume_twin_evidence(self, evidence_package: Any) -> dict[str, Any]:
        """Apply Accepted Educational+ package to Twin when P5 flag is ON.

        Twin observes only. It never evaluates evidence and never advances
        Progress. Fail-open: Twin failures must not unwind session completion.
        """
        try:
            result = self._twin_consumer.consume(evidence_package)
            return result.to_opaque()
        except Exception as exc:  # noqa: BLE001 — Twin must not break session UX
            logger.warning(
                "sdt004_twin_consume_failed_open err=%s",
                exc,
            )
            return {
                "twin_updated": False,
                "reason": "twin_consume_failed_open",
                "authority": "student_digital_twin",
                "evidence_authority": "educational_evidence_authority",
            }

    def _complete_mission_if_authorised(
        self,
        *,
        student_id: str,
        mission_instance_id: str,
        advance_progress: bool,
        package_id: str,
        evidence_disposition: str | None = None,
        may_complete_mission: bool | None = None,
    ) -> bool:
        """Complete Runtime C mission when Authority authorises it.

        SR-003: Progress Engine authorises coverage when singularity is ON.
        Progress advancement is independent of Twin consumption (SDT-004).
        """
        mid = (mission_instance_id or "").strip()
        if not mid:
            return False
        completer = self._mission_completer
        if completer is None:
            try:
                from app.application.educational_runtime_engine.service import (
                    EducationalRuntimeEngineService,
                )

                completer = EducationalRuntimeEngineService()
            except Exception:  # noqa: BLE001 — fail-open for unit tests without DB
                logger.warning(
                    "evidence_gate_mission_completer_unavailable package=%s",
                    package_id,
                )
                return False
        try:
            user_id = int(student_id)
        except (TypeError, ValueError):
            logger.warning(
                "evidence_gate_non_numeric_student_id student=%s package=%s",
                student_id,
                package_id,
            )
            return False
        try:
            if hasattr(completer, "complete_mission"):
                kwargs: dict[str, Any] = {
                    "user_id": user_id,
                    "mission_instance_id": mid,
                    "advance_progress": advance_progress,
                    "evidence_package_id": package_id,
                }
                if self._progress_engine.singularity_enabled():
                    kwargs["evidence_disposition"] = evidence_disposition
                    kwargs["may_complete_mission"] = may_complete_mission
                completer.complete_mission(**kwargs)
            else:
                return False
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "evidence_gate_mission_complete_failed mission=%s err=%s",
                mid,
                exc,
            )
            return False
        return True

    def _study_progress_opaque(
        self,
        *,
        twin_result: dict[str, Any] | None,
        topic_id: str | None,
        curriculum_identity: str | None,
    ) -> dict[str, Any] | None:
        """Attach Progress Engine Study Progress when singularity is ON.

        Fail-open: absence of enrolment / curriculum must not unwind session UX.
        Twin estimates are optional projection annotations only.
        """
        twin = TwinEstimateInput.from_opaque(twin_result)
        try:
            from app.application.educational_runtime_engine.service import (
                EducationalRuntimeEngineService,
            )
            from app.models.educational_runtime_engine import RuntimeEnrolment

            identity = (curriculum_identity or "").strip()
            if not identity:
                return {
                    "authority": "progress_engine",
                    "twin_estimates_applied": twin.is_present(),
                    "current_topic_id": topic_id,
                    "reason": "curriculum_identity_unavailable",
                }
            enrolment = RuntimeEnrolment.query.filter_by(
                curriculum_identity=identity
            ).first()
            if enrolment is None:
                return {
                    "authority": "progress_engine",
                    "twin_estimates_applied": twin.is_present(),
                    "current_topic_id": topic_id,
                    "curriculum_identity": identity,
                    "reason": "enrolment_unavailable_for_projection",
                }
            engine = EducationalRuntimeEngineService(
                progress_engine=self._progress_engine
            )
            study = engine.get_study_progress(
                user_id=enrolment.user_id,
                subject_code=enrolment.subject_code,
                twin_estimates=twin,
            )
            return study.to_opaque()
        except Exception as exc:  # noqa: BLE001 — Progress projection fail-open
            logger.warning(
                "sr003_study_progress_projection_failed_open err=%s",
                exc,
            )
            return {
                "authority": "progress_engine",
                "twin_estimates_applied": twin.is_present(),
                "current_topic_id": topic_id,
                "reason": "study_progress_projection_failed_open",
            }


def _educational_package_id_from_sequence(seq: dict[str, Any] | None) -> str:
    """Recover sitting package id from activity sequence (RO1-R1)."""
    if not isinstance(seq, dict):
        return ""
    direct = str(seq.get("educational_package_id") or "").strip()
    if direct:
        return direct
    for raw in seq.get("activities") or ():
        if not isinstance(raw, dict):
            continue
        pid = str(raw.get("package_id") or "").strip()
        if pid:
            return pid
    for obj in seq.get("learning_objectives") or ():
        if isinstance(obj, dict):
            oid = str(obj.get("objective_id") or "").strip()
        else:
            oid = str(obj or "").strip()
        if ":lo" in oid:
            return oid.split(":lo", 1)[0].strip()
        if ":sc-" in oid:
            return oid.split(":sc-", 1)[0].strip()
    return ""
