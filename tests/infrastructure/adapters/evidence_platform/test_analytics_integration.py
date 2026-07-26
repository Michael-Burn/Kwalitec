"""Integration tests — Learning Evidence Platform E4 Analytics & Projection."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    AVAILABILITY_AVAILABLE,
    GATE_PASSED,
    QUALITY_PASS,
    AnalyticsEngine,
    AnalyticsSummary,
    EvidenceFactory,
    EvidencePlatformAdapter,
    EvidenceProjection,
    EvidenceProjector,
    ExperimentArm,
    ExperimentDefinition,
    ExperimentFramework,
    ObservedEvent,
    PolicyDefinition,
    PolicyEvaluationFactory,
    build_evidence_platform_adapter,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import EVIDENCE_ANALYTICS_EVENT_TYPES


def _full_event(*, student_id: str = "42", **overrides) -> ObservedEvent:
    base = {
        "student_id": student_id,
        "event_type": "mission_completed",
        "observed_at": "2026-07-25T12:00:00+00:00",
        "ingested_at": "2026-07-25T12:00:01+00:00",
        "as_of": "2026-07-25T12:00:00+00:00",
        "claim_boundary": "organisation",
        "evidence_class": "FACT_EVENT",
        "runtime_a": {
            "mission": {"mission_id": f"mission-{student_id}", "topic_code": "T1"},
            "evidence_id": f"ra-{student_id}",
        },
        "experience": {"delivery_id": f"exp-del-{student_id}"},
        "strategy": {"intervention_id": f"strat-{student_id}"},
        "adaptive": {"decision_id": f"adapt-{student_id}"},
        "twin": {"twin_id": f"twin-{student_id}"},
        "payload_summary": {"outcome": "completed"},
    }
    base.update(overrides)
    return ObservedEvent(**base)


def _experiment() -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id="exp-e4-integration",
        definition_version="e2.0",
        title="E4 integration",
        arms=(
            ExperimentArm(
                arm_id="control",
                label="control",
                exposure="shadow_only",
            ),
            ExperimentArm(
                arm_id="treatment_a",
                label="treatment_a",
                exposure="shadow_only",
            ),
        ),
        assignment_mechanism="hash",
        pre_registration="pre-reg-e4-integration",
        status="running",
        primary_outcomes=("organisation_completion",),
        policy_id="pol-e4-integration",
    )


def _policy() -> PolicyDefinition:
    return PolicyDefinition(
        policy_id="pol-e4-integration",
        policy_version="1.0.0",
        definition_version="e3.0",
        title="E4 integration policy",
        intent="Descriptive soak feeding analytics aggregation",
        owner_layer="strategy",
        claim_boundary_intent="organisation",
        principles=("ep.study.horizon_structure",),
        sp_mapping=("SP8",),
        experiment_ids=("exp-e4-integration",),
        evaluation_kind="shadow_descriptive",
        evaluation_eligibility={"min_observations": 3, "min_students": 2},
        educational_rationale={
            "organisation_vs_learning_note": (
                "Organisation lift is not learning depth."
            ),
        },
        statistical_plan={"design": "descriptive_soak"},
        status="active",
        spec_ref="adr-ms006-pol-e4-integration",
        limitations=("shadow_only",),
    )


def _pipeline_inputs():
    framework = ExperimentFramework()
    framework.register_definition(_experiment())
    evidence_factory = EvidenceFactory()
    observations = []
    records = []
    for index in range(4):
        student_id = str(50 + index)
        record = evidence_factory.create(_full_event(student_id=student_id))
        assert record.quality.result == QUALITY_PASS
        records.append(record)
        observations.append(
            framework.assign(record, experiment_id="exp-e4-integration")
        )
    eval_factory = PolicyEvaluationFactory()
    eval_factory.register_definition(_policy())
    evaluation = eval_factory.evaluate(
        observations, policy_id="pol-e4-integration"
    )
    assert evaluation.gate_result == GATE_PASSED
    return tuple([evaluation]), tuple(observations), tuple(records)


def test_full_e1_to_e4_pipeline_deterministic():
    evaluations, observations, records = _pipeline_inputs()
    engine = AnalyticsEngine()
    projector = EvidenceProjector()

    summaries = [
        engine.aggregate(
            evaluations=evaluations,
            observations=observations,
            evidence_records=records,
        )
        for _ in range(3)
    ]
    assert len({s.serialize() for s in summaries}) == 1
    summary = summaries[0]
    assert isinstance(summary, AnalyticsSummary)
    assert summary.availability == AVAILABILITY_AVAILABLE
    assert summary.evaluation_count == 1
    assert summary.observation_count == 4
    assert summary.evidence_count >= 4
    assert summary.policy_summaries
    assert summary.experiment_summaries
    assert summary.scorecard_slice is not None
    assert summary.trend_metadata.direction == "not_estimable"

    projections = [projector.project(summary) for _ in range(3)]
    assert len({p.serialize() for p in projections}) == 1
    projection = projections[0]
    assert isinstance(projection, EvidenceProjection)
    assert projection.summary_id == summary.summary_id
    assert projection.provenance.summary_id == summary.summary_id
    assert projection.export_ref == summary.contents_ref


def test_adapter_pipeline_matches_engine_and_projector():
    evaluations, observations, records = _pipeline_inputs()
    events = EventRegistry()
    engine = AnalyticsEngine(events=events)
    projector = EvidenceProjector()
    adapter = EvidencePlatformAdapter(
        analytics_engine=engine,
        evidence_projector=projector,
        evidence_projection_port=None,
    )

    via_engine = engine.aggregate(
        evaluations=evaluations,
        observations=observations,
        evidence_records=records,
    )
    via_adapter = adapter.aggregate_analytics(
        evaluations=evaluations,
        observations=observations,
        evidence_records=records,
    )
    assert via_adapter.ok
    assert via_adapter.value.serialize() == via_engine.serialize()

    proj_engine = projector.project(via_engine)
    proj_adapter = adapter.project_evidence(via_engine)
    assert proj_adapter.ok
    assert proj_adapter.value.serialize() == proj_engine.serialize()

    emitted = {event.event_type for event in events.published()}
    assert emitted.issuperset(set(EVIDENCE_ANALYTICS_EVENT_TYPES[:2]))


def test_determinism_across_factory_and_adapter():
    evaluations, observations, records = _pipeline_inputs()
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    first = adapter.aggregate_analytics(
        evaluations=evaluations,
        observations=observations,
        evidence_records=records,
    )
    second = adapter.aggregate_analytics(
        evaluations=evaluations,
        observations=observations,
        evidence_records=records,
    )
    assert first.ok and second.ok
    assert first.value.serialize() == second.value.serialize()

    p1 = adapter.project_evidence(first.value)
    p2 = adapter.project_evidence(second.value)
    assert p1.ok and p2.ok
    assert p1.value.serialize() == p2.value.serialize()
    assert serialize_canonical(p1.value.to_canonical_dict()) == p1.value.serialize()


def test_composition_flag_off_leaves_experience_unchanged():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.evidence_platform is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "true"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert composition_on.evidence_platform is not None
    assert composition_on.evidence_platform.adapter_version == "1.0.0-e5"
    # Analytics wiring must not enable educational authority flags.
    assert flags_on.ENABLE_ADAPTIVE_AUTHORITY is False
    assert flags_on.ENABLE_STRATEGY_ENGINE is False


def test_governance_port_binds_and_exports():
    evaluations, observations, records = _pipeline_inputs()
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    result = adapter.aggregate_analytics(
        evaluations=evaluations,
        observations=observations,
        evidence_records=records,
    )
    assert result.ok
    projection_result = adapter.project_evidence(result.value)
    assert projection_result.ok
    port = adapter.evidence_projection_port
    assert port is not None
    bound = port.get_projection(result.value.summary_id)
    assert bound is not None
    assert bound.serialize() == projection_result.value.serialize()
    export = port.get_governance_export(result.value.summary_id)
    assert export.ok
    assert export.value.serialize() == bound.serialize()
