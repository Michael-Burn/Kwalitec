"""Unit / serialization / immutability tests — Learning Strategy Contracts (S0)."""

from __future__ import annotations

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.strategy_engine import (
    InterventionStep,
    LearningIntervention,
    StrategyContext,
    StrategyEngineAdapter,
    StrategyExplanationPlaceholder,
    StrategyProvenancePlaceholder,
    empty_learning_intervention,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


def test_context_requires_student_id():
    with pytest.raises(ValueError, match="student_id"):
        StrategyContext(student_id="  ")


def test_context_is_immutable():
    context = StrategyContext(
        student_id="7",
        adaptive_recommendation_ref="a1",
        twin_ref="t1",
        runtime_a_evidence_ref="e1",
        intervention_kinds=("SESSION_PLAN",),
        field_provenance={"adaptive": {"availability": "unavailable"}},
        authority_tags=["runtime_a"],
    )
    with pytest.raises(Exception):
        context.student_id = "8"  # type: ignore[misc]
    with pytest.raises(TypeError):
        context.field_provenance["adaptive"] = {}  # type: ignore[index]
    with pytest.raises(AttributeError):
        context.intervention_kinds.append("REVISION_PLAN")  # type: ignore[attr-defined]


def test_intervention_and_steps_are_immutable():
    intervention = LearningIntervention(
        intervention_id="i1",
        educational_objective="structure tonight",
        explanation=StrategyExplanationPlaceholder(
            why_summary="placeholder",
            educational_principle_ids=("ep.director.nightly_topic",),
        ),
        provenance=StrategyProvenancePlaceholder(
            source_service="strategy_engine",
            kind="strategy_derived",
        ),
        kind="SESSION_PLAN",
        steps=(
            InterventionStep(order=1, action_code="orient", summary="Confirm topic"),
        ),
        topic_refs=("T1",),
        limitations=("contracts_only",),
    )
    with pytest.raises(Exception):
        intervention.intervention_id = "x"  # type: ignore[misc]
    with pytest.raises(Exception):
        intervention.explanation.why_summary = "mutated"  # type: ignore[misc]
    with pytest.raises(AttributeError):
        intervention.steps.append(  # type: ignore[attr-defined]
            InterventionStep(order=2, action_code="study", summary="Study")
        )
    with pytest.raises(AttributeError):
        intervention.topic_refs.append("T2")  # type: ignore[attr-defined]


def test_provenance_and_explanation_immutable():
    explanation = StrategyExplanationPlaceholder(
        why_summary="why",
        limitations_codes=("sparse",),
    )
    provenance = StrategyProvenancePlaceholder(
        source_service="strategy_engine",
        availability="unavailable",
        kind="strategy_derived",
    )
    with pytest.raises(Exception):
        explanation.why_summary = "x"  # type: ignore[misc]
    with pytest.raises(Exception):
        provenance.kind = "fact"  # type: ignore[misc]


def test_identical_contexts_serialize_identically():
    left = StrategyContext(
        student_id="1",
        as_of="2026-07-25T10:00:00+00:00",
        adaptive_recommendation_ref="adaptive-1",
        twin_ref="twin-1",
        runtime_a_evidence_ref="evidence-1",
        adaptive_availability="available",
        twin_availability="unavailable",
        runtime_a_availability="available",
        twin_unavailable_reason="contracts_only",
        intervention_kinds=("SESSION_PLAN", "RECOVERY_PLAN"),
        lifecycle_stage="Learning",
        mission_id="9",
        field_provenance={"adaptive": {"availability": "available"}},
        authority_tags=["runtime_a", "adaptive_engine"],
    )
    right = StrategyContext(
        student_id="1",
        as_of="2026-07-25T10:00:00+00:00",
        twin_ref="twin-1",
        adaptive_recommendation_ref="adaptive-1",
        runtime_a_evidence_ref="evidence-1",
        twin_availability="unavailable",
        adaptive_availability="available",
        runtime_a_availability="available",
        twin_unavailable_reason="contracts_only",
        intervention_kinds=("SESSION_PLAN", "RECOVERY_PLAN"),
        lifecycle_stage="Learning",
        mission_id="9",
        authority_tags=["runtime_a", "adaptive_engine"],
        field_provenance={"adaptive": {"availability": "available"}},
    )
    assert left.serialize() == right.serialize()
    assert serialize_canonical(left.to_canonical_dict()) == left.serialize()


def test_identical_interventions_serialize_identically():
    left = LearningIntervention(
        intervention_id="int-1",
        strategy_version="s0.1",
        adaptive_recommendation_ref="adaptive-1",
        twin_ref="twin-1",
        runtime_a_evidence_ref="evidence-1",
        educational_objective="Complete tonight's session",
        explanation=StrategyExplanationPlaceholder(
            why_summary="placeholder",
            educational_principle_ids=("ep.session.completable_shell",),
            input_summary="student_id=1",
        ),
        provenance=StrategyProvenancePlaceholder(
            source_service="strategy_engine",
            source_entity="LearningIntervention",
            collected_at="2026-07-25T10:00:00+00:00",
            availability="unavailable",
            unavailable_reason="contracts_only_no_assembly",
            kind="strategy_derived",
        ),
        kind="SESSION_PLAN",
        steps=(
            InterventionStep(
                order=1,
                action_code="orient",
                summary="Confirm topic",
                minutes=5,
                intent="orient",
            ),
            InterventionStep(order=2, action_code="practice_close", summary="Close"),
        ),
        topic_refs=("T2", "T1"),
        educational_principle_ids=("ep.session.completable_shell",),
        runtime_a_refs=("mission:9",),
        minutes_budget=45,
        limitations=("contracts_only",),
    )
    right = LearningIntervention(
        intervention_id="int-1",
        strategy_version="s0.1",
        twin_ref="twin-1",
        adaptive_recommendation_ref="adaptive-1",
        runtime_a_evidence_ref="evidence-1",
        educational_objective="Complete tonight's session",
        provenance=StrategyProvenancePlaceholder(
            source_entity="LearningIntervention",
            source_service="strategy_engine",
            collected_at="2026-07-25T10:00:00+00:00",
            availability="unavailable",
            unavailable_reason="contracts_only_no_assembly",
            kind="strategy_derived",
        ),
        explanation=StrategyExplanationPlaceholder(
            input_summary="student_id=1",
            why_summary="placeholder",
            educational_principle_ids=("ep.session.completable_shell",),
        ),
        kind="SESSION_PLAN",
        steps=(
            InterventionStep(
                order=1,
                action_code="orient",
                summary="Confirm topic",
                minutes=5,
                intent="orient",
            ),
            InterventionStep(order=2, action_code="practice_close", summary="Close"),
        ),
        topic_refs=("T2", "T1"),
        educational_principle_ids=("ep.session.completable_shell",),
        runtime_a_refs=("mission:9",),
        minutes_budget=45,
        limitations=("contracts_only",),
    )
    assert left.serialize() == right.serialize()
    assert serialize_canonical(left.to_canonical_dict()) == left.serialize()


def test_evaluate_is_deterministic():
    adapter = StrategyEngineAdapter()
    context = StrategyContext(
        student_id="99",
        as_of="2026-07-25T12:00:00+00:00",
        adaptive_recommendation_ref="a",
        twin_ref="t",
        runtime_a_evidence_ref="e",
    )
    first = adapter.evaluate(context)
    second = adapter.evaluate(context)
    assert first.serialize() == second.serialize()


def test_orchestrate_rejects_empty_student_id():
    result = StrategyEngineAdapter().orchestrate(" ")
    assert result.ok is False
    assert result.error_code == "INVALID_STATE"


def test_orchestrate_rejects_mismatched_context_student_id():
    result = StrategyEngineAdapter().orchestrate(
        "1",
        context=StrategyContext(student_id="2"),
    )
    assert result.ok is False
    assert result.error_code == "INVALID_STATE"


def test_empty_intervention_stub_is_structurally_complete():
    intervention = empty_learning_intervention(
        context=StrategyContext(
            student_id="1",
            adaptive_recommendation_ref="a1",
            twin_ref="t1",
            runtime_a_evidence_ref="e1",
        )
    )
    assert intervention.adaptive_recommendation_ref == "a1"
    assert intervention.twin_ref == "t1"
    assert intervention.runtime_a_evidence_ref == "e1"
    assert intervention.authority == "strategy_engine"
    assert intervention.provenance.unavailable_reason == "empty_authentic"
    assert "study" in intervention.to_canonical_dict()
    assert "sequencing" in intervention.to_canonical_dict()


def test_flag_default_off_and_di_wiring():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_STRATEGY_ENGINE is False
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.strategy_engine is None

    flags_on = resolve_v2_feature_flags(environ={"KWALITEC_STRATEGY_ENGINE": "1"})
    assert flags_on.ENABLE_STRATEGY_ENGINE is True
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.strategy_engine, StrategyEngineAdapter)
    assert composition_on.strategy_engine.adapter_id == "strategy_engine"
    assert composition_on.strategy_engine.engine is not None
    # S1 must not cut over Experience ports or mutate Adaptive / Twin wiring.
    assert composition_on.adaptive is not None
    assert composition_on.twin is not None
