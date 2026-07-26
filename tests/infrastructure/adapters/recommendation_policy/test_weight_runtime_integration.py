"""Policy weight Runtime A integration + flag isolation (P3-MS004)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.decision_simulation import (
    DecisionSimulationService,
)
from app.infrastructure.adapters.evidence_platform.contracts import (
    ConsistencySummary,
    EngagementSummary,
    EvidenceAdvisory,
)
from app.infrastructure.adapters.recommendation_policy import (
    WEIGHT_EXPLAINABILITY_KEY,
    RecommendationPolicyEngine,
    build_default_weighting_policy,
    build_recommendation_policy_engine,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.services.recommendation_service import RecommendationService
from tests.conftest import _make_user


def _advisory(*, generated_at: str, streak: int = 7) -> EvidenceAdvisory:
    return EvidenceAdvisory(
        advisory_id="evadv-runtime-weight",
        student_id="1",
        consistency_summary=ConsistencySummary(
            active_streak=streak,
            source_description="Derived from recorded study activity.",
        ),
        engagement_summary=EngagementSummary(),
        generated_at=generated_at,
        evidence_summary_id="evsum-runtime-weight",
        availability="available",
    )


class _StubAdvisoryInjection:
    def __init__(self, advisory: EvidenceAdvisory | None) -> None:
        self.last_advisory = advisory
        self.last_consideration = None

    def prepare_for_recommendation(self, user_id):  # noqa: ANN001
        return None


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


def test_policy_weighting_flag_isolation():
    weight_only = resolve_v2_feature_flags(
        environ={"KWALITEC_POLICY_WEIGHTING": "1"}
    )
    assert weight_only.ENABLE_POLICY_WEIGHTING is True
    assert weight_only.ENABLE_RECOMMENDATION_POLICY is False
    assert weight_only.ENABLE_CONTROLLED_ADVISORY is False
    assert weight_only.ENABLE_ADVISORY_OUTCOME_MEASUREMENT is False
    assert weight_only.ENABLE_DECISION_SIMULATION is False
    assert weight_only.ENABLE_ADAPTIVE_ENGINE is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_RECOMMENDATION_POLICY": "1",
            "KWALITEC_CONTROLLED_ADVISORY": "1",
            "KWALITEC_DECISION_SIMULATION": "1",
        }
    )
    assert others_only.ENABLE_POLICY_WEIGHTING is False
    assert others_only.ENABLE_RECOMMENDATION_POLICY is True


def test_composition_wires_weighting_when_flag_on():
    off_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(environ={})
    )
    assert off_composition.recommendation_policy is None

    on_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_POLICY_WEIGHTING": "1"}
        )
    )
    assert on_composition.recommendation_policy is not None
    assert on_composition.recommendation_policy.is_weighting_enabled() is True
    assert on_composition.controlled_advisory is None


def test_recommendation_service_applies_weight_under_runtime_a(ctx):
    user = _make_user()
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=True,
        policy=build_default_weighting_policy(rollout_percentage=100),
        now=now,
    )
    advisory = _advisory(generated_at="2026-07-24T12:00:00+00:00", streak=7)
    injection = _StubAdvisoryInjection(advisory)
    baseline = RecommendationService.generate_recommendations(user.id, limit=5)
    governed = RecommendationService.generate_recommendations(
        user.id,
        limit=5,
        advisory_injection=injection,
        recommendation_policy=engine,
        simulation_service=DecisionSimulationService(enabled=True),
    )
    assert engine.last_weight_application is not None
    assert engine.last_weight_application.applied is True
    assert engine.last_simulation_divergence is not None
    assert engine.last_simulation_divergence["diverged"] is False
    if governed:
        assert WEIGHT_EXPLAINABILITY_KEY in governed[0]
        explain = governed[0][WEIGHT_EXPLAINABILITY_KEY]
        assert explain["policy_version"]
        assert explain["rule_identifier"]
        assert explain["original_weight"] is not None
        assert explain["adjusted_weight"] is not None
        assert explain["advisory_provenance"]
        assert explain["authority"] == "runtime_a"
        assert WEIGHT_EXPLAINABILITY_KEY not in baseline[0]
    # Runtime A still produced the recommendation titles.
    for item in governed:
        assert "title" in item
        assert item.get("authority") == "runtime_a"


def test_recommendation_service_without_weighting_unchanged(ctx):
    user = _make_user()
    result = RecommendationService.generate_recommendations(user.id, limit=5)
    for item in result:
        assert WEIGHT_EXPLAINABILITY_KEY not in item


def test_build_engine_weighting_only():
    assert build_recommendation_policy_engine(
        enabled=False, weighting_enabled=False
    ) is None
    built = build_recommendation_policy_engine(
        enabled=False,
        weighting_enabled=True,
        environ={"KWALITEC_POLICY_WEIGHTING_ROLLOUT_PERCENTAGE": "100"},
    )
    assert built is not None
    assert built.is_weighting_enabled() is True
