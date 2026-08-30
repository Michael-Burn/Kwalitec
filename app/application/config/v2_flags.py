"""Version 2 dual-run / cutover feature flags.

Environment-driven switches for coexistence until V2-020 retirement.
Safe defaults preserve Version 1 as the live educational path.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def _env_truthy(name: str, *, environ: dict[str, str] | None = None) -> bool:
    env = environ if environ is not None else os.environ
    return env.get(name, "").strip().lower() in _TRUTHY


@dataclass(frozen=True)
class Version2FeatureFlags:
    """Immutable Version 2 rollout switches (ADR-007 dual-run).

    Attributes:
        ENABLE_STUDENT_EXPERIENCE: Expose /student and dashboard entry link.
        ENABLE_DURABLE_STORE: Persist Experience/Session docs via SQLAlchemy.
        SEED_DEMO_LEARNERS: Auto-seed demo opaque projections (dev/demo only).
        INJECT_PHASE_I_ENGINES: Wire opaque engine bridges into adapters.
        ENABLE_MISSION_READ_BRIDGE: Experience Mission read → Runtime A SQL.
        ENABLE_MISSION_START_BRIDGE: Experience Mission start → Runtime A SQL.
        ENABLE_MISSION_RESUME_BRIDGE: Experience Mission resume → Runtime A SQL.
        ENABLE_SESSION_COMPLETION_BRIDGE: Experience session complete → Runtime A.
        ENABLE_RECOMMENDATION_BRIDGE: Experience recommendation read → Runtime A.
        ENABLE_JOURNEY_BRIDGE: Experience Journey read → Runtime A SQL.
        ENABLE_HISTORY_BRIDGE: Experience History read → Runtime A SQL.
        ENABLE_ADAPTIVE_ENGINE: Construct Adaptive Engine Adapter (MS-003 A0+).
        ENABLE_ADAPTIVE_ENGINE_SHADOW: Shadow Adaptive Engine compute (A2).
        ENABLE_ADAPTIVE_AUTHORITY: Experience may serve eligible adaptive
            recommendations as authoritative (A4; requires Engine + Shadow).
        ENABLE_DIGITAL_TWIN: Construct Digital Twin Adapter / contracts
            (MS-004 T0–T5; Experience projection port available; no Experience
            UX authority cutover; Adaptive may consume Twin read-only when ON).
            Also constructs EP-001.1 Student Digital Twin Foundation DI.
        ENABLE_DIGITAL_TWIN_AUTHORITY: Experience StudentTwinPort serves
            Runtime-A-grounded Twin Foundation (EP-001.1; requires
            ENABLE_DIGITAL_TWIN; default OFF; falls back to ExperienceTwinAdapter).
        ENABLE_STUDY_INSIGHTS_CUTOVER: EP-002.5 gated HTTP cutover — dashboard /
            home may serve Twin ``build_study_insights`` projection when Twin
            is ON in approved non-production environments (default OFF;
            legacy ``generate_recommendations`` remains fail-open fallback;
            no production-wide activation).
        ENABLE_READINESS_INTELLIGENCE_CUTOVER: EP-002.6 gated HTTP cutover —
            dashboard / analytics may serve Twin
            ``build_readiness_intelligence`` projection when Twin is ON in
            approved non-production environments (default OFF; legacy
            readiness surface remains fail-open fallback; collectors continue
            to use pure ``get_overall_readiness``; no production-wide
            activation).
        ENABLE_DAILY_PLAN_CUTOVER: EP-002.7 gated HTTP cutover — dashboard /
            mission surfaces may serve Twin ``build_daily_study_plan``
            projection when Twin is ON in approved non-production
            environments (default OFF; legacy ``generate_today_mission``
            remains fail-open fallback and sole ORM persistence authority;
            MissionOptimizer remains quarantined; no production-wide
            activation).
        ENABLE_STRATEGY_ENGINE: Construct Strategy Engine + assembler + planners
            + explainability + Experience projection port (MS-005 S0–S2; no
            Experience authority cutover, shadow validation, or Runtime A /
            Twin / Adaptive mutation).
        ENABLE_EVIDENCE_PLATFORM: Construct Learning Evidence Platform
            contracts / collector / assembler / factory / experiment /
            policy evaluation / analytics aggregation / governance
            projection DI (MS-006 E0–E4; observational only — no
            persistence, policy promotion, or educational writes).
        ENABLE_UNIFIED_JOURNEY: Experience Layer Unified Student Journey
            Framework (P2-MS001–P2-MS004) — Journey Coordinator, stage
            navigation, Daily Mission, DayExperience guided study session,
            and Home primary-mission architecture (default OFF; no
            educational logic, Runtime A / Adaptive / Strategy / Evidence /
            Twin modifications, or persistence).
        ENABLE_EXPERIENCE_OBSERVATION: Experience Observation Bridge
            (P2-MS006) — assemble / publish immutable ExperienceObservation
            records to the Learning Evidence Platform public intake surface
            (default OFF; independently controllable from
            ENABLE_EVIDENCE_PLATFORM; no educational interpretation,
            persistence, or authority changes).
        ENABLE_EXPERIENCE_DIAGNOSTICS: Experience Observability & Diagnostics
            (P2-MS007) — JourneyTrace, observation counters, pipeline health,
            structured operational logs, and internal diagnostics dashboard
            DTOs (default OFF; independently controllable from all other
            flags; no educational authority, persistence, or student UX).
        ENABLE_EXPERIENCE_FEEDBACK: Experience Feedback Loop (P2-MS008) —
            surface factual Evidence read-model summaries on Home ("Your
            Journey") when Unified Journey is also enabled (default OFF;
            independently controllable; display-only — no adaptation,
            recommendation changes, or behavioural optimisation).
        ENABLE_LEARNING_FEEDBACK: Learning Feedback Loop (EP-003.4) —
            record observed student interactions with plans, recommendations,
            and study activities as behavioural evidence only (default OFF;
            independently controllable; no educational decision-making,
            Twin writes, or Runtime A authority changes).
        ENABLE_PERSONAL_LEARNING_PROFILE: Personal Learning Profile (EP-004.1) —
            aggregate observed Learning Feedback evidence into an explainable
            long-term behavioural profile (default OFF; independently
            controllable; summarises evidence only — never ranks, plans,
            scores readiness, or owns educational decisions).
        ENABLE_EVIDENCE_ADVISORY: Evidence Advisory Layer (P2-MS009) —
            expose factual EvidenceAdvisory inputs to Runtime A through
            EvidenceAdvisoryPort + Runtime A injection point (default OFF;
            independently controllable; integration point only — no
            recommendation behaviour change, scoring, or predictions).
        ENABLE_RECOVERY_PLANNER: Study Recovery Engine (P2-MS010) —
            expose RecoveryPlannerPort + RecoveryPlanCandidate advisory
            placeholders to Runtime A (default OFF; independently
            controllable; architecture only — no recovery algorithms,
            schedule optimisation, or recommendation behaviour change).
        ENABLE_DECISION_SIMULATION: Advisory Decision Simulation (P2-MS011) —
            parallel simulation path comparing production Runtime A
            recommendations against advisory-informed structural simulations
            (default OFF; independently controllable; comparison /
            explainability only — never modifies student-facing output).
        ENABLE_ADVISORY_EVALUATION: Advisory Evaluation Framework (P2-MS012) —
            score and analyse simulated recommendation differences for
            actuarial / educational review (default OFF; independently
            controllable; operational metrics only — never modifies Runtime A
            or student-facing behaviour).
        ENABLE_CONTROLLED_ADVISORY: Controlled Advisory Activation (P3-MS001) —
            permit Runtime A to consume exactly one approved Evidence
            Advisory field under policy / freshness / rollout governance
            (default OFF; independently controllable; minimal rationale
            annotation only — reversible; simulation comparison retained).
        ENABLE_ADVISORY_OUTCOME_MEASUREMENT: Advisory Outcome Measurement
            (P3-MS002) — collect operational rollout outcomes and metrics for
            Controlled Advisory Activation (default OFF; independently
            controllable; observation only — never modifies Runtime A,
            ranking, or educational scoring).
        ENABLE_RECOMMENDATION_POLICY: Recommendation Policy Framework
            (P3-MS003) — declarative, versioned policy for when / how
            approved advisory information may influence Runtime A
            recommendations (default OFF; independently controllable;
            policy external to recommendation logic — Runtime A remains sole
            authority).
        ENABLE_POLICY_WEIGHTING: Policy-Governed Weight Application
            (P3-MS004) — permit Runtime A to apply exactly one approved,
            bounded weighting rule (consistency_summary only) under policy /
            freshness / rollout governance (default OFF; independently
            controllable; reversible; Runtime A retains final authority).
        ENABLE_EDUCATIONAL_TRIALS: Controlled Educational Effectiveness Trial
            (P4-MS001) — operational trial framework comparing baseline
            recommendations with policy-weighted recommendations under
            deterministic cohort rollout (default OFF; independently
            controllable; no additional advisory fields; Runtime A remains
            sole educational authority; reversible).
        ENABLE_LONGITUDINAL_EVIDENCE: Longitudinal Learning Evidence Repository
            (P4-MS002) — append-only storage of educational observations
            across sessions / missions / reflections / advisory / trials
            (default OFF; independently controllable; evidence storage only —
            never influences Runtime A, Adaptive, Recovery, or policy).
        ENABLE_EVIDENCE_REVIEW: Educational Evidence Review Workspace
            (P4-MS003) — read-only query / timeline / export over longitudinal
            evidence for human inspection (default OFF; independently
            controllable; never modifies Runtime A, recommendations, policy,
            or educational behaviour).
        SOLE_RUNTIME: Route default home to /student (V2-020 gated cutover).
        ENABLE_FOUNDER_INTELLIGENCE: Show journey-level Founder Intelligence.
    """

    ENABLE_STUDENT_EXPERIENCE: bool = False
    ENABLE_DURABLE_STORE: bool = False
    SEED_DEMO_LEARNERS: bool = True
    INJECT_PHASE_I_ENGINES: bool = False
    ENABLE_MISSION_READ_BRIDGE: bool = False
    ENABLE_MISSION_START_BRIDGE: bool = False
    ENABLE_MISSION_RESUME_BRIDGE: bool = False
    ENABLE_SESSION_COMPLETION_BRIDGE: bool = False
    ENABLE_RECOMMENDATION_BRIDGE: bool = False
    ENABLE_JOURNEY_BRIDGE: bool = False
    ENABLE_HISTORY_BRIDGE: bool = False
    ENABLE_ADAPTIVE_ENGINE: bool = False
    ENABLE_ADAPTIVE_ENGINE_SHADOW: bool = False
    ENABLE_ADAPTIVE_AUTHORITY: bool = False
    ENABLE_DIGITAL_TWIN: bool = False
    ENABLE_DIGITAL_TWIN_AUTHORITY: bool = False
    ENABLE_STUDY_INSIGHTS_CUTOVER: bool = False
    ENABLE_READINESS_INTELLIGENCE_CUTOVER: bool = False
    ENABLE_DAILY_PLAN_CUTOVER: bool = False
    ENABLE_STRATEGY_ENGINE: bool = False
    ENABLE_EVIDENCE_PLATFORM: bool = False
    ENABLE_UNIFIED_JOURNEY: bool = False
    ENABLE_EXPERIENCE_OBSERVATION: bool = False
    ENABLE_EXPERIENCE_DIAGNOSTICS: bool = False
    ENABLE_EXPERIENCE_FEEDBACK: bool = False
    ENABLE_LEARNING_FEEDBACK: bool = False
    ENABLE_PERSONAL_LEARNING_PROFILE: bool = False
    ENABLE_EVIDENCE_ADVISORY: bool = False
    ENABLE_RECOVERY_PLANNER: bool = False
    ENABLE_DECISION_SIMULATION: bool = False
    ENABLE_ADVISORY_EVALUATION: bool = False
    ENABLE_CONTROLLED_ADVISORY: bool = False
    ENABLE_ADVISORY_OUTCOME_MEASUREMENT: bool = False
    ENABLE_RECOMMENDATION_POLICY: bool = False
    ENABLE_POLICY_WEIGHTING: bool = False
    ENABLE_EDUCATIONAL_TRIALS: bool = False
    ENABLE_LONGITUDINAL_EVIDENCE: bool = False
    ENABLE_EVIDENCE_REVIEW: bool = False
    SOLE_RUNTIME: bool = False
    ENABLE_FOUNDER_INTELLIGENCE: bool = False
    # RI-001: Preferred Authority routing (default ON). Explicitly set
    # KWALITEC_RUNTIME_INTEGRATION=0/false/off to force Runtime A only.
    ENABLE_RUNTIME_INTEGRATION: bool = True
        # SR-001A P0 / MISSION-002: mission brief coherence (selection + presentation).
    # Default ON after MISSION-002; set SR_MISSION_BRIEF_COHERENCE=0 to roll back
    # presentation/selection behaviour in emergency (prefer code revert).
    SR_MISSION_BRIEF_COHERENCE: bool = True
    # KWP-002: Commercial Loop Profile — one switch enables the SR student-value
    # bundle (Session Primary + Substance + Completion Product + Evidence Gate +
    # Twin daily loop + Progress singularity). Individual SR_* env vars still
    # override when set. Default OFF in bare process; production sets
    # KWALITEC_COMMERCIAL_LOOP=1 (see render.yaml).
    SR_COMMERCIAL_LOOP: bool = False
    # SR-001A P1 / SR-002: Home Primary → Start/Resume Session → /session/*.
    # Default OFF unless Commercial Loop is ON; set SR_SESSION_PRIMARY=1/0
    # to force. When OFF, Runtime C Mark-complete Primary is restored (rollback).
    SR_SESSION_PRIMARY: bool = False
    # SR-001A P1 emergency/accessibility Mark-complete when session primary is ON.
    # Never default ON after P1; labelled non-product when exposed.
    # Never enabled by Commercial Loop.
    SR_PILOT_MARK_COMPLETE: bool = False
    # SR-001A P2 / LXP-003: Session product completion (pause/resume, finish review).
    # Default OFF unless Commercial Loop is ON.
    # When ON, Finish Review (Yes/Partially/No) is required before session close.
    SR_SESSION_COMPLETION_PRODUCT: bool = False
    # SR-001A P3 / LXP-004A: Session educational substance (Read → Practice → Reflect).
    # Default OFF unless Commercial Loop is ON.
    SR_SESSION_SUBSTANCE: bool = False
    # SR-001A P4 / EV-001B: Evidence Before Completion gate.
    # Default OFF unless Commercial Loop is ON.
    SR_EVIDENCE_GATE: bool = False
    # SR-001A P5 / SDT-004: Twin daily-loop activation.
    # Default OFF unless Commercial Loop is ON.
    # Twin observes Accepted Educational+ only — never evaluates evidence.
    SR_TWIN_DAILY_LOOP: bool = False
    # SR-001A P6 / SR-003: Progress singularity — one Progress Engine.
    # Default OFF unless Commercial Loop is ON.
    SR_PROGRESS_SINGULARITY: bool = False
    # Phase 1 runtime-identity unification: Accept-time SQL evidence-companion
    # Mission for Runtime C sittings (StudyAttempt substrate only).
    # Default OFF; never inherited from Commercial Loop. Explicit env only.
    SR_SESSION_SQL_EVIDENCE_COMPANION: bool = False
    # ADR-027 M0: Adaptive Decision Engine boundary for Runtime C daily sitting.
    # Default OFF; never inherited from Commercial Loop. Explicit env only.
    # When ON, EducationalExperienceService routes through
    # SittingDecisionOrchestrator + Policy V0; Runtime C materialises only.
    ADR027_M0_DECISION_BOUNDARY: bool = False
    # ADR-027 Phase 2 Stage 2: atomic Twin cutover for Estimated Knowledge.
    # Default OFF; never inherited from Commercial Loop. Explicit env only.
    # When ON: Stack A/C EK writes are skipped AND §4.1 readers use
    # LearnerTwinQueryPort. Writers and readers share this single flag so
    # writes never stop while readers still expect A/C updates.
    ADR027_PHASE2_TWIN_CUTOVER: bool = False


_FALSY = frozenset({"0", "false", "no", "off"})


def _env_default_true(name: str, *, environ: dict[str, str] | None = None) -> bool:
    """Truthy by default; only False when explicitly set to a falsy token."""
    env = environ if environ is not None else os.environ
    raw = env.get(name)
    if raw is None or str(raw).strip() == "":
        return True
    return str(raw).strip().lower() not in _FALSY


def resolve_v2_feature_flags(
    *,
    environ: dict[str, str] | None = None,
) -> Version2FeatureFlags:
    """Resolve Version 2 flags from the process environment."""
    durable = _env_truthy("KWALITEC_V2_DURABLE_STORE", environ=environ)
    sole = _env_truthy("KWALITEC_V2_SOLE_RUNTIME", environ=environ)
    student = _env_truthy("KWALITEC_V2_STUDENT_EXPERIENCE", environ=environ) or sole
    umbrella = _env_truthy("KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE", environ=environ)
    continuity = _env_truthy(
        "KWALITEC_EDUCATIONAL_CONTINUITY_BRIDGE", environ=environ
    )
    mission_read = (
        _env_truthy("KWALITEC_MISSION_READ_BRIDGE", environ=environ) or umbrella
    )
    mission_start = (
        _env_truthy("KWALITEC_MISSION_START_BRIDGE", environ=environ) or umbrella
    )
    mission_resume = (
        _env_truthy("KWALITEC_MISSION_RESUME_BRIDGE", environ=environ) or umbrella
    )
    session_completion = (
        _env_truthy("KWALITEC_SESSION_COMPLETION_BRIDGE", environ=environ)
        or umbrella
    )
    recommendation = (
        _env_truthy("KWALITEC_RECOMMENDATION_BRIDGE", environ=environ) or umbrella
    )
    journey = (
        _env_truthy("KWALITEC_JOURNEY_BRIDGE", environ=environ)
        or continuity
        or umbrella
    )
    history = (
        _env_truthy("KWALITEC_HISTORY_BRIDGE", environ=environ)
        or continuity
        or umbrella
    )
    adaptive_umbrella = _env_truthy(
        "KWALITEC_ADAPTIVE_INTELLIGENCE", environ=environ
    )
    adaptive_engine = (
        _env_truthy("KWALITEC_ADAPTIVE_ENGINE", environ=environ) or adaptive_umbrella
    )
    # Directive 004 names KWALITEC_ADAPTIVE_SHADOW; keep ENGINE_SHADOW alias.
    adaptive_shadow = (
        _env_truthy("KWALITEC_ADAPTIVE_SHADOW", environ=environ)
        or _env_truthy("KWALITEC_ADAPTIVE_ENGINE_SHADOW", environ=environ)
    )
    # A4: adaptive authority is independent and defaults OFF.
    adaptive_authority = _env_truthy(
        "KWALITEC_ADAPTIVE_AUTHORITY", environ=environ
    )
    # MS-004 T0–T5: Digital Twin contracts / adapter DI, facet synthesis,
    # snapshot assembly, explainability, Adaptive Twin-input consumption, and
    # Experience Twin projection (default OFF). No Experience UX authority
    # cutover / Twin persistence.
    digital_twin = _env_truthy("KWALITEC_DIGITAL_TWIN", environ=environ)
    # EP-001.1: Twin Authority — Experience StudentTwinPort serves Foundation
    # (requires Digital Twin ON; default OFF).
    digital_twin_authority = _env_truthy(
        "KWALITEC_DIGITAL_TWIN_AUTHORITY", environ=environ
    ) and digital_twin
    # EP-002.5: gated Study Insights HTTP cutover on dashboard/home (requires
    # Digital Twin ON; default OFF; production env still ineligible in cutover
    # eligibility helper; legacy recommendations remain fail-open fallback).
    study_insights_cutover = (
        _env_truthy("KWALITEC_STUDY_INSIGHTS_CUTOVER", environ=environ)
        and digital_twin
    )
    # EP-002.6: gated Readiness Intelligence HTTP cutover on dashboard/analytics
    # (requires Digital Twin ON; default OFF; production env still ineligible;
    # legacy readiness surface remains fail-open; collectors stay on legacy
    # getters).
    readiness_intelligence_cutover = (
        _env_truthy("KWALITEC_READINESS_INTELLIGENCE_CUTOVER", environ=environ)
        and digital_twin
    )
    # EP-002.7: gated Daily Plan / mission HTTP cutover on dashboard/missions
    # (requires Digital Twin ON; default OFF; production env still ineligible;
    # legacy generate_today_mission remains fail-open; MissionOptimizer stays
    # quarantined).
    daily_plan_cutover = (
        _env_truthy("KWALITEC_DAILY_PLAN_CUTOVER", environ=environ) and digital_twin
    )
    # MS-005 S0–S2: Strategy Engine contracts / core orchestration /
    # explainability / Experience projection DI (default OFF). No Experience
    # authority cutover, shadow validation, or upstream mutation.
    strategy_engine = _env_truthy("KWALITEC_STRATEGY_ENGINE", environ=environ)
    # MS-006 E0: Learning Evidence Platform contracts / adapter DI (default
    # OFF). No intake, experiment execution, policy evaluation behaviour,
    # analytics aggregation, persistence, or educational writes.
    evidence_platform = _env_truthy(
        "KWALITEC_EVIDENCE_PLATFORM", environ=environ
    )
    # P2-MS001: Unified Student Journey Framework (Experience orchestration
    # only; default OFF — preserves feature-oriented navigation).
    unified_journey = _env_truthy(
        "KWALITEC_UNIFIED_JOURNEY", environ=environ
    )
    # P2-MS006: Experience Observation Bridge (default OFF). Independently
    # controllable from ENABLE_EVIDENCE_PLATFORM — publisher may be wired
    # without an Evidence sink (publish skips until Evidence is available).
    experience_observation = _env_truthy(
        "KWALITEC_EXPERIENCE_OBSERVATION", environ=environ
    )
    # P2-MS007: Experience Observability & Diagnostics (default OFF).
    # Independently controllable from observation / evidence / journey flags.
    experience_diagnostics = _env_truthy(
        "KWALITEC_EXPERIENCE_DIAGNOSTICS", environ=environ
    )
    # P2-MS008: Experience Feedback Loop (default OFF). Independently
    # controllable — Home factual display only when Unified Journey is also ON.
    experience_feedback = _env_truthy(
        "KWALITEC_EXPERIENCE_FEEDBACK", environ=environ
    )
    # EP-003.4: Learning Feedback Loop (default OFF). Independently
    # controllable — records observed behavioural evidence only; never
    # adapts recommendations, readiness, or plans.
    learning_feedback = _env_truthy(
        "KWALITEC_LEARNING_FEEDBACK", environ=environ
    )
    # EP-004.1: Personal Learning Profile (default OFF). Independently
    # controllable — summarises observed behavioural evidence only; never
    # becomes an educational decision authority.
    personal_learning_profile = _env_truthy(
        "KWALITEC_PERSONAL_LEARNING_PROFILE", environ=environ
    )
    # P2-MS009: Evidence Advisory Layer (default OFF). Independently
    # controllable — Runtime A may read advisory inputs; no behaviour change.
    evidence_advisory = _env_truthy(
        "KWALITEC_EVIDENCE_ADVISORY", environ=environ
    )
    # P2-MS010: Study Recovery Engine (default OFF). Independently
    # controllable — Runtime A may read advisory recovery candidates; no
    # behaviour change, algorithms, or schedule optimisation.
    recovery_planner = _env_truthy(
        "KWALITEC_RECOVERY_PLANNER", environ=environ
    )
    # P2-MS011: Advisory Decision Simulation (default OFF). Independently
    # controllable — parallel comparison path only; never modifies production
    # recommendations returned to the student.
    decision_simulation = _env_truthy(
        "KWALITEC_DECISION_SIMULATION", environ=environ
    )
    # P2-MS012: Advisory Evaluation Framework (default OFF). Independently
    # controllable — operational scoring / review of simulation differences
    # only; never modifies Runtime A or student-facing behaviour.
    advisory_evaluation = _env_truthy(
        "KWALITEC_ADVISORY_EVALUATION", environ=environ
    )
    # P3-MS001: Controlled Advisory Activation (default OFF). Independently
    # controllable — Runtime A may consume one approved advisory field under
    # policy / freshness / rollout gating; reversible via flag.
    controlled_advisory = _env_truthy(
        "KWALITEC_CONTROLLED_ADVISORY", environ=environ
    )
    # P3-MS002: Advisory Outcome Measurement (default OFF). Independently
    # controllable — operational rollout observations / metrics only; never
    # modifies Runtime A behaviour, ranking, or educational scoring.
    advisory_outcome_measurement = _env_truthy(
        "KWALITEC_ADVISORY_OUTCOME_MEASUREMENT", environ=environ
    )
    # P3-MS003: Recommendation Policy Framework (default OFF). Independently
    # controllable — declarative policy resolution / explainability;
    # Runtime A retains final recommendation authority.
    recommendation_policy = _env_truthy(
        "KWALITEC_RECOMMENDATION_POLICY", environ=environ
    )
    # P3-MS004: Policy-Governed Weight Application (default OFF). Independently
    # controllable — exactly one bounded weighting rule
    # (consistency_summary); reversible via flag; Runtime A remains authority.
    policy_weighting = _env_truthy(
        "KWALITEC_POLICY_WEIGHTING", environ=environ
    )
    # P4-MS001: Controlled Educational Effectiveness Trial (default OFF).
    # Independently controllable — deterministic cohort comparison of baseline
    # vs policy-weighted recommendations; no additional advisory fields;
    # Runtime A remains sole educational authority; reversible via flag.
    educational_trials = _env_truthy(
        "KWALITEC_EDUCATIONAL_TRIALS", environ=environ
    )
    # P4-MS002: Longitudinal Learning Evidence Repository (default OFF).
    # Independently controllable — append-only evidence storage only; never
    # influences Runtime A, Adaptive, Recovery, or educational policy.
    longitudinal_evidence = _env_truthy(
        "KWALITEC_LONGITUDINAL_EVIDENCE", environ=environ
    )
    # P4-MS003: Educational Evidence Review Workspace (default OFF).
    # Independently controllable — read-only query / timeline / export over
    # longitudinal evidence; never modifies Runtime A, recommendations,
    # policy, or educational behaviour.
    evidence_review = _env_truthy(
        "KWALITEC_EVIDENCE_REVIEW", environ=environ
    )
    # Production dual-run should not seed demo learners when durable store is on
    # unless explicitly requested.
    seed_explicit = environ.get("KWALITEC_V2_SEED_DEMO") if environ else None
    if seed_explicit is None and environ is None:
        seed_explicit = os.environ.get("KWALITEC_V2_SEED_DEMO")
    if seed_explicit is not None and str(seed_explicit).strip() != "":
        seed = str(seed_explicit).strip().lower() in _TRUTHY
    else:
        seed = not durable
    # Educational Runtime / Continuity Bridges demote demo seed for auth paths.
    if (
        mission_read
        or mission_start
        or mission_resume
        or session_completion
        or recommendation
        or journey
        or history
    ) and seed_explicit is None:
        seed = False
    return Version2FeatureFlags(
        ENABLE_STUDENT_EXPERIENCE=student,
        ENABLE_DURABLE_STORE=durable,
        SEED_DEMO_LEARNERS=seed,
        INJECT_PHASE_I_ENGINES=_env_truthy(
            "KWALITEC_V2_INJECT_ENGINES", environ=environ
        )
        or durable,
        ENABLE_MISSION_READ_BRIDGE=mission_read,
        ENABLE_MISSION_START_BRIDGE=mission_start,
        ENABLE_MISSION_RESUME_BRIDGE=mission_resume,
        ENABLE_SESSION_COMPLETION_BRIDGE=session_completion,
        ENABLE_RECOMMENDATION_BRIDGE=recommendation,
        ENABLE_JOURNEY_BRIDGE=journey,
        ENABLE_HISTORY_BRIDGE=history,
        ENABLE_ADAPTIVE_ENGINE=adaptive_engine,
        ENABLE_ADAPTIVE_ENGINE_SHADOW=adaptive_shadow,
        ENABLE_ADAPTIVE_AUTHORITY=adaptive_authority,
        ENABLE_DIGITAL_TWIN=digital_twin,
        ENABLE_DIGITAL_TWIN_AUTHORITY=digital_twin_authority,
        ENABLE_STUDY_INSIGHTS_CUTOVER=study_insights_cutover,
        ENABLE_READINESS_INTELLIGENCE_CUTOVER=readiness_intelligence_cutover,
        ENABLE_DAILY_PLAN_CUTOVER=daily_plan_cutover,
        ENABLE_STRATEGY_ENGINE=strategy_engine,
        ENABLE_EVIDENCE_PLATFORM=evidence_platform,
        ENABLE_UNIFIED_JOURNEY=unified_journey,
        ENABLE_EXPERIENCE_OBSERVATION=experience_observation,
        ENABLE_EXPERIENCE_DIAGNOSTICS=experience_diagnostics,
        ENABLE_EXPERIENCE_FEEDBACK=experience_feedback,
        ENABLE_LEARNING_FEEDBACK=learning_feedback,
        ENABLE_PERSONAL_LEARNING_PROFILE=personal_learning_profile,
        ENABLE_EVIDENCE_ADVISORY=evidence_advisory,
        ENABLE_RECOVERY_PLANNER=recovery_planner,
        ENABLE_DECISION_SIMULATION=decision_simulation,
        ENABLE_ADVISORY_EVALUATION=advisory_evaluation,
        ENABLE_CONTROLLED_ADVISORY=controlled_advisory,
        ENABLE_ADVISORY_OUTCOME_MEASUREMENT=advisory_outcome_measurement,
        ENABLE_RECOMMENDATION_POLICY=recommendation_policy,
        ENABLE_POLICY_WEIGHTING=policy_weighting,
        ENABLE_EDUCATIONAL_TRIALS=educational_trials,
        ENABLE_LONGITUDINAL_EVIDENCE=longitudinal_evidence,
        ENABLE_EVIDENCE_REVIEW=evidence_review,
        SOLE_RUNTIME=sole,
        ENABLE_FOUNDER_INTELLIGENCE=_env_truthy(
            "KWALITEC_V2_FOUNDER_INTELLIGENCE", environ=environ
        ),
        ENABLE_RUNTIME_INTEGRATION=_env_default_true(
            "KWALITEC_RUNTIME_INTEGRATION", environ=environ
        ),
        SR_MISSION_BRIEF_COHERENCE=_env_default_true(
            "SR_MISSION_BRIEF_COHERENCE", environ=environ
        ),
        SR_COMMERCIAL_LOOP=_commercial_loop_enabled(environ=environ),
        SR_SESSION_PRIMARY=_sr_bundle_flag(
            "SR_SESSION_PRIMARY", environ=environ
        ),
        SR_PILOT_MARK_COMPLETE=_env_truthy(
            "SR_PILOT_MARK_COMPLETE", environ=environ
        ),
        SR_SESSION_COMPLETION_PRODUCT=_sr_bundle_flag(
            "SR_SESSION_COMPLETION_PRODUCT", environ=environ
        ),
        SR_SESSION_SUBSTANCE=_sr_bundle_flag(
            "SR_SESSION_SUBSTANCE", environ=environ
        ),
        SR_EVIDENCE_GATE=_sr_bundle_flag("SR_EVIDENCE_GATE", environ=environ),
        SR_TWIN_DAILY_LOOP=_sr_bundle_flag(
            "SR_TWIN_DAILY_LOOP", environ=environ
        ),
        SR_PROGRESS_SINGULARITY=_sr_bundle_flag(
            "SR_PROGRESS_SINGULARITY", environ=environ
        ),
        SR_SESSION_SQL_EVIDENCE_COMPANION=_env_truthy(
            "SR_SESSION_SQL_EVIDENCE_COMPANION", environ=environ
        ),
        ADR027_M0_DECISION_BOUNDARY=_env_truthy(
            "KWALITEC_ADR027_M0_DECISION_BOUNDARY", environ=environ
        ),
        ADR027_PHASE2_TWIN_CUTOVER=_env_truthy(
            "KWALITEC_ADR027_PHASE2_TWIN_CUTOVER", environ=environ
        ),
    )


def _commercial_loop_enabled(*, environ: dict[str, str] | None = None) -> bool:
    """KWP-002 Commercial Loop Profile master switch.

    Explicit ``KWALITEC_COMMERCIAL_LOOP`` / ``SR_COMMERCIAL_LOOP`` wins.
    When unset, sole-runtime production (G1) inherits ON so students get
    Start Session → practice → reflection instead of Confirm-only rollback.
    """
    env = environ if environ is not None else os.environ
    for key in ("KWALITEC_COMMERCIAL_LOOP", "SR_COMMERCIAL_LOOP"):
        raw = env.get(key)
        if raw is not None and str(raw).strip() != "":
            return str(raw).strip().lower() in _TRUTHY
    return _env_truthy("KWALITEC_V2_SOLE_RUNTIME", environ=environ)


def _sr_bundle_flag(name: str, *, environ: dict[str, str] | None = None) -> bool:
    """Resolve an SR student-value flag, inheriting Commercial Loop when unset.

    Explicit env tokens win. When the variable is absent, Commercial Loop ON
    enables the flag. Pilot Mark-complete is never inherited this way.
    """
    env = environ if environ is not None else os.environ
    raw = env.get(name)
    if raw is not None and str(raw).strip() != "":
        return str(raw).strip().lower() in _TRUTHY
    return _commercial_loop_enabled(environ=environ)


# Process default — resolved at import for convenience; prefer resolve_* in apps.
V2_FEATURE_FLAGS = resolve_v2_feature_flags()
