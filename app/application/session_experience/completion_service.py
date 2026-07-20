"""CompletionService — session summary and return-home workflow."""

from __future__ import annotations

from typing import Any

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


class CompletionService:
    """Project Session Summary / Complete and finish the study workflow.

    Does not compute readiness or recommendations — consumes Twin /
    Adaptive / Runtime opaque facts only.
    """

    def __init__(
        self,
        *,
        session_runtime: SessionRuntimePort | None = None,
        student_twin: StudentTwinPort | None = None,
        adaptive_decision: AdaptiveDecisionPort | None = None,
        registry: SessionExperienceRegistry | None = None,
    ) -> None:
        self._runtime = session_runtime
        self._twin = student_twin
        self._adaptive = adaptive_decision
        self._registry = registry

    def summary(
        self, student_id: str, *, session_id: str
    ) -> CompletionSnapshot:
        """Build the Session Summary projection."""
        return self._project(student_id, session_id=session_id, complete=False)

    def complete(
        self, student_id: str, *, session_id: str
    ) -> CompletionSnapshot:
        """Request educational close via Runtime and project Complete."""
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        runtime = self._require_runtime()
        runtime.complete_session(sid, session_id=sess)
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
        return self._project(sid, session_id=sess, complete=True)

    def _project(
        self, student_id: str, *, session_id: str, complete: bool
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
