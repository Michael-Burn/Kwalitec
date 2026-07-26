"""Unit tests — Learning Evidence Platform E4 Analytics & Projection."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    ANALYTICS_AUDIENCE_GOVERNANCE,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    GATE_PASSED,
    QUALITY_PASS,
    REASON_ANALYTICS_FLAG_OFF,
    RECOMMENDATION_EXPAND_SOAK,
    AnalyticsAggregator,
    AnalyticsEngine,
    AnalyticsExport,
    AnalyticsSummary,
    AnalyticsValidationError,
    EvidenceFactory,
    EvidenceProjection,
    EvidenceProjector,
    ExperimentArm,
    ExperimentDefinition,
    ExperimentFramework,
    ExperimentObservation,
    ObservedEvent,
    PolicyDefinition,
    PolicyEvaluationFactory,
    build_analytics_aggregator,
    build_analytics_engine,
    build_evidence_platform_adapter,
    build_evidence_projection_port,
    build_evidence_projector,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVIDENCE_ANALYTICS_COMPLETED,
    EVIDENCE_ANALYTICS_REQUESTED,
)


def _mission_event(*, student_id: str = "42", **overrides) -> ObservedEvent:
    base = {
        "student_id": student_id,
        "event_type": "mission_completed",
        "observed_at": "2026-07-25T10:00:00+00:00",
        "ingested_at": "2026-07-25T10:00:05+00:00",
        "as_of": "2026-07-25T10:00:00+00:00",
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
        experiment_id="exp-e4-shadow",
        definition_version="e2.0",
        title="E4 shadow",
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
        pre_registration="pre-reg-e4-shadow",
        status="running",
        primary_outcomes=("organisation_completion",),
        policy_id="pol-e4-analytics",
    )


def _policy(**overrides) -> PolicyDefinition:
    base = {
        "policy_id": "pol-e4-analytics",
        "policy_version": "1.0.0",
        "definition_version": "e3.0",
        "title": "E4 analytics policy",
        "intent": "Observe shadow stability for analytics aggregation",
        "owner_layer": "adaptive",
        "claim_boundary_intent": "organisation",
        "principles": ("ep.inspectability.why_tonight",),
        "sp_mapping": ("SP8",),
        "upstream_controls": {"ENABLE_ADAPTIVE_SHADOW": True},
        "experiment_ids": ("exp-e4-shadow",),
        "evaluation_kind": "shadow_descriptive",
        "evaluation_eligibility": {"min_observations": 3, "min_students": 2},
        "educational_rationale": {
            "organisation_vs_learning_note": (
                "Organisation outcomes remain separate from learning depth."
            ),
        },
        "statistical_plan": {"design": "descriptive_soak"},
        "status": "active",
        "spec_ref": "adr-ms006-pol-e4-analytics",
        "limitations": ("shadow_only",),
    }
    base.update(overrides)
    return PolicyDefinition(**base)


def _observations(*, count: int = 4) -> tuple[ExperimentObservation, ...]:
    framework = ExperimentFramework()
    framework.register_definition(_definition_exp())
    factory = EvidenceFactory()
    observations: list[ExperimentObservation] = []
    for index in range(count):
        student_id = str(40 + index)
        record = factory.create(_mission_event(student_id=student_id))
        assert record.quality.result == QUALITY_PASS
        observations.append(
            framework.assign(record, experiment_id="exp-e4-shadow")
        )
    return tuple(observations)


def _evaluations(*, count: int = 1):
    observations = _observations(count=4)
    factory = PolicyEvaluationFactory()
    factory.register_definition(_policy())
    evaluations = []
    for _ in range(count):
        evaluations.append(
            factory.evaluate(observations, policy_id="pol-e4-analytics")
        )
    return tuple(evaluations), observations


def test_build_helpers_respect_feature_flag():
    assert build_analytics_engine(enabled=False) is None
    assert build_analytics_aggregator(enabled=False) is None
    assert build_evidence_projector(enabled=False) is None
    assert build_evidence_projection_port(enabled=False) is None
    assert isinstance(build_analytics_engine(enabled=True), AnalyticsEngine)
    assert isinstance(
        build_analytics_aggregator(enabled=True), AnalyticsAggregator
    )
    assert isinstance(build_evidence_projector(enabled=True), EvidenceProjector)


def test_composition_wires_analytics_only_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.evidence_platform is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert composition_on.evidence_platform is not None
    assert composition_on.evidence_platform.analytics_engine is not None
    assert composition_on.evidence_platform.evidence_projector is not None
    assert composition_on.evidence_platform.evidence_projection_port is not None


def test_aggregator_deterministic():
    evaluations, observations = _evaluations()
    aggregator = AnalyticsAggregator()
    first = aggregator.aggregate(
        evaluations=evaluations, observations=observations
    )
    second = aggregator.aggregate(
        evaluations=evaluations, observations=observations
    )
    assert first.serialize() == second.serialize()
    assert first.evidence_count >= 1
    assert first.evaluation_count == 1
    assert first.experiment_count == 1
    assert first.confidence_summary.evaluations_with_gate_passed >= 0


def test_identical_inputs_identical_summary_every_execution():
    evaluations, observations = _evaluations()
    engine = AnalyticsEngine()
    serializations = {
        engine.aggregate(
            evaluations=evaluations, observations=observations
        ).serialize()
        for _ in range(5)
    }
    assert len(serializations) == 1


def test_engine_produces_immutable_summary_with_provenance():
    evaluations, observations = _evaluations()
    engine = AnalyticsEngine()
    summary = engine.aggregate(
        evaluations=evaluations, observations=observations
    )
    assert summary.summary_id.startswith("asum-")
    assert summary.availability == AVAILABILITY_AVAILABLE
    assert summary.provenance
    assert summary.contents_ref.startswith("aref-")
    with pytest.raises(FrozenInstanceError):
        summary.summary_id = "mutated"  # type: ignore[misc]


def test_inputs_not_mutated_during_aggregate():
    evaluations, observations = _evaluations()
    eval_before = tuple(e.serialize() for e in evaluations)
    obs_before = tuple(o.serialize() for o in observations)
    AnalyticsEngine().aggregate(
        evaluations=evaluations, observations=observations
    )
    assert tuple(e.serialize() for e in evaluations) == eval_before
    assert tuple(o.serialize() for o in observations) == obs_before


def test_projection_deterministic_and_immutable():
    evaluations, observations = _evaluations()
    summary = AnalyticsEngine().aggregate(
        evaluations=evaluations, observations=observations
    )
    projector = EvidenceProjector()
    first = projector.project(summary)
    second = projector.project(summary)
    assert first.serialize() == second.serialize()
    assert first.projection_id.startswith("aproj-")
    assert first.policy_summaries
    assert first.experiment_summaries
    assert first.evidence_counts["evaluations"] == 1
    with pytest.raises(FrozenInstanceError):
        first.headline = "mutated"  # type: ignore[misc]


def test_serialization_round_trip_stable():
    evaluations, observations = _evaluations()
    summary = AnalyticsEngine().aggregate(
        evaluations=evaluations, observations=observations
    )
    projection = EvidenceProjector().project(summary)
    assert serialize_canonical(summary.to_canonical_dict()) == summary.serialize()
    assert (
        serialize_canonical(projection.to_canonical_dict())
        == projection.serialize()
    )


def test_claim_boundary_blocks_not_merged():
    evaluations, observations = _evaluations()
    summary = AnalyticsEngine().aggregate(
        evaluations=evaluations, observations=observations
    )
    assert summary.scorecard_slice is not None
    assert "organisation_block" in summary.scorecard_slice.to_canonical_dict()
    assert "learning_depth_block" in summary.scorecard_slice.to_canonical_dict()
    assert "learning_depth_deferred" in summary.limitations
    assert any(
        "organisation" in c.lower() or "learning" in c.lower()
        for c in summary.narrative_constraints
    )


def test_empty_inputs_produce_unavailable_honest_summary():
    summary = AnalyticsEngine().aggregate()
    assert summary.availability == AVAILABILITY_UNAVAILABLE
    assert summary.unavailable_reason == "empty_authentic"
    projection = EvidenceProjector().project(summary)
    assert projection.availability == AVAILABILITY_UNAVAILABLE


def test_student_coaching_audience_forbidden():
    with pytest.raises(ValueError, match="audience"):
        AnalyticsExport(audience="student_coaching")
    with pytest.raises(AnalyticsValidationError, match="audience"):
        AnalyticsAggregator().aggregate(audience="student_coaching")


def test_telemetry_emitted():
    evaluations, observations = _evaluations()
    events = EventRegistry()
    engine = AnalyticsEngine(events=events)
    summary = engine.aggregate(
        evaluations=evaluations, observations=observations
    )
    types = [event.event_type for event in events.published()]
    assert EVIDENCE_ANALYTICS_REQUESTED in types
    assert EVIDENCE_ANALYTICS_COMPLETED in types
    assert summary.summary_id


def test_projection_port_flag_off_unavailable():
    port = build_evidence_projection_port(enabled=True)
    assert port is not None
    # Simulate disabled port behaviour via direct construction.
    from app.infrastructure.adapters.evidence_platform.projector import (
        EvidenceGovernanceProjectionPort,
    )

    disabled = EvidenceGovernanceProjectionPort(enabled=False)
    summary = AnalyticsSummary(summary_id="asum-test")
    projection = disabled.project_summary(summary)
    assert projection.availability == AVAILABILITY_UNAVAILABLE
    assert projection.unavailable_reason == REASON_ANALYTICS_FLAG_OFF


def test_adapter_aggregate_and_project():
    evaluations, observations = _evaluations()
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    agg = adapter.aggregate_analytics(
        evaluations=evaluations, observations=observations
    )
    assert agg.ok
    assert isinstance(agg.value, AnalyticsSummary)
    proj = adapter.project_evidence(agg.value)
    assert proj.ok
    assert isinstance(proj.value, EvidenceProjection)
    assert proj.value.audience == ANALYTICS_AUDIENCE_GOVERNANCE


def test_export_from_summary():
    evaluations, observations = _evaluations()
    engine = AnalyticsEngine()
    summary = engine.aggregate(
        evaluations=evaluations, observations=observations
    )
    export = engine.export(summary)
    assert export.export_id.startswith("aexp-")
    assert export.audience == ANALYTICS_AUDIENCE_GOVERNANCE
    assert export.contents_ref == summary.contents_ref


def test_evaluation_gate_still_observational():
    evaluations, _observations_tuple = _evaluations()
    evaluation = evaluations[0]
    assert evaluation.gate_result in {GATE_PASSED, "failed", "ineligible"}
    assert evaluation.recommendation in {
        RECOMMENDATION_EXPAND_SOAK,
        "inconclusive",
        "revise",
        "roll_back",
        "keep",
        "",
    }
    # Analytics must not flip educational behaviour flags.
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EVIDENCE_PLATFORM is False
