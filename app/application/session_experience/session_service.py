"""SessionService — overview projection and begin-session workflow."""

from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from app.application.session_experience._registry import SessionExperienceRegistry
from app.application.session_experience._snapshots import overview_snapshot
from app.application.session_experience.dto.overview_snapshot import OverviewSnapshot
from app.application.session_experience.exceptions import (
    OverviewError,
    PortUnavailable,
    SessionNotFound,
)
from app.application.session_experience.ports.mission_port import MissionPort
from app.application.session_experience.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    format_learning_objective_label,
)
from app.domain.session_experience.learning_session import (
    BeginSessionAction,
    LearningSession,
    LearningSessionStatus,
)
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    SessionWorkspace,
    SessionWorkspaceStatus,
)


class SessionService:
    """Project Session Overview and open the focused study workspace.

    Projection / workflow only. No educational ownership.
    """

    def __init__(
        self,
        *,
        session_runtime: SessionRuntimePort | None = None,
        mission: MissionPort | None = None,
        registry: SessionExperienceRegistry | None = None,
    ) -> None:
        self._runtime = session_runtime
        self._mission = mission
        self._registry = registry or SessionExperienceRegistry()

    @property
    def registry(self) -> SessionExperienceRegistry:
        return self._registry

    def open_session(
        self,
        student_id: str,
        *,
        session_id: str | None = None,
        mission_id: str | None = None,
        workspace_id: str | None = None,
    ) -> OverviewSnapshot:
        """Open (or rehydrate) a Learning Session at the Overview surface."""
        sid = _require_id(student_id, "student_id")
        resolved_session_id = self._resolve_session_id(
            sid, session_id=session_id, mission_id=mission_id
        )
        runtime = self._require_runtime()
        opaque = runtime.get_session_overview(sid, session_id=resolved_session_id) or {}
        mission_doc = self._mission_doc(sid, resolved_session_id)
        try:
            session = _build_learning_session(
                sid,
                resolved_session_id,
                opaque,
                mission_doc,
                mission_id=mission_id,
            )
        except ValueError as exc:
            raise OverviewError(str(exc)) from exc

        workspace = SessionWorkspace.create(
            workspace_id or f"sw-{uuid4().hex[:12]}",
            sid,
            resolved_session_id,
            active_surface=SessionSurface.OVERVIEW,
            topic_title=(session.topics[0] if session.topics else session.objective),
        )
        # LXP-003 recovery: restore persisted surface only for in-progress sessions.
        status = str(opaque.get("status") or "").strip().lower()
        if status in {"in_progress", "paused", "ready_to_finish"} and hasattr(
            runtime, "get_runtime_snapshot"
        ):
            snap = (
                runtime.get_runtime_snapshot(sid, session_id=resolved_session_id)
                or {}
            )
            surface_raw = str(snap.get("active_surface") or "").strip().lower()
            if surface_raw and surface_raw != SessionSurface.OVERVIEW.value:
                try:
                    restored = SessionSurface(surface_raw)
                    if restored is not SessionSurface.COMPLETE:
                        workspace = workspace.navigate_to(restored)
                    if snap.get("paused") or status == "paused":
                        workspace = workspace.with_status(
                            SessionWorkspaceStatus.PAUSED
                        )
                except ValueError:
                    pass
        self._registry.put_workspace(workspace)
        self._registry.put_session(session)
        return _overview_with_substance(overview_snapshot(session), opaque)

    def overview(self, student_id: str, *, session_id: str) -> OverviewSnapshot:
        """Return the Session Overview projection."""
        sid = _require_id(student_id, "student_id")
        sess = _require_id(session_id, "session_id")
        runtime = self._require_runtime()
        opaque = runtime.get_session_overview(sid, session_id=sess) or {}
        cached = self._registry.get_session(sess)
        if cached is not None and cached.student_id == sid:
            return _overview_with_substance(overview_snapshot(cached), opaque)
        return self.open_session(sid, session_id=sess)

    def begin(
        self, student_id: str, *, session_id: str
    ) -> OverviewSnapshot:
        """Begin the session via Runtime and advance workspace to Activity."""
        sid = _require_id(student_id, "student_id")
        sess = _require_id(session_id, "session_id")
        runtime = self._require_runtime()
        runtime.begin_session(sid, session_id=sess)
        handle = self._registry.get_session(sess)
        if handle is None:
            self.open_session(sid, session_id=sess)
            handle = self._registry.get_session(sess)
        if handle is None:
            raise SessionNotFound(f"session not found: {sess}")
        updated = handle.with_status(LearningSessionStatus.IN_PROGRESS)
        self._registry.put_session(updated)
        workspace = self._registry.get_workspace_for_session(sess)
        if workspace is not None:
            self._registry.put_workspace(
                workspace.navigate_to(SessionSurface.ACTIVITY).with_status(
                    SessionWorkspaceStatus.ACTIVE
                )
            )
        if hasattr(runtime, "save_surface"):
            runtime.save_surface(sid, session_id=sess, surface="activity")
        return overview_snapshot(updated)

    def pause(self, student_id: str, *, session_id: str) -> OverviewSnapshot:
        """Pause an in-progress session (safe leave)."""
        sid = _require_id(student_id, "student_id")
        sess = _require_id(session_id, "session_id")
        runtime = self._require_runtime()
        if hasattr(runtime, "pause_session"):
            runtime.pause_session(sid, session_id=sess)
        workspace = self._registry.get_workspace_for_session(sess)
        if workspace is not None:
            self._registry.put_workspace(
                workspace.with_status(SessionWorkspaceStatus.PAUSED)
            )
            if hasattr(runtime, "save_surface"):
                runtime.save_surface(
                    sid,
                    session_id=sess,
                    surface=workspace.active_surface.value,
                )
        handle = self._registry.get_session(sess)
        if handle is None:
            return self.open_session(sid, session_id=sess)
        return overview_snapshot(handle)

    def resume(self, student_id: str, *, session_id: str) -> OverviewSnapshot:
        """Resume a paused session at the persisted surface."""
        sid = _require_id(student_id, "student_id")
        sess = _require_id(session_id, "session_id")
        runtime = self._require_runtime()
        surface = "activity"
        if hasattr(runtime, "resume_session"):
            result = runtime.resume_session(sid, session_id=sess) or {}
            surface = str(result.get("active_surface") or surface)
        workspace = self._registry.get_workspace_for_session(sess)
        if workspace is None:
            self.open_session(sid, session_id=sess)
            workspace = self._registry.get_workspace_for_session(sess)
        if workspace is not None:
            try:
                target = SessionSurface(surface)
            except ValueError:
                target = SessionSurface.ACTIVITY
            self._registry.put_workspace(
                workspace.navigate_to(target).with_status(
                    SessionWorkspaceStatus.ACTIVE
                )
            )
        handle = self._registry.get_session(sess)
        if handle is None:
            return self.open_session(sid, session_id=sess)
        return overview_snapshot(handle)

    def update_checklist(
        self,
        student_id: str,
        *,
        session_id: str,
        item_id: str,
        done: bool,
    ) -> OverviewSnapshot:
        """Toggle a plan-checklist item (presentation progress only)."""
        sid = _require_id(student_id, "student_id")
        sess = _require_id(session_id, "session_id")
        runtime = self._require_runtime()
        if hasattr(runtime, "update_checklist"):
            runtime.update_checklist(
                sid, session_id=sess, item_id=item_id, done=done
            )
        return self.overview(sid, session_id=sess)

    def _resolve_session_id(
        self,
        student_id: str,
        *,
        session_id: str | None,
        mission_id: str | None,
    ) -> str:
        if session_id and str(session_id).strip():
            return str(session_id).strip()
        if self._mission is not None and self._mission.is_available():
            today = self._mission.get_todays_session(student_id) or {}
            candidate = today.get("session_id")
            if candidate:
                return str(candidate).strip()
            if mission_id and today.get("mission_id") == mission_id:
                raise OverviewError(
                    "mission resolved but session_id missing from Mission port"
                )
        raise OverviewError("session_id is required to open a Learning Session")

    def _mission_doc(self, student_id: str, session_id: str) -> dict[str, Any]:
        if self._mission is None or not self._mission.is_available():
            return {}
        return (
            self._mission.get_session_status(student_id, session_id=session_id)
            or self._mission.get_todays_session(student_id)
            or {}
        )

    def _require_runtime(self) -> SessionRuntimePort:
        if self._runtime is None or not self._runtime.is_available():
            raise PortUnavailable("session_runtime port unavailable")
        return self._runtime


