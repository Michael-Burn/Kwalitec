"""Unit tests — Learning Evidence Platform E3 Policy Evaluation."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    AUTHORITY_EVIDENCE_PLATFORM,
    EVALUATION_KIND_SHADOW_DESCRIPTIVE,
    GATE_CODE_DEMO_THEATRE,
    GATE_FAILED,
    GATE_INELIGIBLE,
    GATE_PASSED,
    QUALITY_PASS,
    RECOMMENDATION_EXPAND_SOAK,
    RECOMMENDATION_ROLL_BACK,
    EvaluationAssembler,
    EvaluationExplainability,
    EvaluationValidationError,
    EvaluationValidator,
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
    PolicyEvaluator,
    build_evaluation_assembler,
    build_evaluation_validator,
    build_evidence_platform_adapter,
    build_policy_definition_registry,
    build_policy_evaluation_factory,
    build_policy_evaluator,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVIDENCE_EVAL_COMPLETED,
    EVIDENCE_EVAL_REQUESTED,
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
        experiment_id="exp-e3-shadow",
        definition_version="e2.0",
        title="E3 shadow",
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
        pre_registration="pre-reg-e3-shadow",
        status="running",
        primary_outcomes=("organisation_completion",),
        policy_id="pol-adaptive-shadow",
    )


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
            framework.assign(record, experiment_id="exp-e3-shadow")
        )
    return tuple(observations)


def _policy(**overrides) -> PolicyDefinition:
    base = {
        "policy_id": "pol-adaptive-shadow",
        "policy_version": "1.0.0",
        "definition_version": "e3.0",
        "title": "Adaptive shadow parity",
        "intent": "Observe shadow stability without learner-visible change",
        "owner_layer": "adaptive",
        "claim_boundary_intent": "organisation",
        "principles": ("ep.inspectability.why_tonight",),
        "sp_mapping": ("SP8",),
        "upstream_controls": {"ENABLE_ADAPTIVE_SHADOW": True},
        "experiment_ids": ("exp-e3-shadow",),
        "evaluation_kind": EVALUATION_KIND_SHADOW_DESCRIPTIVE,
        "evaluation_eligibility": {"min_observations": 3, "min_students": 2},
        "educational_rationale": {
            "organisation_vs_learning_note": (
                "Organisation outcomes remain separate from learning depth."
            ),
            "student_impact_hypothesis": "No student-facing claim in E3.",
        },
        "statistical_plan": {"design": "descriptive_soak"},
        "status": "active",
        "spec_ref": "adr-ms006-pol-adaptive-shadow",
        "limitations": ("shadow_only",),
    }
    base.update(overrides)
    return PolicyDefinition(**base)


def test_build_helpers_respect_feature_flag():
    assert build_policy_evaluation_factory(enabled=False) is None
    assert build_policy_evaluator(enabled=False) is None
    assert build_evaluation_assembler(enabled=False) is None
    assert build_policy_definition_registry(enabled=False) is None
    assert isinstance(build_evaluation_validator(), EvaluationValidator)
    assert isinstance(
        build_policy_evaluation_factory(enabled=True), PolicyEvaluationFactory
    )


def test_adapter_wires_evaluation_factory_when_enabled():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    assert isinstance(adapter.policy_evaluation_factory, PolicyEvaluationFactory)


def test_composition_wires_evaluation_only_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.evidence_platform is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.evidence_platform, EvidencePlatformAdapter)
    assert isinstance(
        composition_on.evidence_platform.policy_evaluation_factory,
        PolicyEvaluationFactory,
    )


def test_registry_registers_and_looks_up():
    factory = PolicyEvaluationFactory()
    policy = _policy()
    factory.register_definition(policy)
    assert factory.registry.contains("pol-adaptive-shadow")
    assert (
        factory.registry.require("pol-adaptive-shadow").policy_version == "1.0.0"
    )
    with pytest.raises(EvaluationValidationError, match="already registered"):
        factory.register_definition(policy)


def test_validator_rejects_deprecated_for_evaluation():
    validator = EvaluationValidator()
    deprecated = _policy(status="deprecated")
    with pytest.raises(EvaluationValidationError, match="status must be"):
        validator.validate_definition(deprecated, require_evaluable=True)


def test_validator_rejects_empty_observations():
    with pytest.raises(EvaluationValidationError, match="at least one"):
        EvaluationValidator().validate_observations((), _policy())


def test_evaluator_assessment_deterministic():
    observations = _observations()
    policy = _policy()
    evaluator = PolicyEvaluator()
    first = evaluator.assess(observations, policy)
    second = evaluator.assess(observations, policy)
    assert first.serialize() == second.serialize()
    assert first.recommendation == RECOMMENDATION_EXPAND_SOAK
    assert first.observation_count == 4


def test_explainability_five_answers_complete():
    observations = _observations()
    policy = _policy()
    assessment = PolicyEvaluator().assess(observations, policy)
    explanation = EvaluationExplainability().build(
        definition=policy,
        observations=observations,
        assessment=assessment,
    )
    complete, missing = EvaluationValidator().validate_explanation(explanation)
    assert complete is True
    assert missing == ()
    assert explanation.evidence_considered["summary"]
    assert explanation.statistical_basis["design"]
    assert explanation.educational_rationale["intent_summary"]
    assert explanation.policy_version["policy_id"]
    assert explanation.confidence["band"]


def test_demo_markers_fail_gate_and_roll_back():
    observations = list(_observations(count=3))
    tainted = ExperimentObservation(
        observation_id=observations[0].observation_id,
        observation_version=observations[0].observation_version,
        experiment_id=observations[0].experiment_id,
        experiment_version=observations[0].experiment_version,
        arm_id=observations[0].arm_id,
        cohort=observations[0].cohort,
        evidence_id=observations[0].evidence_id,
        evidence_ref=observations[0].evidence_ref,
        student_id=observations[0].student_id,
        assignment_mechanism=observations[0].assignment_mechanism,
        assignment_rationale=observations[0].assignment_rationale,
        metadata={**dict(observations[0].metadata), "marker": "demo"},
        observed_at=observations[0].observed_at,
    )
    observations[0] = tainted
    evaluation = PolicyEvaluationFactory().evaluate(observations, _policy())
    assert GATE_CODE_DEMO_THEATRE in evaluation.gate_codes
    assert evaluation.gate_result == GATE_FAILED
    assert evaluation.recommendation == RECOMMENDATION_ROLL_BACK


def test_insufficient_observations_ineligible():
    observations = _observations(count=1)
    policy = _policy(
        evaluation_eligibility={"min_observations": 5, "min_students": 2}
    )
    evaluation = PolicyEvaluationFactory().evaluate(observations, policy)
    assert evaluation.gate_result == GATE_INELIGIBLE
    assert evaluation.recommendation == RECOMMENDATION_EXPAND_SOAK
    assert evaluation.confidence_band == "insufficient"


def test_factory_produces_immutable_evaluation_with_provenance():
    events = EventRegistry()
    factory = PolicyEvaluationFactory(events=events)
    factory.register_definition(_policy())
    observations = _observations()
    snapshots = [obs.serialize() for obs in observations]
    evaluation = factory.evaluate_registered(
        observations, "pol-adaptive-shadow"
    )
    assert isinstance(evaluation, PolicyEvaluation)
    assert evaluation.evaluation_id.startswith("eval-")
    assert evaluation.evaluation_version == "e3.0"
    assert evaluation.authority == AUTHORITY_EVIDENCE_PLATFORM
    assert evaluation.experiment_refs == ("exp-e3-shadow",)
    assert evaluation.evidence_refs
    assert evaluation.provenance
    assert evaluation.gate_result == GATE_PASSED
    assert evaluation.recommendation == RECOMMENDATION_EXPAND_SOAK
    with pytest.raises(FrozenInstanceError):
        evaluation.gate_result = "failed"  # type: ignore[misc]
    for original, current in zip(snapshots, observations, strict=True):
        assert current.serialize() == original
    emitted = {event.event_type for event in events.published()}
    assert EVIDENCE_EVAL_REQUESTED in emitted
    assert EVIDENCE_EVAL_COMPLETED in emitted


def test_determinism_identical_inputs_identical_evaluation():
    observations = _observations()
    policy = _policy()
    factory = PolicyEvaluationFactory()
    evaluations = [
        factory.evaluate(observations, policy) for _ in range(5)
    ]
    serialised = {item.serialize() for item in evaluations}
    assert len(serialised) == 1
    assert evaluations[0].evaluation_id == evaluations[1].evaluation_id


def test_assembler_applies_gate_without_promotion():
    observations = _observations()
    policy = _policy()
    assessment = PolicyEvaluator().assess(observations, policy)
    explanation = EvaluationExplainability().build(
        definition=policy,
        observations=observations,
        assessment=assessment,
    )
    draft = EvaluationAssembler().assemble(
        definition=policy,
        assessment=assessment,
        explanation=explanation,
        evaluation_id="eval-test",
        created_at="2026-07-25T10:00:00+00:00",
    )
    assert draft.evaluation_id == "eval-test"
    assert draft.gate_result in {GATE_PASSED, GATE_INELIGIBLE, GATE_FAILED}
    assert "promotes_policy" not in draft.to_canonical_dict()
    assert serialize_canonical(draft.to_canonical_dict()) == draft.serialize()
