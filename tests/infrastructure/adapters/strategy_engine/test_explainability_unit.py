"""Unit tests — Strategy Explainability (MS-005 S2)."""

from __future__ import annotations

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.strategy_engine import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    EXPLAINABILITY_VERSION,
    KIND_SESSION_PLAN,
    StrategyContextAssembler,
    StrategyEngine,
    StrategyExplainabilityService,
    StrategyExplainabilityValidationError,
    StrategyExplanationBundle,
    StrategyWhyExplanation,
    TwinFactorConsidered,
    TwinFactorsExplanation,
    build_strategy_explainability_service,
    explanation_is_complete,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


def _runtime_a(**overrides):
    base = {
        "mission": {
            "mission_id": "9",
            "topic_code": "T-MISSION",
            "status": "pending",
        },
        "lifecycle_stage": "Learning",
        "student_goals": {"daily_minutes": 50, "study_plan_id": "plan-1"},
        "evidence": {"evidence_id": "ev-1", "attempts": []},
        "topic_progress": [
            {"topic_id": "T-MISSION", "topic_name": "Mission", "mastery_score": 0.4},
            {"topic_id": "T-ALT", "topic_name": "Alt", "mastery_score": 0.2},
        ],
        "study_attempts": [
            {"id": "a1", "score": 0.3, "outcome": "pass"},
            {"id": "a2", "score": 0.5, "outcome": "pass"},
        ],
    }
    base.update(overrides)
    return base


def _twin(**overrides):
    profile = {
        "cognitive_load_indicators": {
            "label": "medium",
            "availability": "available",
        },
        "confidence_trend": {
            "label": "high confidence",
            "availability": "available",
        },
        "session_habits": {"label": "evening", "availability": "available"},
        "learning_rhythm": {"label": "steady", "availability": "available"},
        "persistence": {"label": "recovering", "availability": "available"},
        "revision_behaviour": {"label": "active", "availability": "available"},
        "consistency": {"label": "regular", "availability": "available"},
    }
    profile.update(overrides.get("profile", {}))
    payload = {
        "twin_id": "twin-1",
        "snapshot_version": "snap-1",
        "profile": profile,
    }
    for key, value in overrides.items():
        if key != "profile":
            payload[key] = value
    return payload


def _adaptive(**overrides):
    base = {
        "decision_id": "adaptive-7",
        "recommendation": {
            "topic_code": "T-ADAPTIVE",
            "title": "Adaptive Topic",
            "decision_kind": "NEXT_FOCUS",
        },
        "explanation": {
            "topic_refs": [
                {"topic_code": "T-ADAPTIVE", "role": "primary"},
                {"topic_code": "T-ALT", "role": "alternative"},
            ]
        },
        "alternatives": [{"topic_code": "T-ALT"}],
    }
    base.update(overrides)
    return base


def _full_intervention(**kwargs):
    assembler = StrategyContextAssembler()
    context = assembler.assemble(
        kwargs.pop("student_id", "42"),
        as_of="2026-07-25T10:00:00",
        runtime_a=kwargs.pop("runtime_a", _runtime_a()),
        twin=kwargs.pop("twin", _twin()),
        adaptive=kwargs.pop("adaptive", _adaptive()),
    )
    return StrategyEngine().evaluate(context)


def test_explanation_dtos_are_immutable():
    why = StrategyWhyExplanation(summary="because", reason_codes=("kind:SESSION_PLAN",))
    factor = TwinFactorConsidered(
        facet_id="learning_rhythm",
        availability="available",
        role="modulator",
    )
    bundle = StrategyExplanationBundle(
        intervention_id="s1-abc",
        educational_objective="Complete tonight's session",
        why=why,
        twin_factors=TwinFactorsExplanation(
            snapshot_ref="twin-1",
            factors_considered=(factor,),
            summary="modulated",
        ),
    )
    with pytest.raises((TypeError, AttributeError)):
        bundle.intervention_id = "x"  # type: ignore[misc]
    with pytest.raises((TypeError, AttributeError)):
        why.reason_codes = ("x",)  # type: ignore[misc]


