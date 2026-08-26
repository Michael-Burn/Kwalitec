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
            (overview.get("topics") or ("Today's topic",))[0]
            if overview.get("topics")
            else "Today's topic"
        )
        self._store.save(self.NS_SNAPSHOT, self._key(sid, sess), snapshot)
        return result

    def pause_session(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(self._engine, "pause_session_opaque"):
            paused = self._engine.pause_session_opaque(sid, session_id=sess)
            if isinstance(paused, dict):
                self._store.save(self.NS_STATUS, self._key(sid, sess), paused)
                return dict(paused)
        result = {
            "session_id": sess,
            "student_id": sid,
            "status": "paused",
            "authority": "learning_session_runtime",
        }
        self._store.save(self.NS_STATUS, self._key(sid, sess), result)
        return result

    def resume_session(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(self._engine, "resume_session_opaque"):
            resumed = self._engine.resume_session_opaque(sid, session_id=sess)
            if isinstance(resumed, dict):
                self._store.save(self.NS_STATUS, self._key(sid, sess), resumed)
                return dict(resumed)
        result = {
            "session_id": sess,
            "student_id": sid,
            "status": "in_progress",
            "authority": "learning_session_runtime",
        }
        self._store.save(self.NS_STATUS, self._key(sid, sess), result)
        return result

    def request_finish(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "request_finish_opaque"
        ):
            ready = self._engine.request_finish_opaque(sid, session_id=sess)
            if isinstance(ready, dict):
                self._store.save(self.NS_STATUS, self._key(sid, sess), ready)
                return dict(ready)
        result = {
            "session_id": sess,
            "student_id": sid,
            "status": "ready_to_finish",
            "finish_review_required": True,
            "authority": "learning_session_runtime",
        }
        self._store.save(self.NS_STATUS, self._key(sid, sess), result)
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
        scored_correct: bool | None = None,
        structured: bool = False,
        score_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Hand response to the educational kernel; return opaque acknowledgement.

        Evidence ownership remains outside Session Experience. This adapter
        only forwards / records a structural acknowledgement. Optional scoring
        facts come from the activity layer (KWP-004).
        """
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "record_response_opaque"
        ):
            try:
                recorded = self._engine.record_response_opaque(
                    sid,
                    session_id=sess,
                    activity_id=activity_id,
                    response=response,
                    scored_correct=scored_correct,
                    structured=structured,
                    score_payload=score_payload,
                )
            except TypeError:
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
            "scored_correct": scored_correct,
        }

    def update_checklist(
        self,
        student_id: str,
        *,
        session_id: str,
        item_id: str,
        done: bool,
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "update_checklist_opaque"
        ):
            updated = self._engine.update_checklist_opaque(
                sid, session_id=sess, item_id=item_id, done=done
            )
            if isinstance(updated, dict):
                return dict(updated)
        return {
            "session_id": sess,
            "student_id": sid,
            "item_id": item_id,
            "done": bool(done),
            "authority": "learning_session_runtime",
        }

    def save_surface(
        self,
        student_id: str,
        *,
        session_id: str,
        surface: str,
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(self._engine, "save_surface_opaque"):
            saved = self._engine.save_surface_opaque(
                sid, session_id=sess, surface=surface
            )
            if isinstance(saved, dict):
                return dict(saved)
        return {
            "session_id": sess,
            "student_id": sid,
            "active_surface": surface,
            "authority": "learning_session_runtime",
        }

    def complete_session(
        self,
        student_id: str,
        *,
        session_id: str,
        finish_verdict: str | None = None,
        finish_notes: str | None = None,
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "complete_session_opaque"
        ):
            completed = self._engine.complete_session_opaque(
                sid,
                session_id=sess,
                finish_verdict=finish_verdict,
                finish_notes=finish_notes,
            )
            if isinstance(completed, dict):
                self._store.save(self.NS_STATUS, self._key(sid, sess), completed)
                return dict(completed)
        result = {
            "session_id": sess,
            "student_id": sid,
            "status": "completed",
            "authority": "learning_session_runtime",
            "mission_completed": False,
            "finish_review": (
                {"verdict": finish_verdict, "notes": finish_notes or ""}
                if finish_verdict
                else None
            ),
        }
        overview = self.get_session_overview(sid, session_id=sess) or {}
        overview = {**overview, "status": "completed"}
        self.put_overview(sid, session_id=sess, document=overview)
        self._store.save(self.NS_STATUS, self._key(sid, sess), result)
        topic = _topic_from_overview(overview)
        completion = default_completion_summary(
            sid, session_id=sess, topic_title=topic
        )
        topics = overview.get("topics") or (topic,)
        if isinstance(topics, str):
            topics = (topics,)
        completion["topics_completed"] = tuple(str(t) for t in topics)
        if finish_verdict:
            completion["finish_review"] = {
                "verdict": finish_verdict,
                "notes": (finish_notes or "").strip(),
            }
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
        return self._load_or_provision_topic_aware(
            self.NS_REFLECTION,
            student_id,
            session_id,
            default_reflection,
        )

    def record_reflection_note(
        self, student_id: str, *, session_id: str, note: str
    ) -> dict[str, Any]:
        """Persist the student's free-text reflection note onto the session record.

        Stored under the same reflection document namespace (``NS_REFLECTION``)
        used by ``get_reflection`` — durable via ``SessionDocumentStore`` when
        ``ENABLE_DURABLE_STORE`` is on (production), process-local memory
        otherwise. Live engine path also writes ``reflection_note`` onto the
        Learning Session handle document. Never scores or interprets the note.
        """
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        sess = session_id.strip()
        cleaned = note.strip()
        if self._engine is not None and hasattr(
            self._engine, "record_reflection_note_opaque"
        ):
            recorded = self._engine.record_reflection_note_opaque(
                sid, session_id=sess, note=cleaned
            )
            if isinstance(recorded, dict):
                # Keep NS_REFLECTION aligned with engine handle persistence.
                overview = self.get_session_overview(sid, session_id=sess) or {}
                existing = (
                    self.get_reflection(sid, session_id=sess)
                    or default_reflection(
                        sid,
                        session_id=sess,
                        topic_title=_topic_from_overview(overview),
                    )
                )
                note_text = str(
                    recorded.get("student_note")
                    if recorded.get("student_note") is not None
                    else cleaned
                )
                updated = {**existing, "student_note": note_text}
                self._store.save(self.NS_REFLECTION, self._key(sid, sess), updated)
                return dict(recorded)
        overview = self.get_session_overview(sid, session_id=sess) or {}
        existing = self.get_reflection(sid, session_id=sess) or default_reflection(
            sid,
            session_id=sess,
            topic_title=_topic_from_overview(overview),
        )
        updated = {**existing, "student_note": cleaned}
        self._store.save(self.NS_REFLECTION, self._key(sid, sess), updated)
        return {
            "recorded": True,
            "student_id": sid,
            "session_id": sess,
            "authority": "learning_session_runtime",
        }

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
        return self._load_or_provision_topic_aware(
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

    def _load_or_provision_topic_aware(
        self,
        namespace: str,
        student_id: str,
        session_id: str,
        factory,
    ) -> dict[str, Any] | None:
        """Provision reflection/completion defaults with overview topic (CQ-004)."""
        key = self._key(student_id, session_id)
        doc = self._store.get(namespace, key)
        if doc is None and self._auto_provision:
            overview = self._store.get(self.NS_OVERVIEW, key) or {}
            topic = _topic_from_overview(overview)
            doc = factory(
                student_id.strip(),
                session_id=session_id.strip(),
                topic_title=topic,
            )
            self._store.save(namespace, key, doc)
        return None if doc is None else deepcopy(doc)

    @staticmethod
    def _key(student_id: str, session_id: str) -> str:
        return f"{student_id.strip()}::{session_id.strip()}"


def _topic_from_overview(overview: dict[str, Any]) -> str:
    topics = overview.get("topics") or ()
    if isinstance(topics, str) and topics.strip():
        return topics.strip()
    if topics:
        first = str(topics[0]).strip()
        if first:
            return first
    for key in ("topic_title", "objective"):
        value = str(overview.get(key) or "").strip()
        if value:
            return value
    return "Today's topic"
