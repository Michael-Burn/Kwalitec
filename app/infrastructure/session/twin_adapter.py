"""SessionTwinAdapter — StudentTwinPort for Learning Session Experience."""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_twin,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.adapters.student_twin.experience_adapter import (
    ExperienceTwinAdapter,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics


class SessionTwinAdapter:
    """Production adapter implementing Session Experience StudentTwinPort.

    Reuses ExperienceTwinAdapter / Twin projections. Never computes readiness.
    """

    ADAPTER_ID = "session_twin"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        twin: ExperienceTwinAdapter | None = None,
        store: ExperienceProjectionStore | None = None,
        twin_engine: Any | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
        seed_demo: bool = True,
    ) -> None:
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._auto_provision = auto_provision
        self._seed_demo = seed_demo
        self._delegate = twin or ExperienceTwinAdapter(
            store=store or ExperienceProjectionStore(),
            twin_engine=twin_engine,
            diagnostics=self._diagnostics,
            available=available,
            auto_provision=auto_provision,
        )
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
        return self._available and self._delegate.is_available()

    def set_available(self, available: bool) -> None:
        self._available = available
        self._delegate.set_available(available)
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    @property
    def delegate(self) -> ExperienceTwinAdapter:
        """Underlying Experience twin adapter (reuse boundary)."""
        return self._delegate

    def put_projection(self, student_id: str, document: dict[str, Any]) -> None:
        """Provision opaque Twin projection via the Experience adapter."""
        self._delegate.put_projection(student_id, document)

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        self._ensure_learner(student_id)
        return self._delegate.get_readiness_summary(student_id)

    def get_learning_insights(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        self._ensure_learner(student_id)
        insights = self._delegate.get_learning_insights(student_id)
        if insights is None:
            return None
        # Session summary prefers a recent_insights tuple when present.
        payload = dict(insights)
        if "recent_insights" not in payload:
            achievements = payload.get("recent_achievements") or ()
            mastered = payload.get("mastered_topics") or ()
            recent = tuple(
                str(item.get("title") if isinstance(item, dict) else item)
                for item in (*achievements, *mastered)
            )
            if recent:
                payload["recent_insights"] = recent
        return payload

    def _ensure_learner(self, student_id: str) -> None:
        if not (self._seed_demo and self._auto_provision):
            return
        sid = student_id.strip()
        store = getattr(self._delegate, "_store", None)
        if store is None:
            return
        doc = store.get(store.twin, sid)
        readiness = (doc or {}).get("readiness") or {}
        stats = (doc or {}).get("statistics") or {}
        if doc is not None and (
            readiness.get("exam_readiness") is not None
            or stats.get("current_exam_readiness") is not None
        ):
            return
        self._delegate.put_projection(sid, seeded_demo_twin(sid))
