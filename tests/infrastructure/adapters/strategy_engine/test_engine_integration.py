"""Integration tests — Strategy Engine orchestration (MS-005 S1)."""

from __future__ import annotations

from app.infrastructure.adapters.adaptive_engine.contracts import (
    AdaptiveOutputBundle,
    ConfidencePlaceholder,
    ExplanationBundle,
    RecommendationPlaceholder,
    TopicRef,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    CognitiveLoadIndicatorsFacet,
    ConfidenceTrendFacet,
    TwinProfile,
    TwinSnapshot,
)
from app.infrastructure.adapters.strategy_engine import (
    KIND_SESSION_PLAN,
    StrategyContextAssembler,
    StrategyEngine,
    StrategyEngineAdapter,
    build_strategy_engine_adapter,
)


def test_assemble_evaluate_roundtrip_with_contract_dtos():
    twin = TwinSnapshot(
        twin_id="twin-dto",
        snapshot_version="sv-1",
        profile=TwinProfile(
            student_id="11",
            cognitive_load_indicators=CognitiveLoadIndicatorsFacet(
                label="low",
                availability="available",
                unavailable_reason="",
            ),
            confidence_trend=ConfidenceTrendFacet(
                label="cautious",
                availability="available",
                unavailable_reason="",
            ),
        ),
    )
    adaptive = AdaptiveOutputBundle(
        decision_id="dec-11",
        recommendation=RecommendationPlaceholder(
            topic_code="T-ADAPTIVE",
            title="Adaptive",
            decision_kind="NEXT_FOCUS",
            label="Adaptive",
        ),
        confidence=ConfidencePlaceholder(band="medium", rationale="stable"),
        explanation=ExplanationBundle(
            topic_refs=(
                TopicRef(topic_code="T-ADAPTIVE", title="Adaptive", role="primary"),
                TopicRef(topic_code="T-ALT", title="Alt", role="alternative"),
            ),
            why_summary="next incomplete leaf",
        ),
    )
    runtime_a = {
        "mission": {
            "mission_id": "21",
            "topic_code": "T-MISSION",
            "status": "pending",
        },
        "lifecycle_stage": "Learning",
        "student_goals": {"daily_minutes": 40},
        "evidence": {"evidence_id": "ev-21"},
        "topic_progress": [
            {"topic_id": "T-MISSION", "mastery_score": 0.55},
        ],
        "study_attempts": [{"id": "att-1", "score": 0.5}],
    }

    adapter = build_strategy_engine_adapter(enabled=True)
    assert adapter is not None
    context = adapter.assemble_context(
        "11",
        as_of="2026-07-25T12:00:00+00:00",
        runtime_a=runtime_a,
        twin=twin,
        adaptive=adaptive,
    )
    assert context.twin_ref == "sv-1"
    assert context.adaptive_recommendation_ref == "dec-11"
    assert context.runtime_a_availability == "available"
    assert context.twin_availability == "available"
    assert context.adaptive_availability == "available"

    intervention = adapter.evaluate(context)
    assert intervention.kind == KIND_SESSION_PLAN
    assert intervention.session.primary_topic == "T-MISSION"
    assert intervention.session.advisory_topic == "T-ADAPTIVE"
    assert list(intervention.study.focus_topics) == ["T-ADAPTIVE", "T-ALT"]
    assert intervention.adaptive_recommendation_ref == "dec-11"
    assert intervention.twin_ref == "sv-1"

    # Determinism across assemble → evaluate path.
    again = adapter.evaluate(
        StrategyContextAssembler().assemble(
            "11",
            as_of="2026-07-25T12:00:00+00:00",
            runtime_a=runtime_a,
            twin=twin,
            adaptive=adaptive,
        )
    )
    assert again.serialize() == intervention.serialize()


def test_planner_consistency_across_engine_and_direct_calls():
    runtime_a = {
        "mission": {"mission_id": "3", "topic_code": "T1", "status": "pending"},
        "lifecycle_stage": "Learning",
        "student_goals": {"daily_minutes": 45},
        "evidence": {"evidence_id": "e3"},
        "study_attempts": [{"id": "1"}, {"id": "2"}, {"id": "3"}],
    }
    twin = {
        "twin_id": "t3",
        "snapshot_version": "s3",
        "profile": {
            "cognitive_load_indicators": {
                "label": "medium",
                "availability": "available",
            },
            "confidence_trend": {
                "label": "high confidence",
                "availability": "available",
            },
        },
    }
    adaptive = {
        "decision_id": "d3",
        "recommendation": {"topic_code": "T9"},
        "alternatives": [{"topic_code": "T8"}],
    }
    context = StrategyContextAssembler().assemble(
        "3",
        as_of="2026-07-25T09:00:00+00:00",
        runtime_a=runtime_a,
        twin=twin,
        adaptive=adaptive,
    )
    engine = StrategyEngine()
    intervention = engine.evaluate(context)
    # All components derive from the same context fingerprint.
    assert intervention.study.focus_topics[0] == "T9"
    assert intervention.session.primary_topic == "T1"
    assert intervention.revision.primary_revision_topic == "T9"
    assert intervention.fatigue.severity_band in {"low", "medium", "high", "critical"}
    assert intervention.confidence.divergence_band in {
        "none",
        "mild",
        "material",
        "severe",
    }
    assert intervention.sequencing.primary_kind == KIND_SESSION_PLAN


def test_orchestrate_rejects_invalid_identity():
    result = StrategyEngineAdapter().orchestrate(" ")
    assert result.ok is False
    assert result.error_code == "INVALID_STATE"
