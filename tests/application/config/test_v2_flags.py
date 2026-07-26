"""Tests for Version 2 dual-run flags and cutover helpers."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.founder.intelligence import FounderIntelligenceService
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.infrastructure.diagnostics.evidence_gates import build_evidence_gates_report


def test_v2_flags_default_keep_v1_primary():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_STUDENT_EXPERIENCE is False
    assert flags.ENABLE_DURABLE_STORE is False
    assert flags.SOLE_RUNTIME is False
    assert flags.SEED_DEMO_LEARNERS is True
    assert flags.ENABLE_MISSION_READ_BRIDGE is False
    assert flags.ENABLE_MISSION_START_BRIDGE is False
    assert flags.ENABLE_MISSION_RESUME_BRIDGE is False
    assert flags.ENABLE_SESSION_COMPLETION_BRIDGE is False
    assert flags.ENABLE_RECOMMENDATION_BRIDGE is False
    assert flags.ENABLE_JOURNEY_BRIDGE is False
    assert flags.ENABLE_HISTORY_BRIDGE is False
    assert flags.ENABLE_ADAPTIVE_ENGINE is False
    assert flags.ENABLE_ADAPTIVE_ENGINE_SHADOW is False
    assert flags.ENABLE_ADAPTIVE_AUTHORITY is False
    assert flags.ENABLE_DIGITAL_TWIN is False
    assert flags.ENABLE_STUDY_INSIGHTS_CUTOVER is False
    assert flags.ENABLE_READINESS_INTELLIGENCE_CUTOVER is False
    assert flags.ENABLE_STRATEGY_ENGINE is False
    assert flags.ENABLE_EVIDENCE_PLATFORM is False
    assert flags.ENABLE_UNIFIED_JOURNEY is False
    assert flags.ENABLE_EXPERIENCE_OBSERVATION is False
    assert flags.ENABLE_EXPERIENCE_DIAGNOSTICS is False
    assert flags.ENABLE_EXPERIENCE_FEEDBACK is False
    assert flags.ENABLE_EVIDENCE_ADVISORY is False
    assert flags.ENABLE_RECOVERY_PLANNER is False
    assert flags.ENABLE_DECISION_SIMULATION is False
    assert flags.ENABLE_ADVISORY_EVALUATION is False
    assert flags.ENABLE_CONTROLLED_ADVISORY is False
    assert flags.ENABLE_ADVISORY_OUTCOME_MEASUREMENT is False
    assert flags.ENABLE_RECOMMENDATION_POLICY is False
    assert flags.ENABLE_POLICY_WEIGHTING is False
    assert flags.ENABLE_EDUCATIONAL_TRIALS is False
    assert flags.ENABLE_LONGITUDINAL_EVIDENCE is False
    assert flags.ENABLE_EVIDENCE_REVIEW is False


def test_v2_flags_dual_run_disables_demo_when_durable():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_V2_STUDENT_EXPERIENCE": "1",
            "KWALITEC_V2_DURABLE_STORE": "1",
        }
    )
    assert flags.ENABLE_STUDENT_EXPERIENCE is True
    assert flags.ENABLE_DURABLE_STORE is True
    assert flags.INJECT_PHASE_I_ENGINES is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_v2_sole_runtime_implies_student_experience():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_V2_SOLE_RUNTIME": "1"})
    assert flags.SOLE_RUNTIME is True
    assert flags.ENABLE_STUDENT_EXPERIENCE is True


def test_mission_read_bridge_flag_disables_demo_seed():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_MISSION_READ_BRIDGE": "1"}
    )
    assert flags.ENABLE_MISSION_READ_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_mission_start_bridge_flag_disables_demo_seed():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_MISSION_START_BRIDGE": "1"}
    )
    assert flags.ENABLE_MISSION_START_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_mission_resume_bridge_flag_disables_demo_seed():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_MISSION_RESUME_BRIDGE": "1"}
    )
    assert flags.ENABLE_MISSION_RESUME_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_session_completion_bridge_flag_disables_demo_seed():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_SESSION_COMPLETION_BRIDGE": "1"}
    )
    assert flags.ENABLE_SESSION_COMPLETION_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_recommendation_bridge_flag_disables_demo_seed():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_RECOMMENDATION_BRIDGE": "1"}
    )
    assert flags.ENABLE_RECOMMENDATION_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_journey_bridge_flag_disables_demo_seed():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_JOURNEY_BRIDGE": "1"})
    assert flags.ENABLE_JOURNEY_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_history_bridge_flag_disables_demo_seed():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_HISTORY_BRIDGE": "1"})
    assert flags.ENABLE_HISTORY_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_educational_continuity_bridge_enables_journey():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_CONTINUITY_BRIDGE": "1"}
    )
    assert flags.ENABLE_JOURNEY_BRIDGE is True
    assert flags.ENABLE_HISTORY_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_educational_runtime_bridge_alias_enables_mission_bridges():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE": "true"}
    )
    assert flags.ENABLE_MISSION_READ_BRIDGE is True
    assert flags.ENABLE_MISSION_START_BRIDGE is True
    assert flags.ENABLE_MISSION_RESUME_BRIDGE is True
    assert flags.ENABLE_SESSION_COMPLETION_BRIDGE is True
    assert flags.ENABLE_RECOMMENDATION_BRIDGE is True
    assert flags.ENABLE_JOURNEY_BRIDGE is True
    assert flags.ENABLE_HISTORY_BRIDGE is True


def test_dual_run_status_labels():
    dual = build_dual_run_status(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_V2_STUDENT_EXPERIENCE": "1"}
        )
    )
    assert dual.label == "dual-run-active"
    assert len(dual.ready_for_cutover_checklist) == 6
    assert dual.mission_read_bridge is False
    assert dual.mission_start_bridge is False
    assert dual.mission_resume_bridge is False
    assert dual.session_completion_bridge is False
    assert dual.recommendation_bridge is False
    assert dual.journey_bridge is False
    assert dual.history_bridge is False
    assert dual.adaptive_engine is False
    assert dual.adaptive_engine_shadow is False
    assert dual.adaptive_authority is False


def test_dual_run_status_includes_mission_bridges():
    dual = build_dual_run_status(
        flags=resolve_v2_feature_flags(
            environ={
                "KWALITEC_MISSION_READ_BRIDGE": "1",
                "KWALITEC_MISSION_START_BRIDGE": "1",
                "KWALITEC_MISSION_RESUME_BRIDGE": "1",
                "KWALITEC_SESSION_COMPLETION_BRIDGE": "1",
                "KWALITEC_RECOMMENDATION_BRIDGE": "1",
                "KWALITEC_JOURNEY_BRIDGE": "1",
                "KWALITEC_HISTORY_BRIDGE": "1",
            }
        )
    )
    assert dual.mission_read_bridge is True
    assert dual.mission_start_bridge is True
    assert dual.mission_resume_bridge is True
    assert dual.session_completion_bridge is True
    assert dual.recommendation_bridge is True
    assert dual.journey_bridge is True
    assert dual.history_bridge is True
    assert dual.adaptive_engine is False


def test_adaptive_engine_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_ADAPTIVE_ENGINE is False
    dual = build_dual_run_status(flags=flags)
    assert dual.adaptive_engine is False
    assert dual.adaptive_engine_shadow is False
    assert dual.adaptive_authority is False


def test_adaptive_engine_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_ADAPTIVE_ENGINE": "1"})
    assert flags.ENABLE_ADAPTIVE_ENGINE is True
    dual = build_dual_run_status(flags=flags)
    assert dual.adaptive_engine is True
    assert dual.adaptive_engine_shadow is False
    assert dual.adaptive_authority is False


def test_adaptive_shadow_flag_alias():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_ADAPTIVE_SHADOW": "1"})
    assert flags.ENABLE_ADAPTIVE_ENGINE_SHADOW is True
    dual = build_dual_run_status(flags=flags)
    assert dual.adaptive_engine_shadow is True


def test_adaptive_authority_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_ADAPTIVE_AUTHORITY": "1"}
    )
    assert flags.ENABLE_ADAPTIVE_AUTHORITY is True
    dual = build_dual_run_status(flags=flags)
    assert dual.adaptive_authority is True
    # Authority alone does not enable Engine / Shadow.
    assert dual.adaptive_engine is False
    assert dual.adaptive_engine_shadow is False


def test_digital_twin_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DIGITAL_TWIN is False
    dual = build_dual_run_status(flags=flags)
    assert dual.digital_twin is False


def test_digital_twin_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_DIGITAL_TWIN": "1"})
    assert flags.ENABLE_DIGITAL_TWIN is True
    dual = build_dual_run_status(flags=flags)
    assert dual.digital_twin is True


def test_study_insights_cutover_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_STUDY_INSIGHTS_CUTOVER is False


def test_study_insights_cutover_flag_requires_twin():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_STUDY_INSIGHTS_CUTOVER": "1"}
    )
    assert flags.ENABLE_STUDY_INSIGHTS_CUTOVER is False


def test_study_insights_cutover_flag_enables_with_twin():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_STUDY_INSIGHTS_CUTOVER": "1",
        }
    )
    assert flags.ENABLE_STUDY_INSIGHTS_CUTOVER is True


def test_readiness_intelligence_cutover_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_READINESS_INTELLIGENCE_CUTOVER is False


def test_readiness_intelligence_cutover_flag_requires_twin():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_READINESS_INTELLIGENCE_CUTOVER": "1"}
    )
    assert flags.ENABLE_READINESS_INTELLIGENCE_CUTOVER is False


def test_readiness_intelligence_cutover_flag_enables_with_twin():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_READINESS_INTELLIGENCE_CUTOVER": "1",
        }
    )
    assert flags.ENABLE_READINESS_INTELLIGENCE_CUTOVER is True


def test_daily_plan_cutover_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DAILY_PLAN_CUTOVER is False


def test_daily_plan_cutover_flag_requires_twin():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_DAILY_PLAN_CUTOVER": "1"}
    )
    assert flags.ENABLE_DAILY_PLAN_CUTOVER is False


def test_daily_plan_cutover_flag_enables_with_twin():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_DAILY_PLAN_CUTOVER": "1",
        }
    )
    assert flags.ENABLE_DAILY_PLAN_CUTOVER is True


def test_strategy_engine_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_STRATEGY_ENGINE is False
    dual = build_dual_run_status(flags=flags)
    assert dual.strategy_engine is False


def test_strategy_engine_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_STRATEGY_ENGINE": "1"})
    assert flags.ENABLE_STRATEGY_ENGINE is True
    dual = build_dual_run_status(flags=flags)
    assert dual.strategy_engine is True


def test_evidence_platform_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EVIDENCE_PLATFORM is False
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_platform is False


def test_evidence_platform_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_EVIDENCE_PLATFORM": "1"})
    assert flags.ENABLE_EVIDENCE_PLATFORM is True
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_platform is True


def test_unified_journey_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_UNIFIED_JOURNEY is False
    dual = build_dual_run_status(flags=flags)
    assert dual.unified_journey is False


def test_unified_journey_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_UNIFIED_JOURNEY": "1"})
    assert flags.ENABLE_UNIFIED_JOURNEY is True
    dual = build_dual_run_status(flags=flags)
    assert dual.unified_journey is True


def test_experience_observation_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EXPERIENCE_OBSERVATION is False
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_observation is False


def test_experience_observation_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_OBSERVATION": "1"}
    )
    assert flags.ENABLE_EXPERIENCE_OBSERVATION is True
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_observation is True


def test_experience_diagnostics_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EXPERIENCE_DIAGNOSTICS is False
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_diagnostics is False


def test_experience_diagnostics_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_DIAGNOSTICS": "1"}
    )
    assert flags.ENABLE_EXPERIENCE_DIAGNOSTICS is True
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_diagnostics is True


def test_experience_feedback_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EXPERIENCE_FEEDBACK is False
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_feedback is False


def test_experience_feedback_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_FEEDBACK": "1"}
    )
    assert flags.ENABLE_EXPERIENCE_FEEDBACK is True
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_feedback is True


def test_evidence_advisory_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EVIDENCE_ADVISORY is False
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_advisory is False


def test_evidence_advisory_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_ADVISORY": "1"}
    )
    assert flags.ENABLE_EVIDENCE_ADVISORY is True
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_advisory is True


def test_recovery_planner_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_RECOVERY_PLANNER is False
    dual = build_dual_run_status(flags=flags)
    assert dual.recovery_planner is False


def test_recovery_planner_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_RECOVERY_PLANNER": "1"}
    )
    assert flags.ENABLE_RECOVERY_PLANNER is True
    dual = build_dual_run_status(flags=flags)
    assert dual.recovery_planner is True


def test_decision_simulation_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DECISION_SIMULATION is False
    dual = build_dual_run_status(flags=flags)
    assert dual.decision_simulation is False


def test_decision_simulation_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_DECISION_SIMULATION": "1"}
    )
    assert flags.ENABLE_DECISION_SIMULATION is True
    dual = build_dual_run_status(flags=flags)
    assert dual.decision_simulation is True


def test_advisory_evaluation_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_ADVISORY_EVALUATION is False
    dual = build_dual_run_status(flags=flags)
    assert dual.advisory_evaluation is False


def test_advisory_evaluation_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_ADVISORY_EVALUATION": "1"}
    )
    assert flags.ENABLE_ADVISORY_EVALUATION is True
    dual = build_dual_run_status(flags=flags)
    assert dual.advisory_evaluation is True


def test_controlled_advisory_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_CONTROLLED_ADVISORY is False
    dual = build_dual_run_status(flags=flags)
    assert dual.controlled_advisory is False


def test_controlled_advisory_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_CONTROLLED_ADVISORY": "1"}
    )
    assert flags.ENABLE_CONTROLLED_ADVISORY is True
    dual = build_dual_run_status(flags=flags)
    assert dual.controlled_advisory is True


def test_advisory_outcome_measurement_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_ADVISORY_OUTCOME_MEASUREMENT is False
    dual = build_dual_run_status(flags=flags)
    assert dual.advisory_outcome_measurement is False


def test_advisory_outcome_measurement_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_ADVISORY_OUTCOME_MEASUREMENT": "1"}
    )
    assert flags.ENABLE_ADVISORY_OUTCOME_MEASUREMENT is True
    dual = build_dual_run_status(flags=flags)
    assert dual.advisory_outcome_measurement is True


def test_recommendation_policy_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_RECOMMENDATION_POLICY is False
    dual = build_dual_run_status(flags=flags)
    assert dual.recommendation_policy is False


def test_recommendation_policy_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_RECOMMENDATION_POLICY": "1"}
    )
    assert flags.ENABLE_RECOMMENDATION_POLICY is True
    dual = build_dual_run_status(flags=flags)
    assert dual.recommendation_policy is True


def test_policy_weighting_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_POLICY_WEIGHTING is False
    dual = build_dual_run_status(flags=flags)
    assert dual.policy_weighting is False


def test_policy_weighting_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_POLICY_WEIGHTING": "1"}
    )
    assert flags.ENABLE_POLICY_WEIGHTING is True
    dual = build_dual_run_status(flags=flags)
    assert dual.policy_weighting is True


def test_educational_trials_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EDUCATIONAL_TRIALS is False
    dual = build_dual_run_status(flags=flags)
    assert dual.educational_trials is False


def test_educational_trials_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_TRIALS": "1"}
    )
    assert flags.ENABLE_EDUCATIONAL_TRIALS is True
    dual = build_dual_run_status(flags=flags)
    assert dual.educational_trials is True


def test_longitudinal_evidence_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_LONGITUDINAL_EVIDENCE is False
    dual = build_dual_run_status(flags=flags)
    assert dual.longitudinal_evidence is False


def test_longitudinal_evidence_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_LONGITUDINAL_EVIDENCE": "1"}
    )
    assert flags.ENABLE_LONGITUDINAL_EVIDENCE is True
    dual = build_dual_run_status(flags=flags)
    assert dual.longitudinal_evidence is True


def test_evidence_review_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EVIDENCE_REVIEW is False
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_review is False


def test_evidence_review_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_REVIEW": "1"}
    )
    assert flags.ENABLE_EVIDENCE_REVIEW is True
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_review is True


def test_evidence_gates_report_blocks_product_evidence():
    report = build_evidence_gates_report()
    assert any(
        i.code == "product_evidence" and not i.technical_ready for i in report.items
    )
    assert report.cutover_blocked is True


def test_founder_intelligence_advisory_empty_without_store():
    snap = FounderIntelligenceService().build(experience_store=None)
    assert snap.signals == ()
    assert "advisory" in snap.notes[0].lower()
