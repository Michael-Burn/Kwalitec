"""CompletionService — session summary, finish review, and return-home workflow.

LXP-003 / SR-001A P2: Finish Review (Yes / Partially / No) is required on the
product path before session close. Never completes a mission (P4 owns that).
"""

from __future__ import annotations

from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.session_experience._registry import SessionExperienceRegistry
from app.application.session_experience._snapshots import completion_snapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
)
from app.application.session_experience.exceptions import (
    CompletionError,
    PortUnavailable,
)
from app.application.session_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.session_experience.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.application.session_experience.ports.student_twin_port import StudentTwinPort
from app.domain.session_experience.completion_projection import (
    CompletionProjection,
    ReturnHomeAction,
)
from app.domain.session_experience.learning_session import LearningSessionStatus
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    SessionWorkspaceStatus,
)

_VALID_VERDICTS = frozenset({"yes", "partially", "no"})


class CompletionService:
    """Project Session Summary / Complete and finish the study workflow.

    Does not compute readiness or recommendations — consumes Twin /
    Adaptive / Runtime opaque facts only. Does not complete missions.
    """

    def __init__(
        self,
        *,
        session_runtime: SessionRuntimePort | None = None,
        student_twin: StudentTwinPort | None = None,
        adaptive_decision: AdaptiveDecisionPort | None = None,
        registry: SessionExperienceRegistry | None = None,
        require_finish_review: bool | None = None,
    ) -> None:
        self._runtime = session_runtime
        self._twin = student_twin
        self._adaptive = adaptive_decision
        self._registry = registry
        self._require_finish_review = require_finish_review

    def summary(
        self, student_id: str, *, session_id: str
    ) -> CompletionSnapshot:
        """Build the Session Summary / Finish Review projection."""
        return self._project(student_id, session_id=session_id, complete=False)

    def request_finish(
        self, student_id: str, *, session_id: str
    ) -> CompletionSnapshot:
        """Enter Ready to Finish and project the Finish Review surface."""
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        runtime = self._require_runtime()
        if hasattr(runtime, "request_finish"):
            runtime.request_finish(sid, session_id=sess)
        if self._registry is not None:
            workspace = self._registry.get_workspace_for_session(sess)
            if workspace is not None:
                self._registry.put_workspace(
                    workspace.navigate_to(SessionSurface.SUMMARY)
                )
            if hasattr(runtime, "save_surface"):
                runtime.save_surface(sid, session_id=sess, surface="summary")
        return self._project(sid, session_id=sess, complete=False)

    def complete(
        self,
        student_id: str,
        *,
        session_id: str,
        finish_verdict: str | None = None,
        finish_notes: str | None = None,
    ) -> CompletionSnapshot:
        """Close the session via Runtime after optional/required Finish Review.

        EV-001B: when the evidence gate authorises mission completion, Runtime
        may set ``mission_completed=True``. Twin remains read-only.
        """
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        runtime = self._require_runtime()
        require_review = self._finish_review_required()
        verdict = (finish_verdict or "").strip().lower() or None
        if require_review and verdict not in _VALID_VERDICTS:
            raise CompletionError(
                "Finish Review requires Yes, Partially, or No before "
                "session completion"
            )
        result = runtime.complete_session(
            sid,
            session_id=sess,
            finish_verdict=verdict,
            finish_notes=finish_notes,
        )
        if isinstance(result, dict) and result.get("error") == "finish_review_required":
            raise CompletionError(
                "Finish Review (Yes / Partially / No) is required before "
                "session completion"
            )
        if isinstance(result, dict) and result.get("error") == "evidence_gate_rejected":
            raise CompletionError(
                str(
                    result.get("message")
                    or "Educational evidence was not accepted for this sitting"
                )
            )
        if self._registry is not None:
            handle = self._registry.get_session(sess)
            if handle is not None:
                self._registry.put_session(
                    handle.with_status(LearningSessionStatus.COMPLETED)
                )
            workspace = self._registry.get_workspace_for_session(sess)
            if workspace is not None:
                self._registry.put_workspace(
                    workspace.navigate_to(SessionSurface.COMPLETE).with_status(
                        SessionWorkspaceStatus.CLOSED
                    )
                )
        return self._project(
            sid,
            session_id=sess,
            complete=True,
            runtime_result=result if isinstance(result, dict) else None,
        )

    def _finish_review_required(self) -> bool:
        if self._require_finish_review is not None:
            return bool(self._require_finish_review)
        return bool(resolve_v2_feature_flags().SR_SESSION_COMPLETION_PRODUCT)

    def _project(
        self,
        student_id: str,
        *,
        session_id: str,
        complete: bool,
        runtime_result: dict[str, Any] | None = None,
    ) -> CompletionSnapshot:
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        runtime = self._require_runtime()
        opaque = runtime.get_completion_summary(sid, session_id=sess) or {}
        twin_doc = {}
        if self._twin is not None and self._twin.is_available():
            twin_doc = self._twin.get_learning_insights(sid) or {}
        recommendation = ""
        next_minutes = None
        if self._adaptive is not None and self._adaptive.is_available():
            rec = self._adaptive.get_todays_recommendation(sid) or {}
            recommendation = str(
                rec.get("title") or rec.get("topic_title") or rec.get("summary") or ""
            )
            next_minutes = _optional_int(rec.get("estimated_minutes"))
        topics_raw = opaque.get("topics_completed") or opaque.get("topics") or ()
        if isinstance(topics_raw, str):
            topics = (topics_raw,)
        else:
            topics = tuple(str(t) for t in topics_raw)
        insights_raw = (
            opaque.get("learning_insights")
            or twin_doc.get("recent_insights")
            or ()
        )
        if isinstance(insights_raw, str):
            insights = (insights_raw,)
        else:
            insights = tuple(str(i) for i in insights_raw)
        review = opaque.get("finish_review")
        metadata: list[tuple[str, str]] = []
        if isinstance(review, dict) and review.get("verdict"):
            metadata.append(("finish_review", str(review.get("verdict"))))
            if review.get("label"):
                metadata.append(("finish_review_label", str(review.get("label"))))
        metadata.append(
            (
                "finish_review_required",
                "true" if self._finish_review_required() and not complete else "false",
            )
        )
        mission_done = bool(opaque.get("mission_completed"))
        progress_done = bool(opaque.get("progress_advanced"))
        if isinstance(runtime_result, dict):
            mission_done = bool(runtime_result.get("mission_completed"))
            progress_done = bool(runtime_result.get("progress_advanced"))
            if runtime_result.get("evidence_disposition"):
                metadata.append(
                    (
                        "evidence_disposition",
                        str(runtime_result.get("evidence_disposition")),
                    )
                )
            if runtime_result.get("message") and runtime_result.get("error"):
                insights = (str(runtime_result.get("message")),) + insights
        elif opaque.get("evidence_disposition"):
            metadata.append(
                ("evidence_disposition", str(opaque.get("evidence_disposition")))
            )
        metadata.append(
            ("mission_completed", "true" if mission_done else "false")
        )
        metadata.append(
            ("progress_advanced", "true" if progress_done else "false")
        )
        twin_updated = bool(opaque.get("twin_updated"))
        if isinstance(runtime_result, dict):
            twin_updated = bool(runtime_result.get("twin_updated"))
        metadata.append(("twin_updated", "true" if twin_updated else "false"))
        # KWP-005 — carry opaque sitting facts for presentation Sitting Report.
        if opaque.get("topic_title"):
            metadata.append(("topic_title", str(opaque.get("topic_title"))))
        for objective in opaque.get("learning_objectives") or ():
            text = str(objective).strip()
            if text:
                metadata.append(("learning_objective", text))
        for ref in opaque.get("syllabus_refs") or ():
            text = str(ref).strip()
            if text:
                metadata.append(("syllabus_ref", text))
        for activity in opaque.get("activities") or ():
            if not isinstance(activity, dict):
                continue
            title = str(activity.get("title") or "").strip()
            stage = str(activity.get("stage") or "").strip()
            done = "1" if activity.get("completed") else "0"
            if title or stage:
                metadata.append(
                    (
                        "activity_item",
                        f"{stage}|{title}|{done}",
                    )
                )
        for obs in opaque.get("observations") or ():
            if isinstance(obs, dict) and obs.get("type_id"):
                metadata.append(("observation_type", str(obs.get("type_id"))))
        # KWP-011 — flatten frozen Sitting Report intelligence into metadata.
        snap_raw = opaque.get("intelligence_snapshot")
        if isinstance(runtime_result, dict) and isinstance(
            runtime_result.get("intelligence_snapshot"), dict
        ):
            snap_raw = runtime_result.get("intelligence_snapshot")
        if isinstance(snap_raw, dict) and snap_raw:
            from app.application.educational_memory.dto import IntelligenceSnapshot
            from app.application.educational_memory.service import (
                EducationalMemoryService,
            )

            snap = IntelligenceSnapshot.from_opaque(snap_raw)
            if snap is not None and snap.has_student_report:
                metadata.extend(
                    EducationalMemoryService.metadata_pairs_for_snapshot(snap)
                )
        try:
            domain = CompletionProjection.create(
                sess,
                sid,
                topics_completed=topics,
                time_studied_minutes=_optional_int(
                    opaque.get("time_studied_minutes")
                    or opaque.get("duration_minutes")
                ),
                activities_completed=int(opaque.get("activities_completed") or 0),
                learning_insights=insights,
                exam_readiness_change=_optional_float(
                    opaque.get("exam_readiness_change")
                    or opaque.get("readiness_delta")
                ),
                exam_readiness_change_label=str(
                    opaque.get("exam_readiness_change_label") or ""
                ),
                next_recommendation=recommendation
                or str(opaque.get("next_recommendation") or ""),
                estimated_next_session_minutes=next_minutes
                or _optional_int(opaque.get("estimated_next_session_minutes")),
                return_home=ReturnHomeAction.create(enabled=True),
                metadata=metadata,
            )
        except ValueError as exc:
            raise CompletionError(str(exc)) from exc
        if complete and self._registry is not None:
            workspace = self._registry.get_workspace_for_session(sess)
            if workspace is not None and not workspace.is_on(SessionSurface.COMPLETE):
                self._registry.put_workspace(
                    workspace.navigate_to(SessionSurface.COMPLETE)
                )
        elif self._registry is not None:
            workspace = self._registry.get_workspace_for_session(sess)
            if workspace is not None and not workspace.is_on(SessionSurface.SUMMARY):
                self._registry.put_workspace(
                    workspace.navigate_to(SessionSurface.SUMMARY)
                )
        return completion_snapshot(domain)

    def _require_runtime(self) -> SessionRuntimePort:
        if self._runtime is None or not self._runtime.is_available():
            raise PortUnavailable("session_runtime port unavailable")
        return self._runtime


def _require_id(value: str, field: str = "student_id") -> str:
    if not isinstance(value, str) or not value.strip():
        raise CompletionError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)
