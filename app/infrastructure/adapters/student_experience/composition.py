"""Student Experience production composition root (V2-018).

Wires Experience port adapters to shared persistence, events, and the
optional Learning Orchestrator learning loop. Application services never
import this module — presentation / factory does.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.application.student_experience.student_experience_service import (
    StudentExperienceService,
)
from app.infrastructure.adapters.adaptive import ExperienceAdaptiveAdapter
from app.infrastructure.adapters.journey import ExperienceJourneyAdapter
from app.infrastructure.adapters.mission.experience_adapter import (
    ExperienceMissionAdapter,
)
from app.infrastructure.adapters.orchestrator import ExperienceOrchestratorAdapter
from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_activity,
    seeded_demo_adaptive,
    seeded_demo_journey,
    seeded_demo_mission,
    seeded_demo_twin,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.adapters.student_experience.registry import (
    PersistedExperienceRegistry,
)
from app.infrastructure.adapters.student_twin.experience_adapter import (
    ExperienceTwinAdapter,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types.experience import (
    history_viewed,
    journey_viewed,
    revision_started,
    student_home_viewed,
)
from app.infrastructure.persistence.unit_of_work import UnitOfWork


class StudentExperienceComposition:
    """Production composition root for Student Experience adapters."""

    def __init__(
        self,
        *,
        store: ExperienceProjectionStore | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        uow: UnitOfWork | None = None,
        learning_loop: Any | None = None,
        enable_learning_loop: bool = True,
        twin_engine: Any | None = None,
        decision_engine: Any | None = None,
        mission_engine: Any | None = None,
        journey_engine: Any | None = None,
        seed_demo_learners: bool = True,
    ) -> None:
        self.events = events or EventRegistry()
        self.diagnostics = diagnostics or AdapterDiagnostics()
        self.uow = uow or UnitOfWork()
        self.store = store or ExperienceProjectionStore(uow=self.uow)
        self.learning_loop = learning_loop
        self._enable_learning_loop = bool(enable_learning_loop)
        self.registry = PersistedExperienceRegistry(self.store)

        self.twin = ExperienceTwinAdapter(
            store=self.store,
            twin_engine=twin_engine,
            events=self.events,
            diagnostics=self.diagnostics,
        )
        self.adaptive = ExperienceAdaptiveAdapter(
            store=self.store,
            decision_engine=decision_engine,
            events=self.events,
            diagnostics=self.diagnostics,
        )
        self.journey = ExperienceJourneyAdapter(
            store=self.store,
            journey_engine=journey_engine,
            events=self.events,
            diagnostics=self.diagnostics,
        )
        self.orchestrator = ExperienceOrchestratorAdapter(
            store=self.store,
            events=self.events,
            diagnostics=self.diagnostics,
        )
        self.mission = ExperienceMissionAdapter(
            store=self.store,
            mission_engine=mission_engine,
            events=self.events,
            diagnostics=self.diagnostics,
            on_session_started=self._run_learning_loop,
        )
        self._seed_demo = seed_demo_learners

    def seed_learner(self, student_id: str, *, demo: bool = True) -> None:
        """Provision opaque projections for a learner into production stores."""
        sid = student_id.strip()
        if demo:
            self.twin.put_projection(sid, seeded_demo_twin(sid))
            self.adaptive.put_projection(sid, seeded_demo_adaptive(sid))
            self.journey.put_projection(sid, seeded_demo_journey(sid))
            self.mission.put_projection(sid, seeded_demo_mission(sid))
            self.orchestrator.put_projection(sid, seeded_demo_activity(sid))
        else:
            self.twin.get_learner_summary(sid)
            self.adaptive.get_todays_recommendation(sid)
            self.journey.get_journey_progress(sid)
            self.mission.get_todays_session(sid)
            self.orchestrator.get_activity_status(sid)

    def ensure_learner(self, student_id: str) -> None:
        """Ensure learner projections exist (demo seed when enabled)."""
        sid = student_id.strip()
        existing = self.store.get(self.store.twin, sid)
        if existing is None and self._seed_demo:
            self.seed_learner(sid, demo=True)

    def build_service(self) -> StudentExperienceService:
        """Construct a StudentExperienceService bound to production adapters."""
        return StudentExperienceService(
            student_twin=self.twin,
            adaptive_decision=self.adaptive,
            mission=self.mission,
            learning_journey=self.journey,
            learning_orchestrator=self.orchestrator,
            registry=self.registry,  # type: ignore[arg-type]
        )

    def emit_surface_viewed(self, surface: str, student_id: str) -> None:
        """Emit Student Experience surface observability events."""
        sid = student_id.strip()
        key = (surface or "").strip().lower()
        ids = CorrelationContext.current()
        payload = {"student_id": sid, "surface": key}
        builders = {
            "home": student_home_viewed,
            "journey": journey_viewed,
            "history": history_viewed,
        }
        builder = builders.get(key)
        if builder is not None:
            self.events.publish(
                builder(
                    payload,
                    correlation_id=ids.correlation_id or "",
                    source="student_experience",
                )
            )

    def emit_revision_started(
        self, student_id: str, *, option_id: str | None = None
    ) -> None:
        """Emit RevisionStarted observability event."""
        ids = CorrelationContext.current()
        self.events.publish(
            revision_started(
                {
                    "student_id": student_id.strip(),
                    "option_id": option_id,
                },
                correlation_id=ids.correlation_id or "",
                source="student_experience",
            )
        )

    def _ensure_learning_loop(self) -> Any | None:
        """Lazily construct the Learning Orchestrator adapter when enabled."""
        if self.learning_loop is not None:
            return self.learning_loop
        if not self._enable_learning_loop:
            return None
        from app.infrastructure.adapters.learning_orchestrator import (
            LearningOrchestratorAdapter,
        )

        self.learning_loop = LearningOrchestratorAdapter()
        return self.learning_loop

    def _run_learning_loop(
        self, student_id: str, session_result: dict[str, Any]
    ) -> None:
        """Execute Version 2 learning loop after session start.

        Mission → Session evidence → Twin update → Adaptive recalculation →
        Updated Home projections. Educational math stays in engines / stores.
        """
        sid = student_id.strip()
        tokens = CorrelationContext.set(correlation_id=f"loop:{sid}")
        try:
            with self.uow.transaction():
                self.orchestrator.set_activity_status(
                    sid,
                    status="in_progress",
                    status_label="Learning session in progress",
                )
                loop = self._ensure_learning_loop()
                if loop is not None:
                    request = OrchestrationRequest(
                        event_type="session_completed",
                        learner_id=sid,
                        event_id=str(
                            session_result.get("experience_session_id")
                            or session_result.get("session_id")
                        ),
                        occurred_at=datetime.now(tz=UTC),
                        subject_id="EXPERIENCE",
                        session_id=str(session_result.get("session_id") or ""),
                        mission_id=str(session_result.get("mission_id") or ""),
                        correlation_id=CorrelationContext.get_correlation_id(),
                        payload=MappingProxyType(dict(session_result)),
                        metadata=MappingProxyType({}),
                    )
                    loop.orchestrate(request)

                completed = self.mission.complete_session(
                    sid,
                    session_id=str(session_result.get("session_id")),
                    topic_title=str(session_result.get("topic_title") or ""),
                    estimated_minutes=session_result.get("estimated_minutes"),
                )
                twin_ack = self.twin.apply_session_outcome(
                    sid, session_payload=completed
                )
                twin_doc = self.store.get(self.store.twin, sid) or {}
                self.adaptive.recalculate_from_twin(
                    sid, twin_payload={**twin_doc, **twin_ack}
                )
                self.orchestrator.set_activity_status(
                    sid,
                    status="idle",
                    status_label="Ready for today's session",
                )
                recommendation = self.adaptive.get_todays_recommendation(sid) or {}
                self.adaptive.accept_recommendation(
                    sid,
                    decision_id=(
                        None
                        if not recommendation.get("decision_id")
                        else str(recommendation.get("decision_id"))
                    ),
                )
        finally:
            CorrelationContext.reset(tokens)


def build_production_experience(
    *,
    seed_demo_learners: bool = True,
    learning_loop: bool = True,
) -> tuple[StudentExperienceComposition, StudentExperienceService]:
    """Build production Student Experience composition + service."""
    composition = StudentExperienceComposition(
        learning_loop=None,
        enable_learning_loop=learning_loop,
        seed_demo_learners=seed_demo_learners,
    )
    if seed_demo_learners:
        composition.seed_learner("default", demo=True)
    return composition, composition.build_service()
