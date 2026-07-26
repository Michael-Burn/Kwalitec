"""Unit tests — Evidence Shadow Validation & Operational Readiness (MS-006 E5)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    QUALITY_PASS,
    READINESS_READY,
    AnalyticsEngine,
    DeterminismValidator,
    EvidenceFactory,
    EvidencePlatformState,
    EvidenceProjector,
    EvidenceShadowValidator,
    ExperimentArm,
    ExperimentDefinition,
    ExperimentFramework,
    ObservedEvent,
    OperationalHealthMonitor,
    PolicyDefinition,
    PolicyEvaluationFactory,
    ReadinessEvaluator,
    ReadinessReport,
    ValidationCoverage,
    build_evidence_platform_adapter,
    build_evidence_shadow_ops_dashboard,
    build_evidence_shadow_validator,
    verify_evidence_shadow_rollback,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVENT_TYPES,
    EVIDENCE_SHADOW_COMPLETED,
    EVIDENCE_SHADOW_EVENT_TYPES,
    EVIDENCE_SHADOW_HEALTH,
    EVIDENCE_SHADOW_LATENCY,
    EVIDENCE_SHADOW_READINESS,
    EVIDENCE_SHADOW_REQUESTED,
    EVIDENCE_SHADOW_STABILITY,
)

AS_OF = "2026-07-25T12:00:00+00:00"


def _mission_event(*, student_id: str = "42", **overrides) -> ObservedEvent:
    base = {
        "student_id": student_id,
        "event_type": "mission_completed",
        "observed_at": "2026-07-25T10:00:00+00:00",
        "ingested_at": "2026-07-25T10:00:05+00:00",
        "as_of": AS_OF,
        "claim_boundary": "organisation",
        "evidence_class": "FACT_EVENT",
        "runtime_a": {
            "mission": {"mission_id": f"m-{student_id}", "status": "completed"},
            "evidence_id": f"ra-ev-{student_id}",
        },
        "payload_summary": {"mission_status": "completed"},
    }
    base.update(overrides)
    return ObservedEvent(**base)


def _definition_exp() -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id="exp-e5-shadow",
        definition_version="e2.0",
        title="E5 shadow",
        arms=(
            ExperimentArm(
                arm_id="control",
                label="control",
                exposure="shadow_only",
            ),
            ExperimentArm(
                arm_id="treatment",
                label="treatment",
                exposure="shadow_only",
            ),
        ),
        assignment_mechanism="hash",
        pre_registration="pre-reg-e5-shadow",
        status="running",
        primary_outcomes=("organisation_completion",),
        policy_id="pol-e5-shadow",
    )


def _policy(**overrides) -> PolicyDefinition:
    base = {
        "policy_id": "pol-e5-shadow",
        "policy_version": "1.0.0",
        "definition_version": "e3.0",
        "title": "E5 shadow policy",
        "intent": "Observe shadow stability for readiness",
        "owner_layer": "adaptive",
        "claim_boundary_intent": "organisation",
        "principles": ("ep.inspectability.why_tonight",),
        "sp_mapping": ("SP8",),
        "upstream_controls": {"ENABLE_ADAPTIVE_SHADOW": True},
        "experiment_ids": ("exp-e5-shadow",),
        "evaluation_kind": "shadow_descriptive",
        "evaluation_eligibility": {"min_observations": 3, "min_students": 2},
        "educational_rationale": {
            "organisation_vs_learning_note": (
                "Organisation outcomes remain separate from learning depth."
            ),
        },
        "statistical_plan": {"design": "descriptive_soak"},
        "status": "active",
        "spec_ref": "adr-ms006-pol-e5-shadow",
        "limitations": ("shadow_only",),
    }
    base.update(overrides)
    return PolicyDefinition(**base)


def _platform_state():
    framework = ExperimentFramework()
    framework.register_definition(_definition_exp())
    factory = EvidenceFactory()
    evidence_records = []
    observations = []
    for index in range(4):
        student_id = str(50 + index)
        record = factory.create(_mission_event(student_id=student_id))
        assert record.quality.result == QUALITY_PASS
        evidence_records.append(record)
        observations.append(
            framework.assign(record, experiment_id="exp-e5-shadow")
        )
    eval_factory = PolicyEvaluationFactory()
    eval_factory.register_definition(_policy())
    evaluation = eval_factory.evaluate(
        observations, policy_id="pol-e5-shadow", created_at=AS_OF
    )
    analytics = AnalyticsEngine().aggregate(
        evaluations=(evaluation,),
        observations=tuple(observations),
        evidence_records=tuple(evidence_records),
        as_of=AS_OF,
    )
    projection = EvidenceProjector().project(analytics, as_of=AS_OF)
    return EvidencePlatformState(
        evidence_records=tuple(evidence_records),
        observations=tuple(observations),
        evaluations=(evaluation,),
        analytics_summaries=(analytics,),
        projections=(projection,),
    )


def _build_validator(*, events: EventRegistry | None = None) -> EvidenceShadowValidator:
    adapter = build_evidence_platform_adapter(enabled=True)
    validator = build_evidence_shadow_validator(
        enabled=True,
        adapter=adapter,
        events=events or EventRegistry(),
    )
    assert validator is not None
    return validator


def test_evidence_shadow_event_types_registered():
    for event_type in EVIDENCE_SHADOW_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_build_validator_requires_flag():
    assert build_evidence_shadow_validator(enabled=False, adapter=object()) is None
    assert isinstance(
        build_evidence_shadow_validator(enabled=True, adapter=None),
        EvidenceShadowValidator,
    )


def test_disabled_validator_returns_unavailable():
    adapter = build_evidence_platform_adapter(enabled=True)
    validator = EvidenceShadowValidator(adapter=adapter, enabled=False)
    observation = validator.validate_shadow(state=_platform_state(), as_of=AS_OF)
    assert observation.ok is False
    assert observation.error_code == "UNAVAILABLE"


def test_determinism_validator_identical_state():
    state = _platform_state()
    validator = DeterminismValidator()
    first = validator.validate(
        evidence_records=state.evidence_records,
        observations=state.observations,
        evaluations=state.evaluations,
        analytics_summaries=state.analytics_summaries,
        projections=state.projections,
        adapter=build_evidence_platform_adapter(enabled=True),
    )
    second = validator.validate(
        evidence_records=state.evidence_records,
        observations=state.observations,
        evaluations=state.evaluations,
        analytics_summaries=state.analytics_summaries,
        projections=state.projections,
        adapter=build_evidence_platform_adapter(enabled=True),
    )
    assert first.success is True
    assert first.to_canonical_dict() == second.to_canonical_dict()


def test_inputs_remain_immutable_during_validation():
    state = _platform_state()
    before = (
        state.evidence_records[0].serialize(),
        state.observations[0].serialize(),
        state.evaluations[0].serialize(),
        state.analytics_summaries[0].serialize(),
        state.projections[0].serialize(),
    )
    DeterminismValidator().validate(
        evidence_records=state.evidence_records,
        observations=state.observations,
        evaluations=state.evaluations,
        analytics_summaries=state.analytics_summaries,
        projections=state.projections,
        adapter=build_evidence_platform_adapter(enabled=True),
    )
    after = (
        state.evidence_records[0].serialize(),
        state.observations[0].serialize(),
        state.evaluations[0].serialize(),
        state.analytics_summaries[0].serialize(),
        state.projections[0].serialize(),
    )
    assert before == after
    with pytest.raises(FrozenInstanceError):
        state.evidence_records[0].student_id = "mutated"  # type: ignore[misc]


def test_readiness_report_immutable_and_deterministic():
    state = _platform_state()
    determinism = DeterminismValidator().validate(
        evidence_records=state.evidence_records,
        observations=state.observations,
        evaluations=state.evaluations,
        analytics_summaries=state.analytics_summaries,
        projections=state.projections,
    )
    evaluator = ReadinessEvaluator()
    first = evaluator.evaluate(
        determinism=determinism,
        coverage=state.coverage(),
        as_of=AS_OF,
        rollback_ok=True,
    )
    second = evaluator.evaluate(
        determinism=determinism,
        coverage=state.coverage(),
        as_of=AS_OF,
        rollback_ok=True,
    )
    assert isinstance(first, ReadinessReport)
    assert first.serialize() == second.serialize()
    assert first.report_id == second.report_id
    assert first.readiness_status == READINESS_READY
    assert first.influences_student is False
    assert first.deploys_policy is False
    with pytest.raises(FrozenInstanceError):
        first.ok = False  # type: ignore[misc]


def test_operational_health_monitor_rates():
    monitor = OperationalHealthMonitor()
    monitor.record_execution(
        ok=True,
        determinism_success=True,
        readiness_status="ready",
        evidence_count=1,
        observation_count=1,
        evaluation_count=1,
        analytics_count=1,
        projection_count=1,
        latency_ms=12.5,
    )
    monitor.record_execution(
        ok=False,
        determinism_success=False,
        readiness_status="not_ready",
        drift_signals=2,
        latency_ms=20.0,
    )
    snapshot = monitor.snapshot()
    assert snapshot.executions == 2
    assert snapshot.validation_success_count == 1
    assert snapshot.determinism_attempts == 2
    assert snapshot.determinism_success_count == 1
    assert snapshot.drift_signal_count == 2
    assert snapshot.validation_success_rate == 0.5


def test_shadow_validator_emits_telemetry():
    events = EventRegistry()
    validator = _build_validator(events=events)
    observation = validator.validate_shadow(state=_platform_state(), as_of=AS_OF)
    assert observation.ok is True
    assert observation.report is not None
    types = {event.event_type for event in events.published()}
    assert EVIDENCE_SHADOW_REQUESTED in types
    assert EVIDENCE_SHADOW_STABILITY in types
    assert EVIDENCE_SHADOW_COMPLETED in types
    assert EVIDENCE_SHADOW_LATENCY in types
    assert EVIDENCE_SHADOW_HEALTH in types
    assert EVIDENCE_SHADOW_READINESS in types


def test_identical_state_identical_readiness_every_execution():
    validator = _build_validator()
    state = _platform_state()
    serializations = {
        validator.validate_shadow(state=state, as_of=AS_OF).report.serialize()
        for _ in range(5)
    }
    assert len(serializations) == 1


def test_composition_wires_shadow_only_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.evidence_platform is None
    assert composition_off.evidence_shadow is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert composition_on.evidence_platform is not None
    assert composition_on.evidence_shadow is not None
    assert isinstance(composition_on.evidence_shadow, EvidenceShadowValidator)


def test_rollback_controller_removes_evidence_participation():
    result = verify_evidence_shadow_rollback()
    assert result.ok is True
    assert result.evidence_disabled_removes_participation is True
    assert result.runtime_a_unchanged is True
    assert result.twin_flags_unchanged is True
    assert result.adaptive_flags_unchanged is True
    assert result.strategy_flags_unchanged is True
    assert result.experience_preserved is True


def test_ops_dashboard_payload():
    validator = _build_validator()
    validator.validate_shadow(state=_platform_state(), as_of=AS_OF)
    payload = build_evidence_shadow_ops_dashboard(validator)
    shadow = payload["evidence_shadow_validation"]
    assert shadow["enabled"] is True
    assert shadow["influences_student"] is False
    assert shadow["deploys_policy"] is False
    assert shadow["last_report"] is not None
    assert shadow["health"]["executions"] >= 1


def test_validation_coverage_serialize_stable():
    coverage = ValidationCoverage(
        evidence_records=1,
        observations=2,
        evaluations=1,
        analytics_summaries=1,
        projections=1,
        subsystems_covered=(
            "evidence_collection",
            "experiment_framework",
            "policy_evaluation",
            "analytics",
            "projection",
        ),
    )
    assert coverage.serialize() == coverage.serialize()
