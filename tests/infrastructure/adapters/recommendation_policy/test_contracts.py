"""Recommendation Policy Framework contract tests (P3-MS003)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.recommendation_policy import (
    DEFAULT_ADVISORY_RULE_ID,
    DEFAULT_APPLIED_WEIGHTING_RULE_ID,
    DEFAULT_MAX_WEIGHT_ADJUSTMENT,
    DEFAULT_POLICY_ID,
    DEFAULT_POLICY_VERSION,
    INFLUENCE_ANNOTATE,
    REASON_DUPLICATE_RULE_ID,
    REASON_EMPTY_RULE_ID,
    REASON_UNKNOWN_INFLUENCE_MODE,
    REASON_WEIGHT_BOUNDS_INVALID,
    REASON_WEIGHT_FIELD_NOT_APPROVED,
    RECOMMENDATION_POLICY_VERSION,
    WEIGHT_EXPLAINABILITY_KEY,
    AdvisoryRule,
    RecommendationPolicy,
    RecommendationPolicyExplainability,
    WeightApplication,
    WeightingRule,
    build_default_recommendation_policy,
    build_default_weighting_policy,
    clamp_weight_adjustment,
    compute_consistency_weight_delta,
    explainability_fields_present,
    explainability_from_decision,
    explainability_from_weight_application,
    validate_recommendation_policy,
    weight_explainability_fields_present,
)
from app.infrastructure.adapters.recommendation_policy.contracts import (
    PolicyDecision,
)


def test_recommendation_policy_immutable_and_versioned():
    policy = build_default_recommendation_policy()
    assert policy.policy_id == DEFAULT_POLICY_ID
    assert policy.version == DEFAULT_POLICY_VERSION
    assert policy.version == RECOMMENDATION_POLICY_VERSION
    assert len(policy.advisory_rules) >= 1
    assert policy.advisory_rules[0].rule_id == DEFAULT_ADVISORY_RULE_ID
    assert policy.advisory_rules[0].influence_mode == INFLUENCE_ANNOTATE
    with pytest.raises(Exception):
        policy.version = "mutated"  # type: ignore[misc]


def test_policy_versioning_is_independent():
    v1 = build_default_recommendation_policy(version="p3.ms003.1")
    v2 = build_default_recommendation_policy(version="p3.ms003.2")
    assert v1.version != v2.version
    assert v1.policy_id == v2.policy_id
    assert v1.serialize() != v2.serialize()


def test_advisory_and_weighting_rules_immutable():
    policy = build_default_recommendation_policy()
    with pytest.raises(Exception):
        policy.advisory_rules[0].enabled = False  # type: ignore[misc]
    for rule in policy.weighting_rules:
        with pytest.raises(Exception):
            rule.weight = 99.0  # type: ignore[misc]


def test_validate_rejects_duplicate_rule_ids():
    policy = RecommendationPolicy(
        policy_id="bad",
        version="x",
        effective_from="2026-01-01T00:00:00+00:00",
        advisory_rules=(
            AdvisoryRule(rule_id="same", advisory_field="consistency_summary"),
            AdvisoryRule(rule_id="same", advisory_field="engagement_summary"),
        ),
    )
    assert validate_recommendation_policy(policy) == REASON_DUPLICATE_RULE_ID


def test_validate_rejects_empty_rule_id():
    policy = RecommendationPolicy(
        policy_id="bad",
        version="x",
        effective_from="2026-01-01T00:00:00+00:00",
        advisory_rules=(
            AdvisoryRule(rule_id="", advisory_field="consistency_summary"),
        ),
    )
    assert validate_recommendation_policy(policy) == REASON_EMPTY_RULE_ID


def test_validate_rejects_unknown_influence_mode():
    policy = RecommendationPolicy(
        policy_id="bad",
        version="x",
        effective_from="2026-01-01T00:00:00+00:00",
        advisory_rules=(
            AdvisoryRule(
                rule_id="r1",
                advisory_field="consistency_summary",
                influence_mode="autonomous_optimise",
            ),
        ),
    )
    assert validate_recommendation_policy(policy) == REASON_UNKNOWN_INFLUENCE_MODE


def test_validate_default_policy_ok():
    assert validate_recommendation_policy(build_default_recommendation_policy()) is None


def test_policy_decision_weighting_applied_flag_is_explicit():
    """DTO records weighting_applied when set (P3-MS004); default remains False."""
    decision = PolicyDecision(
        applicable=True,
        reason="applicable_rules_resolved",
        policy_id="p",
        policy_version="v",
        weighting_applied=True,
    )
    assert decision.weighting_applied is True
    denied = PolicyDecision(
        applicable=True,
        reason="applicable_rules_resolved",
        policy_id="p",
        policy_version="v",
    )
    assert denied.weighting_applied is False


def test_explainability_requires_core_fields():
    decision = PolicyDecision(
        applicable=True,
        reason="applicable_rules_resolved",
        policy_id="recommendation-policy-p3-ms003",
        policy_version="p3.ms003.1",
        advisory_inputs_considered={"advisory_present": False},
        rationale="Policy rules resolved for Runtime A consideration.",
    )
    record = explainability_from_decision(decision)
    assert explainability_fields_present(record) is True
    assert record.authority == "runtime_a"
    assert record.weighting_applied is False

    incomplete = RecommendationPolicyExplainability(
        policy_version="",
        rationale="",
        advisory_inputs_considered={},
    )
    assert explainability_fields_present(incomplete) is False


def test_weighting_rule_canonical():
    rule = WeightingRule(
        rule_id="wgt-1",
        factor="consistency_streak",
        weight=0.1,
        enabled=False,
        rationale="reserved",
        advisory_field="consistency_summary",
        max_adjustment=0.05,
        apply_to_ranking=False,
    )
    payload = rule.to_canonical_dict()
    assert payload["rule_id"] == "wgt-1"
    assert payload["weight"] == 0.1
    assert payload["enabled"] is False
    assert payload["advisory_field"] == "consistency_summary"
    assert payload["max_adjustment"] == 0.05
    assert payload["apply_to_ranking"] is False


def test_weight_application_immutable_contract():
    app = WeightApplication(
        application_id="wgtapp-1",
        policy_version="p3.ms004.1",
        rule_id=DEFAULT_APPLIED_WEIGHTING_RULE_ID,
        advisory_field="consistency_summary",
        base_weight=1.0,
        adjusted_weight=1.04,
        adjustment_reason="policy_weight_applied",
        provenance={"advisory_id": "a1"},
        generated_at="2026-07-25T12:00:00+00:00",
        applied=True,
    )
    assert app.delta == pytest.approx(0.04)
    with pytest.raises(Exception):
        app.adjusted_weight = 2.0  # type: ignore[misc]
    payload = explainability_from_weight_application(app)
    assert weight_explainability_fields_present(payload) is True
    assert payload["original_weight"] == 1.0
    assert payload["rule_identifier"] == DEFAULT_APPLIED_WEIGHTING_RULE_ID
    assert WEIGHT_EXPLAINABILITY_KEY == "policy_weight_application"


def test_bounded_adjustment_helpers():
    assert compute_consistency_weight_delta(active_streak=0) == 0.0
    delta = compute_consistency_weight_delta(
        active_streak=7, max_adjustment=DEFAULT_MAX_WEIGHT_ADJUSTMENT
    )
    assert delta == pytest.approx(DEFAULT_MAX_WEIGHT_ADJUSTMENT)
    over = compute_consistency_weight_delta(
        active_streak=100, max_adjustment=0.05
    )
    assert over == pytest.approx(0.05)
    adjusted = clamp_weight_adjustment(
        base_weight=1.0, proposed_delta=0.2, max_adjustment=0.05
    )
    assert adjusted == pytest.approx(1.05)
    adjusted_neg = clamp_weight_adjustment(
        base_weight=1.0, proposed_delta=-0.2, max_adjustment=0.05
    )
    assert adjusted_neg == pytest.approx(0.95)


def test_default_weighting_policy_valid_and_single_field():
    policy = build_default_weighting_policy(rollout_percentage=100)
    assert validate_recommendation_policy(policy) is None
    ranking = [r for r in policy.weighting_rules if r.apply_to_ranking and r.enabled]
    assert len(ranking) == 1
    assert ranking[0].advisory_field == "consistency_summary"
    assert ranking[0].max_adjustment == DEFAULT_MAX_WEIGHT_ADJUSTMENT


def test_validate_rejects_unapproved_weight_field():
    policy = build_default_weighting_policy(
        weighting_rules=(
            WeightingRule(
                rule_id="wgt-bad",
                factor="engagement",
                enabled=True,
                apply_to_ranking=True,
                advisory_field="engagement_summary",
                max_adjustment=0.05,
            ),
        )
    )
    assert validate_recommendation_policy(policy) == REASON_WEIGHT_FIELD_NOT_APPROVED


def test_validate_rejects_excessive_max_adjustment():
    policy = build_default_weighting_policy(
        weighting_rules=(
            WeightingRule(
                rule_id="wgt-huge",
                factor="consistency_summary.active_streak",
                enabled=True,
                apply_to_ranking=True,
                advisory_field="consistency_summary",
                max_adjustment=0.5,
            ),
        )
    )
    assert validate_recommendation_policy(policy) == REASON_WEIGHT_BOUNDS_INVALID
