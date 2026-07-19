"""ExperienceOrchestratorAdapter — LearningOrchestratorPort for Experience."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.adapters.student_experience.defaults import (
    default_activity_document,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.events.registry import EventRegistry


class ExperienceOrchestratorAdapter:
    """Production adapter implementing LearningOrchestratorPort.

    Observes learning activity status for presentation. Does not own
    pipeline order or educational decisions.
    """

    ADAPTER_ID = "experience_orchestrator"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        store: ExperienceProjectionStore | None = None,
        orchestrator: Any | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
    ) -> None:
        self._store = store or ExperienceProjectionStore()
        self._orchestrator = orchestrator
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
        """Persist an opaque activity projection."""
        sid = student_id.strip()
        payload = deepcopy(document)
        payload["student_id"] = sid
        payload.setdefault("authority", "learning_orchestrator")
        self._store.save(self._store.activity, sid, payload)

    def get_activity_status(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        return {
            "status": doc.get("status") or "idle",
            "status_label": doc.get("status_label") or "",
        }

    def acknowledge_activity(
        self, student_id: str, *, activity_id: str
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        doc = self._load(sid) or default_activity_document(sid)
        acknowledged = dict(doc.get("acknowledged") or {})
        acknowledged[activity_id] = True
        doc["acknowledged"] = acknowledged
        self._store.save(self._store.activity, sid, doc)
        return {"activity_id": activity_id, "acknowledged": True}

    def set_activity_status(
        self,
        student_id: str,
        *,
        status: str,
        status_label: str = "",
    ) -> dict[str, Any]:
        """Update activity status after orchestration cycles."""
        sid = student_id.strip()
        doc = self._load(sid) or default_activity_document(sid)
        doc["status"] = status
        doc["status_label"] = status_label or status
        self._store.save(self._store.activity, sid, doc)
        return {"status": status, "status_label": doc["status_label"]}

    def _load(self, student_id: str) -> dict[str, Any] | None:
        sid = student_id.strip()
        if self._orchestrator is not None and hasattr(
            self._orchestrator, "get_activity_status_opaque"
        ):
            projected = self._orchestrator.get_activity_status_opaque(sid)
            if isinstance(projected, dict):
                self.put_projection(sid, projected)
                return deepcopy(projected)
        doc = self._store.get(self._store.activity, sid)
        if doc is None and self._auto_provision:
            doc = default_activity_document(sid)
            self._store.save(self._store.activity, sid, doc)
        return None if doc is None else deepcopy(doc)
