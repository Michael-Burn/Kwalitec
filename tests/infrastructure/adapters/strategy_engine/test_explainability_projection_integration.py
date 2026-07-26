"""Integration tests — Strategy Explainability & Projection (MS-005 S2)."""

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
    StrategyEngineAdapter,
    StrategyExperienceProjectionPort,
    StrategyExplainabilityService,
    StrategyProjector,
    build_strategy_engine_adapter,
    build_strategy_explainability_service,
    build_strategy_projection_port,
    build_strategy_projector,
    explanation_is_complete,
    serialize_canonical,
)


def _runtime_a():
    return {
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


def test_engine_explain_project_roundtrip_deterministic():
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

    adapter = build_strategy_engine_adapter(enabled=True)
    explainability = build_strategy_explainability_service(enabled=True)
    projector = build_strategy_projector(enabled=True)
    port = build_strategy_projection_port(
        enabled=True,
        projector=projector,
        explainability=explainability,
    )
    assert adapter is not None
    assert explainability is not None
    assert projector is not None
    assert port is not None

    context = adapter.assemble_context(
        "11",
        as_of="2026-07-25T12:00:00",
        runtime_a=_runtime_a(),
        twin=twin,
        adaptive=adaptive,
    )
    intervention_a = adapter.evaluate(context)
    intervention_b = adapter.evaluate(context)
    assert intervention_a.serialize() == intervention_b.serialize()
    assert intervention_a.kind == KIND_SESSION_PLAN

    explanation_a = explainability.explain(intervention_a)
    explanation_b = explainability.explain(intervention_b)
    assert explanation_a.serialize() == explanation_b.serialize()
    assert explanation_is_complete(explanation_a)

    projection_a = projector.project(
        intervention_a, explanation=explanation_a, student_id="11"
    )
    projection_b = projector.project(
        intervention_b, explanation=explanation_b, student_id="11"
    )
    assert projection_a.serialize() == projection_b.serialize()

    served = port.serve_projection(intervention_a, student_id="11")
    assert served.serialize() == projection_a.serialize()
    opaque = port.get_tonight_opaque("11")
    assert opaque is not None
    assert opaque["strategy_decision_id"] == intervention_a.intervention_id
    assert opaque["authority"] == "strategy_engine"
    assert isinstance(opaque["session_plan"], dict)


def test_explainability_consistency_across_identical_interventions():
    adapter = StrategyEngineAdapter()
    service = StrategyExplainabilityService()
    context = adapter.assemble_context(
        "77",
        as_of="2026-07-25T08:00:00",
        runtime_a=_runtime_a(),
        twin={
            "twin_id": "twin-77",
            "profile": {
                "session_habits": {"availability": "available", "label": "morning"},
                "learning_rhythm": {"availability": "available", "label": "steady"},
            },
        },
        adaptive={
            "decision_id": "dec-77",
            "recommendation": {
                "topic_code": "T-ADAPTIVE",
                "decision_kind": "NEXT_FOCUS",
            },
            "explanation": {
                "topic_refs": [{"topic_code": "T-ADAPTIVE", "role": "primary"}]
            },
        },
    )
    interventions = [adapter.evaluate(context) for _ in range(3)]
    payloads = [service.explain(item).serialize() for item in interventions]
    assert len(set(payloads)) == 1


def test_projection_does_not_change_engine_behaviour():
    adapter = StrategyEngineAdapter()
    context = adapter.assemble_context(
        "88",
        as_of="2026-07-25T09:00:00",
        runtime_a=_runtime_a(),
        twin={"twin_id": "twin-88", "profile": {}},
        adaptive={
            "decision_id": "dec-88",
            "recommendation": {
                "topic_code": "T-ADAPTIVE",
                "decision_kind": "NEXT_FOCUS",
            },
        },
    )
    before = adapter.evaluate(context).serialize()
    explainability = StrategyExplainabilityService()
    projector = StrategyProjector()
    port = StrategyExperienceProjectionPort(
        projector=projector, explainability=explainability
    )
    intervention = adapter.evaluate(context)
    port.serve_projection(intervention, student_id="88")
    after = adapter.evaluate(context).serialize()
    assert before == after
    assert (
        serialize_canonical(intervention.to_canonical_dict())
        == intervention.serialize()
    )
