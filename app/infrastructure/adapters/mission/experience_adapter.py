"""ExperienceMissionAdapter — MissionPort for Student Experience."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.infrastructure.adapters.student_experience.defaults import (
    default_mission_document,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    learning_session_completed,
    mission_updated,
)
from app.infrastructure.events.types.experience import learning_session_started


class ExperienceMissionAdapter:
    """Production adapter implementing Student Experience MissionPort.

    Delivers Today's Session. Does not invent next-action recommendations.
    """

    ADAPTER_ID = "experience_mission"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        store: ExperienceProjectionStore | None = None,
        mission_engine: Any | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
        on_session_started: Any | None = None,
    ) -> None:
        self._store = store or ExperienceProjectionStore()
        self._engine = mission_engine
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._auto_provision = auto_provision
        self._on_session_started = on_session_started
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    def put_projection(self, student_id: str, document: dict[str, Any]) -> None:
        """Persist an opaque Mission projection."""
        sid = student_id.strip()
        payload = deepcopy(document)
        payload["student_id"] = sid
        payload["authority"] = "mission_engine"
        payload["next_action_authority"] = False
        self._store.save(self._store.mission, sid, payload)

    def get_todays_session(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        session = doc.get("todays_session")
        return None if session is None else dict(session)

    def start_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Start Today's Session via Mission delivery; run learning-loop hook."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        doc = self._load(sid) or default_mission_document(sid)
        today = dict(doc.get("todays_session") or {})
        resolved_mission = mission_id or today.get("mission_id") or f"mission:{sid}"
        resolved_session = (
            session_id or today.get("session_id") or f"sess-{uuid4().hex[:12]}"
        )
        started_at = datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
        if self._engine is not None and hasattr(self._engine, "start_opaque"):
            started = self._engine.start_opaque(
                sid, mission_id=resolved_mission, session_id=resolved_session
            )
            if isinstance(started, dict):
                result = dict(started)
            else:
                result = self._default_start_result(
                    sid,
                    mission_id=resolved_mission,
                    session_id=resolved_session,
                    topic_title=str(today.get("topic_title") or ""),
                    estimated_minutes=today.get("estimated_minutes"),
                    started_at=started_at,
                )
        else:
            result = self._default_start_result(
                sid,
                mission_id=resolved_mission,
                session_id=resolved_session,
                topic_title=str(today.get("topic_title") or ""),
                estimated_minutes=today.get("estimated_minutes"),
                started_at=started_at,
            )

        sessions = dict(doc.get("sessions") or {})
        sessions[str(result["session_id"])] = dict(result)
        doc["todays_session"] = {
            **today,
            "mission_id": result["mission_id"],
            "session_id": result["session_id"],
            "topic_title": result.get("topic_title") or today.get("topic_title"),
            "estimated_minutes": result.get("estimated_minutes"),
            "status": "in_progress",
        }
        doc["sessions"] = sessions
        doc["authority"] = "mission_engine"
        doc["next_action_authority"] = False
        self._store.save(self._store.mission, sid, doc)
        self._store.save(
            self._store.sessions,
            str(result["experience_session_id"]),
            {
                "experience_session_id": result["experience_session_id"],
                "student_id": sid,
                **result,
            },
        )

        ids = CorrelationContext.current()
        self._events.publish(
            learning_session_started(
                {
                    "student_id": sid,
                    "mission_id": result["mission_id"],
                    "session_id": result["session_id"],
                    "experience_session_id": result["experience_session_id"],
                },
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
        self._events.publish(
            mission_updated(
                {
                    "mission_id": result["mission_id"],
                    "learner_id": sid,
                    "status": "in_progress",
                    "authority": "mission_engine",
                    "next_action_authority": False,
                },
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )

        if self._on_session_started is not None:
            self._on_session_started(sid, result)

        return result

    def complete_session(
        self,
        student_id: str,
        *,
        session_id: str,
        topic_title: str = "",
        estimated_minutes: int | None = None,
    ) -> dict[str, Any]:
        """Mark a session complete and emit LearningSessionCompleted."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        doc = self._load(sid) or default_mission_document(sid)
        sessions = dict(doc.get("sessions") or {})
        existing = dict(sessions.get(session_id) or {})
        completed_at = datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
        existing.update(
            {
                "session_id": session_id,
                "status": "completed",
                "completed_at": completed_at,
                "topic_title": topic_title or existing.get("topic_title") or "",
                "estimated_minutes": (
                    estimated_minutes
                    if estimated_minutes is not None
                    else existing.get("estimated_minutes")
                ),
            }
        )
        sessions[session_id] = existing
        today = dict(doc.get("todays_session") or {})
        if str(today.get("session_id") or "") == session_id:
            today["status"] = "completed"
            doc["todays_session"] = today
        doc["sessions"] = sessions
        self._store.save(self._store.mission, sid, doc)
        ids = CorrelationContext.current()
        payload = {
            "student_id": sid,
            "session_id": session_id,
            "mission_id": existing.get("mission_id"),
            "topic_title": existing.get("topic_title"),
            "estimated_minutes": existing.get("estimated_minutes"),
            "completed_at": completed_at,
        }
        self._events.publish(
            learning_session_completed(
                payload,
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
        return payload

    def get_session_status(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        sessions = doc.get("sessions") or {}
        status = sessions.get(session_id)
        if status is not None:
            return dict(status)
        today = doc.get("todays_session") or {}
        if str(today.get("session_id") or "") == session_id:
            return dict(today)
        return None

    def _load(self, student_id: str) -> dict[str, Any] | None:
        sid = student_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "get_todays_session_opaque"
        ):
            projected = self._engine.get_todays_session_opaque(sid)
            if isinstance(projected, dict):
                wrapped = default_mission_document(sid)
                wrapped["todays_session"] = projected
                self.put_projection(sid, wrapped)
                return deepcopy(wrapped)
        doc = self._store.get(self._store.mission, sid)
        if doc is None and self._auto_provision:
            doc = default_mission_document(sid)
            self._store.save(self._store.mission, sid, doc)
        return None if doc is None else deepcopy(doc)

    @staticmethod
    def _default_start_result(
        student_id: str,
        *,
        mission_id: str,
        session_id: str,
        topic_title: str,
        estimated_minutes: Any,
        started_at: str,
    ) -> dict[str, Any]:
        return {
            "experience_session_id": f"es-{session_id}",
            "mission_id": str(mission_id),
            "session_id": str(session_id),
            "topic_title": topic_title,
            "estimated_minutes": (
                None if estimated_minutes is None else int(estimated_minutes)
            ),
            "started_at": started_at,
            "status": "in_progress",
            "student_id": student_id,
        }
