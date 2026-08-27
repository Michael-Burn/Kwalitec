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
            scored_raw = (result or {}).get("scored_correct")
            scored_correct: bool | None
            if scored_raw is True:
                scored_correct = True
            elif scored_raw is False:
                scored_correct = False
            else:
                scored_correct = None
            self._runtime.record_response(
                sid,
                session_id=sess,
                activity_id=aid,
                response=text,
                scored_correct=scored_correct,
                structured=bool((result or {}).get("emit_structured")),
                score_payload=dict((result or {}).get("score_payload") or {}),
            )
        current = engine.get_current_activity(sid, session_id=sess) or {}
        merged = {**current, **(result or {})}
        try:
            domain = _build_activity(
                sess,
                merged,
                phase=ActivityPhase.EXPLAINED
                if merged.get("explanation")
                or merged.get("feedback_outcome")
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
    activity_index = int(
        opaque.get("activity_index")
        or opaque.get("index")
        or opaque.get("position")
        or 1
    )
    activities_total = int(
        opaque.get("activities_total") or opaque.get("total") or 1
    )
    next_label = str(opaque.get("next_action_label") or "").strip()
    if not next_label:
        next_label = (
            "Continue to Reflection"
            if activity_index >= activities_total
            else "Continue"
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
        explanation=_explanation_text(opaque.get("explanation")),
        phase=resolved_phase,
        activity_index=activity_index,
        activities_total=activities_total,
        next_action_label=next_label,
        topic_title=str(opaque.get("topic_title") or opaque.get("topic") or ""),
        activity_type=str(
            opaque.get("activity_type") or opaque.get("stage") or ""
        ),
        stage_label=str(opaque.get("stage_label") or ""),
        feedback_outcome=str(opaque.get("feedback_outcome") or ""),
        model_answer=str(opaque.get("model_answer") or ""),
        common_mistake=str(opaque.get("common_mistake") or ""),
        next_action=str(
            opaque.get("next_action") or opaque.get("next_action_label") or ""
        ),
        scored_correct=_optional_bool(opaque.get("scored_correct")),
        response_type=str(opaque.get("response_type") or ""),
        choices=_parse_choices(opaque.get("choices")),
    )


def _parse_choices(raw: Any) -> tuple[tuple[str, str], ...]:
    """Normalise opaque choice payloads to (id, label) pairs."""
    if not raw:
        return ()
    pairs: list[tuple[str, str]] = []
    for item in raw:
        if isinstance(item, dict):
            cid = str(item.get("id") or "").strip()
            label = str(item.get("label") or "").strip()
            if cid and label:
                pairs.append((cid, label))
        elif isinstance(item, list | tuple) and len(item) >= 2:
            cid = str(item[0]).strip()
            label = str(item[1]).strip()
            if cid and label:
                pairs.append((cid, label))
    return tuple(pairs)


def _explanation_text(value: Any) -> str:
    """Coerce opaque explanation payloads to learner-facing string copy."""
    if value is None:
        return ""
    if isinstance(value, dict):
        for key in ("summary", "text", "body", "explanation"):
            text = str(value.get(key) or "").strip()
            if text:
                return text
        return ""
    return str(value).strip()


def _optional_bool(value: Any) -> bool | None:
    if value is True:
        return True
    if value is False:
        return False
    return None


def _require_id(value: str, field: str = "student_id") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ActivityError(f"{field} must be a non-empty string")
    return value.strip()
