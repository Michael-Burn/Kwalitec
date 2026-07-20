"""SessionService — overview projection and begin-session workflow."""

from __future__ import annotations

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
from app.domain.session_experience.learning_session import (
    BeginSessionAction,
    LearningSession,
    LearningSessionStatus,
)
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    SessionWorkspace,
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
        self._registry.put_workspace(workspace)
        self._registry.put_session(session)
        return overview_snapshot(session)

    def overview(self, student_id: str, *, session_id: str) -> OverviewSnapshot:
        """Return the Session Overview projection."""
        sid = _require_id(student_id, "student_id")
        sess = _require_id(session_id, "session_id")
        cached = self._registry.get_session(sess)
        if cached is not None and cached.student_id == sid:
            return overview_snapshot(cached)
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
                workspace.navigate_to(SessionSurface.ACTIVITY)
            )
        return overview_snapshot(updated)

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
