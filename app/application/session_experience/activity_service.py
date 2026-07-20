"""ActivityService — learning activity projection and response workflow."""

from __future__ import annotations

from typing import Any

from app.application.session_experience._registry import SessionExperienceRegistry
from app.application.session_experience._snapshots import activity_snapshot
from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.exceptions import (
    ActivityError,
    PortUnavailable,
)
from app.application.session_experience.ports.activity_engine_port import (
    ActivityEnginePort,
)
from app.application.session_experience.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.domain.session_experience.activity_projection import (
    ActivityPhase,
    ActivityProjection,
)
from app.domain.session_experience.session_workspace import SessionSurface


class ActivityService:
    """Project Learning Activities and route responses through ports.

    Presentation never owns evidence. Responses flow:
    Student Response → Activity Engine → Session Runtime (evidence) →
    Orchestrator / Twin / Adaptive (outside this package).
    """

    def __init__(
        self,
        *,
        activity_engine: ActivityEnginePort | None = None,
        session_runtime: SessionRuntimePort | None = None,
        registry: SessionExperienceRegistry | None = None,
    ) -> None:
        self._activity = activity_engine
        self._runtime = session_runtime
        self._registry = registry

    def current(
        self, student_id: str, *, session_id: str
    ) -> ActivitySnapshot:
        """Return the current activity projection."""
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        engine = self._require_activity()
        opaque = engine.get_current_activity(sid, session_id=sess)
        if not opaque:
            raise ActivityError("no current activity available")
        try:
            domain = _build_activity(sess, opaque)
        except ValueError as exc:
            raise ActivityError(str(exc)) from exc
        return activity_snapshot(domain)

    def submit_response(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> ActivitySnapshot:
        """Submit a learner response through Activity + Runtime ports."""
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        aid = _require_id(activity_id, field="activity_id")
        text = (response or "").strip()
        if not text:
            raise ActivityError("response must not be empty")
        engine = self._require_activity()
        result = engine.submit_response(
            sid, session_id=sess, activity_id=aid, response=text
        )
        if self._runtime is not None and self._runtime.is_available():
            self._runtime.record_response(
                sid, session_id=sess, activity_id=aid, response=text
            )
        current = engine.get_current_activity(sid, session_id=sess) or {}
        merged = {**current, **(result or {})}
        try:
            domain = _build_activity(
                sess,
                merged,
                phase=ActivityPhase.EXPLAINED
                if merged.get("explanation")
                else ActivityPhase.COMPLETED,
            )
        except ValueError as exc:
            raise ActivityError(str(exc)) from exc
        return activity_snapshot(domain)

    def advance(
        self, student_id: str, *, session_id: str
    ) -> ActivitySnapshot | None:
        """Advance to the next activity; None when sequence is finished."""
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        engine = self._require_activity()
        nxt = engine.advance_activity(sid, session_id=sess)
        if not nxt:
            if self._registry is not None:
                workspace = self._registry.get_workspace_for_session(sess)
                if workspace is not None:
                    self._registry.put_workspace(
                        workspace.navigate_to(SessionSurface.REFLECTION)
                    )
            return None
        try:
            domain = _build_activity(sess, nxt)
        except ValueError as exc:
            raise ActivityError(str(exc)) from exc
        return activity_snapshot(domain)

    def _require_activity(self) -> ActivityEnginePort:
        if self._activity is None or not self._activity.is_available():
            raise PortUnavailable("activity_engine port unavailable")
        return self._activity


def _build_activity(
    session_id: str,
    opaque: dict[str, Any],
    *,
    phase: ActivityPhase | None = None,
) -> ActivityProjection:
    hints_raw = opaque.get("hints") or ()
    if isinstance(hints_raw, str):
        hints = (hints_raw,)
    else:
        hints = tuple(str(h) for h in hints_raw)
    resolved_phase = phase
    if resolved_phase is None:
        resolved_phase = ActivityPhase(
            str(opaque.get("phase") or ActivityPhase.READY.value).lower()
        )
    return ActivityProjection.create(
        str(opaque.get("activity_id") or opaque.get("id") or "activity-1"),
        session_id,
        question=str(opaque.get("question") or opaque.get("prompt") or ""),
        context=str(opaque.get("context") or ""),
        supporting_material=str(
            opaque.get("supporting_material") or opaque.get("material") or ""
        ),
        hints=hints,
        answer_prompt=str(opaque.get("answer_prompt") or "Your answer"),
        explanation=str(opaque.get("explanation") or ""),
        phase=resolved_phase,
        activity_index=int(opaque.get("activity_index") or opaque.get("index") or 1),
        activities_total=int(
            opaque.get("activities_total") or opaque.get("total") or 1
        ),
        next_action_label=str(opaque.get("next_action_label") or "Continue"),
        topic_title=str(opaque.get("topic_title") or opaque.get("topic") or ""),
    )


def _require_id(value: str, field: str = "student_id") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ActivityError(f"{field} must be a non-empty string")
    return value.strip()
