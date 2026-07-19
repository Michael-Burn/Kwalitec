"""ExperienceTwinAdapter — StudentTwinPort for Student Experience."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.adapters.student_experience.defaults import (
    default_twin_document,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types.experience import profile_updated


class ExperienceTwinAdapter:
    """Production adapter implementing Student Experience StudentTwinPort.

    Reads opaque Twin projections from infrastructure stores / optional
    twin_engine. Never computes readiness or mastery.
    """

    ADAPTER_ID = "experience_student_twin"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        store: ExperienceProjectionStore | None = None,
        twin_engine: Any | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
    ) -> None:
        self._store = store or ExperienceProjectionStore()
        self._engine = twin_engine
        self._events = events or EventRegistry()
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

    def put_projection(self, student_id: str, document: dict[str, Any]) -> None:
        """Persist an opaque Twin projection (engine / composition write)."""
        sid = student_id.strip()
        payload = deepcopy(document)
        payload["student_id"] = sid
        payload.setdefault("authority", "student_twin")
        self._store.save(self._store.twin, sid, payload)

    def get_learner_summary(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        return {
            "display_name": doc.get("display_name") or "",
            "examination_label": doc.get("examination_label") or "",
            "exam_countdown_days": doc.get("exam_countdown_days"),
            "preferences": dict(doc.get("preferences") or {}),
            "goals": tuple(doc.get("goals") or ()),
            "account": dict(doc.get("account") or {}),
            "statistics": dict(doc.get("statistics") or {}),
        }

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        readiness = dict(doc.get("readiness") or {})
        if not readiness and doc.get("exam_readiness") is not None:
            readiness = {
                "examination_label": doc.get("examination_label") or "",
                "exam_countdown_days": doc.get("exam_countdown_days"),
                "exam_readiness": doc.get("exam_readiness"),
                "readiness_score": doc.get("exam_readiness"),
                "readiness_label": doc.get("readiness_label") or "",
            }
        return readiness or {
            "examination_label": doc.get("examination_label") or "",
            "exam_countdown_days": doc.get("exam_countdown_days"),
            "exam_readiness": (doc.get("statistics") or {}).get(
                "current_exam_readiness"
            ),
            "readiness_score": (doc.get("statistics") or {}).get(
                "current_exam_readiness"
            ),
            "readiness_label": "",
        }

    def get_learning_insights(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        insights = dict(doc.get("insights") or {})
        return insights or {
            "completed_sessions": (),
            "total_study_minutes": 0,
            "readiness_progression": (),
            "mastered_topics": (),
            "revision_history": (),
            "recent_achievements": (),
            "sessions_completed": 0,
            "topics_mastered": 0,
        }

    def apply_session_outcome(
        self,
        student_id: str,
        *,
        session_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Structurally append session evidence to Twin projection.

        Educational recalculation is delegated to twin_engine when present.
        """
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        doc = self._load(sid) or default_twin_document(sid)
        if self._engine is not None and hasattr(self._engine, "project_opaque"):
            projected = self._engine.project_opaque(doc, session_payload)
            if isinstance(projected, dict):
                doc.update(projected)
        else:
            insights = dict(doc.get("insights") or {})
            completed = list(insights.get("completed_sessions") or [])
            completed.append(
                {
                    "session_id": session_payload.get("session_id"),
                    "topic_title": session_payload.get("topic_title") or "",
                    "completed_at": session_payload.get("completed_at") or "",
                    "study_minutes": session_payload.get("estimated_minutes") or 0,
                }
            )
            insights["completed_sessions"] = tuple(completed[-50:])
            insights["total_study_minutes"] = int(
                insights.get("total_study_minutes") or 0
            ) + int(session_payload.get("estimated_minutes") or 0)
            insights["sessions_completed"] = int(
                insights.get("sessions_completed") or 0
            ) + 1
            stats = dict(doc.get("statistics") or {})
            stats["total_study_minutes"] = insights["total_study_minutes"]
            stats["sessions_completed"] = insights["sessions_completed"]
            doc["insights"] = insights
            doc["statistics"] = stats
            revision_history = list(insights.get("revision_history") or [])
            topic = str(session_payload.get("topic_title") or "").strip()
            if topic:
                revision_history.append(topic)
                insights["revision_history"] = tuple(revision_history[-50:])
                doc["insights"] = insights
        doc["authority"] = "student_twin"
        self._store.save(self._store.twin, sid, doc)
        ids = CorrelationContext.current()
        self._events.publish(
            profile_updated(
                {
                    "student_id": sid,
                    "component": self.ADAPTER_ID,
                    "sessions_completed": (doc.get("statistics") or {}).get(
                        "sessions_completed"
                    ),
                },
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
        return {"ok": True, "student_id": sid, "authority": "student_twin"}

    def _load(self, student_id: str) -> dict[str, Any] | None:
        sid = student_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "get_learner_summary_opaque"
        ):
            projected = self._engine.get_learner_summary_opaque(sid)
            if isinstance(projected, dict):
                self.put_projection(sid, projected)
                return deepcopy(projected)
        doc = self._store.get(self._store.twin, sid)
        if doc is None and self._auto_provision:
            doc = default_twin_document(sid)
            self._store.save(self._store.twin, sid, doc)
        return None if doc is None else deepcopy(doc)
