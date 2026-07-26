"""Unit / serialization / determinism tests — Adaptive Decision Contracts (A0)."""

from __future__ import annotations

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AdaptiveEngineAdapter,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    ConfidencePlaceholder,
    EvidenceRef,
    ExplanationBundle,
    RecommendationPlaceholder,
    RuleRef,
    empty_adaptive_output,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


def test_input_bundle_requires_student_id():
    with pytest.raises(ValueError, match="student_id"):
        AdaptiveInputBundle(student_id="  ")


def test_input_bundle_is_immutable():
    bundle = AdaptiveInputBundle(
        student_id="7",
        evidence={"accepted": True},
        topic_progress=[{"topic_code": "A"}],
        study_attempts=[{"id": "1"}],
        authority_tags=["runtime_a"],
    )
    with pytest.raises(Exception):
        bundle.student_id = "8"  # type: ignore[misc]
    with pytest.raises(TypeError):
        bundle.evidence["accepted"] = False  # type: ignore[index]
    with pytest.raises(AttributeError):
        bundle.topic_progress.append({"topic_code": "B"})  # type: ignore[attr-defined]


def test_output_bundle_is_immutable():
    output = empty_adaptive_output()
    with pytest.raises(Exception):
        output.decision_id = "x"  # type: ignore[misc]
    with pytest.raises(Exception):
        output.explanation.input_summary = "mutated"  # type: ignore[misc]


def test_identical_inputs_serialize_identically():
    left = AdaptiveInputBundle(
        student_id="1",
        as_of="2026-07-25",
        evidence={"count": 2, "kinds": ["attempt"]},
        topic_progress=[{"topic_code": "T2"}, {"topic_code": "T1"}],
        study_attempts=[{"id": "3", "score": 0.5}],
        readiness={"coverage": 0.4},
        mission={"mission_id": "9", "status": "In Progress"},
        curriculum={"syllabus": "CM1", "leaves": ["T1", "T2"]},
        student_goals={"exam_date": "2026-09-01", "minutes": 45},
        authority_tags=["runtime_a", "curriculum"],
        lifecycle_stage="Learning",
    )
    right = AdaptiveInputBundle(
        student_id="1",
        as_of="2026-07-25",
        evidence={"kinds": ["attempt"], "count": 2},
        topic_progress=[{"topic_code": "T2"}, {"topic_code": "T1"}],
        study_attempts=[{"score": 0.5, "id": "3"}],
        readiness={"coverage": 0.4},
        mission={"status": "In Progress", "mission_id": "9"},
        curriculum={"leaves": ["T1", "T2"], "syllabus": "CM1"},
        student_goals={"minutes": 45, "exam_date": "2026-09-01"},
        authority_tags=["runtime_a", "curriculum"],
        lifecycle_stage="Learning",
    )
    assert left.serialize() == right.serialize()
    assert serialize_canonical(left.to_canonical_dict()) == left.serialize()


def test_explanation_and_output_serialize_deterministically():
    explanation = ExplanationBundle(
        evidence_refs=(
            EvidenceRef(kind="attempt", id="1", note="ok"),
            EvidenceRef(kind="mission", id="2"),
        ),
        rule_refs=(
            RuleRef(
                rule_or_model_id="adaptive.weak_topic_priority",
                version="1",
            ),
        ),
        confidence=ConfidencePlaceholder(score=0.2, band="low", rationale="sparse"),
        input_summary="sparse evidence",
        recommendation_rationale="",
        why_summary="",
        why_reason_codes=("sparse_evidence",),
        topic_refs=(),
        alternatives_rationale="",
        limitations_codes=("sparse_evidence",),
        limitations_summary="New learner",
        mission_aligned=None,
        mission_note="",
    )
    output = AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(decision_kind="COMPOSITE"),
        confidence=ConfidencePlaceholder(band="low"),
        explanation=explanation,
        decision_id="",
    )
    assert output.serialize() == AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(decision_kind="COMPOSITE"),
        confidence=ConfidencePlaceholder(band="low"),
        explanation=explanation,
        decision_id="",
    ).serialize()


def test_evaluate_is_deterministic_for_identical_inputs():
    adapter = AdaptiveEngineAdapter()
    inputs = AdaptiveInputBundle(student_id="99", evidence={"n": 0})
    first = adapter.evaluate(inputs)
    second = adapter.evaluate(inputs)
    assert first.serialize() == second.serialize()


def test_decide_rejects_empty_student_id():
    result = AdaptiveEngineAdapter().decide(" ")
    assert result.ok is False
    assert result.error_code == "INVALID_STATE"


def test_flag_default_off_and_di_wiring():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_ADAPTIVE_ENGINE is False
    assert flags_off.ENABLE_ADAPTIVE_ENGINE_SHADOW is False
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.adaptive_engine is None
    assert composition_off.adaptive_input_assembler is None

    flags_on = resolve_v2_feature_flags(environ={"KWALITEC_ADAPTIVE_ENGINE": "1"})
    assert flags_on.ENABLE_ADAPTIVE_ENGINE is True
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.adaptive_engine, AdaptiveEngineAdapter)
    assert composition_on.adaptive_input_assembler is not None
    # A0/A1 must not cut over Experience AdaptiveDecisionPort to the Adaptive Engine.
    assert composition_on.adaptive._recommendation_read is None
    assert composition_on.adaptive_engine is not composition_on.adaptive
    assert composition_on.adaptive_engine.adapter_id == "adaptive_engine"


def test_umbrella_flag_enables_adaptive_engine():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_ADAPTIVE_INTELLIGENCE": "true"}
    )
    assert flags.ENABLE_ADAPTIVE_ENGINE is True
