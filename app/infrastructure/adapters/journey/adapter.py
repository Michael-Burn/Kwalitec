"""ExperienceJourneyAdapter — LearningJourneyPort for Student Experience."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.adapters.student_experience.defaults import (
    default_journey_document,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.events.registry import EventRegistry


class ExperienceJourneyAdapter:
    """Production adapter implementing Student Experience LearningJourneyPort.

    Projects journey progress. Never invents Topic Complete.
    """

    ADAPTER_ID = "experience_journey"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        store: ExperienceProjectionStore | None = None,
        journey_engine: Any | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
    ) -> None:
        self._store = store or ExperienceProjectionStore()
        self._engine = journey_engine
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
        """Persist an opaque Journey projection."""
        sid = student_id.strip()
        payload = deepcopy(document)
        payload["student_id"] = sid
        payload.setdefault("authority", "learning_journey")
        self._store.save(self._store.journey, sid, payload)

    def get_journey_progress(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        progress = doc.get("progress")
        return None if progress is None else dict(progress)

    def get_topic_list(self, student_id: str) -> tuple[dict[str, Any], ...]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return ()
        topics = doc.get("topics") or ()
        return tuple(dict(item) for item in topics)

    def _load(self, student_id: str) -> dict[str, Any] | None:
        sid = student_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "get_journey_progress_opaque"
        ):
            projected = self._engine.get_journey_progress_opaque(sid)
            if isinstance(projected, dict):
                wrapped = default_journey_document(sid)
                if "progress" in projected or "topics" in projected:
                    wrapped.update(projected)
                else:
                    wrapped["progress"] = projected
                self.put_projection(sid, wrapped)
                return deepcopy(wrapped)
        doc = self._store.get(self._store.journey, sid)
        if doc is None and self._auto_provision:
            doc = default_journey_document(sid)
            self._store.save(self._store.journey, sid, doc)
        return None if doc is None else deepcopy(doc)
