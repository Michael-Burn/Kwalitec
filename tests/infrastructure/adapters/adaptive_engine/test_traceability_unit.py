"""Unit tests — Adaptive Observational Traceability (MS-003 A5)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AUTHORITY_ADAPTIVE_ENGINE,
    AUTHORITY_SHADOW_ONLY,
    LINEAGE_STAGES,
    AdaptiveEngineExecutor,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    AdaptiveShadowOrchestrator,
    ConfidencePlaceholder,
    DecisionTrace,
    EvidenceRef,
    ExplanationBundle,
    FeatureFlagSnapshot,
    RecommendationPlaceholder,
    RuleRef,
    TraceabilityService,
    build_decision_lineage,
    build_traceability_service,
    new_correlation_id,
    resolve_correlation_id,
    runtime_a_snapshot_id,
)
from app.infrastructure.adapters.adaptive_engine.gate import (
    ExplainabilityGate,
    ExplainabilityGateResult,
)
from app.infrastructure.adapters.adaptive_engine.provenance import (
    available_provenance,
)
from app.infrastructure.adapters.adaptive_engine.quality_rules import QualityViolation
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_TRACE_CREATED,
    ADAPTIVE_TRACE_EVENT_TYPES,
    ADAPTIVE_TRACE_FAILED,
    ADAPTIVE_TRACE_RECONSTRUCTED,
    EVENT_TYPES,
)


def _complete_output(*, decision_id: str = "a5-unit-1") -> AdaptiveOutputBundle:
    return AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(
            topic_code="T1",
            title="Topic One",
            decision_kind="NEXT_FOCUS",
            label="Topic One",
        ),
        confidence=ConfidencePlaceholder(score=0.7, band="medium"),
        explanation=ExplanationBundle(
            evidence_refs=(
                EvidenceRef(kind="study_attempt", id="attempt-1"),
            ),
            rule_refs=(
                RuleRef(
                    rule_or_model_id="adaptive.shadow.mission_aligned",
                    version="1.0.0-a2",
                ),
            ),
            confidence=ConfidencePlaceholder(score=0.7, band="medium"),
            input_summary="student_id=1",
            recommendation_rationale="Mission-aligned next focus.",
            why_summary="Continue today's mission topic.",
            inputs_used=("mission", "curriculum"),
            inputs_unavailable=(),
            mission_aligned=True,
        ),
        decision_id=decision_id,
        authority=AUTHORITY_ADAPTIVE_ENGINE,
    )


def _inputs(
    student_id: str = "42", *, as_of: str = "2026-07-25"
) -> AdaptiveInputBundle:
    return AdaptiveInputBundle(
        student_id=student_id,
        as_of=as_of,
        evidence={"attempt_count": 1, "attempts": [{"id": "attempt-1"}]},
        mission={"topic_code": "T1", "title": "Topic One"},
        curriculum={"next_incomplete_leaf": "T1"},
        field_provenance={
            "mission": available_provenance(
                source_service="mission",
                source_entity="Mission",
                collected_at=as_of,
            ).to_canonical_dict(),
            "curriculum": available_provenance(
                source_service="curriculum",
                source_entity="Curriculum",
                collected_at=as_of,
            ).to_canonical_dict(),
            "evidence": available_provenance(
                source_service="evidence",
                source_entity="StudyAttempt",
                collected_at=as_of,
            ).to_canonical_dict(),
        },
    )


def test_trace_event_types_registered():
    for event_type in ADAPTIVE_TRACE_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_build_traceability_service_respects_enabled_flag():
    assert build_traceability_service(enabled=False) is None
    svc = build_traceability_service(enabled=True)
    assert isinstance(svc, TraceabilityService)
    assert svc.is_enabled() is True


def test_decision_id_unique_across_distinct_inputs():
    svc = TraceabilityService(events=EventRegistry())
    out_a = _complete_output(decision_id="dec-a")
    out_b = _complete_output(decision_id="dec-b")
    t1 = svc.record_decision(
        student_id="1",
        inputs=_inputs("1", as_of="2026-07-25"),
        output=out_a,
        correlation_id="corr-1",
        executed_at="2026-07-25T10:00:00+00:00",
    )
    t2 = svc.record_decision(
        student_id="2",
        inputs=_inputs("2", as_of="2026-07-26"),
        output=out_b,
        correlation_id="corr-2",
        executed_at="2026-07-25T10:00:01+00:00",
    )
    assert t1 is not None and t2 is not None
    assert t1.decision_id != t2.decision_id
    assert t1.decision_id == "dec-a"
    assert t2.decision_id == "dec-b"


def test_minted_decision_id_when_output_missing():
    svc = TraceabilityService(events=EventRegistry())
    t1 = svc.record_decision(
        student_id="1",
        output=None,
        correlation_id="corr-m1",
        error_code="UNAVAILABLE",
        message="boom",
        executed_at="2026-07-25T10:00:00+00:00",
    )
    t2 = svc.record_decision(
        student_id="1",
        output=None,
        correlation_id="corr-m2",
        error_code="UNAVAILABLE",
        message="boom2",
        executed_at="2026-07-25T10:00:01+00:00",
    )
    assert t1 is not None and t2 is not None
    assert t1.decision_id.startswith("a5-")
    assert t2.decision_id.startswith("a5-")
    assert t1.decision_id != t2.decision_id


def test_correlation_id_consistent_across_lifecycle():
    events = EventRegistry()
    corr = new_correlation_id()
    with CorrelationContext.bind(correlation_id=corr):
        assert resolve_correlation_id(None) == corr
        svc = TraceabilityService(events=events)
        trace = svc.record_decision(
            student_id="9",
            inputs=_inputs("9"),
            output=_complete_output(decision_id="corr-dec"),
            correlation_id=None,
            executed_at="2026-07-25T10:00:00+00:00",
        )
        assert trace is not None
        assert trace.correlation_id == corr
        published = events.published()
        created = [e for e in published if e.event_type == ADAPTIVE_TRACE_CREATED]
        assert len(created) == 1
        assert created[0].correlation_id == corr
        assert created[0].payload["correlation_id"] == corr


def test_complete_decision_trace_fields():
    svc = TraceabilityService(
        events=EventRegistry(),
        feature_flags=FeatureFlagSnapshot(
            engine_enabled=True,
            shadow_enabled=True,
            authority_enabled=False,
        ),
        engine_version="1.0.0-a2",
    )
    inputs = _inputs("7")
    output = _complete_output(decision_id="full-1")
    gate = ExplainabilityGateResult(
        passed=True,
        eligible_for_future_authority=True,
        observational_only=False,
        violations=(),
        decision_id="full-1",
    )
    trace = svc.record_decision(
        student_id="7",
        inputs=inputs,
        output=output,
        gate_result=gate,
        authority_status=AUTHORITY_SHADOW_ONLY,
        correlation_id="corr-full",
        executed_at="2026-07-25T12:00:00+00:00",
    )
    assert isinstance(trace, DecisionTrace)
    assert trace.decision_id == "full-1"
    assert trace.correlation_id == "corr-full"
    assert trace.engine_version == "1.0.0-a2"
    assert trace.feature_flag_state.engine_enabled is True
    assert trace.feature_flag_state.shadow_enabled is True
    assert trace.runtime_a_snapshot_id == runtime_a_snapshot_id(inputs)
    assert trace.input_bundle_ref.startswith("input-")
    assert trace.output_bundle_ref.startswith("output-")
    assert trace.explainability_gate_result["passed"] is True
    assert trace.authority_status == AUTHORITY_SHADOW_ONLY
    assert trace.executed_at == "2026-07-25T12:00:00+00:00"
    assert list(trace.lineage.stages) == list(LINEAGE_STAGES)


def test_lineage_reconstruction_deterministic():
    svc = TraceabilityService(events=EventRegistry())
    output = _complete_output(decision_id="lin-1")
    gate = ExplainabilityGateResult(
        passed=False,
        eligible_for_future_authority=False,
        observational_only=True,
        violations=(
            QualityViolation(rule_id="r1", message="incomplete"),
        ),
        decision_id="lin-1",
        error_code="EXPLAINABILITY_INCOMPLETE",
    )
    svc.record_decision(
        student_id="3",
        inputs=_inputs("3"),
        output=output,
        gate_result=gate,
        correlation_id="corr-lin",
        executed_at="2026-07-25T12:00:00+00:00",
    )
    first = svc.reconstruct_lineage("lin-1")
    second = svc.reconstruct_lineage("lin-1")
    assert first is not None and second is not None
    assert first.serialize() == second.serialize()
    assert first.stages == LINEAGE_STAGES
    assert first.explainability_passed is False
    types = [e.event_type for e in svc._events.published()]
    assert ADAPTIVE_TRACE_RECONSTRUCTED in types


def test_build_decision_lineage_stages_order():
    lineage = build_decision_lineage(
        inputs=_inputs("1"),
        output=_complete_output(),
        gate_result=None,
        routing_decision="shadow_only",
        delivery_status="shadow_only",
    )
    assert lineage.stages == LINEAGE_STAGES
    assert "study_attempt:attempt-1" in lineage.evidence_ref_ids


def test_trace_failed_telemetry_on_error_code():
    events = EventRegistry()
    svc = TraceabilityService(events=events)
    svc.record_decision(
        student_id="1",
        correlation_id="corr-fail",
        error_code="RuntimeError",
        message="assemble failed",
        executed_at="2026-07-25T12:00:00+00:00",
    )
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_TRACE_FAILED in types
    assert ADAPTIVE_TRACE_CREATED not in types


def test_disabled_service_records_nothing():
    svc = TraceabilityService(events=EventRegistry(), enabled=False)
    assert svc.record_decision(student_id="1", output=_complete_output()) is None
    assert svc.all_traces() == ()


def test_composition_wires_traceability_when_engine_on():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_ADAPTIVE_ENGINE": "1"}
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_traceability is not None
    assert composition.adaptive_traceability.is_enabled() is True


def test_composition_no_traceability_when_flags_off():
    flags = resolve_v2_feature_flags(environ={})
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_traceability is None


def test_shadow_orchestrator_records_trace():
    events = EventRegistry()
    executor = AdaptiveEngineExecutor()
    inputs = _inputs("11")
    svc = TraceabilityService(
        events=events,
        feature_flags=FeatureFlagSnapshot(
            engine_enabled=True, shadow_enabled=True
        ),
    )
    gate = ExplainabilityGate(events=events, enabled=True)
    orchestrator = AdaptiveShadowOrchestrator(
        assembler=None,
        executor=executor,
        events=events,
        enabled=True,
        explainability_gate=gate,
        traceability=svc,
    )
    result = orchestrator.execute_shadow("11", inputs=inputs)
    assert result.ok is True
    assert orchestrator.last_trace is not None
    assert orchestrator.last_trace.decision_id == result.value.decision_id
    assert orchestrator.last_trace.authority_status == AUTHORITY_SHADOW_ONLY
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_TRACE_CREATED in types
