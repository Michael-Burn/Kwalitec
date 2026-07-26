"""Unit tests — Adaptive Shadow Soak (MS-003 A6)."""

from __future__ import annotations

from types import SimpleNamespace
from unittest import mock

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AUTHORITY_ADAPTIVE_ENGINE,
    DRIFT_DETERMINISM_FAILURE,
    DRIFT_MISSING_EXPLANATION,
    DRIFT_TRACE_FAILURE,
    DRIFT_UNEXPECTED_RECOMMENDATION_CHANGE,
    DRIFT_UNEXPLAINED_DIVERGENCE,
    AdaptiveEngineExecutor,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    AdaptiveShadowOrchestrator,
    ConfidencePlaceholder,
    DeterminismMonitor,
    DriftDetectionMonitor,
    EvidenceRef,
    ExplanationBundle,
    RecommendationComparisonMonitor,
    RecommendationPlaceholder,
    RuleRef,
    ShadowSoakOrchestrator,
    SoakHealthMetrics,
    build_shadow_soak_orchestrator,
    build_soak_ops_dashboard,
    verify_adaptive_rollback,
)
from app.infrastructure.adapters.adaptive_engine.contracts import AdaptiveDecisionResult
from app.infrastructure.adapters.adaptive_engine.provenance import (
    available_provenance,
    unavailable_provenance,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_ENGINE_SHADOW_COMPARE,
    ADAPTIVE_SOAK_COMPARE,
    ADAPTIVE_SOAK_COMPLETED,
    ADAPTIVE_SOAK_EVENT_TYPES,
    ADAPTIVE_SOAK_HEALTH,
    ADAPTIVE_SOAK_LATENCY,
    ADAPTIVE_SOAK_REQUESTED,
    EVENT_TYPES,
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


def _complete_output(
    *, topic_code: str = "T1", title: str = "Topic One"
) -> AdaptiveOutputBundle:
    return AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(
            topic_code=topic_code,
            title=title,
            decision_kind="NEXT_FOCUS",
            label=title,
        ),
        confidence=ConfidencePlaceholder(score=0.7, band="medium"),
        explanation=ExplanationBundle(
            evidence_refs=(EvidenceRef(kind="study_attempt", id="a1"),),
            rule_refs=(
                RuleRef(
                    rule_or_model_id="adaptive.shadow.next_incomplete_leaf",
                    version="1.0.0-a2",
                ),
            ),
            confidence=ConfidencePlaceholder(score=0.7, band="medium"),
            recommendation_rationale="Next incomplete leaf.",
            why_summary="Continue the syllabus.",
            inputs_used=("curriculum", "topic_progress"),
            inputs_unavailable=(),
        ),
        decision_id="a6-test-1",
        authority=AUTHORITY_ADAPTIVE_ENGINE,
    )


def test_soak_event_types_registered():
    for event_type in ADAPTIVE_SOAK_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_comparison_monitor_agrees_on_topic_code():
    monitor = RecommendationComparisonMonitor()
    comparison = monitor.compare(
        {"title": "Other", "topic_code": "T1", "category": "Weak"},
        _complete_output(topic_code="T1", title="Topic One"),
    )
    assert comparison.agreed is True
    assert comparison.divergence_reason == ""


def test_comparison_monitor_diverges_on_topic_code():
    monitor = RecommendationComparisonMonitor()
    comparison = monitor.compare(
        {"title": "Baseline", "topic_code": "BASE", "category": "Weak"},
        _complete_output(topic_code="T1", title="Topic One"),
    )
    assert comparison.agreed is False
    assert comparison.divergence_reason == "topic_code_mismatch"


def test_determinism_monitor_identical_replay():
    executor = AdaptiveEngineExecutor()
    inputs = AdaptiveInputBundle(
        student_id="7",
        as_of="2026-07-25",
        curriculum={
            "leaves": [
                {"topic_id": "1", "topic_name": "Done", "order": 1},
                {"topic_id": "2", "topic_name": "Next Leaf", "order": 2},
            ],
            "leaf_count": 2,
        },
        topic_progress=(
            {
                "topic_id": "1",
                "topic_name": "Done",
                "completed": True,
                "mastery_score": 0.9,
            },
        ),
        field_provenance=_full_available_provenance(),
    )
    result = DeterminismMonitor().verify_replay(executor, inputs)
    assert result.success is True
    assert result.first_decision_id == result.second_decision_id


def test_drift_detection_missing_explanation_and_determinism():
    incomplete = AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(topic_code="T1", title="T"),
        confidence=ConfidencePlaceholder(band=""),
        explanation=ExplanationBundle(),
        decision_id="x",
    )
    signals = DriftDetectionMonitor().detect(
        student_id="42",
        adaptive=incomplete,
        determinism=SimpleNamespace(success=False, detail="output_serialize_mismatch"),
        trace_ok=False,
        comparison=RecommendationComparisonMonitor().compare(
            {"topic_code": "OTHER", "title": "Other"},
            incomplete,
        ),
    )
    kinds = {s.kind for s in signals}
    assert DRIFT_MISSING_EXPLANATION in kinds
    assert DRIFT_DETERMINISM_FAILURE in kinds
    assert DRIFT_TRACE_FAILURE in kinds
    assert DRIFT_UNEXPLAINED_DIVERGENCE in kinds


