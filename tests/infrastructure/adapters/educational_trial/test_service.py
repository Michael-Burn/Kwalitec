"""EducationalTrialService + cohort / metrics / flag tests (P4-MS001)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.educational_trial import (
    COHORT_BASELINE,
    COHORT_TREATMENT,
    COHORT_UNASSIGNED,
    METRIC_MISSION_COMPLETION,
    METRIC_POLICY_ACTIVATION,
    METRIC_RECOMMENDATION_ACCEPTANCE,
    METRIC_REFLECTION_COMPLETION,
    METRIC_STUDY_SESSION_COMPLETION,
    TRIAL_STATUS_ACTIVE,
    TRIAL_STATUS_DRAFT,
    UNAVAILABLE,
    EducationalTrial,
    EducationalTrialService,
    assign_cohort,
    build_educational_trial_service,
    student_bucket,
    student_in_treatment,
)
from app.infrastructure.adapters.evidence_platform.contracts import (
    ConsistencySummary,
    EngagementSummary,
    EvidenceAdvisory,
)
from app.infrastructure.adapters.recommendation_policy import (
    WEIGHT_EXPLAINABILITY_KEY,
    build_default_weighting_policy,
    build_recommendation_policy_engine,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.services.recommendation_service import RecommendationService
from tests.conftest import _make_user


def _active_trial(*, rollout: int = 50) -> EducationalTrial:
    return EducationalTrial(
        trial_id="educational-trial-p4-ms001",
        policy_version="p3.ms004.1",
        rollout_percentage=rollout,
        start_date="2026-07-25",
        end_date="2026-08-25",
        status=TRIAL_STATUS_ACTIVE,
    )


def _advisory(*, generated_at: str, streak: int = 7) -> EvidenceAdvisory:
    return EvidenceAdvisory(
        advisory_id="evadv-trial",
        student_id="1",
        consistency_summary=ConsistencySummary(
            active_streak=streak,
            source_description="Derived from recorded study activity.",
        ),
        engagement_summary=EngagementSummary(),
        generated_at=generated_at,
        evidence_summary_id="evsum-trial",
        availability="available",
    )


class _StubAdvisoryInjection:
    def __init__(self, advisory: EvidenceAdvisory | None) -> None:
        self.last_advisory = advisory
        self.last_consideration = None

    def prepare_for_recommendation(self, user_id):  # noqa: ANN001
        return None


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


def test_flag_isolation_from_all_prior_flags():
    trial_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_TRIALS": "1"}
    )
    assert trial_only.ENABLE_EDUCATIONAL_TRIALS is True
    assert trial_only.ENABLE_POLICY_WEIGHTING is False
    assert trial_only.ENABLE_RECOMMENDATION_POLICY is False
    assert trial_only.ENABLE_CONTROLLED_ADVISORY is False
    assert trial_only.ENABLE_ADVISORY_OUTCOME_MEASUREMENT is False
    assert trial_only.ENABLE_ADAPTIVE_ENGINE is False
    assert trial_only.ENABLE_EVIDENCE_PLATFORM is False
    assert trial_only.ENABLE_LONGITUDINAL_EVIDENCE is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_POLICY_WEIGHTING": "1",
            "KWALITEC_RECOMMENDATION_POLICY": "1",
            "KWALITEC_CONTROLLED_ADVISORY": "1",
            "KWALITEC_ADVISORY_OUTCOME_MEASUREMENT": "1",
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
            "KWALITEC_LONGITUDINAL_EVIDENCE": "1",
        }
    )
    assert others_only.ENABLE_EDUCATIONAL_TRIALS is False


def test_cohort_assignment_is_stable_and_reproducible():
    trial = _active_trial(rollout=40)
    first = assign_cohort("student-42", trial)
    second = assign_cohort("student-42", trial)
    assert first.serialize() == second.serialize()
    assert first.cohort in {COHORT_BASELINE, COHORT_TREATMENT}
    assert first.bucket == student_bucket(
        "student-42", trial_id=trial.trial_id, salt=trial.rollout_salt
    )
    assert first.authorised_for_weighting == (first.cohort == COHORT_TREATMENT)


def test_rollout_allocation_extremes():
    trial_zero = _active_trial(rollout=0)
    trial_full = _active_trial(rollout=100)
    assert assign_cohort("student-a", trial_zero).cohort == COHORT_BASELINE
    assert assign_cohort("student-a", trial_full).cohort == COHORT_TREATMENT
    assert student_in_treatment(
        "student-a",
        rollout_percentage=0,
        trial_id=trial_zero.trial_id,
    ) is False
    assert student_in_treatment(
        "student-a",
        rollout_percentage=100,
        trial_id=trial_full.trial_id,
    ) is True


def test_inactive_trial_leaves_students_unassigned():
    draft = EducationalTrial(status=TRIAL_STATUS_DRAFT, rollout_percentage=100)
    assignment = assign_cohort("student-a", draft)
    assert assignment.cohort == COHORT_UNASSIGNED
    assert assignment.authorised_for_weighting is False


def test_service_disabled_returns_unavailable():
    service = EducationalTrialService(enabled=False, trial=_active_trial())
    result = service.assign_cohort("1")
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    # Disabled service does not interpose on existing weighting behaviour.
    assert service.authorises_policy_weighting("1") is True


def test_metrics_aggregation_and_reporting_are_reproducible():
    service = EducationalTrialService(enabled=True, trial=_active_trial(rollout=50))
    generated_at = "2026-07-25T12:00:00+00:00"
    for student, metric, occurred in (
        ("s1", METRIC_RECOMMENDATION_ACCEPTANCE, True),
        ("s2", METRIC_MISSION_COMPLETION, True),
        ("s3", METRIC_STUDY_SESSION_COMPLETION, False),
        ("s4", METRIC_REFLECTION_COMPLETION, True),
        ("s5", METRIC_POLICY_ACTIVATION, True),
    ):
        assignment = service.assign_cohort(
            student, generated_at=generated_at
        ).assignment
        assert assignment is not None
        service.record_metric(
            metric_name=metric,
            cohort=assignment.cohort,
            occurred=occurred,
            generated_at=generated_at,
            policy_activated=metric == METRIC_POLICY_ACTIVATION and occurred,
        )

    first = service.generate_summary(generated_at=generated_at)
    second = service.generate_summary(generated_at=generated_at)
    assert first.ok is True and second.ok is True
    assert first.summary is not None and second.summary is not None
    assert first.summary.serialize() == second.summary.serialize()
    assert first.summary.trial is not None
    assert first.summary.trial.policy_version == "p3.ms004.1"
    assert first.summary.trial.rollout_percentage == 50
    assert first.summary.observation_period_start == "2026-07-25"
    assert first.summary.cohort_statistics is not None
    assert first.summary.activation_statistics is not None
    assert first.summary.metrics is not None
    assert first.summary.metrics.observation_count == 5


def test_composition_wires_trial_when_flag_on():
    off_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(environ={})
    )
    assert off_composition.educational_trial is None

    on_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_EDUCATIONAL_TRIALS": "1"}
        )
    )
    assert on_composition.educational_trial is not None
    assert on_composition.educational_trial.is_enabled() is True


def test_build_helper_respects_enabled_flag():
    assert build_educational_trial_service(enabled=False) is None
    built = build_educational_trial_service(enabled=True)
    assert built is not None
    assert built.is_enabled() is True


def test_runtime_a_weighting_only_for_authorised_treatment_cohort(ctx):
    user = _make_user()
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    advisory = _advisory(generated_at="2026-07-24T12:00:00+00:00", streak=7)
    injection = _StubAdvisoryInjection(advisory)
    policy = build_default_weighting_policy(rollout_percentage=100)

    # Force treatment by 100% rollout.
    treatment_engine = build_recommendation_policy_engine(
        enabled=True,
        weighting_enabled=True,
        policy=policy,
        now=now,
    )
    assert treatment_engine is not None
    treatment_trial = EducationalTrialService(
        enabled=True, trial=_active_trial(rollout=100)
    )
    treatment_recs = RecommendationService.generate_recommendations(
        user.id,
        limit=3,
        advisory_injection=injection,
        recommendation_policy=treatment_engine,
        educational_trial=treatment_trial,
    )
    assert treatment_trial.authorises_policy_weighting(str(user.id)) is True
    assert treatment_engine.last_weight_application is not None
    assert treatment_engine.last_weight_application.applied is True
    if treatment_recs:
        assert WEIGHT_EXPLAINABILITY_KEY in treatment_recs[0]

    # Force baseline by 0% rollout — weighting must not apply.
    baseline_engine = build_recommendation_policy_engine(
        enabled=True,
        weighting_enabled=True,
        policy=policy,
        now=now,
    )
    assert baseline_engine is not None
    baseline_trial = EducationalTrialService(
        enabled=True, trial=_active_trial(rollout=0)
    )
    baseline_recs = RecommendationService.generate_recommendations(
        user.id,
        limit=3,
        advisory_injection=injection,
        recommendation_policy=baseline_engine,
        educational_trial=baseline_trial,
    )
    assert baseline_recs is not None
    assert baseline_trial.authorises_policy_weighting(str(user.id)) is False
    weight_app = baseline_engine.last_weight_application
    assert weight_app is None or weight_app.applied is False
    if baseline_recs:
        # Student-facing baseline path must not carry an applied weight artefact.
        explain = baseline_recs[0].get(WEIGHT_EXPLAINABILITY_KEY)
        assert explain is None or explain.get("applied") is not True
