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
        mission_read: Any | None = None,
        mission_start: Any | None = None,
        mission_resume: Any | None = None,
        session_completion: Any | None = None,
        recommendation_read: Any | None = None,
        journey_read: Any | None = None,
        history_read: Any | None = None,
        adaptive_engine: Any | None = None,
        adaptive_input_assembler: Any | None = None,
        adaptive_shadow: Any | None = None,
        explainability_gate: Any | None = None,
        adaptive_port_router: Any | None = None,
        adaptive_traceability: Any | None = None,
        adaptive_soak: Any | None = None,
        digital_twin: Any | None = None,
        twin_facet_assembler: Any | None = None,
        twin_snapshot_builder: Any | None = None,
        twin_explainability: Any | None = None,
        twin_input_adapter: Any | None = None,
        student_twin_projector: Any | None = None,
        student_twin_projection_port: Any | None = None,
        twin_shadow: Any | None = None,
        twin_foundation: Any | None = None,
        twin_authority: bool = False,
        strategy_engine: Any | None = None,
        strategy_explainability: Any | None = None,
        strategy_projector: Any | None = None,
        strategy_projection_port: Any | None = None,
        strategy_shadow: Any | None = None,
        evidence_platform: Any | None = None,
        evidence_shadow: Any | None = None,
        journey_coordinator: Any | None = None,
        experience_observation: Any | None = None,
        experience_diagnostics: Any | None = None,
        experience_feedback: Any | None = None,
        learning_feedback: Any | None = None,
        evidence_advisory_injection: Any | None = None,
        recovery_planner: Any | None = None,
        recovery_injection: Any | None = None,
        decision_simulation: Any | None = None,
        advisory_evaluation: Any | None = None,
        controlled_advisory: Any | None = None,
        advisory_outcome_measurement: Any | None = None,
        recommendation_policy: Any | None = None,
        educational_trial: Any | None = None,
        longitudinal_evidence: Any | None = None,
        evidence_review: Any | None = None,
    ) -> None:
        self.events = events or EventRegistry()
        self.diagnostics = diagnostics or AdapterDiagnostics()
        self.uow = uow or UnitOfWork()
        self.store = store or ExperienceProjectionStore(uow=self.uow)
        self.learning_loop = learning_loop
        self._enable_learning_loop = bool(enable_learning_loop)
        self.registry = PersistedExperienceRegistry(self.store)
        self._mission_read = mission_read
        self._mission_start = mission_start
        self._mission_resume = mission_resume
        self._session_completion = session_completion
        self._recommendation_read = recommendation_read
        self._journey_read = journey_read
        self._history_read = history_read
        # MS-003 A0–A6: Adaptive Engine pipeline. Experience AdaptiveDecisionPort
        # serves adaptive only when adaptive_port_router cutover is active
        # (Engine + Shadow + Authority); otherwise RecommendationService path.
        # A5 TraceabilityService / A6 Shadow Soak are observational only
        # (no educational writes; soak never influences the student).
        self.adaptive_engine = adaptive_engine
        self.adaptive_input_assembler = adaptive_input_assembler
        self.adaptive_shadow = adaptive_shadow
        self.explainability_gate = explainability_gate
        self.adaptive_port_router = adaptive_port_router
        self.adaptive_traceability = adaptive_traceability
        self.adaptive_soak = adaptive_soak
        # MS-004 T0–T6: Digital Twin contracts, facet synthesis, snapshot
        # assembly, explainability, Adaptive Twin-input adapter (read-only),
        # Experience Twin projection port, Twin Shadow Validation
        # (observational only), and EP-001.1 Foundation. ExperienceTwinAdapter
        # remains UX StudentTwinPort unless ENABLE_DIGITAL_TWIN_AUTHORITY is ON.
        self.digital_twin = digital_twin
        self.twin_facet_assembler = twin_facet_assembler
        self.twin_snapshot_builder = twin_snapshot_builder
        self.twin_explainability = twin_explainability
        self.twin_input_adapter = twin_input_adapter
        self.student_twin_projector = student_twin_projector
        self.student_twin_projection_port = student_twin_projection_port
        self.twin_shadow = twin_shadow
        self.twin_foundation = twin_foundation
        self.twin_authority_enabled = bool(twin_authority)
        # MS-005 S0–S3: Strategy Engine contracts, core orchestration,
        # explainability, Experience projection port DI, and Strategy Shadow
        # Validation (observational only). No Experience authority cutover or
        # upstream Runtime A / Twin / Adaptive mutation.
        self.strategy_engine = strategy_engine
        self.strategy_explainability = strategy_explainability
        self.strategy_projector = strategy_projector
        self.strategy_projection_port = strategy_projection_port
        self.strategy_shadow = strategy_shadow
        # MS-006 E0–E5: Learning Evidence Platform contracts / collection /
        # experiment / policy / analytics / Shadow Validation DI.
        # Observational measurement surface — never educational decision
        # authority. No policy deployment or Experience UX influence.
        self.evidence_platform = evidence_platform
        self.evidence_shadow = evidence_shadow
        # P2-MS001: Unified Student Journey Coordinator (Experience
        # orchestration only — no educational logic or Programme I mutation).
        self.journey_coordinator = journey_coordinator
        # P2-MS006: Experience Observation Bridge (one-way factual publish
        # to Evidence public intake). Observational only — no educational
        # interpretation, persistence, or authority changes.
        self.experience_observation = experience_observation
        # P2-MS007: Experience Observability & Diagnostics (JourneyTrace,
        # counters, pipeline health, structured logs). Internal ops only —
        # no educational authority or student UX.
        self.experience_diagnostics = experience_diagnostics
        # P2-MS008: Experience Feedback Loop (Evidence factual read → Home
        # "Your Journey"). Display-only — no adaptation or recommendation
        # changes.
        self.experience_feedback = experience_feedback
        # EP-003.4: Learning Feedback Loop (observed behavioural evidence).
        # Record-only — no educational decision-making or Twin writes.
        self.learning_feedback = learning_feedback
        # P2-MS009: Evidence Advisory Layer injection for Runtime A.
        # Integration point only — advisory inputs may be read/documented;
        # recommendation behaviour unchanged.
        self.evidence_advisory_injection = evidence_advisory_injection
        # P2-MS010: Study Recovery Engine injection for Runtime A.
        # Architecture only — recovery candidates may be read/documented;
        # recommendation behaviour unchanged; all candidates advisory_only.
        self.recovery_planner = recovery_planner
        self.recovery_injection = recovery_injection
        # P2-MS011: Advisory Decision Simulation (parallel comparison only).
        # Never modifies student-facing recommendations.
        self.decision_simulation = decision_simulation
        # P2-MS012: Advisory Evaluation Framework (ops / review only).
        # Consumes simulation outputs; never modifies Runtime A behaviour.
        self.advisory_evaluation = advisory_evaluation
        # P3-MS001: Controlled Advisory Activation (minimal Runtime A
        # consumption of one approved Evidence Advisory field). Default OFF;
        # reversible; simulation comparison retained.
        self.controlled_advisory = controlled_advisory
        # P3-MS002: Advisory Outcome Measurement (ops observation only).
        # Collects rollout outcomes / metrics; never modifies Runtime A.
        self.advisory_outcome_measurement = advisory_outcome_measurement
        # P3-MS003: Recommendation Policy Framework (declarative policy
        # resolution / explainability). Policy is advisory to Runtime A.
        # P3-MS004: when ENABLE_POLICY_WEIGHTING is ON, the same engine may
        # resolve a single bounded WeightApplication for Runtime A to apply.
        self.recommendation_policy = recommendation_policy
        # P4-MS001: Controlled Educational Effectiveness Trial (deterministic
        # baseline vs treatment cohorts; operational metrics / reporting).
        # Gates Runtime A policy weighting to authorised treatment cohorts
        # only when ENABLE_EDUCATIONAL_TRIALS is ON.
        self.educational_trial = educational_trial
        # P4-MS002: Longitudinal Learning Evidence Repository (append-only
        # educational observation storage). Evidence only — never influences
        # Runtime A, Adaptive, Recovery, or educational policy.
        self.longitudinal_evidence = longitudinal_evidence
        # P4-MS003: Educational Evidence Review Workspace (read-only query /
        # timeline / export). Human inspection only — never influences
        # Runtime A, recommendations, policy, or educational behaviour.
        self.evidence_review = evidence_review
        experience_twin = ExperienceTwinAdapter(
            store=self.store,
            twin_engine=twin_engine,
            events=self.events,
            diagnostics=self.diagnostics,
        )
        if twin_authority and twin_foundation is not None:
            from app.infrastructure.adapters.digital_twin.authority import (
                build_student_twin_foundation_authority_port,
            )

            authority_port = build_student_twin_foundation_authority_port(
                enabled=True,
                foundation=twin_foundation,
                fallback=experience_twin,
            )
            self.twin = authority_port or experience_twin
        else:
            self.twin = experience_twin
        self._experience_twin = experience_twin
        self.adaptive = ExperienceAdaptiveAdapter(
            store=self.store,
            decision_engine=(
                None if recommendation_read is not None else decision_engine
            ),
            recommendation_read=recommendation_read,
            adaptive_port_router=adaptive_port_router,
            events=self.events,
            diagnostics=self.diagnostics,
        )
        self.journey = ExperienceJourneyAdapter(
            store=self.store,
            journey_engine=(
                None if journey_read is not None else journey_engine
            ),
            journey_read=journey_read,
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
            mission_read=mission_read,
            mission_start=mission_start,
            mission_resume=mission_resume,
            session_completion=session_completion,
            events=self.events,
            diagnostics=self.diagnostics,
            on_session_started=self._run_learning_loop,
        )
        self._seed_demo = seed_demo_learners and not bool(twin_authority)

    def seed_learner(self, student_id: str, *, demo: bool = True) -> None:
        """Provision opaque projections for a learner into production stores."""
        sid = student_id.strip()
        # Under Twin Authority, never seed demo Twin theatre — Foundation is SoT.
        twin_demo = demo and not self.twin_authority_enabled
        if demo:
            if twin_demo and hasattr(self._experience_twin, "put_projection"):
                self._experience_twin.put_projection(sid, seeded_demo_twin(sid))
            # Bridged recommendation reads must not receive seeded_demo_adaptive.
            if self._recommendation_read is None:
                self.adaptive.put_projection(sid, seeded_demo_adaptive(sid))
            # Bridged journey reads must not receive seeded_demo_journey.
            if self._journey_read is None:
                self.journey.put_projection(sid, seeded_demo_journey(sid))
            # Bridged mission reads/starts/resumes/completes must not receive
            # seeded_demo_mission.
            if (
                self._mission_read is None
                and self._mission_start is None
                and self._mission_resume is None
                and self._session_completion is None
            ):
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
            history_read=self._history_read,
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

        When Session Completion Bridge is wired, this loop must not mark the
        SQL session complete after start (Evidence Before Completion +
        lifecycle integrity). UX activity markers and optional orchestrator
        hooks may still run.
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

                # Session Completion Bridge owns educational completion.
                # Auto-complete after start would end the SQL session early.
                if self._session_completion is not None:
                    self.orchestrator.set_activity_status(
                        sid,
                        status="in_progress",
                        status_label="Learning session in progress",
                    )
                    return

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
    seed_demo_learners: bool | None = None,
    learning_loop: bool = True,
    store: ExperienceProjectionStore | None = None,
    flags: Any | None = None,
) -> tuple[StudentExperienceComposition, StudentExperienceService]:
    """Build production Student Experience composition + service."""
    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.infrastructure.composition import (
        build_experience_projection_store,
        build_opaque_engines,
    )

    active = flags or resolve_v2_feature_flags()
    seed = (
        active.SEED_DEMO_LEARNERS
        if seed_demo_learners is None
        else seed_demo_learners
    )
    projection_store = store or build_experience_projection_store(flags=active)
    engines = build_opaque_engines(flags=active)
    from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
    from app.infrastructure.events.registry import EventRegistry

    events = EventRegistry()
    diagnostics = AdapterDiagnostics()
    mission_read = None
    mission_start = None
    mission_resume = None
    session_completion = None
    recommendation_read = None
    journey_read = None
    history_read = None
    adaptive_engine = None
    adaptive_input_assembler = None
    adaptive_shadow = None
    explainability_gate = None
    adaptive_port_router = None
    adaptive_traceability = None
    adaptive_soak = None
    digital_twin = None
    twin_facet_assembler = None
    twin_snapshot_builder = None
    twin_explainability = None
    twin_input_adapter = None
    student_twin_projector = None
    student_twin_projection_port = None
    twin_shadow = None
    twin_foundation = None
    strategy_engine = None
    strategy_explainability = None
    strategy_projector = None
    strategy_projection_port = None
    strategy_shadow = None
    evidence_platform = None
    evidence_shadow = None
    journey_coordinator = None
    experience_observation = None
    experience_diagnostics = None
    experience_feedback = None
    learning_feedback = None
    evidence_advisory_injection = None
    recovery_planner = None
    recovery_injection = None
    decision_simulation = None
    advisory_evaluation = None
    controlled_advisory = None
    advisory_outcome_measurement = None
    recommendation_policy = None
    educational_trial = None
    longitudinal_evidence = None
    evidence_review = None
    if (
        active.ENABLE_MISSION_READ_BRIDGE
        or active.ENABLE_MISSION_START_BRIDGE
        or active.ENABLE_MISSION_RESUME_BRIDGE
        or active.ENABLE_SESSION_COMPLETION_BRIDGE
        or active.ENABLE_RECOMMENDATION_BRIDGE
        or active.ENABLE_JOURNEY_BRIDGE
        or active.ENABLE_HISTORY_BRIDGE
    ):
        from app.infrastructure.adapters.educational_runtime_bridge import (
            HistoryAdapter,
            JourneyAdapter,
            MissionReadAdapter,
            MissionResumeAdapter,
            MissionStartAdapter,
            RecommendationAdapter,
            SessionCompletionAdapter,
        )

        if active.ENABLE_MISSION_READ_BRIDGE:
            mission_read = MissionReadAdapter(
                events=events,
                diagnostics=diagnostics,
            )
        if active.ENABLE_MISSION_START_BRIDGE:
            mission_start = MissionStartAdapter(
                events=events,
                diagnostics=diagnostics,
            )
        if active.ENABLE_MISSION_RESUME_BRIDGE:
            mission_resume = MissionResumeAdapter(
                events=events,
                diagnostics=diagnostics,
            )
        if active.ENABLE_SESSION_COMPLETION_BRIDGE:
            session_completion = SessionCompletionAdapter(
                events=events,
                diagnostics=diagnostics,
            )
        if active.ENABLE_RECOMMENDATION_BRIDGE:
            recommendation_read = RecommendationAdapter(
                events=events,
                diagnostics=diagnostics,
            )
        if active.ENABLE_JOURNEY_BRIDGE:
            journey_read = JourneyAdapter(
                events=events,
                diagnostics=diagnostics,
            )
        if active.ENABLE_HISTORY_BRIDGE:
            history_read = HistoryAdapter(
                events=events,
                diagnostics=diagnostics,
            )
    # MS-004 Twin DI before Adaptive so TwinInputAdapter can be injected.
    if active.ENABLE_DIGITAL_TWIN:
        from app.infrastructure.adapters.adaptive_engine import (
            build_twin_input_adapter,
        )
        from app.infrastructure.adapters.digital_twin import (
            build_digital_twin_adapter,
            build_student_digital_twin_foundation,
            build_student_twin_projection_port,
            build_student_twin_projector,
            build_twin_explainability_service,
            build_twin_facet_assembler,
            build_twin_shadow_validator,
            build_twin_snapshot_builder,
        )

        # T0–T3: Twin contracts / facets / snapshots / explainability.
        # T4: TwinInputAdapter for Adaptive read-only consumption.
        # T5: StudentTwinProjector / StudentTwinProjectionPort (projection only).
        # T6: TwinShadowValidator — observational shadow validation only.
        # EP-001.1: StudentDigitalTwinFoundation (canonical learner-state read).
        # ExperienceTwinAdapter remains UX StudentTwinPort unless Authority ON.
        digital_twin = build_digital_twin_adapter(enabled=True)
        twin_facet_assembler = build_twin_facet_assembler(enabled=True)
        twin_snapshot_builder = build_twin_snapshot_builder(
            enabled=True,
            facet_assembler=twin_facet_assembler,
        )
        twin_explainability = build_twin_explainability_service(enabled=True)
        twin_input_adapter = build_twin_input_adapter(enabled=True)
        student_twin_projector = build_student_twin_projector(enabled=True)
        student_twin_projection_port = build_student_twin_projection_port(
            enabled=True,
            projector=student_twin_projector,
        )
        twin_shadow = build_twin_shadow_validator(
            enabled=True,
            snapshot_builder=twin_snapshot_builder,
            explainability=twin_explainability,
            projector=student_twin_projector,
            events=events,
        )
        twin_foundation = build_student_digital_twin_foundation(
            enabled=True,
            facet_assembler=twin_facet_assembler,
            snapshot_builder=twin_snapshot_builder,
        )
    # MS-005 S0–S3: Strategy Engine core orchestration + explainability +
    # Experience projection DI + observational Shadow Validation
    # (no Experience authority cutover).
    if active.ENABLE_STRATEGY_ENGINE:
        from app.infrastructure.adapters.strategy_engine import (
            build_strategy_engine_adapter,
            build_strategy_explainability_service,
            build_strategy_projection_port,
            build_strategy_projector,
            build_strategy_shadow_validator,
        )

        strategy_engine = build_strategy_engine_adapter(enabled=True)
        strategy_explainability = build_strategy_explainability_service(
            enabled=True
        )
        strategy_projector = build_strategy_projector(enabled=True)
        strategy_projection_port = build_strategy_projection_port(
            enabled=True,
            projector=strategy_projector,
            explainability=strategy_explainability,
        )
        strategy_shadow = build_strategy_shadow_validator(
            enabled=True,
            adapter=strategy_engine,
            explainability=strategy_explainability,
            projector=strategy_projector,
            events=events,
        )
    # MS-006 E0–E5: Learning Evidence Platform + observational Shadow Validation
    # (no policy deployment or Experience influence).
    if active.ENABLE_EVIDENCE_PLATFORM:
        from app.infrastructure.adapters.evidence_platform import (
            build_evidence_platform_adapter,
            build_evidence_shadow_validator,
        )

        evidence_platform = build_evidence_platform_adapter(enabled=True)
        evidence_shadow = build_evidence_shadow_validator(
            enabled=True,
            adapter=evidence_platform,
            events=events,
        )
    # P2-MS001: Unified Student Journey Framework DI (orchestration only).
    if active.ENABLE_UNIFIED_JOURNEY:
        from app.application.unified_journey import JourneyCoordinator

        journey_coordinator = JourneyCoordinator()
    # P2-MS006: Experience Observation Bridge DI (observational publish only).
    # Independently controllable from ENABLE_EVIDENCE_PLATFORM — when Evidence
    # is OFF the publisher is still constructed but publish() skips intake.
    if active.ENABLE_EXPERIENCE_OBSERVATION:
        from app.infrastructure.adapters.experience_observation import (
            build_experience_observation_publisher,
        )

        experience_observation = build_experience_observation_publisher(
            enabled=True,
            evidence=evidence_platform,
        )
    # P2-MS007: Experience Observability & Diagnostics DI (ops visibility).
    # Independently controllable from observation / evidence / journey flags.
    if active.ENABLE_EXPERIENCE_DIAGNOSTICS:
        from app.infrastructure.adapters.experience_observation import (
            build_experience_observation_diagnostics,
        )

        experience_diagnostics = build_experience_observation_diagnostics(
            enabled=True,
            observation_flag=active.ENABLE_EXPERIENCE_OBSERVATION,
            evidence_flag=active.ENABLE_EVIDENCE_PLATFORM,
            unified_journey_flag=active.ENABLE_UNIFIED_JOURNEY,
            publisher=experience_observation,
            evidence=evidence_platform,
            events=events,
        )
        if experience_observation is not None and experience_diagnostics is not None:
            experience_observation.bind_diagnostics(experience_diagnostics)
    # P2-MS008: Experience Feedback Loop DI (factual Home display only).
    # Independently controllable — reader constructed when flag ON; Evidence
    # sink may be None (load returns None until Evidence is available).
    if active.ENABLE_EXPERIENCE_FEEDBACK:
        from app.infrastructure.adapters.experience_feedback import (
            build_experience_feedback_reader,
        )

        experience_feedback = build_experience_feedback_reader(
            enabled=True,
            evidence=evidence_platform,
        )
    # EP-003.4: Learning Feedback Loop DI (observed behavioural evidence only).
    # Independently controllable — recorder constructed when flag ON; Runtime A
    # emitters fail-open when recorder is unbound or flag OFF.
    if active.ENABLE_LEARNING_FEEDBACK:
        from app.infrastructure.adapters.learning_feedback import (
            bind_learning_feedback_recorder,
            build_learning_feedback_recorder,
        )

        learning_feedback = build_learning_feedback_recorder(enabled=True)
        bind_learning_feedback_recorder(learning_feedback)
    # P2-MS009: Evidence Advisory Layer DI (Runtime A injection point only).
    # Independently controllable — injection constructed when flag ON; Evidence
    # port may be None (read returns None until Evidence is available).
    if active.ENABLE_EVIDENCE_ADVISORY:
        from app.services.evidence_advisory_injection import (
            build_runtime_a_evidence_advisory_injection,
        )

        evidence_advisory_injection = build_runtime_a_evidence_advisory_injection(
            enabled=True,
            port=evidence_platform,
        )
    # P2-MS010: Study Recovery Engine DI (Runtime A injection point only).
    # Independently controllable — adapter + injection constructed when flag ON.
    if active.ENABLE_RECOVERY_PLANNER:
        from app.infrastructure.adapters.recovery_planner import (
            build_study_recovery_planner_adapter,
        )
        from app.services.recovery_injection import (
            build_runtime_a_recovery_injection,
        )

        recovery_planner = build_study_recovery_planner_adapter(enabled=True)
        recovery_injection = build_runtime_a_recovery_injection(
            enabled=True,
            port=recovery_planner,
        )
    # P2-MS011: Advisory Decision Simulation DI (parallel comparison only).
    # Independently controllable — never modifies student-facing output.
    if active.ENABLE_DECISION_SIMULATION:
        from app.infrastructure.adapters.decision_simulation import (
            build_decision_simulation_service,
        )

        decision_simulation = build_decision_simulation_service(enabled=True)
    # P2-MS012: Advisory Evaluation Framework DI (ops / review only).
    # Independently controllable — never modifies Runtime A or student UX.
    if active.ENABLE_ADVISORY_EVALUATION:
        from app.infrastructure.adapters.advisory_evaluation import (
            build_advisory_evaluation_service,
        )

        advisory_evaluation = build_advisory_evaluation_service(enabled=True)
    # P3-MS001: Controlled Advisory Activation DI (single approved field).
    # Independently controllable — minimal rationale annotation only when
    # policy, flag, freshness, and rollout gates allow.
    if active.ENABLE_CONTROLLED_ADVISORY:
        from app.infrastructure.adapters.controlled_advisory import (
            build_controlled_advisory_activation,
        )

        controlled_advisory = build_controlled_advisory_activation(enabled=True)
    # P3-MS002: Advisory Outcome Measurement DI (ops observation only).
    # Independently controllable — never modifies Runtime A or ranking.
    if active.ENABLE_ADVISORY_OUTCOME_MEASUREMENT:
        from app.infrastructure.adapters.advisory_outcome import (
            build_advisory_outcome_measurement_service,
        )

        advisory_outcome_measurement = build_advisory_outcome_measurement_service(
            enabled=True
        )
    # P3-MS003 / P3-MS004: Recommendation Policy Framework (+ optional
    # policy-governed weight application). Independently controllable —
    # Runtime A may consult policy / apply one bounded weight rule;
    # Runtime A retains final recommendation authority.
    if active.ENABLE_RECOMMENDATION_POLICY or active.ENABLE_POLICY_WEIGHTING:
        from app.infrastructure.adapters.recommendation_policy import (
            build_recommendation_policy_engine,
        )

        recommendation_policy = build_recommendation_policy_engine(
            enabled=active.ENABLE_RECOMMENDATION_POLICY
            or active.ENABLE_POLICY_WEIGHTING,
            weighting_enabled=active.ENABLE_POLICY_WEIGHTING,
        )
    # P4-MS001: Controlled Educational Effectiveness Trial DI.
    # Independently controllable — deterministic cohort gate + operational
    # metrics / reporting; Runtime A remains sole educational authority.
    if active.ENABLE_EDUCATIONAL_TRIALS:
        from app.infrastructure.adapters.educational_trial import (
            build_educational_trial_service,
        )

        educational_trial = build_educational_trial_service(enabled=True)
    # P4-MS002: Longitudinal Learning Evidence Repository DI.
    # Independently controllable — append-only evidence storage only; never
    # passed into Runtime A recommendation paths or educational policy.
    if active.ENABLE_LONGITUDINAL_EVIDENCE:
        from app.infrastructure.adapters.longitudinal_evidence import (
            build_longitudinal_evidence_repository,
        )

        longitudinal_evidence = build_longitudinal_evidence_repository(enabled=True)
    # P4-MS003: Educational Evidence Review Workspace DI.
    # Independently controllable — read-only query / timeline / export over
    # longitudinal evidence; never passed into Runtime A recommendation paths.
    if active.ENABLE_EVIDENCE_REVIEW:
        from app.infrastructure.adapters.evidence_review import (
            build_evidence_query_service,
        )

        evidence_review = build_evidence_query_service(
            enabled=True,
            repository=longitudinal_evidence,
        )
    if active.ENABLE_ADAPTIVE_ENGINE or active.ENABLE_ADAPTIVE_ENGINE_SHADOW:
        from app.infrastructure.adapters.adaptive_engine import (
            FeatureFlagSnapshot,
            adaptive_experience_cutover_active,
            build_adaptive_engine_adapter,
            build_adaptive_engine_executor,
            build_adaptive_experience_port_router,
            build_adaptive_input_assembler,
            build_adaptive_shadow_orchestrator,
            build_explainability_gate,
            build_shadow_soak_orchestrator,
            build_traceability_service,
        )

        # A1/A2/A3: Assembler + Executor + Adapter (+ Shadow / Gate when flagged).
        # T4: optional TwinInputAdapter when KWALITEC_DIGITAL_TWIN is ON.
        adaptive_input_assembler = build_adaptive_input_assembler(
            enabled=True,
            twin_input=twin_input_adapter,
        )
        adaptive_executor = build_adaptive_engine_executor(enabled=True)
        adaptive_engine = build_adaptive_engine_adapter(
            enabled=True,
            input_assembler=adaptive_input_assembler,
            executor=adaptive_executor,
        )
        # A5 Observational Traceability follows Engine / Shadow flags (no
        # behavioural change; no educational persistence).
        adaptive_traceability = build_traceability_service(
            enabled=True,
            events=events,
            feature_flags=FeatureFlagSnapshot(
                engine_enabled=active.ENABLE_ADAPTIVE_ENGINE,
                shadow_enabled=active.ENABLE_ADAPTIVE_ENGINE_SHADOW,
                authority_enabled=active.ENABLE_ADAPTIVE_AUTHORITY,
            ),
            engine_version=(
                getattr(adaptive_executor, "EXECUTOR_VERSION", None) or "1.0.0-a2"
            ),
        )
        # A3 Explainability Gate requires both Engine and Shadow flags.
        if (
            active.ENABLE_ADAPTIVE_ENGINE
            and active.ENABLE_ADAPTIVE_ENGINE_SHADOW
        ):
            explainability_gate = build_explainability_gate(
                enabled=True,
                events=events,
            )
        if active.ENABLE_ADAPTIVE_ENGINE_SHADOW:
            adaptive_shadow = build_adaptive_shadow_orchestrator(
                enabled=True,
                assembler=adaptive_input_assembler,
                executor=adaptive_executor,
                events=events,
                explainability_gate=explainability_gate,
                traceability=adaptive_traceability,
            )
            # A6 Shadow Soak — observational compare/measure; never UX authority.
            adaptive_soak = build_shadow_soak_orchestrator(
                enabled=True,
                shadow=adaptive_shadow,
                events=events,
            )
        # A4: Experience AdaptiveDecisionPort cutover requires Engine + Shadow
        # + Authority (all default OFF). RecommendationService remains primary
        # unless authority is explicitly enabled.
        if adaptive_experience_cutover_active(
            engine_enabled=active.ENABLE_ADAPTIVE_ENGINE,
            shadow_enabled=active.ENABLE_ADAPTIVE_ENGINE_SHADOW,
            authority_enabled=active.ENABLE_ADAPTIVE_AUTHORITY,
        ):
            adaptive_port_router = build_adaptive_experience_port_router(
                enabled=True,
                assembler=adaptive_input_assembler,
                engine=adaptive_engine,
                gate=explainability_gate,
                events=events,
                traceability=adaptive_traceability,
            )
    composition = StudentExperienceComposition(
        store=projection_store,
        uow=projection_store.uow,
        events=events,
        diagnostics=diagnostics,
        learning_loop=None,
        enable_learning_loop=learning_loop,
        twin_engine=engines.get("twin_engine"),
        decision_engine=engines.get("decision_engine"),
        # When Mission / Completion Bridges are on, do not inject opaque mission
        # engine — Runtime A is sole educational authority for mission.
        mission_engine=(
            None
            if (
                mission_read is not None
                or mission_start is not None
                or mission_resume is not None
                or session_completion is not None
            )
            else engines.get("mission_engine")
        ),
        # When Journey Bridge is on, Runtime A is sole Journey authority.
        journey_engine=(
            None if journey_read is not None else engines.get("journey_engine")
        ),
        seed_demo_learners=seed,
        mission_read=mission_read,
        mission_start=mission_start,
        mission_resume=mission_resume,
        session_completion=session_completion,
        recommendation_read=recommendation_read,
        journey_read=journey_read,
        history_read=history_read,
        adaptive_engine=adaptive_engine,
        adaptive_input_assembler=adaptive_input_assembler,
        adaptive_shadow=adaptive_shadow,
        explainability_gate=explainability_gate,
        adaptive_port_router=adaptive_port_router,
        adaptive_traceability=adaptive_traceability,
        adaptive_soak=adaptive_soak,
        digital_twin=digital_twin,
        twin_facet_assembler=twin_facet_assembler,
        twin_snapshot_builder=twin_snapshot_builder,
        twin_explainability=twin_explainability,
        twin_input_adapter=twin_input_adapter,
        student_twin_projector=student_twin_projector,
        student_twin_projection_port=student_twin_projection_port,
        twin_shadow=twin_shadow,
        twin_foundation=twin_foundation,
        twin_authority=active.ENABLE_DIGITAL_TWIN_AUTHORITY,
        strategy_engine=strategy_engine,
        strategy_explainability=strategy_explainability,
        strategy_projector=strategy_projector,
        strategy_projection_port=strategy_projection_port,
        strategy_shadow=strategy_shadow,
        evidence_platform=evidence_platform,
        evidence_shadow=evidence_shadow,
        journey_coordinator=journey_coordinator,
        experience_observation=experience_observation,
        experience_diagnostics=experience_diagnostics,
        experience_feedback=experience_feedback,
        learning_feedback=learning_feedback,
        evidence_advisory_injection=evidence_advisory_injection,
        recovery_planner=recovery_planner,
        recovery_injection=recovery_injection,
        decision_simulation=decision_simulation,
        advisory_evaluation=advisory_evaluation,
        controlled_advisory=controlled_advisory,
        advisory_outcome_measurement=advisory_outcome_measurement,
        recommendation_policy=recommendation_policy,
        educational_trial=educational_trial,
        longitudinal_evidence=longitudinal_evidence,
        evidence_review=evidence_review,
    )
    if seed:
        composition.seed_learner("default", demo=True)
    return composition, composition.build_service()
