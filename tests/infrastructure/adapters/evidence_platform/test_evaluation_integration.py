"""Integration tests — Learning Evidence Platform E3 Policy Evaluation."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    AVAILABILITY_AVAILABLE,
    GATE_PASSED,
    QUALITY_PASS,
    RECOMMENDATION_EXPAND_SOAK,
    EvidenceFactory,
    EvidencePlatformAdapter,
    ExperimentArm,
    ExperimentDefinition,
    ExperimentFramework,
    ExperimentObservation,
    ObservedEvent,
    PolicyDefinition,
    PolicyEvaluation,
    PolicyEvaluationFactory,
    build_evidence_platform_adapter,
    build_policy_evaluation_factory,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import EVIDENCE_EVAL_EVENT_TYPES


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
        experiment_id="exp-e3-integration",
        definition_version="e2.0",
        title="E3 integration",
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
        pre_registration="pre-reg-e3-integration",
        status="running",
        primary_outcomes=("organisation_completion",),
        policy_id="pol-e3-integration",
    )


def _policy() -> PolicyDefinition:
    return PolicyDefinition(
        policy_id="pol-e3-integration",
        policy_version="1.0.0",
        definition_version="e3.0",
        title="E3 integration policy",
        intent="Descriptive soak of shadow experiment observations",
        owner_layer="strategy",
        claim_boundary_intent="organisation",
        principles=("ep.study.horizon_structure",),
        sp_mapping=("SP8",),
        experiment_ids=("exp-e3-integration",),
        evaluation_kind="shadow_descriptive",
        evaluation_eligibility={"min_observations": 3, "min_students": 2},
        educational_rationale={
            "organisation_vs_learning_note": (
                "Organisation lift is not learning depth."
            ),
        },
        statistical_plan={"design": "descriptive_soak"},
        status="active",
        spec_ref="spec-e3-integration",
    )


def _pipeline_observations(*, count: int = 4) -> tuple[ExperimentObservation, ...]:
    events = EventRegistry()
    framework = ExperimentFramework(events=events)
    framework.register_definition(_experiment())
    adapter = EvidencePlatformAdapter(
        factory=EvidenceFactory(events=events),
        experiment_framework=framework,
        policy_evaluation_factory=PolicyEvaluationFactory(events=events),
    )
    observations: list[ExperimentObservation] = []
    for index in range(count):
        student_id = str(50 + index)
        event = _full_event(student_id=student_id)
        original_event = event.serialize()
        collected = adapter.assemble_record(student_id, event=event)
        assert collected.ok is True
        record = collected.value
        assert record is not None
        assert record.quality.result == QUALITY_PASS
        assert record.availability == AVAILABILITY_AVAILABLE
        original_record = record.serialize()
        assigned = adapter.assign_to_experiment(
            record, experiment_id="exp-e3-integration"
        )
        assert assigned.ok is True
        observation = assigned.value
        assert isinstance(observation, ExperimentObservation)
        assert event.serialize() == original_event
        assert record.serialize() == original_record
        observations.append(observation)
    return tuple(observations)


def test_collect_assign_evaluate_pipeline():
    events = EventRegistry()
    framework = ExperimentFramework(events=events)
    framework.register_definition(_experiment())
    evaluation_factory = PolicyEvaluationFactory(events=events)
    evaluation_factory.register_definition(_policy())
    adapter = EvidencePlatformAdapter(
        factory=EvidenceFactory(events=events),
        experiment_framework=framework,
        policy_evaluation_factory=evaluation_factory,
    )
    observations = []
    for index in range(4):
        student_id = str(60 + index)
        record = adapter.collect_event(_full_event(student_id=student_id))
        assigned = adapter.assign_to_experiment(
            record, experiment_id="exp-e3-integration"
        )
        assert assigned.ok is True
        observations.append(assigned.value)

    snapshots = [obs.serialize() for obs in observations]
    result = adapter.evaluate_policy(
        observations, policy_id="pol-e3-integration"
    )
    assert result.ok is True
    evaluation = result.value
    assert isinstance(evaluation, PolicyEvaluation)
    assert evaluation.policy_id == "pol-e3-integration"
    assert evaluation.gate_result == GATE_PASSED
    assert evaluation.recommendation == RECOMMENDATION_EXPAND_SOAK
    assert evaluation.experiment_refs == ("exp-e3-integration",)
    assert evaluation.evidence_refs
    assert evaluation.explanation.evidence_considered
    assert evaluation.explanation.statistical_basis
    assert evaluation.explanation.educational_rationale
    assert evaluation.explanation.policy_version
    assert evaluation.explanation.confidence
    for original, current in zip(snapshots, observations, strict=True):
        assert current.serialize() == original

    emitted = {event.event_type for event in events.published()}
    assert EVIDENCE_EVAL_EVENT_TYPES[0] in emitted
    assert EVIDENCE_EVAL_EVENT_TYPES[1] in emitted


def test_determinism_across_factory_and_adapter():
    observations = _pipeline_observations()
    policy = _policy()
    via_factory = PolicyEvaluationFactory().evaluate(observations, policy)
    adapter = EvidencePlatformAdapter(
        policy_evaluation_factory=PolicyEvaluationFactory(),
    )
    via_adapter = adapter.evaluate_policy(observations, policy)
    assert via_adapter.ok is True
    assert via_adapter.value is not None
    assert via_factory.serialize() == via_adapter.value.serialize()
    assert via_factory.evaluation_id == via_adapter.value.evaluation_id


def test_identical_inputs_identical_evaluation_every_execution():
    observations = _pipeline_observations()
    policy = _policy()
    factory = PolicyEvaluationFactory()
    evaluations = [factory.evaluate(observations, policy) for _ in range(5)]
    serialised = {item.serialize() for item in evaluations}
    assert len(serialised) == 1
    assert evaluations[0].evaluation_id.startswith("eval-")


def test_serialization_round_trip_stable():
    evaluation = PolicyEvaluationFactory().evaluate(
        _pipeline_observations(), _policy()
    )
    payload = evaluation.to_canonical_dict()
    assert serialize_canonical(payload) == evaluation.serialize()
    assert payload["policy_id"] == evaluation.policy_id
    assert payload["provenance"]


def test_flag_off_no_evaluation_factory_no_experience_change():
    flags = resolve_v2_feature_flags(environ={})
    composition, _ = build_production_experience(flags=flags)
    assert composition.evidence_platform is None
    assert build_policy_evaluation_factory(enabled=False) is None
    assert build_evidence_platform_adapter(enabled=False) is None


def test_flag_on_composition_evaluation_isolated():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    composition, _ = build_production_experience(flags=flags)
    adapter = composition.evidence_platform
    assert isinstance(adapter, EvidencePlatformAdapter)
    assert adapter.policy_evaluation_factory is not None
    adapter.experiment_framework.register_definition(_experiment())
    adapter.policy_evaluation_factory.register_definition(_policy())
    observations = []
    for index in range(3):
        student_id = str(70 + index)
        record = adapter.collect_event(_full_event(student_id=student_id))
        assigned = adapter.assign_to_experiment(
            record, experiment_id="exp-e3-integration"
        )
        assert assigned.ok is True
        observations.append(assigned.value)
    result = adapter.evaluate_policy(
        observations, policy_id="pol-e3-integration"
    )
    assert result.ok is True
    assert isinstance(result.value, PolicyEvaluation)
    assert result.value.authority == "evidence_platform"
    assert result.value.recommendation == RECOMMENDATION_EXPAND_SOAK
