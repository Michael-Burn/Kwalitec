"""Unit tests — Explainability Gate (MS-003 A3)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AdaptiveEngineExecutor,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    AdaptiveShadowOrchestrator,
    ConfidencePlaceholder,
    EvidenceRef,
    ExplainabilityGate,
    ExplanationBundle,
    RecommendationPlaceholder,
    RuleRef,
    build_explainability_gate,
    empty_adaptive_output,
    evaluate_quality_rules,
    validate_explanation_bundle,
)
from app.infrastructure.adapters.adaptive_engine.provenance import (
    available_provenance,
    unavailable_provenance,
)
from app.infrastructure.adapters.adaptive_engine.quality_rules import (
    RULE_CONFIDENCE_PRESENT,
    RULE_EVIDENCE_REFS_PRESENT,
    RULE_INPUTS_USED_POPULATED,
    RULE_RECOMMENDATION_PRESENT,
    RULE_RECOMMENDATION_RATIONALE_PRESENT,
    RULE_RULE_REFS_PRESENT,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVENT_TYPES,
    EXPLAINABILITY_GATE_EVENT_TYPES,
    EXPLAINABILITY_GATE_FAILED,
    EXPLAINABILITY_GATE_LATENCY,
    EXPLAINABILITY_GATE_PASSED,
    EXPLAINABILITY_GATE_REQUESTED,
)


def _prov_map(available: tuple[str, ...], unavailable: tuple[str, ...] = ()) -> dict:
    collected_at = "2026-07-25"
    out = {
        name: available_provenance(
            source_service="stub",
            source_entity=name,
            collected_at=collected_at,
        ).to_canonical_dict()
        for name in available
    }
    for name in unavailable:
        out[name] = unavailable_provenance(
            source_service="stub",
            source_entity=name,
            collected_at=collected_at,
            reason="UNAVAILABLE",
        ).to_canonical_dict()
    return out


def _full_available_provenance() -> dict:
    return _prov_map(
        (
            "evidence",
            "topic_progress",
            "study_attempts",
            "mission",
            "readiness",
            "curriculum",
            "student_goals",
            "lifecycle_stage",
        )
    )


def _complete_output() -> AdaptiveOutputBundle:
    """Build a complete AdaptiveOutputBundle via the deterministic executor."""
    executor = AdaptiveEngineExecutor()
    inputs = AdaptiveInputBundle(
        student_id="7",
        as_of="2026-07-25",
        evidence={
            "attempt_count": 2,
            "authorised_count": 1,
            "attempts": [
                {
                    "attempt_id": "11",
                    "study_date": "2026-07-24",
                    "authorised_structured_results": True,
                }
            ],
        },
        topic_progress=(
            {
                "topic_id": "1",
                "topic_name": "Done",
                "completed": True,
                "mastery_score": 0.9,
            },
        ),
        curriculum={
            "leaves": [
                {"topic_id": "1", "topic_name": "Done", "order": 1},
                {"topic_id": "2", "topic_name": "Next Leaf", "order": 2},
            ],
            "leaf_count": 2,
        },
        lifecycle_stage="Learning",
        field_provenance=_full_available_provenance(),
    )
    return executor.evaluate(inputs)


def test_complete_bundle_passes_gate():
    gate = ExplainabilityGate(events=EventRegistry(), enabled=True)
    output = _complete_output()
    before = output.serialize()
    result = gate.validate(output, student_id="7")
    assert result.passed is True
    assert result.eligible_for_future_authority is True
    assert result.observational_only is True  # A3 does not cut over Experience
    assert result.violations == ()
    assert output.serialize() == before


def test_incomplete_bundle_fails_and_stays_observational():
    gate = ExplainabilityGate(events=EventRegistry(), enabled=True)
    output = empty_adaptive_output(input_summary="empty")
    before = output.serialize()
    result = gate.validate(output, student_id="7")
    assert result.passed is False
    assert result.eligible_for_future_authority is False
    assert result.observational_only is True
    assert result.error_code == "EXPLAINABILITY_INCOMPLETE"
    assert len(result.violations) >= 1
    assert output.serialize() == before


def test_gate_emits_pass_telemetry():
    events = EventRegistry()
    gate = ExplainabilityGate(events=events, enabled=True)
    result = gate.validate(_complete_output(), student_id="7")
    assert result.passed is True
    types = [e.event_type for e in events.published()]
    assert EXPLAINABILITY_GATE_REQUESTED in types
    assert EXPLAINABILITY_GATE_PASSED in types
    assert EXPLAINABILITY_GATE_LATENCY in types
    assert EXPLAINABILITY_GATE_FAILED not in types


def test_gate_emits_fail_telemetry():
    events = EventRegistry()
    gate = ExplainabilityGate(events=events, enabled=True)
    result = gate.validate(empty_adaptive_output(), student_id="7")
    assert result.passed is False
    types = [e.event_type for e in events.published()]
    assert EXPLAINABILITY_GATE_REQUESTED in types
    assert EXPLAINABILITY_GATE_FAILED in types
    assert EXPLAINABILITY_GATE_LATENCY in types
    failed = next(
        e for e in events.published() if e.event_type == EXPLAINABILITY_GATE_FAILED
    )
    assert failed.payload["eligible_for_future_authority"] is False
    assert failed.payload["observational_only"] is True


def test_quality_rules_individual_failures():
    base = _complete_output()

    no_rec = AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(),
        confidence=base.confidence,
        explanation=base.explanation,
        decision_id=base.decision_id,
    )
    assert any(
        v.rule_id == RULE_RECOMMENDATION_PRESENT
        for v in evaluate_quality_rules(no_rec)
    )

    no_conf = AdaptiveOutputBundle(
        recommendation=base.recommendation,
        confidence=ConfidencePlaceholder(),
        explanation=ExplanationBundle(
            evidence_refs=base.explanation.evidence_refs,
            rule_refs=base.explanation.rule_refs,
            confidence=ConfidencePlaceholder(),
            recommendation_rationale=base.explanation.recommendation_rationale,
            inputs_used=base.explanation.inputs_used,
            inputs_unavailable=base.explanation.inputs_unavailable,
        ),
        decision_id=base.decision_id,
    )
    assert any(
        v.rule_id == RULE_CONFIDENCE_PRESENT for v in evaluate_quality_rules(no_conf)
    )

    no_evidence = AdaptiveOutputBundle(
        recommendation=base.recommendation,
        confidence=base.confidence,
        explanation=ExplanationBundle(
            evidence_refs=(),
            rule_refs=base.explanation.rule_refs,
            confidence=base.confidence,
            recommendation_rationale=base.explanation.recommendation_rationale,
            inputs_used=base.explanation.inputs_used,
            inputs_unavailable=base.explanation.inputs_unavailable,
        ),
        decision_id=base.decision_id,
    )
    assert any(
        v.rule_id == RULE_EVIDENCE_REFS_PRESENT
        for v in evaluate_quality_rules(no_evidence)
    )

    no_used = AdaptiveOutputBundle(
        recommendation=base.recommendation,
        confidence=base.confidence,
        explanation=ExplanationBundle(
            evidence_refs=base.explanation.evidence_refs,
            rule_refs=base.explanation.rule_refs,
            confidence=base.confidence,
            recommendation_rationale=base.explanation.recommendation_rationale,
            inputs_used=(),
            inputs_unavailable=base.explanation.inputs_unavailable,
        ),
        decision_id=base.decision_id,
    )
    assert any(
        v.rule_id == RULE_INPUTS_USED_POPULATED
        for v in evaluate_quality_rules(no_used)
    )

    no_rationale = AdaptiveOutputBundle(
        recommendation=base.recommendation,
        confidence=base.confidence,
        explanation=ExplanationBundle(
            evidence_refs=base.explanation.evidence_refs,
            rule_refs=base.explanation.rule_refs,
            confidence=base.confidence,
            recommendation_rationale="",
            inputs_used=base.explanation.inputs_used,
            inputs_unavailable=base.explanation.inputs_unavailable,
        ),
        decision_id=base.decision_id,
    )
    assert any(
        v.rule_id == RULE_RECOMMENDATION_RATIONALE_PRESENT
        for v in evaluate_quality_rules(no_rationale)
    )

    no_rules = AdaptiveOutputBundle(
        recommendation=base.recommendation,
        confidence=base.confidence,
        explanation=ExplanationBundle(
            evidence_refs=base.explanation.evidence_refs,
            rule_refs=(),
            confidence=base.confidence,
            recommendation_rationale=base.explanation.recommendation_rationale,
            inputs_used=base.explanation.inputs_used,
            inputs_unavailable=base.explanation.inputs_unavailable,
        ),
        decision_id=base.decision_id,
    )
    assert any(
        v.rule_id == RULE_RULE_REFS_PRESENT for v in evaluate_quality_rules(no_rules)
    )


def test_validate_explanation_bundle_standalone():
    complete = _complete_output().explanation
    assert validate_explanation_bundle(complete) == ()

    incomplete = ExplanationBundle(
        evidence_refs=(EvidenceRef(kind="attempt", id="1"),),
        rule_refs=(RuleRef(rule_or_model_id="adaptive.shadow.next_incomplete_leaf"),),
        recommendation_rationale="ok",
        inputs_used=(),
        inputs_unavailable=(),
    )
    violations = validate_explanation_bundle(incomplete)
    assert any(v.rule_id == RULE_INPUTS_USED_POPULATED for v in violations)


def test_gate_does_not_mutate_recommendation():
    gate = ExplainabilityGate(events=EventRegistry(), enabled=True)
    output = _complete_output()
    original_topic = output.recommendation.topic_code
    original_kind = output.recommendation.decision_kind
    before = output.serialize()
    gate.validate(output, student_id="7")
    assert output.serialize() == before
    assert output.recommendation.topic_code == original_topic
    assert output.recommendation.decision_kind == original_kind


def test_shadow_invokes_gate_when_wired():
    events = EventRegistry()
    gate = ExplainabilityGate(events=events, enabled=True)
    output_inputs = AdaptiveInputBundle(
        student_id="42",
        as_of="2026-07-25",
        evidence={
            "attempt_count": 1,
            "attempts": [
                {
                    "attempt_id": "99",
                    "study_date": "2026-07-25",
                    "authorised_structured_results": True,
                }
            ],
        },
        curriculum={
            "leaves": [{"topic_id": "1", "topic_name": "A", "order": 1}],
            "leaf_count": 1,
        },
        field_provenance=_full_available_provenance(),
    )

    class _Assembler:
        def assemble(self, student_id, *, as_of=None):
            return output_inputs

    orch = AdaptiveShadowOrchestrator(
        assembler=_Assembler(),
        executor=AdaptiveEngineExecutor(),
        events=events,
        enabled=True,
        explainability_gate=gate,
    )
    result = orch.execute_shadow("42", as_of="2026-07-25")
    assert result.ok is True
    assert orch.last_gate_result is not None
    assert orch.last_gate_result.passed is True
    types = [e.event_type for e in events.published()]
    assert EXPLAINABILITY_GATE_PASSED in types


def test_di_wires_gate_only_when_both_flags_on():
    both = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _ = build_production_experience(flags=both)
    assert composition.explainability_gate is not None
    assert isinstance(composition.explainability_gate, ExplainabilityGate)
    assert composition.adaptive_shadow is not None
    assert (
        composition.adaptive_shadow.explainability_gate
        is composition.explainability_gate
    )

    shadow_only = resolve_v2_feature_flags(
        environ={"KWALITEC_ADAPTIVE_SHADOW": "1"}
    )
    composition_shadow, _ = build_production_experience(flags=shadow_only)
    assert composition_shadow.explainability_gate is None
    assert composition_shadow.adaptive_shadow is not None
    assert composition_shadow.adaptive_shadow.explainability_gate is None

    engine_only = resolve_v2_feature_flags(
        environ={"KWALITEC_ADAPTIVE_ENGINE": "1"}
    )
    composition_engine, _ = build_production_experience(flags=engine_only)
    assert composition_engine.explainability_gate is None
    assert composition_engine.adaptive_shadow is None

    off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=off)
    assert composition_off.explainability_gate is None
    assert composition_off.adaptive_shadow is None


def test_build_explainability_gate_helper():
    assert build_explainability_gate(enabled=False) is None
    gate = build_explainability_gate(enabled=True)
    assert isinstance(gate, ExplainabilityGate)


def test_explainability_gate_events_registered():
    for event_type in EXPLAINABILITY_GATE_EVENT_TYPES:
        assert event_type in EVENT_TYPES
