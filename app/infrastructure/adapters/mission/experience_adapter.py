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
        mission_read: Any | None = None,
        mission_start: Any | None = None,
        mission_resume: Any | None = None,
        session_completion: Any | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
        on_session_started: Any | None = None,
    ) -> None:
        self._store = store or ExperienceProjectionStore()
        self._engine = mission_engine
        self._mission_read = mission_read
        self._mission_start = mission_start
        self._mission_resume = mission_resume
        self._session_completion = session_completion
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        # Bridge path must never auto-provision demo mission documents.
        self._auto_provision = (
            bool(auto_provision)
            and mission_read is None
            and mission_start is None
            and mission_resume is None
            and session_completion is None
        )
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
        if self._mission_read is not None:
            return self._read_via_bridge(student_id)
        doc = self._load(student_id)
        if doc is None:
            return None
        session = doc.get("todays_session")
        return None if session is None else dict(session)

    def _read_via_bridge(self, student_id: str) -> dict[str, Any] | None:
        """Mission Read Bridge path — Runtime A only; never seeded_demo_*."""
        sid = student_id.strip()
        bridge = self._mission_read
        if hasattr(bridge, "get_todays_session"):
            result = bridge.get_todays_session(sid)
            # BridgeResult envelope
            if hasattr(result, "ok"):
                if not result.ok:
                    return None
                value = result.value
                if isinstance(value, dict):
                    self._cache_bridged_session(sid, value)
                    return dict(value)
                return None
            if isinstance(result, dict):
                self._cache_bridged_session(sid, result)
                return dict(result)
            return None
        if hasattr(bridge, "get_todays_session_opaque"):
            projected = bridge.get_todays_session_opaque(sid)
            if isinstance(projected, dict):
                self._cache_bridged_session(sid, projected)
                return dict(projected)
            return None
        return None

    def _cache_bridged_session(
        self, student_id: str, session: dict[str, Any]
    ) -> None:
        """Store bridged projection as UX cache (not educational authority)."""
        payload = {
            "student_id": student_id,
            "todays_session": dict(session),
            "sessions": {
                str(session.get("session_id") or session.get("mission_id") or ""): dict(
                    session
                )
            },
            "authority": "planning_service",
            "next_action_authority": False,
        }
        self._store.save(self._store.mission, student_id, payload)

    def start_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Start Today's Session via Mission delivery; run learning-loop hook."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        if self._mission_start is not None:
            return self._start_via_bridge(
                student_id, mission_id=mission_id, session_id=session_id
            )
        sid = student_id.strip()
        doc = self._load(sid) or default_mission_document(sid)
        today = dict(doc.get("todays_session") or {})
        resolved_mission = mission_id or today.get("mission_id") or f"mission:{sid}"
        resolved_session = (
            session_id or today.get("session_id") or f"sess-{uuid4().hex[:12]}"
        )
        started_at = datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
        defaults = self._default_start_result(
            sid,
            mission_id=resolved_mission,
            session_id=resolved_session,
            topic_title=str(today.get("topic_title") or ""),
            estimated_minutes=today.get("estimated_minutes"),
            started_at=started_at,
        )
        result = dict(defaults)
        if self._engine is not None and hasattr(self._engine, "start_opaque"):
            started = self._engine.start_opaque(
                sid, mission_id=resolved_mission, session_id=resolved_session
            )
            if isinstance(started, dict):
                # Opaque engines may omit Experience identity keys (e.g.
                # experience_session_id). Keep required defaults, overlay the rest.
                result = self._normalize_start_result(defaults, started)

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

        self._emit_session_started(sid, result)

        if self._on_session_started is not None:
            self._on_session_started(sid, result)

        return result

    def _start_via_bridge(
        self,
        student_id: str,
        *,
        mission_id: str | None,
        session_id: str | None,
    ) -> dict[str, Any]:
        """Mission Start Bridge path — Runtime A only; never seeded_demo_*."""
        from app.application.student_experience.exceptions import (
            StudentExperienceError,
        )

        sid = student_id.strip()
        bridge = self._mission_start
        result = bridge.start_session(
            sid, mission_id=mission_id, session_id=session_id
        )
        if hasattr(result, "ok"):
            if not result.ok or result.value is None:
                code = getattr(result, "error_code", None) or "UNAVAILABLE"
                message = getattr(result, "message", None) or (
                    "Mission Start Bridge could not start today's session"
                )
                raise StudentExperienceError(f"{code}: {message}")
            started = dict(result.value)
        elif isinstance(result, dict):
            started = dict(result)
        else:
            raise StudentExperienceError(
                "UNAVAILABLE: Mission Start Bridge returned no session"
            )

        self._cache_bridged_start(sid, started)
        self._emit_session_started(sid, started)
        if self._on_session_started is not None:
            self._on_session_started(sid, started)
        return started

    def _cache_bridged_start(
        self, student_id: str, started: dict[str, Any]
    ) -> None:
        """Cache bridged start projection as UX state (not educational SoT)."""
        session_key = str(
            started.get("session_id") or started.get("mission_id") or ""
        )
        experience_key = str(
            started.get("experience_session_id") or f"es-{session_key}"
        )
        today = {
            "student_id": student_id,
            "mission_id": started.get("mission_id"),
            "session_id": started.get("session_id"),
            "topic_title": started.get("topic_title") or "",
            "estimated_minutes": started.get("estimated_minutes"),
            "status": "in_progress",
            "authority": started.get("authority") or "study_session_service",
            "next_action_authority": False,
        }
        payload = {
            "student_id": student_id,
            "todays_session": dict(today),
            "sessions": {session_key: dict(started)} if session_key else {},
            "authority": "study_session_service",
            "next_action_authority": False,
        }
        self._store.save(self._store.mission, student_id, payload)
        if experience_key:
            self._store.save(
                self._store.sessions,
                experience_key,
                {
                    "experience_session_id": experience_key,
                    "student_id": student_id,
                    **started,
                },
            )

    def _emit_session_started(
        self, student_id: str, result: dict[str, Any]
    ) -> None:
        ids = CorrelationContext.current()
        self._events.publish(
            learning_session_started(
                {
                    "student_id": student_id,
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
                    "learner_id": student_id,
                    "status": "in_progress",
                    "authority": result.get("authority") or "mission_engine",
                    "next_action_authority": False,
                },
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
    def complete_session(
        self,
        student_id: str,
        *,
        session_id: str,
        topic_title: str = "",
        estimated_minutes: int | None = None,
        outcome: dict[str, Any] | None = None,
        mission_id: str | None = None,
    ) -> dict[str, Any]:
        """Mark a session complete and emit LearningSessionCompleted."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        if self._session_completion is not None:
            return self._complete_via_bridge(
                student_id,
                session_id=session_id,
                topic_title=topic_title,
                estimated_minutes=estimated_minutes,
                outcome=outcome,
                mission_id=mission_id,
            )
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

    def _complete_via_bridge(
        self,
        student_id: str,
        *,
        session_id: str,
        topic_title: str,
        estimated_minutes: int | None,
        outcome: dict[str, Any] | None,
        mission_id: str | None,
    ) -> dict[str, Any]:
        """Session Completion Bridge path — Runtime A only; never seeded_demo_*."""
        from app.application.student_experience.exceptions import (
            StudentExperienceError,
        )

        sid = student_id.strip()
        bridge = self._session_completion
        result = bridge.complete_session(
            sid,
            session_id=session_id,
            mission_id=mission_id,
            outcome=outcome,
            topic_title=topic_title,
            estimated_minutes=estimated_minutes,
        )
        if hasattr(result, "ok"):
            if not result.ok or result.value is None:
                code = getattr(result, "error_code", None) or "UNAVAILABLE"
                message = getattr(result, "message", None) or (
                    "Session Completion Bridge could not complete the session"
                )
                raise StudentExperienceError(f"{code}: {message}")
            completed = dict(result.value)
        elif isinstance(result, dict):
            completed = dict(result)
        else:
            raise StudentExperienceError(
                "UNAVAILABLE: Session Completion Bridge returned no session"
            )

        self._cache_bridged_completion(sid, completed)
        ids = CorrelationContext.current()
        self._events.publish(
            learning_session_completed(
                {
                    "student_id": sid,
                    "session_id": completed.get("session_id"),
                    "mission_id": completed.get("mission_id"),
                    "topic_title": completed.get("topic_title"),
                    "estimated_minutes": completed.get("estimated_minutes"),
                    "completed_at": completed.get("completed_at"),
                    "educational_complete": completed.get("educational_complete"),
                    "evidence_accepted": completed.get("evidence_accepted"),
                },
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
        self._events.publish(
            mission_updated(
                {
                    "mission_id": completed.get("mission_id"),
                    "learner_id": sid,
                    "status": "completed",
                    "authority": completed.get("authority")
                    or "study_session_service",
                    "next_action_authority": False,
                },
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
        return completed

    def _cache_bridged_completion(
        self, student_id: str, completed: dict[str, Any]
    ) -> None:
        """Cache bridged completion projection as UX state (not educational SoT)."""
        session_key = str(
            completed.get("session_id") or completed.get("mission_id") or ""
        )
        experience_key = str(
            completed.get("experience_session_id") or f"es-{session_key}"
        )
        today = {
            "student_id": student_id,
            "mission_id": completed.get("mission_id"),
            "session_id": completed.get("session_id"),
            "topic_title": completed.get("topic_title") or "",
            "estimated_minutes": completed.get("estimated_minutes"),
            "status": "completed",
            "tasks": list(completed.get("tasks") or []),
            "authority": completed.get("authority") or "study_session_service",
            "next_action_authority": False,
            "educational_complete": completed.get("educational_complete", True),
            "evidence_accepted": completed.get("evidence_accepted", False),
        }
        payload = {
            "student_id": student_id,
            "todays_session": dict(today),
            "sessions": {session_key: dict(completed)} if session_key else {},
            "authority": "study_session_service",
            "next_action_authority": False,
        }
        self._store.save(self._store.mission, student_id, payload)
        if experience_key:
            self._store.save(
                self._store.sessions,
                experience_key,
                {
                    "experience_session_id": experience_key,
                    "student_id": student_id,
                    **completed,
                },
            )
    def get_session_status(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        if self._mission_resume is not None:
            return self._resume_status_via_bridge(student_id, session_id=session_id)
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

    def resume_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Resume an active study session via Mission Resume Bridge or cache."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        if self._mission_resume is not None:
            return self._resume_via_bridge(
                student_id, mission_id=mission_id, session_id=session_id
            )
        sid = student_id.strip()
        if session_id:
            status = self.get_session_status(sid, session_id=session_id)
            if status is not None and str(status.get("status") or "") == "in_progress":
                return dict(status)
        today = self.get_todays_session(sid) or {}
        if str(today.get("status") or "") == "in_progress":
            return dict(today)
        from app.application.student_experience.exceptions import (
            StudentExperienceError,
        )

        raise StudentExperienceError(
            "NOT_FOUND: no active in-progress session to resume"
        )

    def _resume_via_bridge(
        self,
        student_id: str,
        *,
        mission_id: str | None,
        session_id: str | None,
    ) -> dict[str, Any]:
        """Mission Resume Bridge path — Runtime A only; never seeded_demo_*."""
        from app.application.student_experience.exceptions import (
            StudentExperienceError,
        )

        sid = student_id.strip()
        bridge = self._mission_resume
        result = bridge.resume_session(
            sid, mission_id=mission_id, session_id=session_id
        )
        if hasattr(result, "ok"):
            if not result.ok or result.value is None:
                code = getattr(result, "error_code", None) or "UNAVAILABLE"
                message = getattr(result, "message", None) or (
                    "Mission Resume Bridge could not resume the active session"
                )
                raise StudentExperienceError(f"{code}: {message}")
            resumed = dict(result.value)
        elif isinstance(result, dict):
            resumed = dict(result)
        else:
            raise StudentExperienceError(
                "UNAVAILABLE: Mission Resume Bridge returned no session"
            )

        self._cache_bridged_resume(sid, resumed)
        return resumed

    def _resume_status_via_bridge(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Status lookup through Mission Resume Bridge (fail closed → None)."""
        sid = student_id.strip()
        bridge = self._mission_resume
        if hasattr(bridge, "get_session_status"):
            result = bridge.get_session_status(sid, session_id=session_id)
        else:
            result = bridge.resume_session(sid, session_id=session_id)
        if hasattr(result, "ok"):
            if not result.ok:
                return None
            value = result.value
            if isinstance(value, dict):
                self._cache_bridged_resume(sid, value)
                return dict(value)
            return None
        if isinstance(result, dict):
            self._cache_bridged_resume(sid, result)
            return dict(result)
        return None

    def _cache_bridged_resume(
        self, student_id: str, resumed: dict[str, Any]
    ) -> None:
        """Cache bridged resume projection as UX state (not educational SoT)."""
        session_key = str(
            resumed.get("session_id") or resumed.get("mission_id") or ""
        )
        experience_key = str(
            resumed.get("experience_session_id") or f"es-{session_key}"
        )
        today = {
            "student_id": student_id,
            "mission_id": resumed.get("mission_id"),
            "session_id": resumed.get("session_id"),
            "topic_title": resumed.get("topic_title") or "",
            "estimated_minutes": resumed.get("estimated_minutes"),
            "status": resumed.get("status") or "in_progress",
            "tasks": list(resumed.get("tasks") or []),
            "authority": resumed.get("authority") or "study_session_service",
            "next_action_authority": False,
            "resumed": True,
        }
        payload = {
            "student_id": student_id,
            "todays_session": dict(today),
            "sessions": {session_key: dict(resumed)} if session_key else {},
            "authority": "study_session_service",
            "next_action_authority": False,
        }
        self._store.save(self._store.mission, student_id, payload)
        if experience_key:
            self._store.save(
                self._store.sessions,
                experience_key,
                {
                    "experience_session_id": experience_key,
                    "student_id": student_id,
                    **resumed,
                },
            )

    def _load(self, student_id: str) -> dict[str, Any] | None:
        sid = student_id.strip()
        # Mission Read Bridge owns get_todays_session; do not use opaque engine
        # or demo auto-provision on the bridged read path.
        if self._mission_read is not None:
            return None
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

    @staticmethod
    def _normalize_start_result(
        defaults: dict[str, Any], opaque: dict[str, Any]
    ) -> dict[str, Any]:
        """Merge opaque engine output with Experience-required start fields.

        MissionOpaqueBridge (and similar) return session/mission ids without
        ``experience_session_id``. Home → Start Session previously KeyError'd
        on that missing key when engines were injected.
        """
        merged = dict(defaults)
        for key, value in opaque.items():
            if value is None:
                continue
            if key == "experience_session_id" and not str(value).strip():
                continue
            merged[key] = value
        session_id = str(merged.get("session_id") or defaults["session_id"])
        merged["session_id"] = session_id
        merged["mission_id"] = str(
            merged.get("mission_id") or defaults["mission_id"]
        )
        if not str(merged.get("experience_session_id") or "").strip():
            merged["experience_session_id"] = f"es-{session_id}"
        merged["student_id"] = str(
            merged.get("student_id") or defaults["student_id"]
        )
        if not merged.get("status"):
            merged["status"] = "in_progress"
        if not merged.get("started_at"):
            merged["started_at"] = defaults["started_at"]
        if not merged.get("topic_title"):
            merged["topic_title"] = defaults.get("topic_title") or ""
        if merged.get("estimated_minutes") is None:
            merged["estimated_minutes"] = defaults.get("estimated_minutes")
        return merged
