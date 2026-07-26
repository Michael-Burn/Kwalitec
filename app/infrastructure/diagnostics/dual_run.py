"""Dual-run observability helpers for Version 2 coexistence (ADR-007)."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.config.v2_flags import (
    Version2FeatureFlags,
    resolve_v2_feature_flags,
)


@dataclass(frozen=True)
class DualRunStatus:
    """Operational dual-run status for Founder / ops surfaces."""

    student_experience_enabled: bool
    durable_store: bool
    seed_demo: bool
    engines_injected: bool
    mission_read_bridge: bool
    mission_start_bridge: bool
    mission_resume_bridge: bool
    session_completion_bridge: bool
    recommendation_bridge: bool
    journey_bridge: bool
    history_bridge: bool
    adaptive_engine: bool
    adaptive_engine_shadow: bool
    adaptive_authority: bool
    adaptive_shadow_soak: bool
    digital_twin: bool
    strategy_engine: bool
    evidence_platform: bool
    unified_journey: bool
    experience_observation: bool
    experience_diagnostics: bool
    experience_feedback: bool
    learning_feedback: bool
    personal_learning_profile: bool
    evidence_advisory: bool
    recovery_planner: bool
    decision_simulation: bool
    advisory_evaluation: bool
    controlled_advisory: bool
    advisory_outcome_measurement: bool
    recommendation_policy: bool
    policy_weighting: bool
    educational_trials: bool
    longitudinal_evidence: bool
    evidence_review: bool
    sole_runtime: bool
    founder_intelligence: bool
    label: str
    ready_for_cutover_checklist: tuple[str, ...]


def build_dual_run_status(
    *,
    flags: Version2FeatureFlags | None = None,
) -> DualRunStatus:
    """Project dual-run feature flags into an ops-facing status."""
    active = flags or resolve_v2_feature_flags()
    if active.SOLE_RUNTIME:
        label = "sole-runtime-v2"
    elif active.ENABLE_STUDENT_EXPERIENCE:
        label = "dual-run-active"
    else:
        label = "v1-primary"
    checklist = (
        "Persistence + adapters stable in production dual-run",
        "Student path explainable end-to-end on V2",
        "No unresolved dual-authority defects",
        "Founder Studio operable over Management/Ingestion",
        "Product Strategy evidence gates satisfied",
        "V2-020 retirement runbook executed",
    )
    return DualRunStatus(
        student_experience_enabled=active.ENABLE_STUDENT_EXPERIENCE,
        durable_store=active.ENABLE_DURABLE_STORE,
        seed_demo=active.SEED_DEMO_LEARNERS,
        engines_injected=active.INJECT_PHASE_I_ENGINES,
        mission_read_bridge=active.ENABLE_MISSION_READ_BRIDGE,
        mission_start_bridge=active.ENABLE_MISSION_START_BRIDGE,
        mission_resume_bridge=active.ENABLE_MISSION_RESUME_BRIDGE,
        session_completion_bridge=active.ENABLE_SESSION_COMPLETION_BRIDGE,
        recommendation_bridge=active.ENABLE_RECOMMENDATION_BRIDGE,
        journey_bridge=active.ENABLE_JOURNEY_BRIDGE,
        history_bridge=active.ENABLE_HISTORY_BRIDGE,
        adaptive_engine=active.ENABLE_ADAPTIVE_ENGINE,
        adaptive_engine_shadow=active.ENABLE_ADAPTIVE_ENGINE_SHADOW,
        adaptive_authority=active.ENABLE_ADAPTIVE_AUTHORITY,
        # A6 soak DI follows Shadow flag (observational; no new authority flag).
        adaptive_shadow_soak=active.ENABLE_ADAPTIVE_ENGINE_SHADOW,
        digital_twin=active.ENABLE_DIGITAL_TWIN,
        strategy_engine=active.ENABLE_STRATEGY_ENGINE,
        evidence_platform=active.ENABLE_EVIDENCE_PLATFORM,
        unified_journey=active.ENABLE_UNIFIED_JOURNEY,
        experience_observation=active.ENABLE_EXPERIENCE_OBSERVATION,
        experience_diagnostics=active.ENABLE_EXPERIENCE_DIAGNOSTICS,
        experience_feedback=active.ENABLE_EXPERIENCE_FEEDBACK,
        learning_feedback=active.ENABLE_LEARNING_FEEDBACK,
        personal_learning_profile=active.ENABLE_PERSONAL_LEARNING_PROFILE,
        evidence_advisory=active.ENABLE_EVIDENCE_ADVISORY,
        recovery_planner=active.ENABLE_RECOVERY_PLANNER,
        decision_simulation=active.ENABLE_DECISION_SIMULATION,
        advisory_evaluation=active.ENABLE_ADVISORY_EVALUATION,
        controlled_advisory=active.ENABLE_CONTROLLED_ADVISORY,
        advisory_outcome_measurement=active.ENABLE_ADVISORY_OUTCOME_MEASUREMENT,
        recommendation_policy=active.ENABLE_RECOMMENDATION_POLICY,
        policy_weighting=active.ENABLE_POLICY_WEIGHTING,
        educational_trials=active.ENABLE_EDUCATIONAL_TRIALS,
        longitudinal_evidence=active.ENABLE_LONGITUDINAL_EVIDENCE,
        evidence_review=active.ENABLE_EVIDENCE_REVIEW,
        sole_runtime=active.SOLE_RUNTIME,
        founder_intelligence=active.ENABLE_FOUNDER_INTELLIGENCE,
        label=label,
        ready_for_cutover_checklist=checklist,
    )
