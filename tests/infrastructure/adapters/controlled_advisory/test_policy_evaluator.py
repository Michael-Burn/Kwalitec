"""Controlled Advisory Policy Evaluator tests (P3-MS001)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.infrastructure.adapters.controlled_advisory import (
    REASON_ADVISORY_MISSING,
    REASON_ADVISORY_STALE,
    REASON_ALLOWED,
    REASON_FLAG_OFF,
    REASON_MULTIPLE_FIELDS,
    REASON_ROLLOUT_EXCLUDED,
    AdvisoryPolicy,
    ControlledAdvisoryPolicyEvaluator,
    build_default_advisory_policy,
    student_in_rollout,
)
from app.infrastructure.adapters.evidence_platform.contracts import (
    ConsistencySummary,
    EngagementSummary,
    EvidenceAdvisory,
)


def _advisory(*, generated_at: str, streak: int = 3) -> EvidenceAdvisory:
    return EvidenceAdvisory(
        advisory_id="evadv-test",
        student_id="7",
        consistency_summary=ConsistencySummary(
            active_streak=streak,
            source_description="Derived from recorded study activity.",
        ),
        engagement_summary=EngagementSummary(),
        generated_at=generated_at,
        evidence_summary_id="evsum-1",
        availability="available",
    )


def test_evaluator_denies_when_flag_off():
    evaluator = ControlledAdvisoryPolicyEvaluator(
        enabled=False,
        policy=build_default_advisory_policy(rollout_percentage=100),
    )
    decision = evaluator.evaluate(
        student_id="7",
        advisory=_advisory(generated_at="2026-07-25T10:00:00+00:00"),
    )
    assert decision.allowed is False
    assert decision.reason == REASON_FLAG_OFF


def test_evaluator_allows_valid_fresh_advisory_in_rollout():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    policy = build_default_advisory_policy(
        rollout_percentage=100,
        max_age_hours=168,
    )
    evaluator = ControlledAdvisoryPolicyEvaluator(
        enabled=True, policy=policy, now=now
    )
    decision = evaluator.evaluate(
        student_id="7",
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert decision.allowed is True
    assert decision.reason == REASON_ALLOWED
    assert decision.advisory_field == "consistency_summary"
    assert decision.policy_version == policy.policy_version
    assert decision.evidence_provenance["advisory_id"] == "evadv-test"


def test_evaluator_rejects_stale_advisory():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    policy = build_default_advisory_policy(
        rollout_percentage=100,
        max_age_hours=24,
    )
    evaluator = ControlledAdvisoryPolicyEvaluator(
        enabled=True, policy=policy, now=now
    )
    decision = evaluator.evaluate(
        student_id="7",
        advisory=_advisory(generated_at="2026-07-01T12:00:00+00:00"),
    )
    assert decision.allowed is False
    assert decision.reason == REASON_ADVISORY_STALE


def test_evaluator_rejects_missing_advisory():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    policy = build_default_advisory_policy(rollout_percentage=100)
    evaluator = ControlledAdvisoryPolicyEvaluator(
        enabled=True, policy=policy, now=now
    )
    decision = evaluator.evaluate(student_id="7", advisory=None)
    assert decision.allowed is False
    assert decision.reason == REASON_ADVISORY_MISSING


def test_evaluator_rejects_rollout_exclusion():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    policy = build_default_advisory_policy(rollout_percentage=0)
    evaluator = ControlledAdvisoryPolicyEvaluator(
        enabled=True, policy=policy, now=now
    )
    decision = evaluator.evaluate(
        student_id="7",
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert decision.allowed is False
    assert decision.reason == REASON_ROLLOUT_EXCLUDED


def test_evaluator_rejects_multiple_fields_policy():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    policy = AdvisoryPolicy(
        policy_id="bad",
        enabled_advisory_fields=("consistency_summary", "engagement_summary"),
        activation_conditions={"max_age_hours": 168},
        rollout_percentage=100,
        policy_version="x",
        effective_from="1970-01-01T00:00:00+00:00",
    )
    evaluator = ControlledAdvisoryPolicyEvaluator(
        enabled=True, policy=policy, now=now
    )
    decision = evaluator.evaluate(
        student_id="7",
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert decision.allowed is False
    assert decision.reason == REASON_MULTIPLE_FIELDS


def test_rollout_gating_deterministic():
    assert student_in_rollout("student-a", rollout_percentage=0) is False
    assert student_in_rollout("student-a", rollout_percentage=100) is True
    first = student_in_rollout("student-a", rollout_percentage=50)
    second = student_in_rollout("student-a", rollout_percentage=50)
    assert first is second
