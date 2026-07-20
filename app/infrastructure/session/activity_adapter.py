"""SessionActivityAdapter — ActivityEnginePort for Learning Session Experience."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.session.defaults import (
    default_activity,
    default_activity_progress,
)
from app.infrastructure.session.store import SessionDocumentStore


class SessionActivityAdapter:
    """Production adapter implementing Session Experience ActivityEnginePort.

    Translates activity sequence state into opaque activity documents and
    optionally delegates to an injected activity engine. Never scores answers
    or invents mastery.
    """

    ADAPTER_ID = "session_activity"
    ADAPTER_VERSION = "1.0.0"
    NS_SEQUENCE = "activity.sequence"
    NS_CURRENT = "activity.current"

    def __init__(
        self,
        *,
        store: SessionDocumentStore | None = None,
        activity_engine: Any | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
        activity_count: int = 3,
    ) -> None:
        self._store = store or SessionDocumentStore()
        self._engine = activity_engine
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._auto_provision = auto_provision
        self._activity_count = max(1, int(activity_count))
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

    def put_sequence(
        self, student_id: str, *, session_id: str, document: dict[str, Any]
    ) -> None:
        """Provision opaque activity sequence state for a session."""
        payload = deepcopy(document)
        payload["student_id"] = student_id.strip()
        payload["session_id"] = session_id.strip()
        payload.setdefault("authority", "learning_activity_engine")
        self._store.save(self.NS_SEQUENCE, self._key(student_id, session_id), payload)

    def get_current_activity(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "get_current_activity_opaque"
        ):
            projected = self._engine.get_current_activity_opaque(
                sid, session_id=sess
            )
            if isinstance(projected, dict):
                self._store.save(self.NS_CURRENT, self._key(sid, sess), projected)
                return deepcopy(projected)
        seq = self._ensure_sequence(sid, sess)
        index = int(seq.get("index") or 1)
        total = int(seq.get("total") or self._activity_count)
        if index > total:
            return None
        activity = default_activity(sid, session_id=sess, index=index, total=total)
        self._store.save(self.NS_CURRENT, self._key(sid, sess), activity)
        return deepcopy(activity)

    def submit_response(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "submit_response_opaque"
        ):
            submitted = self._engine.submit_response_opaque(
                sid,
                session_id=sess,
                activity_id=activity_id,
                response=response,
            )
            if isinstance(submitted, dict):
                return dict(submitted)
        seq = self._ensure_sequence(sid, sess)
        index = int(seq.get("index") or 1)
        total = int(seq.get("total") or self._activity_count)
        result = {
            "activity_id": activity_id,
            "explanation": (
                "Review the worked example and compare it with your reasoning."
            ),
            "phase": "explained",
            "activity_index": index,
            "activities_total": total,
            "question": f"Question {index}",
            "next_action_label": "Continue",
            "authority": "learning_activity_engine",
        }
        current = self.get_current_activity(sid, session_id=sess) or {}
        merged = {**current, **result}
        self._store.save(self.NS_CURRENT, self._key(sid, sess), merged)
        return result

    def advance_activity(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "advance_activity_opaque"
        ):
            advanced = self._engine.advance_activity_opaque(sid, session_id=sess)
            if advanced is None:
                return None
            if isinstance(advanced, dict):
                self._store.save(self.NS_CURRENT, self._key(sid, sess), advanced)
                return deepcopy(advanced)
        seq = self._ensure_sequence(sid, sess)
        index = int(seq.get("index") or 1)
        total = int(seq.get("total") or self._activity_count)
        if index >= total:
            seq["index"] = total + 1
            seq["completed"] = total
            self.put_sequence(sid, session_id=sess, document=seq)
            return None
        seq["index"] = index + 1
        seq["completed"] = index
        self.put_sequence(sid, session_id=sess, document=seq)
        return self.get_current_activity(sid, session_id=sess)

    def get_activity_progress(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "get_activity_progress_opaque"
        ):
            projected = self._engine.get_activity_progress_opaque(
                sid, session_id=sess
            )
            if isinstance(projected, dict):
                return deepcopy(projected)
        seq = self._ensure_sequence(sid, sess)
        completed = int(seq.get("completed") or 0)
        total = int(seq.get("total") or self._activity_count)
        return default_activity_progress(
            sid, session_id=sess, completed=completed, total=total
        )

    def _ensure_sequence(self, student_id: str, session_id: str) -> dict[str, Any]:
        key = self._key(student_id, session_id)
        doc = self._store.get(self.NS_SEQUENCE, key)
        if doc is None:
            if not self._auto_provision:
                return {
                    "student_id": student_id,
                    "session_id": session_id,
                    "index": 1,
                    "completed": 0,
                    "total": self._activity_count,
                }
            doc = {
                "student_id": student_id,
                "session_id": session_id,
                "index": 1,
                "completed": 0,
                "total": self._activity_count,
                "authority": "learning_activity_engine",
            }
            self._store.save(self.NS_SEQUENCE, key, doc)
        return deepcopy(doc)

    @staticmethod
    def _key(student_id: str, session_id: str) -> str:
        return f"{student_id.strip()}::{session_id.strip()}"
