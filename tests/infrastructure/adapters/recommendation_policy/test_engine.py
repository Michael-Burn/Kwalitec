"""Recommendation Policy Engine tests (P3-MS003)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.infrastructure.adapters.recommendation_policy import (
    DEFAULT_ADVISORY_RULE_ID,
    POLICY_EXPLAINABILITY_KEY,
    REASON_EFFECTIVE_FROM_FUTURE,
    REASON_FLAG_OFF,
    REASON_NO_RULES_APPLICABLE,
    REASON_RULES_RESOLVED,
    AdvisoryRule,
    RecommendationPolicyEngine,
    WeightingRule,
    build_default_recommendation_policy,
    build_recommendation_policy_engine,
)


def test_engine_resolves_applicable_advisory_rule():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        policy=build_default_recommendation_policy(),
        now=now,
    )
    decision = engine.resolve(student_id="7", advisory=None)
    assert decision.applicable is True
    assert decision.reason == REASON_RULES_RESOLVED
    assert DEFAULT_ADVISORY_RULE_ID in decision.applicable_rule_ids
    assert decision.weighting_applied is False
    assert decision.authority == "recommendation_policy"
    # Default weighting rule is disabled — not applicable.
    for rule in decision.weighting_rules_applicable:
        assert rule.applicable is False
        assert rule.applied_to_ranking is False


def test_engine_flag_off_denies():
    engine = RecommendationPolicyEngine(
        enabled=False,
        policy=build_default_recommendation_policy(),
    )
    decision = engine.resolve(student_id="7")
    assert decision.applicable is False
    assert decision.reason == REASON_FLAG_OFF
    assert decision.feature_flag_enabled is False


def test_engine_future_effective_from():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    policy = build_default_recommendation_policy(
        effective_from="2099-01-01T00:00:00+00:00"
    )
    engine = RecommendationPolicyEngine(enabled=True, policy=policy, now=now)
    decision = engine.resolve(student_id="7")
    assert decision.applicable is False
    assert decision.reason == REASON_EFFECTIVE_FROM_FUTURE


def test_engine_no_rules_applicable_when_all_disabled():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    policy = build_default_recommendation_policy(
        advisory_rules=(
            AdvisoryRule(
                rule_id="adv-off",
                advisory_field="consistency_summary",
                enabled=False,
            ),
        ),
        weighting_rules=(
            WeightingRule(
                rule_id="wgt-off",
                factor="reserved",
                enabled=False,
            ),
        ),
    )
    engine = RecommendationPolicyEngine(enabled=True, policy=policy, now=now)
    decision = engine.resolve(student_id="7")
    assert decision.applicable is False
    assert decision.reason == REASON_NO_RULES_APPLICABLE


def test_engine_exposes_enabled_weighting_without_applying():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    policy = build_default_recommendation_policy(
        advisory_rules=(),
        weighting_rules=(
            WeightingRule(
                rule_id="wgt-expose",
                factor="consistency_streak",
                weight=0.25,
                enabled=True,
                rationale="declared only",
            ),
        ),
    )
    engine = RecommendationPolicyEngine(enabled=True, policy=policy, now=now)
    decision = engine.resolve(student_id="7")
    assert decision.applicable is True
    assert decision.weighting_applied is False
    assert len(decision.weighting_rules_applicable) == 1
    resolved = decision.weighting_rules_applicable[0]
    assert resolved.applicable is True
    assert resolved.applied_to_ranking is False
    assert resolved.weight == 0.25
    assert "weighting_rules_resolved_not_applied" in resolved.rationale


def test_engine_attach_explainability_does_not_reorder():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        policy=build_default_recommendation_policy(),
        now=now,
    )
    production = [
        {
            "title": "Clear your review backlog",
            "category": "Review",
            "priority": "Critical",
            "reason": "Overdue reviews.",
        },
        {
            "title": "Practice weak topic",
            "category": "Weak Topic",
            "priority": "High",
            "reason": "Low mastery.",
        },
    ]
    result = engine.apply_to_recommendations("7", production)
    assert [r["title"] for r in result] == [r["title"] for r in production]
    assert [r["priority"] for r in result] == [r["priority"] for r in production]
    assert production[0].get(POLICY_EXPLAINABILITY_KEY) is None
    assert result[0][POLICY_EXPLAINABILITY_KEY]["policy_version"]
    assert result[0][POLICY_EXPLAINABILITY_KEY]["rule_identifiers"]
    assert "advisory_inputs_considered" in result[0][POLICY_EXPLAINABILITY_KEY]
    assert result[0][POLICY_EXPLAINABILITY_KEY]["rationale"]
    assert result[0][POLICY_EXPLAINABILITY_KEY]["weighting_applied"] is False
    assert result[0]["authority"] == "runtime_a"


def test_engine_flag_off_leaves_recommendations_untouched():
    engine = RecommendationPolicyEngine(
        enabled=False,
        policy=build_default_recommendation_policy(),
    )
    production = [
        {
            "title": "Clear your review backlog",
            "priority": "Critical",
            "reason": "Overdue reviews.",
        }
    ]
    result = engine.apply_to_recommendations("7", production)
    assert result == production
    assert POLICY_EXPLAINABILITY_KEY not in result[0]


def test_build_engine_respects_enabled_flag():
    assert build_recommendation_policy_engine(enabled=False) is None
    built = build_recommendation_policy_engine(enabled=True)
    assert built is not None
    assert built.is_enabled() is True
    assert built.validate() is None


def test_policy_version_from_environ():
    policy = build_default_recommendation_policy()
    from app.infrastructure.adapters.recommendation_policy import (
        resolve_recommendation_policy,
    )

    resolved = resolve_recommendation_policy(
        environ={
            "KWALITEC_RECOMMENDATION_POLICY_VERSION": "p3.ms003.custom",
            "KWALITEC_RECOMMENDATION_POLICY_ID": "custom-policy",
        }
    )
    assert resolved.version == "p3.ms003.custom"
    assert resolved.policy_id == "custom-policy"
    assert policy.version != resolved.version