def _build_learning_session(
    student_id: str,
    session_id: str,
    opaque: dict[str, Any],
    mission_doc: dict[str, Any],
    *,
    mission_id: str | None,
) -> LearningSession:
    topics_raw = opaque.get("topics") or mission_doc.get("topics") or ()
    if isinstance(topics_raw, str):
        topics = (topics_raw,)
    else:
        topics = tuple(str(t) for t in topics_raw)
    mid = (
        mission_id
        or opaque.get("mission_id")
        or mission_doc.get("mission_id")
    )
    experience_id = str(
        opaque.get("experience_session_id") or f"es-{session_id}"
    )
    return LearningSession.create(
        experience_id,
        student_id,
        session_id,
        status=str(opaque.get("status") or LearningSessionStatus.OVERVIEW.value),
        mission_id=None if mid is None else str(mid),
        objective=str(
            opaque.get("objective")
            or opaque.get("todays_objective")
            or mission_doc.get("objective")
            or ""
        ),
        learning_goal=str(
            opaque.get("learning_goal") or mission_doc.get("learning_goal") or ""
        ),
        estimated_minutes=_optional_int(
            opaque.get("estimated_minutes")
            or opaque.get("estimated_duration_minutes")
            or mission_doc.get("estimated_minutes")
        ),
        activity_count=int(
            opaque.get("activity_count")
            or opaque.get("number_of_activities")
            or len(opaque.get("activities") or ())
            or 0
        ),
        topics=topics,
        expected_readiness_improvement=_optional_float(
            opaque.get("expected_readiness_improvement")
        ),
        why_studying=str(
            opaque.get("why_studying")
            or opaque.get("rationale")
            or opaque.get("why")
            or ""
        ),
        begin_action=BeginSessionAction.create(
            enabled=True,
            session_id=session_id,
            mission_id=None if mid is None else str(mid),
        ),
    )


def _overview_with_substance(
    snap: OverviewSnapshot, opaque: dict[str, Any]
) -> OverviewSnapshot:
    """Attach package-derived learning objectives when present on overview opaque."""
    raw = opaque.get("learning_objectives") or ()
    if isinstance(raw, str) and raw.strip():
        objectives = (raw.strip(),)
    else:
        labels: list[str] = []
        for item in raw:
            if isinstance(item, str) and item.strip():
                labels.append(item.strip())
                continue
            if isinstance(item, dict):
                text = str(item.get("text") or "").strip()
                if not text:
                    continue
                code = str(item.get("code") or "").strip()
                labels.append(
                    format_learning_objective_label(code=code, text=text)
                )
        objectives = tuple(labels)
    substance = str(opaque.get("substance") or "").strip()
    meta = list(snap.metadata)
    if substance:
        meta = [(k, v) for k, v in meta if k != "substance"]
        meta.append(("substance", substance))
    if not objectives and not substance:
        return snap
    return replace(
        snap,
        learning_objectives=objectives or snap.learning_objectives,
        metadata=tuple(meta),
    )


def _require_id(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OverviewError(f"{field_name} must be a non-empty string")
    return value.strip()


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)
