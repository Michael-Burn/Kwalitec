"""Educational trial contract tests (P4-MS001)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.educational_trial import (
    APPROVED_ADVISORY_FIELD,
    COHORT_BASELINE,
    COHORT_TREATMENT,
    EDUCATIONAL_TRIAL_VERSION,
    METRIC_RECOMMENDATION_ACCEPTANCE,
    TRIAL_STATUS_ACTIVE,
    TRIAL_STATUS_DRAFT,
    ActivationStatistics,
    CohortAssignment,
    CohortStatistics,
    EducationalTrial,
    TrialMetricObservation,
    TrialMetrics,
    TrialSummary,
    validate_educational_trial,
)


def test_educational_trial_immutable_and_locks_advisory_field():
    trial = EducationalTrial(
        trial_id="trial-1",
        policy_version="p3.ms004.1",
        rollout_percentage=25,
        advisory_field="engagement_summary",
        start_date="2026-07-25",
        end_date="2026-08-25",
        status=TRIAL_STATUS_ACTIVE,
    )
    assert trial.advisory_field == APPROVED_ADVISORY_FIELD
    assert trial.rollout_percentage == 25
    assert trial.is_active is True
    with pytest.raises(Exception):
        trial.rollout_percentage = 50  # type: ignore[misc]


def test_educational_trial_clamps_rollout_and_normalises_status():
    trial = EducationalTrial(
        rollout_percentage=250,
        status="not-a-status",
        success_metrics=("recommendation_acceptance", "mastery_score", ""),
    )
    assert trial.rollout_percentage == 100
    assert trial.status == TRIAL_STATUS_DRAFT
    assert trial.success_metrics == (METRIC_RECOMMENDATION_ACCEPTANCE,)
    assert validate_educational_trial(trial)[0] is True


def test_educational_trial_canonical_serialization_is_stable():
    trial = EducationalTrial(
        trial_id="trial-stable",
        policy_version="p3.ms004.1",
        rollout_percentage=10,
        start_date="2026-07-25",
        end_date="2026-08-25",
        status=TRIAL_STATUS_ACTIVE,
    )
    first = trial.serialize()
    second = EducationalTrial(**trial.to_canonical_dict()).serialize()
    assert first == second
    assert trial.trial_version == EDUCATIONAL_TRIAL_VERSION


def test_cohort_assignment_and_metric_observation_contracts():
    assignment = CohortAssignment(
        trial_id="trial-1",
        student_key="trialstu-abc",
        cohort=COHORT_TREATMENT,
        rollout_percentage=50,
        bucket=12,
        authorised_for_weighting=True,
        policy_version="p3.ms004.1",
    )
    assert assignment.cohort == COHORT_TREATMENT
    assert assignment.authorised_for_weighting is True

    observation = TrialMetricObservation(
        observation_id="obs-1",
        trial_id="trial-1",
        metric_name=METRIC_RECOMMENDATION_ACCEPTANCE,
        cohort=COHORT_BASELINE,
        occurred=True,
        policy_version="p3.ms004.1",
    )
    assert observation.operational_only is True
    assert "recommendation_acceptance" in observation.serialize()


def test_trial_summary_requires_typed_children():
    trial = EducationalTrial(status=TRIAL_STATUS_ACTIVE, rollout_percentage=20)
    summary = TrialSummary(
        summary_id="sum-1",
        trial=trial,
        cohort_statistics=CohortStatistics(baseline_count=1, treatment_count=1),
        activation_statistics=ActivationStatistics(policy_activation_count=1),
        metrics=TrialMetrics(observation_count=2, recommendation_acceptance_rate=0.5),
        observation_period_start=trial.start_date,
        observation_period_end=trial.end_date,
    )
    payload = summary.to_canonical_dict()
    assert payload["trial"]["trial_id"] == trial.trial_id
    assert payload["metrics"]["recommendation_acceptance_rate"] == 0.5
    with pytest.raises(TypeError):
        TrialSummary(summary_id="bad", trial="nope")  # type: ignore[arg-type]
