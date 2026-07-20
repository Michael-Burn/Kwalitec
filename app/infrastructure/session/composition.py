"""Session Experience production composition root (V2-020A).

Wires Session Experience port adapters to shared in-memory stores and
reuses Student Experience Twin / Adaptive / Mission adapters. Application
services never import this module — presentation / factory does.
"""

from __future__ import annotations

from typing import Any

from app.application.session_experience.facade import SessionExperienceService
from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_adaptive,
    seeded_demo_mission,
    seeded_demo_twin,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.session.activity_adapter import SessionActivityAdapter
from app.infrastructure.session.adaptive_adapter import SessionAdaptiveAdapter
from app.infrastructure.session.defaults import (
    default_session_overview,
)
from app.infrastructure.session.mission_adapter import SessionMissionAdapter
from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter
from app.infrastructure.session.store import SessionDocumentStore
from app.infrastructure.session.twin_adapter import SessionTwinAdapter


class SessionExperienceComposition:
    """Production composition root for Session Experience adapters."""

    def __init__(
        self,
        *,
        store: SessionDocumentStore | None = None,
        experience_store: ExperienceProjectionStore | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        runtime_engine: Any | None = None,
        activity_engine: Any | None = None,
        twin_engine: Any | None = None,
        decision_engine: Any | None = None,
        mission_engine: Any | None = None,
        seed_demo_learners: bool = True,
        activity_count: int = 3,
    ) -> None:
        self.diagnostics = diagnostics or AdapterDiagnostics()
        self.store = store or SessionDocumentStore()
        self.experience_store = experience_store or ExperienceProjectionStore()
        self._seed_demo = seed_demo_learners

        self.runtime = SessionRuntimeAdapter(
            store=self.store,
            runtime_engine=runtime_engine,
            diagnostics=self.diagnostics,
        )
        self.activity = SessionActivityAdapter(
            store=self.store,
            activity_engine=activity_engine,
            diagnostics=self.diagnostics,
            activity_count=activity_count,
        )
        self.mission = SessionMissionAdapter(
            store=self.experience_store,
            mission_engine=mission_engine,
            diagnostics=self.diagnostics,
            seed_demo=seed_demo_learners,
        )
        self.twin = SessionTwinAdapter(
            store=self.experience_store,
            twin_engine=twin_engine,
            diagnostics=self.diagnostics,
            seed_demo=seed_demo_learners,
        )
        self.adaptive = SessionAdaptiveAdapter(
            store=self.experience_store,
            decision_engine=decision_engine,
            diagnostics=self.diagnostics,
            seed_demo=seed_demo_learners,
        )

    def seed_learner(self, student_id: str, *, demo: bool = True) -> None:
        """Provision opaque projections for a learner into production stores."""
        sid = student_id.strip()
        if demo:
            self.twin.put_projection(sid, seeded_demo_twin(sid))
            self.adaptive.put_projection(sid, seeded_demo_adaptive(sid))
            self.mission.put_projection(sid, seeded_demo_mission(sid))
            today = self.mission.get_todays_session(sid) or {}
            session_id = str(today.get("session_id") or "sess-1")
            mission_id = str(today.get("mission_id") or "m1")
            overview = default_session_overview(
                sid, session_id=session_id, mission_id=mission_id
            )
            overview["topics"] = tuple(today.get("topics") or overview["topics"])
            overview["objective"] = str(
                today.get("objective") or overview["objective"]
            )
            overview["estimated_minutes"] = today.get("estimated_minutes") or 30
            self.runtime.put_overview(sid, session_id=session_id, document=overview)
        else:
            self.mission.get_todays_session(sid)
            self.twin.get_readiness_summary(sid)
            self.adaptive.get_todays_recommendation(sid)

    def ensure_learner(self, student_id: str) -> None:
        """Ensure learner projections exist (demo seed when enabled)."""
        sid = student_id.strip()
        if self.mission.get_todays_session(sid) is None and self._seed_demo:
            self.seed_learner(sid, demo=True)

    def build_service(self) -> SessionExperienceService:
        """Construct a SessionExperienceService bound to production adapters."""
        return SessionExperienceService(
            session_runtime=self.runtime,
            activity_engine=self.activity,
            mission=self.mission,
            student_twin=self.twin,
            adaptive_decision=self.adaptive,
        )


def build_production_session_experience(
    *,
    seed_demo_learners: bool | None = None,
    store: SessionDocumentStore | None = None,
    experience_store: ExperienceProjectionStore | None = None,
    flags: Any | None = None,
) -> tuple[SessionExperienceComposition, SessionExperienceService]:
    """Build production Session Experience composition + service."""
    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.infrastructure.composition import (
        build_experience_projection_store,
        build_opaque_engines,
        build_session_document_store,
    )

    active = flags or resolve_v2_feature_flags()
    seed = (
        active.SEED_DEMO_LEARNERS
        if seed_demo_learners is None
        else seed_demo_learners
    )
    shared = experience_store or build_experience_projection_store(flags=active)
    session_store = store or build_session_document_store(
        flags=active, experience_store=shared
    )
    engines = build_opaque_engines(flags=active)
    composition = SessionExperienceComposition(
        store=session_store,
        experience_store=shared,
        runtime_engine=engines.get("runtime_engine"),
        activity_engine=engines.get("activity_engine"),
        twin_engine=engines.get("twin_engine"),
        decision_engine=engines.get("decision_engine"),
        mission_engine=engines.get("mission_engine"),
        seed_demo_learners=seed,
    )
    if seed:
        composition.seed_learner("default", demo=True)
    return composition, composition.build_service()
