"""ExperienceAdaptiveAdapter — AdaptiveDecisionPort for Student Experience."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.adapters.student_experience.defaults import (
    default_adaptive_document,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import adaptive_decision_generated
from app.infrastructure.events.types.experience import (
    recommendation_accepted,
    recommendation_dismissed,
)


class ExperienceAdaptiveAdapter:
    """Production adapter implementing Student Experience AdaptiveDecisionPort.

    Sole next-action authority bridge (ADR-005). Never invents recommendations.
    """

    ADAPTER_ID = "experience_adaptive"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        store: ExperienceProjectionStore | None = None,
        decision_engine: Any | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
    ) -> None:
        self._store = store or ExperienceProjectionStore()
        self._engine = decision_engine
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
        """Persist an opaque Adaptive projection."""
        sid = student_id.strip()
        payload = deepcopy(document)
        payload["student_id"] = sid
        payload["authority"] = "adaptive_decision_engine"
        payload["next_action_authority"] = True
        self._store.save(self._store.adaptive, sid, payload)

    def get_todays_recommendation(
        self, student_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        recommendation = doc.get("recommendation")
        return None if recommendation is None else dict(recommendation)

    def get_revision_options(
        self, student_id: str
    ) -> tuple[dict[str, Any], ...]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return ()
        options = doc.get("revision_options") or ()
        return tuple(dict(item) for item in options)

    def get_decision_explanation(
        self, student_id: str, *, decision_id: str | None = None
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        doc = self._load(student_id)
        if doc is None:
            return None
        explanations = dict(doc.get("explanations") or {})
        if decision_id and decision_id in explanations:
            return dict(explanations[decision_id])
        recommendation = doc.get("recommendation") or {}
        explanation = recommendation.get("explanation")
        return None if explanation is None else dict(explanation)

    def accept_recommendation(
        self, student_id: str, *, decision_id: str | None = None
    ) -> dict[str, Any]:
        """Record recommendation acceptance (delivery hand-off only)."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        ids = CorrelationContext.current()
        payload = {
            "student_id": student_id.strip(),
            "decision_id": decision_id,
            "accepted": True,
            "authority": "adaptive_decision_engine",
        }
        self._events.publish(
            recommendation_accepted(
                payload,
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
        return payload

    def dismiss_recommendation(
        self, student_id: str, *, decision_id: str | None = None
    ) -> dict[str, Any]:
        """Record recommendation dismissal (no alternative invention)."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        ids = CorrelationContext.current()
        payload = {
            "student_id": student_id.strip(),
            "decision_id": decision_id,
            "dismissed": True,
            "authority": "adaptive_decision_engine",
        }
        self._events.publish(
            recommendation_dismissed(
                payload,
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
        return payload

    def recalculate_from_twin(
        self,
        student_id: str,
        *,
        twin_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Request Adaptive recalculation after Twin update.

        Delegates to decision_engine when present; otherwise retains stored
        recommendation without inventing a new next action.
        """
        self._diagnostics.record_call(self.ADAPTER_ID)
        sid = student_id.strip()
        doc = self._load(sid) or default_adaptive_document(sid)
        if self._engine is not None and hasattr(self._engine, "decide_opaque"):
            decided = self._engine.decide_opaque(
                sid, twin_payload=twin_payload
            )
            if isinstance(decided, dict):
                if "recommendation" in decided or "revision_options" in decided:
                    doc.update(decided)
                else:
                    doc["recommendation"] = decided
                    if decided.get("decision_id"):
                        explanations = dict(doc.get("explanations") or {})
                        if decided.get("explanation"):
                            explanations[str(decided["decision_id"])] = dict(
                                decided["explanation"]
                            )
                        doc["explanations"] = explanations
        doc["authority"] = "adaptive_decision_engine"
        doc["next_action_authority"] = True
        doc["twin_ref"] = twin_payload.get("student_id") or sid
        self._store.save(self._store.adaptive, sid, doc)
        ids = CorrelationContext.current()
        event_payload = {
            "student_id": sid,
            "component": self.ADAPTER_ID,
            "ok": True,
            "authority": "adaptive_decision_engine",
            "next_action_authority": True,
            "decision_id": (doc.get("recommendation") or {}).get("decision_id"),
        }
        self._events.publish(
            adaptive_decision_generated(
                event_payload,
                correlation_id=ids.correlation_id or "",
                source=self.ADAPTER_ID,
            )
        )
        return event_payload

    def _load(self, student_id: str) -> dict[str, Any] | None:
        sid = student_id.strip()
        if self._engine is not None and hasattr(
            self._engine, "get_todays_recommendation_opaque"
        ):
            projected = self._engine.get_todays_recommendation_opaque(sid)
            if isinstance(projected, dict):
                wrapped = default_adaptive_document(sid)
                wrapped["recommendation"] = projected
                if projected.get("explanation") and projected.get("decision_id"):
                    wrapped["explanations"] = {
                        str(projected["decision_id"]): dict(
                            projected["explanation"]
                        )
                    }
                self.put_projection(sid, wrapped)
                return deepcopy(wrapped)
        doc = self._store.get(self._store.adaptive, sid)
        if doc is None and self._auto_provision:
            doc = default_adaptive_document(sid)
            self._store.save(self._store.adaptive, sid, doc)
        return None if doc is None else deepcopy(doc)
