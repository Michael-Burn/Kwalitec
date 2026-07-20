"""SessionAdaptiveAdapter — AdaptiveDecisionPort for Learning Session Experience."""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.adaptive.adapter import ExperienceAdaptiveAdapter
from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_adaptive,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics


class SessionAdaptiveAdapter:
    """Production adapter implementing Session Experience AdaptiveDecisionPort.

    Reuses ExperienceAdaptiveAdapter / Adaptive projections. Never invents
    recommendations (ADR-005).
    """

    ADAPTER_ID = "session_adaptive"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        adaptive: ExperienceAdaptiveAdapter | None = None,
        store: ExperienceProjectionStore | None = None,
        decision_engine: Any | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
        seed_demo: bool = True,
    ) -> None:
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._auto_provision = auto_provision
        self._seed_demo = seed_demo
        self._delegate = adaptive or ExperienceAdaptiveAdapter(
            store=store or ExperienceProjectionStore(),
            decision_engine=decision_engine,
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
    def delegate(self) -> ExperienceAdaptiveAdapter:
        """Underlying Experience adaptive adapter (reuse boundary)."""
        return self._delegate

    def put_projection(self, student_id: str, document: dict[str, Any]) -> None:
        """Provision opaque Adaptive projection via the Experience adapter."""
        self._delegate.put_projection(student_id, document)

    def get_todays_recommendation(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        self._ensure_learner(student_id)
        recommendation = self._delegate.get_todays_recommendation(student_id)
        return None if recommendation is None else dict(recommendation)

    def _ensure_learner(self, student_id: str) -> None:
        sid = student_id.strip()
        recommendation = self._delegate.get_todays_recommendation(sid)
        if recommendation is not None:
            return
        if self._seed_demo and self._auto_provision:
            self._delegate.put_projection(sid, seeded_demo_adaptive(sid))
