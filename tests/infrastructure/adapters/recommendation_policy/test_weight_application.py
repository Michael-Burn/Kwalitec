"""Policy-governed weight application engine tests (P3-MS004)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.infrastructure.adapters.evidence_platform.contracts import (
    ConsistencySummary,
    EngagementSummary,
    EvidenceAdvisory,
)
from app.infrastructure.adapters.recommendation_policy import (
    DEFAULT_APPLIED_WEIGHTING_RULE_ID,
    DEFAULT_MAX_WEIGHT_ADJUSTMENT,
    REASON_WEIGHT_ADVISORY_STALE,
    REASON_WEIGHT_APPLIED,
    REASON_WEIGHT_ROLLOUT_EXCLUDED,
    REASON_WEIGHTING_FLAG_OFF,
    WEIGHT_EXPLAINABILITY_KEY,
    RecommendationPolicyEngine,
    build_default_weighting_policy,
    weight_explainability_fields_present,
)


def _advisory(*, generated_at: str, streak: int = 7) -> EvidenceAdvisory:
    return EvidenceAdvisory(
        advisory_id="evadv-weight",
        student_id="7",
        consistency_summary=ConsistencySummary(
            active_streak=streak,
            source_description="Derived from recorded study activity.",
        ),
        engagement_summary=EngagementSummary(),
        generated_at=generated_at,
        evidence_summary_id="evsum-weight",
        availability="available",
    )


def test_resolve_weight_application_when_allowed():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=True,
        policy=build_default_weighting_policy(rollout_percentage=100),
        now=now,
    )
    advisory = _advisory(generated_at="2026-07-24T12:00:00+00:00", streak=7)
    application = engine.resolve_weight_application(
        student_id="7", advisory=advisory
    )
    assert application.applied is True
    assert application.rule_id == DEFAULT_APPLIED_WEIGHTING_RULE_ID
    assert application.advisory_field == "consistency_summary"
    assert application.base_weight == 1.0
    assert application.adjusted_weight == pytest.approx(
        1.0 + DEFAULT_MAX_WEIGHT_ADJUSTMENT
    )
    assert REASON_WEIGHT_APPLIED in application.adjustment_reason
    assert abs(application.delta) <= DEFAULT_MAX_WEIGHT_ADJUSTMENT + 1e-9
    assert application.provenance.get("advisory_id") == "evadv-weight"


def test_resolve_weight_denied_when_flag_off():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=False,
        policy=build_default_weighting_policy(rollout_percentage=100),
        now=now,
    )
    application = engine.resolve_weight_application(
        student_id="7",
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert application.applied is False
    assert application.adjustment_reason == REASON_WEIGHTING_FLAG_OFF
    assert application.base_weight == application.adjusted_weight


def test_resolve_weight_denied_when_rollout_zero():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=True,
        policy=build_default_weighting_policy(rollout_percentage=0),
        now=now,
    )
    application = engine.resolve_weight_application(
        student_id="7",
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert application.applied is False
    assert application.adjustment_reason == REASON_WEIGHT_ROLLOUT_EXCLUDED


def test_resolve_weight_denied_when_stale():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=True,
        policy=build_default_weighting_policy(
            rollout_percentage=100, max_age_hours=1
        ),
        now=now,
    )
    application = engine.resolve_weight_application(
        student_id="7",
        advisory=_advisory(generated_at="2026-07-20T12:00:00+00:00"),
    )
    assert application.applied is False
    assert application.adjustment_reason == REASON_WEIGHT_ADVISORY_STALE


def test_apply_weight_records_explainability_and_bounds():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=True,
        policy=build_default_weighting_policy(rollout_percentage=100),
        now=now,
    )
    production = [
        {
            "title": "Practice weak topic",
            "category": "Weak Topic",
            "priority": "High",
            "reason": "Low mastery.",
        },
        {
            "title": "Clear your review backlog",
            "category": "Review",
            "priority": "Critical",
            "reason": "Overdue reviews.",
        },
    ]
    result = engine.apply_weight_to_recommendations(
        "7",
        production,
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00", streak=7),
    )
    assert production[0].get(WEIGHT_EXPLAINABILITY_KEY) is None
    assert WEIGHT_EXPLAINABILITY_KEY in result[0]
    explain = result[0][WEIGHT_EXPLAINABILITY_KEY]
    assert weight_explainability_fields_present(explain) is True
    assert explain["applied"] is True
    assert explain["advisory_field"] == "consistency_summary"
    assert abs(explain["adjusted_weight"] - explain["original_weight"]) <= (
        DEFAULT_MAX_WEIGHT_ADJUSTMENT + 1e-9
    )
    # Critical should rank above High after weight application.
    assert result[0]["priority"] == "Critical"
    assert result[0]["scoring_weight"] > result[1]["scoring_weight"]


def test_apply_weight_records_denial_reason_without_reorder():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=True,
        policy=build_default_weighting_policy(rollout_percentage=0),
        now=now,
    )
    production = [
        {"title": "A", "priority": "High", "reason": "x"},
        {"title": "B", "priority": "Critical", "reason": "y"},
    ]
    result = engine.apply_weight_to_recommendations(
        "7",
        production,
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert [r["title"] for r in result] == ["A", "B"]
    assert result[0][WEIGHT_EXPLAINABILITY_KEY]["applied"] is False
    assert (
        result[0][WEIGHT_EXPLAINABILITY_KEY]["adjustment_reason"]
        == REASON_WEIGHT_ROLLOUT_EXCLUDED
    )


def test_rollback_flag_off_leaves_recommendations_untouched():
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=False,
        policy=build_default_weighting_policy(rollout_percentage=100),
    )
    production = [
        {"title": "A", "priority": "Critical", "reason": "x"},
    ]
    result = engine.apply_weight_to_recommendations(
        "7",
        production,
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert result == production
    assert WEIGHT_EXPLAINABILITY_KEY not in result[0]


def test_simulation_consistency_no_divergence():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=True,
        policy=build_default_weighting_policy(rollout_percentage=100),
        now=now,
    )
    advisory = _advisory(generated_at="2026-07-24T12:00:00+00:00", streak=4)
    production = [
        {"title": "A", "priority": "Medium", "reason": "x"},
        {"title": "B", "priority": "High", "reason": "y"},
    ]
    weighted = engine.apply_weight_to_recommendations(
        "7", production, advisory=advisory
    )
    mirrored = engine.apply_weight_to_recommendations(
        "7",
        [
            {"title": "A", "priority": "Medium", "reason": "x"},
            {"title": "B", "priority": "High", "reason": "y"},
        ],
        advisory=advisory,
    )
    comparison = engine.compare_weight_simulation(weighted, mirrored)
    assert comparison["diverged"] is False
    assert comparison["divergence_count"] == 0


def test_simulation_flags_divergence_beyond_tolerance():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    engine = RecommendationPolicyEngine(
        enabled=True,
        weighting_enabled=True,
        policy=build_default_weighting_policy(
            rollout_percentage=100, divergence_tolerance=0.001
        ),
        now=now,
    )
    production = [{"title": "A", "priority": "High", "scoring_weight": 1.0}]
    simulated = [{"title": "A", "priority": "High", "scoring_weight": 1.05}]
    comparison = engine.compare_weight_simulation(production, simulated)
    assert comparison["diverged"] is True
    assert comparison["divergence_count"] == 1
