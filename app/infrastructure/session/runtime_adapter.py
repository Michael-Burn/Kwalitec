"""SessionRuntimeAdapter — SessionRuntimePort for Learning Session Experience."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.session.defaults import (
    default_completion_summary,
    default_reflection,
    default_runtime_snapshot,
    default_session_overview,
)
from app.infrastructure.session.store import SessionDocumentStore


class SessionRuntimeAdapter:
    """Production adapter implementing Session Experience SessionRuntimePort.

    Translates student/session identity into opaque runtime documents and
    optionally delegates to an injected runtime engine. Never computes
    educational closure law.
    """

    ADAPTER_ID = "session_runtime"
    ADAPTER_VERSION = "1.0.0"
    NS_OVERVIEW = "runtime.overview"
    NS_SNAPSHOT = "runtime.snapshot"
    NS_REFLECTION = "runtime.reflection"
    NS_COMPLETION = "runtime.completion"
    NS_STATUS = "runtime.status"

    def __init__(
        self,
        *,
        store: SessionDocumentStore | None = None,
        runtime_engine: Any | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
    ) -> None:
        self._store = store or SessionDocumentStore()
        self._engine = runtime_engine
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._auto_provision = auto_provision
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

    def put_overview(
        self, student_id: str, *, session_id: str, document: dict[str, Any]
    ) -> None:
        """Provision opaque overview facts for a session."""
        payload = deepcopy(document)
        payload["student_id"] = student_id.strip()
        payload["session_id"] = session_id.strip()
        payload.setdefault("authority", "learning_session_runtime")
        self._store.save(self.NS_OVERVIEW, self._key(student_id, session_id), payload)

    def get_session_overview(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        if self._engine is not None and hasattr(
            self._engine, "get_session_overview_opaque"
        ):
            projected = self._engine.get_session_overview_opaque(
                student_id.strip(), session_id=session_id.strip()
            )
            if isinstance(projected, dict):
                self.put_overview(
                    student_id, session_id=session_id, document=projected
                )
                return deepcopy(projected)
        return self._load_or_provision(
            self.NS_OVERVIEW,
            student_id,
            session_id,
            default_session_overview,
        )

    def begin_session(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(self._engine, "begin_session_opaque"):
            started = self._engine.begin_session_opaque(sid, session_id=sess)
            if isinstance(started, dict):
                result = dict(started)
                self._store.save(self.NS_STATUS, self._key(sid, sess), result)
                return result
        overview = self.get_session_overview(sid, session_id=sess) or {}
        result = {
            "session_id": sess,
            "student_id": sid,
            "mission_id": overview.get("mission_id"),
            "status": "in_progress",
            "authority": "learning_session_runtime",
        }
        overview = {**overview, "status": "in_progress"}
        self.put_overview(sid, session_id=sess, document=overview)
        self._store.save(self.NS_STATUS, self._key(sid, sess), result)
        snapshot = default_runtime_snapshot(sid, session_id=sess)
        snapshot["current_topic"] = (
            (overview.get("topics") or ("Core methods",))[0]
            if overview.get("topics")
            else "Core methods"
        )
        self._store.save(self.NS_SNAPSHOT, self._key(sid, sess), snapshot)
        return result

    def get_runtime_snapshot(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        if self._engine is not None and hasattr(
            self._engine, "get_runtime_snapshot_opaque"
        ):
            projected = self._engine.get_runtime_snapshot_opaque(
                student_id.strip(), session_id=session_id.strip()
            )
            if isinstance(projected, dict):
                self._store.save(
                    self.NS_SNAPSHOT,
                    self._key(student_id, session_id),
                    projected,
                )
                return deepcopy(projected)
        return self._load_or_provision(
            self.NS_SNAPSHOT,
            student_id,
            session_id,
            default_runtime_snapshot,
        )

    def record_response(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        """Hand response to the educational kernel; return opaque acknowledgement.

        Evidence ownership remains outside Session Experience. This adapter
        only forwards / records a structural acknowledgement.
        """
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "record_response_opaque"
        ):
            recorded = self._engine.record_response_opaque(
                sid,
                session_id=sess,
                activity_id=activity_id,
                response=response,
            )
            if isinstance(recorded, dict):
                return dict(recorded)
        return {
            "recorded": True,
            "student_id": sid,
            "session_id": sess,
            "activity_id": activity_id,
            "authority": "learning_session_runtime",
        }

    def complete_session(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "complete_session_opaque"
        ):
            completed = self._engine.complete_session_opaque(sid, session_id=sess)
            if isinstance(completed, dict):
                self._store.save(self.NS_STATUS, self._key(sid, sess), completed)
                return dict(completed)
        result = {
            "session_id": sess,
            "student_id": sid,
            "status": "completed",
            "authority": "learning_session_runtime",
        }
        overview = self.get_session_overview(sid, session_id=sess) or {}
        overview = {**overview, "status": "completed"}
        self.put_overview(sid, session_id=sess, document=overview)
        self._store.save(self.NS_STATUS, self._key(sid, sess), result)
        completion = default_completion_summary(sid, session_id=sess)
        topics = overview.get("topics") or ("Core methods",)
        completion["topics_completed"] = tuple(topics)
        self._store.save(self.NS_COMPLETION, self._key(sid, sess), completion)
        return result

    def get_reflection(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        if self._engine is not None and hasattr(self._engine, "get_reflection_opaque"):
            projected = self._engine.get_reflection_opaque(
                student_id.strip(), session_id=session_id.strip()
            )
            if isinstance(projected, dict):
                self._store.save(
                    self.NS_REFLECTION,
                    self._key(student_id, session_id),
                    projected,
                )
                return deepcopy(projected)
        return self._load_or_provision(
            self.NS_REFLECTION,
            student_id,
            session_id,
            default_reflection,
        )

    def get_completion_summary(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        if self._engine is not None and hasattr(
            self._engine, "get_completion_summary_opaque"
        ):
            projected = self._engine.get_completion_summary_opaque(
                student_id.strip(), session_id=session_id.strip()
            )
            if isinstance(projected, dict):
                self._store.save(
                    self.NS_COMPLETION,
                    self._key(student_id, session_id),
                    projected,
                )
                return deepcopy(projected)
        return self._load_or_provision(
            self.NS_COMPLETION,
            student_id,
            session_id,
            default_completion_summary,
        )

    def _load_or_provision(
        self,
        namespace: str,
        student_id: str,
        session_id: str,
        factory,
    ) -> dict[str, Any] | None:
        key = self._key(student_id, session_id)
        doc = self._store.get(namespace, key)
        if doc is None and self._auto_provision:
            doc = factory(student_id.strip(), session_id=session_id.strip())
            self._store.save(namespace, key, doc)
        return None if doc is None else deepcopy(doc)

    @staticmethod
    def _key(student_id: str, session_id: str) -> str:
        return f"{student_id.strip()}::{session_id.strip()}"