def test_drift_unexpected_recommendation_change():
    signals = DriftDetectionMonitor().detect(
        student_id="42",
        adaptive=_complete_output(topic_code="T2"),
        prior_adaptive_topic_code="T1",
    )
    assert any(s.kind == DRIFT_UNEXPECTED_RECOMMENDATION_CHANGE for s in signals)


def test_health_metrics_rates():
    health = SoakHealthMetrics()
    health.record_execution(
        ok=True,
        agreed=True,
        explainability_passed=True,
        trace_created=True,
        determinism_success=True,
        fallback=False,
        drift_signals=0,
        latency_ms=12.5,
    )
    health.record_execution(
        ok=True,
        agreed=False,
        explainability_passed=True,
        trace_created=True,
        determinism_success=True,
        fallback=False,
        drift_signals=1,
        latency_ms=7.5,
    )
    snap = health.snapshot()
    assert snap.executions == 2
    assert snap.recommendation_agreement_rate == 0.5
    assert snap.recommendation_divergence_rate == 0.5
    assert snap.explainability_pass_rate == 1.0
    assert snap.trace_creation_rate == 1.0
    assert snap.deterministic_replay_success_rate == 1.0
    assert snap.mean_execution_latency_ms == 10.0


def test_shadow_soak_orchestrator_compare_measure_discard():
    events = EventRegistry()
    output = _complete_output(topic_code="T1", title="Topic One")
    shadow = mock.Mock(spec=AdaptiveShadowOrchestrator)
    shadow.execute_shadow.return_value = AdaptiveDecisionResult(ok=True, value=output)
    shadow.last_gate_result = SimpleNamespace(passed=True)
    shadow.last_trace = SimpleNamespace(decision_id="a6-test-1")
    shadow._assembler = None
    shadow._executor = AdaptiveEngineExecutor()
    shadow._traceability = object()

    baseline_svc = SimpleNamespace(
        generate_recommendations=mock.Mock(
            return_value=[
                {"title": "Topic One", "topic_code": "T1", "category": "Weak"}
            ]
        )
    )
    soak = ShadowSoakOrchestrator(
        shadow=shadow,
        events=events,
        enabled=True,
        recommendation_service=baseline_svc,
        emit_health_on_complete=True,
    )
    observation = soak.execute_soak(
        "42",
        as_of="2026-07-25",
        inputs=AdaptiveInputBundle(
            student_id="42",
            as_of="2026-07-25",
            curriculum={"leaves": [], "leaf_count": 0},
            field_provenance=_full_available_provenance(),
        ),
        run_determinism_replay=True,
    )
    assert observation.ok is True
    assert observation.comparison is not None
    assert observation.comparison.agreed is True
    assert observation.explainability_passed is True
    assert observation.trace_created is True
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_SOAK_REQUESTED in types
    assert ADAPTIVE_SOAK_COMPLETED in types
    assert ADAPTIVE_SOAK_COMPARE in types
    assert ADAPTIVE_ENGINE_SHADOW_COMPARE in types
    assert ADAPTIVE_SOAK_LATENCY in types
    assert ADAPTIVE_SOAK_HEALTH in types
    # Soak observation must not be treated as Experience authority.
    assert observation.to_canonical_dict()["ok"] is True
    dashboard = build_soak_ops_dashboard(soak)
    assert dashboard["adaptive_shadow_soak"]["influences_student"] is False


def test_build_shadow_soak_requires_shadow():
    assert build_shadow_soak_orchestrator(enabled=True, shadow=None) is None
    assert build_shadow_soak_orchestrator(enabled=False, shadow=mock.Mock()) is None


def test_composition_wires_soak_when_shadow_on():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_shadow is not None
    assert composition.adaptive_soak is not None
    assert composition.adaptive_port_router is None


def test_composition_no_soak_when_shadow_off():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_ADAPTIVE_ENGINE": "1"}
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_shadow is None
    assert composition.adaptive_soak is None


def test_dual_run_status_exposes_soak_hook():
    status = build_dual_run_status(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_ADAPTIVE_SHADOW": "1"}
        )
    )
    assert status.adaptive_shadow_soak is True
    assert status.adaptive_authority is False


def test_rollback_verification_immediate():
    result = verify_adaptive_rollback()
    assert result.ok is True
    assert result.engine_disabled_restores_recommendation is True
    assert result.authority_disabled_restores_recommendation is True
    assert result.cutover_inactive_when_engine_off is True
    assert result.cutover_inactive_when_authority_off is True
