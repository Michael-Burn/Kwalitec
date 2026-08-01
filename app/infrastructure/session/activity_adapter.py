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
    NS_OVERVIEW = "runtime.overview"

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
        topic = self._topic_for(sid, sess)
        why = self._why_for(sid, sess)
        if self._engine is not None and hasattr(
            self._engine, "get_current_activity_opaque"
        ):
            try:
                projected = self._engine.get_current_activity_opaque(
                    sid, session_id=sess, topic_title=topic
                )
            except TypeError:
                projected = self._engine.get_current_activity_opaque(
                    sid, session_id=sess
                )
            if isinstance(projected, dict):
                enriched = self._enrich_activity(
                    projected, topic=topic, why_studying=why
                )
                # Preserve post-answer explanation until the learner advances.
                # Package engines project the raw sequence item (no explanation);
                # without this merge, Submit Answer appears to succeed but the
                # activity surface never switches to Continue.
                enriched = self._merge_explained_state(
                    enriched,
                    self._store.get(self.NS_CURRENT, self._key(sid, sess)),
                )
                self._store.save(self.NS_CURRENT, self._key(sid, sess), enriched)
                return deepcopy(enriched)
        seq = self._ensure_sequence(sid, sess)
        index = int(seq.get("index") or 1)
        total = int(seq.get("total") or self._activity_count)
        if index > total:
            return None
        activity = default_activity(
            sid,
            session_id=sess,
            index=index,
            total=total,
            topic_title=topic,
            why_studying=why,
        )
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
        topic = self._topic_for(sid, sess)
        why = self._why_for(sid, sess)
        if self._engine is not None and hasattr(
            self._engine, "submit_response_opaque"
        ):
            try:
                submitted = self._engine.submit_response_opaque(
                    sid,
                    session_id=sess,
                    activity_id=activity_id,
                    response=response,
                    topic_title=topic,
                )
            except TypeError:
                submitted = self._engine.submit_response_opaque(
                    sid,
                    session_id=sess,
                    activity_id=activity_id,
                    response=response,
                )
            if isinstance(submitted, dict):
                enriched = self._enrich_activity(
                    dict(submitted), topic=topic, why_studying=why
                )
                prior = self._store.get(self.NS_CURRENT, self._key(sid, sess)) or {}
                if prior.get("activity_id") == enriched.get("activity_id"):
                    merged = {**prior, **enriched}
                else:
                    merged = enriched
                merged = self._merge_explained_state(merged, enriched)
                self._store.save(self.NS_CURRENT, self._key(sid, sess), merged)
                return deepcopy(merged)
        seq = self._ensure_sequence(sid, sess)
        index = int(seq.get("index") or 1)
        total = int(seq.get("total") or self._activity_count)
        is_final = index >= total
        result = {
            "activity_id": activity_id,
            "explanation": (
                f"Compare your reasoning with the worked example for {topic}. "
                "Note one idea you would keep and one you would adjust."
            ),
            "phase": "explained",
            "activity_index": index,
            "activities_total": total,
            "topic_title": topic,
            "next_action_label": (
                "Continue to Reflection" if is_final else "Continue"
            ),
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
                topic = self._topic_for(sid, sess)
                why = self._why_for(sid, sess)
                enriched = self._enrich_activity(
                    advanced, topic=topic, why_studying=why
                )
                self._store.save(self.NS_CURRENT, self._key(sid, sess), enriched)
                return deepcopy(enriched)
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
        topic = self._topic_for(sid, sess)
        if self._engine is not None and hasattr(
            self._engine, "get_activity_progress_opaque"
        ):
            projected = self._engine.get_activity_progress_opaque(
                sid, session_id=sess
            )
            if isinstance(projected, dict):
                if not projected.get("current_topic"):
                    projected = {**projected, "current_topic": topic}
                return deepcopy(projected)
        seq = self._ensure_sequence(sid, sess)
        completed = int(seq.get("completed") or 0)
        total = int(seq.get("total") or self._activity_count)
        return default_activity_progress(
            sid,
            session_id=sess,
            completed=completed,
            total=total,
            topic_title=topic,
        )

    def _topic_for(self, student_id: str, session_id: str) -> str:
        """Best-effort topic from runtime overview — fail-open to defaults."""
        overview = self._store.get(self.NS_OVERVIEW, self._key(student_id, session_id))
        if not isinstance(overview, dict):
            return "today's topic"
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
        return "today's topic"

    def _why_for(self, student_id: str, session_id: str) -> str:
        """Best-effort mission why from runtime overview — presentation only."""
        overview = self._store.get(self.NS_OVERVIEW, self._key(student_id, session_id))
        if not isinstance(overview, dict):
            return ""
        for key in ("why_studying", "rationale", "why"):
            value = str(overview.get(key) or "").strip()
            if value:
                return value
        return ""

    @staticmethod
    def _merge_explained_state(
        projected: dict[str, Any],
        existing: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Keep post-answer feedback on the same activity_id across reloads."""
        if not isinstance(existing, dict):
            return projected
        if existing.get("activity_id") != projected.get("activity_id"):
            return projected
        explained = bool(
            existing.get("explanation")
            or existing.get("feedback_outcome")
            or existing.get("model_answer")
            or str(existing.get("phase") or "").strip().lower() == "explained"
        )
        if not explained:
            return projected
        merged = dict(projected)
        for key in (
            "explanation",
            "phase",
            "feedback_outcome",
            "feedback_explanation",
            "model_answer",
            "common_mistake",
            "next_action",
            "next_action_label",
            "scored_correct",
            "emit_structured",
            "score_payload",
        ):
            value = existing.get(key)
            if value not in (None, "", (), [], {}):
                merged[key] = value
        return merged

    def _enrich_activity(
        self,
        opaque: dict[str, Any],
        *,
        topic: str,
        why_studying: str = "",
    ) -> dict[str, Any]:
        """Normalize bridge/default activity facts for learner-facing substance."""
        enriched = dict(opaque)
        index = int(
            enriched.get("activity_index")
            or enriched.get("index")
            or enriched.get("position")
            or 1
        )
        total = int(
            enriched.get("activities_total")
            or enriched.get("total")
            or self._activity_count
        )
        enriched.setdefault("activity_index", index)
        enriched.setdefault("activities_total", total)
        # Preserve package-derived substance — do not overwrite with Core methods.
        if str(enriched.get("substance") or "") == "package":
            enriched.setdefault("authority", "learning_activity_engine")
            if index >= total:
                enriched["next_action_label"] = str(
                    enriched.get("next_action_label") or "Continue to Reflection"
                )
            else:
                enriched.setdefault("next_action_label", "Continue")
            return enriched

        if not str(enriched.get("topic_title") or "").strip():
            enriched["topic_title"] = topic
        resolved_topic = str(enriched.get("topic_title") or topic).strip()
        why = (why_studying or "").strip()
        prompt = str(enriched.get("question") or enriched.get("prompt") or "").strip()
        if not prompt or prompt.lower().startswith("practice item"):
            seeded = default_activity(
                str(enriched.get("student_id") or ""),
                session_id=str(enriched.get("session_id") or ""),
                index=index,
                total=total,
                topic_title=resolved_topic,
                why_studying=why,
            )
            for key in (
                "question",
                "context",
                "supporting_material",
                "hints",
                "answer_prompt",
            ):
                if not str(enriched.get(key) or "").strip():
                    enriched[key] = seeded[key]
            if not prompt or prompt.lower().startswith("practice item"):
                enriched["question"] = seeded["question"]
                enriched["context"] = seeded["context"]
        # CQ-005: prefer mission-why context when overview already carries it.
        if why and (
            not str(enriched.get("context") or "").strip()
            or str(enriched.get("context") or "")
            .lower()
            .startswith("focused practice on")
        ):
            enriched["context"] = f"You're practising {resolved_topic} because {why}"
        explanation = enriched.get("explanation")
        if isinstance(explanation, dict):
            enriched["explanation"] = str(
                explanation.get("summary")
                or explanation.get("text")
                or explanation.get("body")
                or ""
            ).strip()
        if not str(enriched.get("explanation") or "").strip() and enriched.get(
            "submitted"
        ):
            enriched["explanation"] = (
                f"Compare your reasoning with the worked example for "
                f"{resolved_topic}. Note one idea you would keep and one "
                "you would adjust."
            )
        if index >= total:
            enriched["next_action_label"] = "Continue to Reflection"
        else:
            enriched.setdefault("next_action_label", "Continue")
        enriched.setdefault("authority", "learning_activity_engine")
        return enriched

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
