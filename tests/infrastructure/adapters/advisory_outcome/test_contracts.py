"""Advisory Outcome Measurement DTO contract tests (P3-MS002)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.advisory_outcome.contracts import (
    ACTION_ACCEPTED,
    ACTION_VIEWED,
    ACTIVATION_STATUS_ACTIVATED,
    ACTIVATION_STATUS_FAILED,
    AUTHORITY_ADVISORY_OUTCOME,
    COHORT_IN_ROLLOUT,
    OUTCOME_MEASUREMENT_VERSION,
    ActionCorrelation,
    ActivationStatistics,
    AdvisoryOutcome,
    OutcomeMeasurementSummary,
    RolloutMetrics,
    explainability_fields_present,
)


def test_advisory_outcome_is_frozen():
    outcome = AdvisoryOutcome(
        outcome_id="advout-1",
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        recommendation_id="rec-1",
        student_action_observed=ACTION_ACCEPTED,
        observation_window="session",
        generated_at="2026-07-25T12:00:00+00:00",
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision="policy_allows_approved_field",
        provenance={"source_service": "advisory_outcome_measurement"},
    )
    with pytest.raises(Exception):
        outcome.outcome_id = "mutated"  # type: ignore[misc]


def test_advisory_outcome_has_no_personal_identifier_field():
    outcome = AdvisoryOutcome(
        outcome_id="advout-1",
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        recommendation_id="rec-1",
        student_action_observed=ACTION_VIEWED,
        observation_window="session",
        rollout_cohort=COHORT_IN_ROLLOUT,
        activation_decision="policy_allows_approved_field",
        provenance={"advisory_id": "evadv-1"},
    )
    payload = outcome.to_canonical_dict()
    assert "student_id" not in payload
    assert "user_id" not in payload
    assert "email" not in payload
    assert payload["authority"] == AUTHORITY_ADVISORY_OUTCOME
    assert payload["measurement_version"] == OUTCOME_MEASUREMENT_VERSION
    assert payload["operational_only"] is True


def test_advisory_outcome_coerces_unknown_status_and_action():
    outcome = AdvisoryOutcome(
        outcome_id="advout-1",
        activation_status="not-a-status",
        student_action_observed="teleport",
        rollout_cohort="mystery",
    )
    assert outcome.activation_status == ACTIVATION_STATUS_FAILED
    assert outcome.student_action_observed == "not_observed"
    assert outcome.rollout_cohort == "unknown"


def test_explainability_fields_required():
    incomplete = AdvisoryOutcome(
        outcome_id="advout-1",
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        activation_decision="policy_allows_approved_field",
        rollout_cohort=COHORT_IN_ROLLOUT,
        provenance={},
    )
    assert explainability_fields_present(incomplete) is False

    complete = AdvisoryOutcome(
        outcome_id="advout-2",
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        activation_decision="policy_allows_approved_field",
        rollout_cohort=COHORT_IN_ROLLOUT,
        provenance={"source_service": "advisory_outcome_measurement"},
    )
    assert explainability_fields_present(complete) is True


def test_rollout_metrics_clamp_rates_and_freeze():
    metrics = RolloutMetrics(
        outcome_count=10,
        activation_rate=1.5,
        acceptance_rate=-0.2,
        recommendation_interaction_rate=0.4,
        rollback_count=1,
        activation_failures=2,
        activation_status_counts={"activated": 7},
        action_counts={"accepted": 3},
    )
    assert metrics.activation_rate == 1.0
    assert metrics.acceptance_rate == 0.0
    assert metrics.recommendation_interaction_rate == 0.4
    assert metrics.operational_only is True
    with pytest.raises(Exception):
        metrics.outcome_count = 99  # type: ignore[misc]
    payload = metrics.to_canonical_dict()
    assert payload["rollback_count"] == 1
    assert payload["activation_failures"] == 2
    assert payload["activation_status_counts"]["activated"] == 7


def test_activation_statistics_and_correlation_are_operational_only():
    statistics = ActivationStatistics(
        total_outcomes=4,
        activated_count=2,
        rejected_count=1,
        failed_count=1,
        by_advisory_field={"consistency_summary": 4},
    )
    correlation = ActionCorrelation(
        activated_action_counts={"accepted": 1, "viewed": 1},
        rejected_action_counts={"ignored": 1},
    )
    assert statistics.operational_only is True
    assert correlation.operational_only is True
    assert statistics.to_canonical_dict()["activated_count"] == 2
    assert correlation.to_canonical_dict()["activated_action_counts"]["accepted"] == 1


def test_outcome_measurement_summary_requires_typed_collections():
    outcome = AdvisoryOutcome(
        outcome_id="advout-1",
        policy_version="p3.ms001.1",
        advisory_field="consistency_summary",
        activation_status=ACTIVATION_STATUS_ACTIVATED,
        activation_decision="policy_allows_approved_field",
        rollout_cohort=COHORT_IN_ROLLOUT,
        provenance={"source_service": "advisory_outcome_measurement"},
    )
    metrics = RolloutMetrics(outcome_count=1, activation_rate=1.0)
    summary = OutcomeMeasurementSummary(
        summary_id="advoutsum-1",
        metrics=metrics,
        outcomes=(outcome,),
        notes=("Operational only.",),
    )
    assert summary.operational_only is True
    assert summary.to_canonical_dict()["metrics"]["outcome_count"] == 1
    with pytest.raises(TypeError):
        OutcomeMeasurementSummary(
            summary_id="bad",
            outcomes=("not-an-outcome",),  # type: ignore[arg-type]
        )
