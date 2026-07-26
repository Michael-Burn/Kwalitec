"""AdvisoryOutcomeMeasurementService + feature-flag isolation tests (P3-MS002)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.advisory_outcome import (
    ACTION_ACCEPTED,
    ACTION_IGNORED,
    ACTION_INTERACTED,
    ACTION_VIEWED,
    ACTIVATION_STATUS_ACTIVATED,
    ACTIVATION_STATUS_FAILED,
    ACTIVATION_STATUS_REJECTED,
    ACTIVATION_STATUS_ROLLED_BACK,
    COHORT_EXCLUDED,
    COHORT_IN_ROLLOUT,
    UNAVAILABLE,
    AdvisoryOutcome,
    AdvisoryOutcomeMeasurementService,
    build_advisory_outcome_measurement_service,
    explainability_fields_present,
)
from app.infrastructure.adapters.controlled_advisory import (
    REASON_ALLOWED,
    REASON_ROLLOUT_EXCLUDED,
    AdvisoryActivationDecision,
    ControlledAdvisoryExplainability,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status


def _activated_decision() -> AdvisoryActivationDecision:
    return AdvisoryActivationDecision(
        allowed=True,
        reason=REASON_ALLOWED,
        policy_id="controlled-advisory-p3-ms001",
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        feature_flag_enabled=True,
        rollout_percentage=25,
        in_rollout=True,
        advisory_id="evadv-1",
        evidence_provenance={"active_streak": 3},
    )


def _rejected_decision() -> AdvisoryActivationDecision:
    return AdvisoryActivationDecision(
        allowed=False,
        reason=REASON_ROLLOUT_EXCLUDED,
        policy_id="controlled-advisory-p3-ms001",
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        feature_flag_enabled=True,
        rollout_percentage=25,
        in_rollout=False,
        evidence_provenance={"rollout_bucket": 80},
    )


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


def test_flag_isolation_from_all_prior_flags():
    measurement_only = resolve_v2_feature_flags(
        environ={"KWALITEC_ADVISORY_OUTCOME_MEASUREMENT": "1"}
    )
    assert measurement_only.ENABLE_ADVISORY_OUTCOME_MEASUREMENT is True
    assert measurement_only.ENABLE_CONTROLLED_ADVISORY is False
    assert measurement_only.ENABLE_ADVISORY_EVALUATION is False
    assert measurement_only.ENABLE_DECISION_SIMULATION is False
    assert measurement_only.ENABLE_RECOVERY_PLANNER is False
    assert measurement_only.ENABLE_EVIDENCE_ADVISORY is False
    assert measurement_only.ENABLE_EXPERIENCE_FEEDBACK is False
    assert measurement_only.ENABLE_EVIDENCE_PLATFORM is False
    assert measurement_only.ENABLE_STRATEGY_ENGINE is False
    assert measurement_only.ENABLE_ADAPTIVE_ENGINE is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_CONTROLLED_ADVISORY": "1",
            "KWALITEC_ADVISORY_EVALUATION": "1",
            "KWALITEC_DECISION_SIMULATION": "1",
            "KWALITEC_RECOVERY_PLANNER": "1",
            "KWALITEC_EVIDENCE_ADVISORY": "1",
            "KWALITEC_EXPERIENCE_FEEDBACK": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
            "KWALITEC_STRATEGY_ENGINE": "1",
            "KWALITEC_ADAPTIVE_ENGINE": "1",
        }
    )
    assert others_only.ENABLE_ADVISORY_OUTCOME_MEASUREMENT is False


def test_record_outcome_preserves_explainability_and_provenance():
    service = AdvisoryOutcomeMeasurementService(enabled=True)
    result = service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        recommendation_id="rec-9",
        student_action_observed=ACTION_ACCEPTED,
        observation_window="session",
        generated_at="2026-07-25T12:00:00+00:00",
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision=REASON_ALLOWED,
        provenance={
            "advisory_id": "evadv-9",
            "policy_id": "controlled-advisory-p3-ms001",
        },
    )
    assert result.ok is True
    outcome = result.outcome
    assert isinstance(outcome, AdvisoryOutcome)
    assert explainability_fields_present(outcome) is True
    assert outcome.policy_version == "p3.ms001.1"
    assert outcome.advisory_field == "consistency_summary"
    assert outcome.rollout_cohort == COHORT_IN_ROLLOUT
    assert outcome.activation_decision == REASON_ALLOWED
    assert outcome.provenance["advisory_id"] == "evadv-9"
    assert outcome.provenance["source_service"] == "advisory_outcome_measurement"
    assert "student_id" not in outcome.to_canonical_dict()


def test_record_from_activation_decision_and_explainability():
    service = AdvisoryOutcomeMeasurementService(enabled=True)
    allowed = service.record_from_activation(
        _activated_decision(),
        recommendation_id="rec-a",
        student_action_observed=ACTION_VIEWED,
        generated_at="2026-07-25T12:00:00+00:00",
    )
    assert allowed.ok is True
    assert allowed.outcome is not None
    assert allowed.outcome.activation_status == ACTIVATION_STATUS_ACTIVATED
    assert allowed.outcome.rollout_cohort == COHORT_IN_ROLLOUT
    assert allowed.outcome.activation_decision == REASON_ALLOWED
    assert explainability_fields_present(allowed.outcome) is True

    rejected = service.record_from_activation(
        _rejected_decision(),
        recommendation_id="rec-b",
        student_action_observed=ACTION_IGNORED,
    )
    assert rejected.ok is True
    assert rejected.outcome is not None
    assert rejected.outcome.activation_status == ACTIVATION_STATUS_REJECTED
    assert rejected.outcome.rollout_cohort == COHORT_EXCLUDED

    explainability = ControlledAdvisoryExplainability(
        activated=True,
        advisory_field_used="consistency_summary",
        policy_version="p3.ms001.1",
        activation_reason=REASON_ALLOWED,
        evidence_provenance={"advisory_id": "evadv-2"},
        advisory_id="evadv-2",
        policy_id="controlled-advisory-p3-ms001",
    )
    from_explain = service.record_from_activation(
        explainability,
        recommendation_id="rec-c",
        student_action_observed=ACTION_INTERACTED,
    )
    assert from_explain.ok is True
    assert from_explain.outcome is not None
    assert from_explain.outcome.activation_status == ACTIVATION_STATUS_ACTIVATED
    assert from_explain.outcome.advisory_field == "consistency_summary"


def test_aggregate_activation_statistics_and_correlate_actions():
    service = AdvisoryOutcomeMeasurementService(enabled=True)
    service.record_from_activation(
        _activated_decision(),
        recommendation_id="rec-1",
        student_action_observed=ACTION_ACCEPTED,
    )
    service.record_from_activation(
        _activated_decision(),
        recommendation_id="rec-2",
        student_action_observed=ACTION_VIEWED,
    )
    service.record_from_activation(
        _rejected_decision(),
        recommendation_id="rec-3",
        student_action_observed=ACTION_IGNORED,
    )
    service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_FAILED,
        recommendation_id="rec-4",
        student_action_observed=ACTION_IGNORED,
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision="controlled_advisory_activation_failed",
        provenance={"error": "timeout"},
    )
    service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ROLLED_BACK,
        recommendation_id="rec-5",
        student_action_observed=ACTION_IGNORED,
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision="controlled_advisory_rolled_back",
        provenance={"rollback": True},
    )

    stats_result = service.aggregate_activation_statistics(
        generated_at="2026-07-25T12:00:00+00:00"
    )
    assert stats_result.ok is True
    stats = stats_result.activation_statistics
    assert stats is not None
    assert stats.total_outcomes == 5
    assert stats.activated_count == 2
    assert stats.rejected_count == 1
    assert stats.failed_count == 1
    assert stats.rolled_back_count == 1
    assert stats.by_advisory_field["consistency_summary"] == 5
    assert stats.operational_only is True

    corr_result = service.correlate_actions()
    assert corr_result.ok is True
    correlation = corr_result.action_correlation
    assert correlation is not None
    assert correlation.activated_action_counts[ACTION_ACCEPTED] == 1
    assert correlation.activated_action_counts[ACTION_VIEWED] == 1
    assert correlation.rejected_action_counts[ACTION_IGNORED] == 1
    assert correlation.failed_action_counts[ACTION_IGNORED] == 1
    assert correlation.rolled_back_action_counts[ACTION_IGNORED] == 1


def test_aggregate_rollout_metrics():
    service = AdvisoryOutcomeMeasurementService(enabled=True)
    # 2 activated (1 accepted, 1 interacted), 1 rejected, 1 failed, 1 rollback
    service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        recommendation_id="rec-1",
        student_action_observed=ACTION_ACCEPTED,
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision=REASON_ALLOWED,
        provenance={"k": 1},
    )
    service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        recommendation_id="rec-2",
        student_action_observed=ACTION_INTERACTED,
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision=REASON_ALLOWED,
        provenance={"k": 2},
    )
    service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_REJECTED,
        recommendation_id="rec-3",
        student_action_observed=ACTION_IGNORED,
        rollout_cohort=COHORT_EXCLUDED,
        activation_decision=REASON_ROLLOUT_EXCLUDED,
        provenance={"k": 3},
    )
    service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_FAILED,
        recommendation_id="rec-4",
        student_action_observed=ACTION_IGNORED,
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision="activation_failed",
        provenance={"k": 4},
    )
    service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ROLLED_BACK,
        recommendation_id="rec-5",
        student_action_observed=ACTION_IGNORED,
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision="rolled_back",
        provenance={"k": 5},
    )

    metrics_result = service.aggregate_rollout_metrics(
        generated_at="2026-07-25T12:00:00+00:00"
    )
    assert metrics_result.ok is True
    metrics = metrics_result.metrics
    assert metrics is not None
    assert metrics.outcome_count == 5
    assert metrics.activation_rate == 0.4
    assert metrics.acceptance_rate == 0.5  # 1 accepted / 2 activated
    assert metrics.recommendation_interaction_rate == 1.0  # both activated engaged
    assert metrics.rollback_count == 1
    assert metrics.activation_failures == 1
    assert metrics.rejection_count == 1
    assert metrics.operational_only is True


def test_generate_summary_includes_metrics_statistics_correlation():
    service = AdvisoryOutcomeMeasurementService(enabled=True)
    service.record_from_activation(
        _activated_decision(),
        recommendation_id="rec-1",
        student_action_observed=ACTION_ACCEPTED,
        generated_at="2026-07-25T12:00:00+00:00",
    )
    service.record_from_activation(
        _rejected_decision(),
        recommendation_id="rec-2",
        student_action_observed=ACTION_IGNORED,
        generated_at="2026-07-25T12:00:00+00:00",
    )
    summary_result = service.generate_summary(
        generated_at="2026-07-25T12:00:00+00:00"
    )
    assert summary_result.ok is True
    summary = summary_result.summary
    assert summary is not None
    assert summary.metrics is not None
    assert summary.activation_statistics is not None
    assert summary.action_correlation is not None
    assert len(summary.outcomes) == 2
    assert summary.operational_only is True
    assert any("Runtime A" in note for note in summary.notes)
    assert any("learning quality" in note.lower() for note in summary.notes)


def test_measurement_is_deterministic():
    service = AdvisoryOutcomeMeasurementService(enabled=True)
    first = service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        recommendation_id="rec-fixed",
        student_action_observed=ACTION_ACCEPTED,
        observation_window="session",
        generated_at="2026-07-25T12:00:00+00:00",
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision=REASON_ALLOWED,
        provenance={"advisory_id": "evadv-fixed"},
    )
    service.clear_outcomes()
    second = service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        recommendation_id="rec-fixed",
        student_action_observed=ACTION_ACCEPTED,
        observation_window="session",
        generated_at="2026-07-25T12:00:00+00:00",
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision=REASON_ALLOWED,
        provenance={"advisory_id": "evadv-fixed"},
    )
    assert first.ok and second.ok
    assert first.outcome is not None and second.outcome is not None
    assert first.outcome.outcome_id == second.outcome.outcome_id
    assert first.outcome.serialize() == second.outcome.serialize()


def test_service_disabled_returns_unavailable():
    service = AdvisoryOutcomeMeasurementService(enabled=False)
    result = service.record_outcome(
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        activation_decision=REASON_ALLOWED,
        rollout_cohort=COHORT_IN_ROLLOUT,
        provenance={"k": 1},
    )
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    assert service.outcomes == ()
    assert service.aggregate_rollout_metrics().ok is False
    assert service.aggregate_activation_statistics().ok is False
    assert service.correlate_actions().ok is False
    assert service.generate_summary().ok is False


def test_build_helper_and_composition_isolation(ctx):
    assert build_advisory_outcome_measurement_service(enabled=False) is None
    built = build_advisory_outcome_measurement_service(enabled=True)
    assert isinstance(built, AdvisoryOutcomeMeasurementService)
    assert built.is_enabled() is True

    off_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(environ={})
    )
    assert off_composition.advisory_outcome_measurement is None

    on_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_ADVISORY_OUTCOME_MEASUREMENT": "1"}
        )
    )
    assert on_composition.advisory_outcome_measurement is not None
    assert on_composition.advisory_outcome_measurement.is_enabled() is True
    # Independent: measurement ON does not enable controlled advisory Runtime A path.
    assert on_composition.controlled_advisory is None


def test_empty_cohort_metrics_are_zero():
    service = AdvisoryOutcomeMeasurementService(enabled=True)
    result = service.aggregate_rollout_metrics(())
    assert result.ok is True
    metrics = result.metrics
    assert metrics is not None
    assert metrics.outcome_count == 0
    assert metrics.activation_rate == 0.0
    assert metrics.acceptance_rate == 0.0
    assert metrics.recommendation_interaction_rate == 0.0
    assert metrics.rollback_count == 0
    assert metrics.activation_failures == 0
