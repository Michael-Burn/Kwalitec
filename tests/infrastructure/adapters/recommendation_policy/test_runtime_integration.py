"""Recommendation Policy Runtime A integration + flag isolation (P3-MS003)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.recommendation_policy import (
    POLICY_EXPLAINABILITY_KEY,
    RecommendationPolicyEngine,
    build_default_recommendation_policy,
    build_recommendation_policy_engine,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.services.recommendation_service import RecommendationService
from tests.conftest import _make_user


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


def test_recommendation_policy_flag_isolation():
    policy_only = resolve_v2_feature_flags(
        environ={"KWALITEC_RECOMMENDATION_POLICY": "1"}
    )
    assert policy_only.ENABLE_RECOMMENDATION_POLICY is True
    assert policy_only.ENABLE_POLICY_WEIGHTING is False
    assert policy_only.ENABLE_CONTROLLED_ADVISORY is False
    assert policy_only.ENABLE_ADVISORY_OUTCOME_MEASUREMENT is False
    assert policy_only.ENABLE_ADVISORY_EVALUATION is False
    assert policy_only.ENABLE_DECISION_SIMULATION is False
    assert policy_only.ENABLE_EVIDENCE_ADVISORY is False
    assert policy_only.ENABLE_RECOVERY_PLANNER is False
    assert policy_only.ENABLE_ADAPTIVE_ENGINE is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_CONTROLLED_ADVISORY": "1",
            "KWALITEC_ADVISORY_OUTCOME_MEASUREMENT": "1",
            "KWALITEC_ADVISORY_EVALUATION": "1",
            "KWALITEC_DECISION_SIMULATION": "1",
            "KWALITEC_EVIDENCE_ADVISORY": "1",
            "KWALITEC_POLICY_WEIGHTING": "1",
        }
    )
    assert others_only.ENABLE_RECOMMENDATION_POLICY is False
    assert others_only.ENABLE_CONTROLLED_ADVISORY is True
    assert others_only.ENABLE_POLICY_WEIGHTING is True


def test_composition_wires_policy_engine_when_flag_on():
    off_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(environ={})
    )
    assert off_composition.recommendation_policy is None

    on_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_RECOMMENDATION_POLICY": "1"}
        )
    )
    assert on_composition.recommendation_policy is not None
    assert on_composition.recommendation_policy.is_enabled() is True
    assert on_composition.controlled_advisory is None
    assert on_composition.advisory_outcome_measurement is None


def test_recommendation_service_attaches_policy_explainability(ctx):
    user = _make_user()
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        policy=build_default_recommendation_policy(),
        now=now,
    )
    baseline = RecommendationService.generate_recommendations(user.id, limit=5)
    governed = RecommendationService.generate_recommendations(
        user.id,
        limit=5,
        recommendation_policy=engine,
    )
    assert engine.last_decision is not None
    assert engine.last_decision.applicable is True
    assert [r["title"] for r in governed] == [r["title"] for r in baseline]
    assert [r["priority"] for r in governed] == [r["priority"] for r in baseline]
    if governed:
        assert POLICY_EXPLAINABILITY_KEY in governed[0]
        explain = governed[0][POLICY_EXPLAINABILITY_KEY]
        assert explain["policy_version"]
        assert explain["rule_identifiers"]
        assert "advisory_inputs_considered" in explain
        assert explain["rationale"]
        assert explain["weighting_applied"] is False
        assert explain["authority"] == "runtime_a"
        assert POLICY_EXPLAINABILITY_KEY not in baseline[0]


def test_recommendation_service_without_policy_unchanged(ctx):
    user = _make_user()
    result = RecommendationService.generate_recommendations(user.id, limit=5)
    for item in result:
        assert POLICY_EXPLAINABILITY_KEY not in item


def test_runtime_a_retains_final_authority(ctx):
    """Policy never invents recommendations — Runtime A produces them."""
    user = _make_user()
    engine = build_recommendation_policy_engine(enabled=True)
    assert engine is not None
    decision = engine.resolve_for_recommendation(user.id)
    # Decision has no recommendation payload.
    payload = decision.to_canonical_dict()
    assert "recommendations" not in payload
    assert "title" not in payload
    assert "priority" not in payload

    produced = RecommendationService.generate_recommendations(
        user.id, limit=3, recommendation_policy=engine
    )
    # Titles come from Runtime A ranking, not from policy.
    for item in produced:
        assert "title" in item
        assert item.get("authority") == "runtime_a"