def test_explain_covers_mandatory_questions():
    service = StrategyExplainabilityService()
    intervention = _full_intervention()
    bundle = service.explain(intervention)

    assert isinstance(bundle, StrategyExplanationBundle)
    assert bundle.explainability_version == EXPLAINABILITY_VERSION
    assert bundle.educational_objective
    assert bundle.why.summary
    assert bundle.why.reason_codes
    assert bundle.runtime_a_evidence_refs
    assert bundle.twin_factors.snapshot_ref
    assert bundle.adaptive_consumed.availability == AVAILABILITY_AVAILABLE
    assert bundle.adaptive_consumed.decision_id
    assert bundle.educational_principles
    for principle in bundle.educational_principles:
        assert principle.principle_id
        assert principle.how_applied
    assert bundle.confidence.band in {"low", "medium", "high"}
    assert bundle.confidence.rationale
    assert bundle.limitations is not None
    assert bundle.alternatives is not None
    assert bundle.planner_contributions
    planner_ids = {item.planner_id for item in bundle.planner_contributions}
    assert planner_ids == {
        "study_planner",
        "session_planner",
        "revision_planner",
        "recovery_planner",
        "fatigue_manager",
        "confidence_manager",
        "intervention_planner",
    }
    assert explanation_is_complete(bundle)
    assert intervention.kind == KIND_SESSION_PLAN


def test_explain_is_deterministic():
    service = StrategyExplainabilityService()
    intervention = _full_intervention()
    left = service.explain(intervention).serialize()
    right = service.explain(intervention).serialize()
    assert left == right
    assert serialize_canonical(
        service.explain(intervention).to_canonical_dict()
    ) == left


def test_explain_serialization_stable_keys():
    service = StrategyExplainabilityService()
    bundle = service.explain(_full_intervention())
    payload = bundle.to_canonical_dict()
    assert set(payload) >= {
        "why",
        "runtime_a_evidence_refs",
        "twin_factors",
        "adaptive_consumed",
        "educational_principles",
        "confidence",
        "alternatives",
        "limitations",
        "planner_contributions",
        "educational_objective",
    }
    assert serialize_canonical(payload) == bundle.serialize()


def test_explain_documents_unavailable_adaptive():
    service = StrategyExplainabilityService()
    intervention = _full_intervention(adaptive={})
    bundle = service.explain(intervention)
    assert bundle.adaptive_consumed.availability == AVAILABILITY_UNAVAILABLE
    assert bundle.adaptive_consumed.unavailable_reason
    assert "adaptive_unavailable" in bundle.limitations.codes


def test_explain_documents_unavailable_twin():
    service = StrategyExplainabilityService()
    intervention = _full_intervention(twin={})
    bundle = service.explain(intervention)
    assert "twin_unavailable" in bundle.limitations.codes
    assert bundle.twin_factors.summary


def test_disabled_service_raises():
    service = StrategyExplainabilityService(enabled=False)
    with pytest.raises(StrategyExplainabilityValidationError):
        service.explain(_full_intervention())


def test_build_helper_respects_flag():
    assert build_strategy_explainability_service(enabled=False) is None
    built = build_strategy_explainability_service(enabled=True)
    assert built is not None
    assert built.is_enabled()


def test_flag_default_off_and_di_none():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_STRATEGY_ENGINE is False
    composition, _ = build_production_experience(flags=flags)
    assert composition.strategy_engine is None
    assert composition.strategy_explainability is None
    assert composition.strategy_projector is None
    assert composition.strategy_projection_port is None


def test_flag_on_wires_explainability_di():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_STRATEGY_ENGINE": "1"}
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.strategy_engine is not None
    assert composition.strategy_explainability is not None
    assert composition.strategy_explainability.is_enabled()
