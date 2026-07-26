"""Unit tests — Strategy Shadow Validation (MS-005 S3)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.strategy_engine import (
    DRIFT_DETERMINISM_FAILURE,
    DRIFT_INTERVENTION_INSTABILITY,
    DRIFT_PLANNER_INCONSISTENCY,
    ExplainabilityConsistencyMonitor,
    InterventionStabilityMonitor,
    PlannerConsistencyMonitor,
    ProjectionConsistencyMonitor,
    StrategyDriftDetectionMonitor,
    StrategyShadowHealth,
    StrategyShadowValidator,
    build_strategy_engine_adapter,
    build_strategy_explainability_service,
    build_strategy_projector,
    build_strategy_shadow_ops_dashboard,
    build_strategy_shadow_validator,
    explanation_is_complete,
    verify_strategy_shadow_rollback,
)
from app.infrastructure.adapters.strategy_engine.shadow_monitors import (
    StabilityResult,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVENT_TYPES,
    STRATEGY_SHADOW_COMPLETED,
    STRATEGY_SHADOW_EVENT_TYPES,
    STRATEGY_SHADOW_HEALTH,
    STRATEGY_SHADOW_LATENCY,
    STRATEGY_SHADOW_REQUESTED,
    STRATEGY_SHADOW_ROLLBACK_VERIFIED,
    STRATEGY_SHADOW_STABILITY,
)

AS_OF = "2026-07-25T12:00:00"


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


def _twin():
    return {
        "twin_id": "twin-shadow",
        "snapshot_version": "sv-1",
        "profile": {
            "cognitive_load_indicators": {
                "label": "low",
                "availability": "available",
            },
            "confidence_trend": {
                "label": "cautious",
                "availability": "available",
            },
        },
    }


def _adaptive():
    return {
        "decision_id": "dec-shadow",
        "recommendation": {
            "topic_code": "T-ADAPTIVE",
            "title": "Adaptive",
            "decision_kind": "NEXT_FOCUS",
        },
        "alternatives": [{"topic_code": "T-ALT"}],
    }


def _build_validator(*, events: EventRegistry | None = None) -> StrategyShadowValidator:
    adapter = build_strategy_engine_adapter(enabled=True)
    explainability = build_strategy_explainability_service(enabled=True)
    projector = build_strategy_projector(enabled=True)
    validator = build_strategy_shadow_validator(
        enabled=True,
        adapter=adapter,
        explainability=explainability,
        projector=projector,
        events=events or EventRegistry(),
    )
    assert validator is not None
    return validator


def test_strategy_shadow_event_types_registered():
    for event_type in STRATEGY_SHADOW_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_build_validator_requires_flag_and_adapter():
    assert build_strategy_shadow_validator(enabled=False, adapter=object()) is None
    assert build_strategy_shadow_validator(enabled=True, adapter=None) is None


def test_disabled_validator_returns_unavailable():
    adapter = build_strategy_engine_adapter(enabled=True)
    validator = StrategyShadowValidator(adapter=adapter, enabled=False)
    observation = validator.validate_shadow(
        "7",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    assert observation.ok is False
    assert observation.error_code == "UNAVAILABLE"


def test_empty_student_id_rejected():
    validator = _build_validator()
    observation = validator.validate_shadow(" ")
    assert observation.ok is False
    assert observation.error_code == "INVALID_STATE"


def test_intervention_stability_monitor_identical_replay():
    adapter = build_strategy_engine_adapter(enabled=True)
    assert adapter is not None
    context = adapter.assemble_context(
        "7",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    intervention = adapter.evaluate(context)
    result = InterventionStabilityMonitor().verify_replay(
        adapter.engine,
        context,
        intervention=intervention,
    )
    assert result.success is True
    assert result.detail == "identical_intervention_replay"


def test_explainability_and_projection_consistency_monitors():
    adapter = build_strategy_engine_adapter(enabled=True)
    explainability = build_strategy_explainability_service(enabled=True)
    projector = build_strategy_projector(enabled=True)
    assert adapter is not None and explainability is not None and projector is not None
    context = adapter.assemble_context(
        "7",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    intervention = adapter.evaluate(context)
    explanation = explainability.explain(intervention)
    projection = projector.project(
        intervention, explanation=explanation, student_id="7", as_of=AS_OF
    )
    assert explanation_is_complete(explanation) is True
    assert (
        ExplainabilityConsistencyMonitor()
        .verify_replay(explainability, intervention, explanation=explanation)
        .success
        is True
    )
    assert (
        ProjectionConsistencyMonitor()
        .verify_replay(
            projector,
            intervention,
            explanation=explanation,
            student_id="7",
            as_of=AS_OF,
            projection=projection,
        )
        .success
        is True
    )


def test_planner_consistency_monitor_coherent():
    adapter = build_strategy_engine_adapter(enabled=True)
    assert adapter is not None
    context = adapter.assemble_context(
        "7",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    intervention = adapter.evaluate(context)
    result = PlannerConsistencyMonitor().verify(intervention, context)
    assert result.success is True
    assert result.detail == "planner_outputs_coherent"


def test_drift_monitor_emits_instability_signals():
    signals = StrategyDriftDetectionMonitor().detect(
        student_id="7",
        intervention_stability=StabilityResult(
            success=False, detail="intervention_serialize_mismatch"
        ),
        planner_consistency=StabilityResult(
            success=False, detail="sequencing_primary_kind_mismatch"
        ),
        determinism_success=False,
    )
    kinds = {s.kind for s in signals}
    assert DRIFT_INTERVENTION_INSTABILITY in kinds
    assert DRIFT_PLANNER_INCONSISTENCY in kinds
    assert DRIFT_DETERMINISM_FAILURE in kinds


def test_health_metrics_rates():
    health = StrategyShadowHealth()
    health.record_execution(
        ok=True,
        intervention_ok=True,
        projection_ok=True,
        explainability_ok=True,
        planner_consistency_ok=True,
        determinism_success=True,
        drift_signals=1,
        latency_ms=12.5,
    )
    health.record_rollback(ok=True)
    health.record_feature_flag_isolation(passed=True)
    snap = health.snapshot()
    assert snap.executions == 1
    assert snap.intervention_generation_success_rate == 1.0
    assert snap.projection_success_rate == 1.0
    assert snap.explainability_success_rate == 1.0
    assert snap.planner_consistency_success_rate == 1.0
    assert snap.deterministic_replay_success_rate == 1.0
    assert snap.rollback_success_rate == 1.0
    assert snap.feature_flag_isolation_pass_rate == 1.0
    assert snap.mean_execution_latency_ms == 12.5


def test_shadow_pipeline_unit_emits_telemetry():
    events = EventRegistry()
    validator = _build_validator(events=events)
    observation = validator.validate_shadow(
        "7",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    assert observation.ok is True
    assert observation.determinism_ok is True
    assert observation.intervention_ok is True
    assert observation.explainability_ok is True
    assert observation.projection_ok is True
    assert observation.planner_consistency_ok is True
    types = [e.event_type for e in events.published()]
    assert STRATEGY_SHADOW_REQUESTED in types
    assert STRATEGY_SHADOW_COMPLETED in types
    assert STRATEGY_SHADOW_STABILITY in types
    assert STRATEGY_SHADOW_LATENCY in types
    assert STRATEGY_SHADOW_HEALTH in types


def test_ops_dashboard_payload():
    validator = _build_validator()
    validator.validate_shadow(
        "7",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    dashboard = build_strategy_shadow_ops_dashboard(validator)
    payload = dashboard["strategy_shadow_validation"]
    assert payload["enabled"] is True
    assert payload["influences_student"] is False
    assert payload["phase"] == "s3_shadow_validation"
    assert payload["last_observation"] is not None


def test_feature_flag_composition_wires_shadow():
    flags_off = resolve_v2_feature_flags(
        environ={"KWALITEC_STRATEGY_ENGINE": "0"}
    )
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.strategy_engine is None
    assert composition_off.strategy_shadow is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_STRATEGY_ENGINE": "1"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert composition_on.strategy_engine is not None
    assert composition_on.strategy_shadow is not None
    assert composition_on.strategy_shadow.validator_id == "strategy_shadow_validator"


def test_rollback_verifier_unit():
    events = EventRegistry()
    result = verify_strategy_shadow_rollback(events=events)
    assert result.ok is True
    assert result.strategy_disabled_removes_participation is True
    assert result.runtime_a_unchanged is True
    assert result.twin_flags_unchanged is True
    assert result.adaptive_flags_unchanged is True
    assert result.experience_preserved is True
    assert result.feature_flag_isolation_ok is True
    assert STRATEGY_SHADOW_ROLLBACK_VERIFIED in [
        e.event_type for e in events.published()
    ]
