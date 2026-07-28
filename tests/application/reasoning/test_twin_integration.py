"""AP-002D3 — decision generation, Twin updates, provenance, determinism."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from app.application.reasoning.decisions.decision_generator import DecisionGenerator
from app.application.reasoning.decisions.errors import (
    DuplicateDecision,
    UnsupportedDecisionVersion,
)
from app.application.reasoning.decisions.twin_updater import TwinUpdater
from app.application.reasoning.decisions.validator import DecisionValidator
from app.application.reasoning.decisions.versions import (
    APPROVED_MASTERY_LEARNING_RATE,
    APPROVED_MASTERY_PRIOR,
    DECISION_VERSION,
)
from app.application.reasoning.dto.decision_dto import DecisionResultDTO
from app.application.reasoning.interpretation.evidence_interpreter import (
    EvidenceInterpreter,
)
from app.application.reasoning.mappers.decision_mapper import map_decision_result
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.ranking import RankingBreakdown
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalResult,
)
from app.domain.educational_reasoning.mastery_update import MasteryUpdateRule
from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.observations.category import ObservationCategory
from app.domain.reasoning.observations.observation_set import EducationalObservationSet
from app.domain.student_digital_twin.learning_state import LearningState
from tests.application.reasoning.conftest import FIXED_AT, make_bundle, make_item


def _ranking() -> RankingBreakdown:
    return RankingBreakdown(
        semantic_similarity=0.5,
        graph_proximity=0.8,
        confidence=0.9,
        founder_verification=1.0,
        document_version=0.5,
        entity_freshness=0.5,
        relationship_strength=0.7,
        evidence_count=0.5,
        rank_score=0.88,
    )


def _make_retrieval_stub(*, concept_id: str = "concept-bayes") -> MagicMock:
    stub = MagicMock()
    evidence = (
        EvidenceItem(
            evidence_id="ev-d3-1",
            role="definition",
            excerpt="Bayes theorem definition",
            entity_id=concept_id,
        ),
    )
    ranked = RankedEvidence(
        entity_id=concept_id,
        kind="concept",
        title="Bayes Theorem",
        body="definition",
        document_id=1,
        version_label="2026",
        confidence=0.9,
        confidence_band="high",
        verified=True,
        provenance_id="prov-d3-1",
        rank_score=0.88,
        ranking=_ranking(),
        evidence=evidence,
        prerequisites=(),
        related_concepts=(),
        supporting_formulae=(),
        worked_examples=(),
        practice_questions=(),
        learning_objectives=(),
    )
    stub.retrieve.return_value = RetrievalResult(
        query_text=concept_id,
        intent=QueryIntent.DEFINITION,
        profile=RetrievalProfile.MISSION_ENGINE,
        results=(ranked,),
        concept_ids=(concept_id,),
        learning_objective_ids=(),
        definition_ids=(),
        formula_ids=(),
        example_ids=(),
        practice_question_ids=(),
        prerequisite_ids=(),
        related_concept_ids=(),
        retrieval_log_id="rl-d3-1",
    )
    return stub


@pytest.fixture
def twin(ctx):
    return StudentDigitalTwinService().create(
        student_id="student-d3-1",
        display_name="D3 Student",
        subject_code="CS1",
        workspace_id="ws-d3",
        twin_id="twin-d3-1",
    )


@pytest.fixture
def reasoning(ctx) -> StudentReasoningService:
    return StudentReasoningService(retrieval=_make_retrieval_stub())


def _interpret(bundle=None, *, request_id: str = "rrq-d3"):
    return EvidenceInterpreter().interpret_bundle(
        bundle or make_bundle(),
        correlation_id="corr-d3",
        reasoning_request_id=request_id,
        interpreted_at=FIXED_AT,
    )


def test_approved_mastery_constants_match_rule() -> None:
    assert APPROVED_MASTERY_LEARNING_RATE == MasteryUpdateRule.learning_rate
    assert APPROVED_MASTERY_PRIOR == MasteryUpdateRule.prior


def test_decision_generation_from_observation_set(twin) -> None:
    interpretation = _interpret()
    result = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-d3",
        session_id=interpretation.context.session_id,
        decided_at=FIXED_AT,
    )
    categories = {d.category for d in result.decision_set.decisions}
    assert DecisionCategory.MASTERY_BELIEF_UPDATE in categories
    assert DecisionCategory.CONFIDENCE_BELIEF_UPDATE in categories
    assert DecisionCategory.PROVENANCE_RECORDED in categories
    assert result.context.decision_version == DECISION_VERSION


def test_twin_update_applies_mastery_and_versions(twin) -> None:
    interpretation = _interpret()
    prior_version = twin.version
    prior_obs_count = len(twin.observations)
    result = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-d3",
        decided_at=FIXED_AT,
    )
    updated = TwinUpdater().apply(twin, result.decision_set, updated_at=FIXED_AT)
    assert updated.version == prior_version + 1
    assert len(updated.observations) == prior_obs_count
    mastery = updated.mastery.get("concept-bayes")
    assert mastery is not None
    assert mastery.mastery_score > 0
    assert updated.reasoning_history
    assert updated.learning_state.exam_readiness == twin.learning_state.exam_readiness


def test_provenance_complete_on_decisions_and_history(twin) -> None:
    interpretation = _interpret()
    result = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-d3",
        decided_at=FIXED_AT,
    )
    for decision in result.decision_set.decisions:
        assert decision.provenance["evidence_bundle_id"] == "bundle-1"
        assert decision.provenance["educational_observation_ids"]
        assert decision.provenance["reasoning_request_id"] == "rrq-d3"
        assert decision.provenance["decision_id"] == decision.decision_id
        assert decision.provenance["decision_version"] == DECISION_VERSION
        assert decision.provenance["assessment_session_id"] == "sess-1"
        assert decision.provenance["correlation_id"] == "corr-d3"
        assert decision.traceability["twin_id"] == twin.twin_id

    updated = TwinUpdater().apply(twin, result.decision_set, updated_at=FIXED_AT)
    step = updated.reasoning_history[-1].steps[0]
    assert step.code == "educational_decision_set"
    assert step.inputs["evidence_bundle_id"] == "bundle-1"
    assert step.outputs["assessment_session_id"] == "sess-1"
    assert step.outputs["correlation_id"] == "corr-d3"
    assert step.outputs["reasoning_request_id"] == "rrq-d3"
    assert step.outputs["decision_ids"]


def test_deterministic_replay_identical_twin_state(twin) -> None:
    interpretation = _interpret()
    first_decisions = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-d3",
        decided_at=FIXED_AT,
    )
    second_decisions = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-d3",
        decided_at=FIXED_AT,
    )
    assert first_decisions.decision_ids == second_decisions.decision_ids
    assert [
        (d.category, d.value, dict(d.payload))
        for d in first_decisions.decision_set.decisions
    ] == [
        (d.category, d.value, dict(d.payload))
        for d in second_decisions.decision_set.decisions
    ]

    first_twin = TwinUpdater().apply(
        twin, first_decisions.decision_set, updated_at=FIXED_AT
    )
    second_twin = TwinUpdater().apply(
        twin, second_decisions.decision_set, updated_at=FIXED_AT
    )
    assert first_twin.mastery.get("concept-bayes").mastery_score == (
        second_twin.mastery.get("concept-bayes").mastery_score
    )
    assert first_twin.confidence.score == second_twin.confidence.score
    assert first_twin.version == second_twin.version


def test_duplicate_protection_rejects_repeated_evidence(twin) -> None:
    interpretation = _interpret()
    result = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-d3",
        decided_at=FIXED_AT,
    )
    updated = TwinUpdater().apply(twin, result.decision_set, updated_at=FIXED_AT)
    with pytest.raises(DuplicateDecision):
        TwinUpdater().apply(updated, result.decision_set, updated_at=FIXED_AT)


def test_soft_signals_alone_preserve_uncertainty(twin) -> None:
    item = make_item(correctness=None, confidence=3)
    bundle = make_bundle(
        items=(item,),
        observation_ids=(item.observation_id,),
        question_ids=(item.question_id,),
        summary_count=1,
    )
    interpretation = EvidenceInterpreter().interpret_bundle(
        bundle,
        correlation_id="corr-soft",
        reasoning_request_id="rrq-soft",
        interpreted_at=FIXED_AT,
    )
    soft_obs = tuple(
        o
        for o in interpretation.observation_set.observations
        if o.category is not ObservationCategory.OBSERVED_CORRECTNESS
    )
    soft_set = EducationalObservationSet(
        set_id=interpretation.observation_set.set_id,
        observations=soft_obs,
        interpretation_version=interpretation.observation_set.interpretation_version,
        evidence_bundle_id=interpretation.observation_set.evidence_bundle_id,
        reasoning_request_id=interpretation.observation_set.reasoning_request_id,
    )
    result = DecisionGenerator().generate(
        soft_set,
        twin=twin,
        correlation_id="corr-soft",
        decided_at=FIXED_AT,
    )
    categories = {d.category for d in result.decision_set.decisions}
    assert DecisionCategory.UNCERTAINTY_PRESERVED in categories
    assert DecisionCategory.MASTERY_BELIEF_UPDATE not in categories
    updated = TwinUpdater().apply(twin, result.decision_set, updated_at=FIXED_AT)
    assert updated.mastery.records == twin.mastery.records


def test_cold_start_learner_gets_honest_belief(twin) -> None:
    assert twin.mastery.records == ()
    assert twin.confidence.score == 0.0
    updated, _ = StudentReasoningService(
        retrieval=_make_retrieval_stub()
    ).integrate_assessment_evidence(
        twin,
        bundle=make_bundle(),
        correlation_id="corr-cold",
        reasoning_request_id="rrq-cold",
        interpreted_at=FIXED_AT,
        persist=False,
    )
    record = updated.mastery.get("concept-bayes")
    assert record is not None
    assert 0.0 < record.mastery_score < 1.0
    assert record.confidence < 0.95


def test_sparse_and_conflicting_observations(twin) -> None:
    items = (
        make_item(
            item_id="i1",
            observation_id="o1",
            question_id="q1",
            correctness="correct",
        ),
        make_item(
            item_id="i2",
            observation_id="o2",
            question_id="q2",
            correctness="incorrect",
            misconception_tags=("confuses_prior",),
        ),
        make_item(
            item_id="i3",
            observation_id="o3",
            question_id="q3",
            correctness="correct",
        ),
    )
    bundle = make_bundle(
        items=items,
        observation_ids=tuple(i.observation_id for i in items),
        question_ids=tuple(i.question_id for i in items),
        summary_count=3,
    )
    interpretation = _interpret(bundle, request_id="rrq-conflict")
    result = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-conflict",
        decided_at=FIXED_AT,
    )
    mastery_decision = next(
        d
        for d in result.decision_set.decisions
        if d.category is DecisionCategory.MASTERY_BELIEF_UPDATE
    )
    score = APPROVED_MASTERY_PRIOR
    for positive in (True, False, True):
        target = 1.0 if positive else 0.0
        score = score + APPROVED_MASTERY_LEARNING_RATE * (target - score)
    assert mastery_decision.value == round(score, 4)


def test_unsupported_decision_version_rejected(twin) -> None:
    interpretation = _interpret()
    result = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-d3",
        decided_at=FIXED_AT,
    )
    from dataclasses import replace

    bad = result.decision_set
    object.__setattr__(bad, "decision_version", "nope.v0")
    object.__setattr__(
        bad,
        "context",
        replace(result.context, decision_version="nope.v0"),
    )
    with pytest.raises(UnsupportedDecisionVersion):
        DecisionValidator().validate(bad, twin=twin)


def test_integrate_assessment_evidence_end_to_end(reasoning, twin) -> None:
    before_obs = len(twin.observations)
    updated, decision_result = reasoning.integrate_assessment_evidence(
        twin,
        bundle=make_bundle(),
        correlation_id="corr-e2e",
        reasoning_request_id="rrq-e2e",
        interpreted_at=FIXED_AT,
        persist=True,
    )
    assert updated.twin_id == twin.twin_id
    assert len(updated.observations) == before_obs
    assert updated.mastery.get("concept-bayes") is not None
    assert decision_result.decision_count >= 2
    reloaded = StudentDigitalTwinService().get(twin.twin_id)
    assert reloaded is not None
    assert reloaded.mastery.get("concept-bayes") is not None
    assert reloaded.version == updated.version


def test_integrate_as_dto(reasoning, twin) -> None:
    updated, dto = reasoning.integrate_assessment_evidence(
        twin,
        bundle=make_bundle(),
        correlation_id="corr-dto",
        reasoning_request_id="rrq-dto",
        interpreted_at=FIXED_AT,
        persist=False,
        as_dto=True,
    )
    assert isinstance(dto, DecisionResultDTO)
    assert dto.correlation_id == "corr-dto"
    assert updated.reasoning_history


def test_mapper_projects_decision_dto(twin) -> None:
    interpretation = _interpret()
    result = DecisionGenerator().generate(
        interpretation.observation_set,
        twin=twin,
        correlation_id="corr-map",
        decided_at=FIXED_AT,
    )
    dto = map_decision_result(result)
    assert dto.set_id == result.decision_set.set_id
    assert len(dto.decisions) == len(result.decision_set)


def test_existing_reason_path_regression(reasoning, twin) -> None:
    updated = reasoning.reason(twin, triggered_by="manual", persist=True)
    assert updated.reasoning_history[-1].triggered_by == "manual"


def test_interpret_still_does_not_mutate_twin(reasoning, twin) -> None:
    before = twin.version
    reasoning.interpret_assessment_evidence(
        bundle=make_bundle(),
        correlation_id="corr-interp",
        reasoning_request_id="rrq-interp",
        interpreted_at=FIXED_AT,
    )
    reloaded = StudentDigitalTwinService().get(twin.twin_id)
    assert reloaded.version == before


def test_repeated_distinct_evidence_accumulates(twin) -> None:
    first_bundle = make_bundle(bundle_id="bundle-a", session_id="sess-a")
    second_bundle = make_bundle(
        bundle_id="bundle-b",
        session_id="sess-b",
        items=(
            make_item(
                item_id="item-b1",
                observation_id="obs-b1",
                question_id="q-b1",
                correctness="correct",
            ),
        ),
        observation_ids=("obs-b1",),
        question_ids=("q-b1",),
        summary_count=1,
    )
    svc = StudentReasoningService(retrieval=_make_retrieval_stub())
    after_first, _ = svc.integrate_assessment_evidence(
        twin,
        bundle=first_bundle,
        correlation_id="corr-a",
        reasoning_request_id="rrq-a",
        interpreted_at=FIXED_AT,
        persist=False,
    )
    score_1 = after_first.mastery.get("concept-bayes").mastery_score
    later = FIXED_AT.replace(microsecond=1) if FIXED_AT.microsecond == 0 else FIXED_AT
    # Use a distinct timestamp via datetime construction.
    later = datetime(2026, 7, 28, 10, 0, 1, tzinfo=UTC).replace(tzinfo=None)
    after_second, _ = svc.integrate_assessment_evidence(
        after_first,
        bundle=second_bundle,
        correlation_id="corr-b",
        reasoning_request_id="rrq-b",
        interpreted_at=later,
        persist=False,
    )
    score_2 = after_second.mastery.get("concept-bayes").mastery_score
    assert score_2 != score_1
    assert after_second.version == after_first.version + 1
    assert after_second.learning_state.exam_readiness == (
        LearningState.empty().exam_readiness
    )
