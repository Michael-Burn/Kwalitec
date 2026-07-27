"""SDT-002 Educational Reasoning Engine tests."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.application.educational_reasoning.educational_reasoning_service import (
    EducationalReasoningService,
)
from app.application.educational_reasoning.persistence import (
    ReasoningPersistenceService,
)
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.query import RetrievalQuery
from app.domain.curriculum_retrieval.ranking import RankingBreakdown
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalResult,
)
from app.domain.educational_reasoning.confidence_update import ConfidenceAdjustmentRule
from app.domain.educational_reasoning.consistency_rule import ConsistencyRule
from app.domain.educational_reasoning.gap_analysis import KnowledgeGapDetectionRule
from app.domain.educational_reasoning.mastery_update import MasteryUpdateRule
from app.domain.educational_reasoning.momentum_rule import LearningMomentumRule
from app.domain.educational_reasoning.readiness_rule import ReadinessContributionRule
from app.domain.educational_reasoning.reasoning_context import (
    CurriculumEvidenceBundle,
    ReasoningContext,
)
from app.domain.educational_reasoning.reasoning_engine import (
    ENGINE_VERSION,
    EducationalReasoningEngine,
)
from app.domain.educational_reasoning.recommendation_rule import RecommendationRule
from app.domain.educational_reasoning.rule_registry import (
    RuleRegistry,
    build_default_registry,
)
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.observation import Observation, ObservationKind
from app.models.educational_reasoning import (
    DecisionRecord,
    EducationalReasoningRun,
    EducationalRuleExecution,
    ReasoningExplanation,
)
from tests.presentation.curriculum_studio.helpers import login_founder


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
            evidence_id="ev-1",
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
        provenance_id="prov-1",
        rank_score=0.88,
        ranking=_ranking(),
        evidence=evidence,
        prerequisites=("concept-conditional",),
        related_concepts=(),
        supporting_formulae=(),
        worked_examples=(),
        practice_questions=(),
        learning_objectives=(),
        graph_distance=1,
    )
    stub.retrieve.return_value = RetrievalResult(
        query_text="Bayes",
        intent=QueryIntent.DEFINITION,
        profile=RetrievalProfile.STUDENT_DIGITAL_TWIN,
        results=(ranked,),
        concept_ids=(concept_id,),
        learning_objective_ids=(),
        definition_ids=(),
        formula_ids=(),
        example_ids=(),
        practice_question_ids=(),
        prerequisite_ids=("concept-conditional",),
        related_concept_ids=(),
        retrieval_log_id="log-1",
    )
    return stub


def _obs(
    *,
    observation_id: str,
    twin_id: str = "twin-eng",
    correct: bool = False,
    concept_id: str = "concept-bayes",
    recorded_at: datetime | None = None,
) -> Observation:
    return Observation.create(
        observation_id=observation_id,
        kind=ObservationKind.QUESTION_ANSWERED,
        twin_id=twin_id,
        student_id="student-eng",
        recorded_at=recorded_at or datetime(2026, 7, 27, 12, 0, 0),
        curriculum_entity_id=concept_id,
        curriculum_entity_kind="concept",
        evidence_reference=f"ev-{observation_id}",
        metadata={"correct": correct, "concept_title": "Bayes Theorem"},
    )


def _context(
    observations: tuple[Observation, ...],
    *,
    evidence: CurriculumEvidenceBundle | None = None,
    workspace_id: str = "ws-eng",
) -> ReasoningContext:
    return ReasoningContext(
        twin_id="twin-eng",
        student_id="student-eng",
        workspace_id=workspace_id,
        subject_code="CS1",
        observations=observations,
        observation_ids=tuple(o.observation_id for o in observations),
        prior_mastery=MasteryMap.empty(),
        curriculum_evidence=evidence or CurriculumEvidenceBundle.empty(),
        triggered_by="test",
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
    )


def test_mastery_update_rule_deterministic():
    observations = (
        _obs(observation_id="o1", correct=False),
        _obs(observation_id="o2", correct=False),
        _obs(observation_id="o3", correct=True),
    )
    ctx = _context(observations)
    a = MasteryUpdateRule().apply(ctx)
    b = MasteryUpdateRule().apply(ctx)
    assert a.mastery is not None and b.mastery is not None
    assert a.mastery.get("concept-bayes").mastery_score == b.mastery.get(
        "concept-bayes"
    ).mastery_score
    assert a.explanation.rule_code == "mastery_update"
    assert a.decisions


def test_confidence_momentum_consistency_readiness_rules():
    observations = (
        _obs(observation_id="o1", correct=True),
        _obs(observation_id="o2", correct=False),
        _obs(
            observation_id="o3",
            correct=True,
            recorded_at=datetime(2026, 7, 28, 12, 0, 0),
        ),
    )
    ctx = _context(observations)
    mastery_ex = MasteryUpdateRule().apply(ctx)
    ctx = ctx.with_updates(
        mastery=mastery_ex.mastery, knowledge=mastery_ex.knowledge
    )
    conf = ConfidenceAdjustmentRule().apply(ctx)
    assert conf.confidence is not None
    assert 0.0 <= conf.confidence.score <= 1.0
    ctx = ctx.with_updates(confidence=conf.confidence)
    mom = LearningMomentumRule().apply(ctx)
    assert mom.momentum is not None
    ctx = ctx.with_updates(momentum=mom.momentum)
    con = ConsistencyRule().apply(ctx)
    assert con.consistency is not None
    ctx = ctx.with_updates(consistency=con.consistency)
    rdy = ReadinessContributionRule().apply(ctx)
    assert rdy.exam_readiness is not None
    assert rdy.retention is not None
    assert all(ex.explanation.summary for ex in (conf, mom, con, rdy))


def test_registry_pluggable_and_ordered():
    registry = build_default_registry()
    codes = [r.code for r in registry.rules]
    assert codes[0] == "mastery_update"
    assert codes[-1] == "recommendation"
    assert "knowledge_gap_detection" in codes
    assert "prerequisite_analysis" in codes

    class _ProbeRule:
        code = "probe"
        name = "Probe"
        description = "test probe"

        def apply(self, context):
            from app.domain.educational_reasoning.explanation import Explanation
            from app.domain.educational_reasoning.reasoning_rule import RuleExecution

            return RuleExecution(
                rule_code=self.code,
                rule_name=self.name,
                explanation=Explanation(
                    summary="probe fired",
                    rule_code=self.code,
                ),
                outputs={"ok": True},
            )

    registry.register(_ProbeRule(), after="recommendation")
    assert registry.get("probe") is not None
    assert registry.list_rules()[-1]["code"] == "probe"

    with pytest.raises(ValueError, match="already registered"):
        registry.register(_ProbeRule())


def test_engine_produces_explainable_result():
    stub = _make_retrieval_stub()
    result = stub.retrieve.return_value
    evidence = CurriculumEvidenceBundle(
        by_concept={"concept-bayes": result},
        all_evidence_ids=("ev-1", "ranked:concept-bayes"),
        retrieval_log_ids=("log-1",),
    )
    observations = (
        _obs(observation_id="o1", correct=False),
        _obs(observation_id="o2", correct=False),
    )
    ctx = _context(observations, evidence=evidence)
    engine_result = EducationalReasoningEngine().reason(ctx)

    assert engine_result.engine_version == ENGINE_VERSION
    assert engine_result.executions
    assert engine_result.explanations
    assert engine_result.decisions
    assert engine_result.mastery.get("concept-bayes") is not None
    assert engine_result.gaps
    assert engine_result.recommendations
    assert engine_result.learning_state.exam_readiness >= 0.0
    # Every decision exposes why / observations / rule
    for decision in engine_result.decisions:
        assert decision.explanation.summary
        assert decision.rule_code
        assert decision.explanation.rule_code == decision.rule_code


def test_gap_rule_requires_curriculum_evidence():
    observations = (_obs(observation_id="o1", correct=False),)
    ctx = _context(observations, evidence=CurriculumEvidenceBundle.empty())
    mastery_ex = MasteryUpdateRule().apply(ctx)
    ctx = ctx.with_updates(mastery=mastery_ex.mastery)
    gaps = KnowledgeGapDetectionRule().apply(ctx)
    assert gaps.gaps == ()


def test_student_reasoning_delegates_to_registry(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-eng",
        workspace_id="ws-eng",
        twin_id="twin-eng-svc",
    )
    for i, correct in enumerate((False, False, True), start=1):
        twin, _ = ObservationService().record(
            twin,
            kind=ObservationKind.QUESTION_ANSWERED,
            curriculum_entity_id="concept-bayes",
            curriculum_entity_kind="concept",
            evidence_reference=f"quiz-{i}",
            metadata={"correct": correct, "concept_title": "Bayes Theorem"},
        )

    svc = StudentReasoningService(retrieval=_make_retrieval_stub())
    assert isinstance(svc.educational_reasoning.registry, RuleRegistry)
    twin = svc.reason(twin, triggered_by="delegate-test", persist=True)

    assert twin.mastery.get("concept-bayes") is not None
    assert twin.knowledge_gaps
    assert twin.recommendations
    assert twin.reasoning_history
    record = twin.reasoning_history[-1]
    assert record.reasoning_version == ENGINE_VERSION
    step_codes = [s.code for s in record.steps]
    assert "mastery_update" in step_codes
    assert "recommendation" in step_codes

    runs = ReasoningPersistenceService().list_runs_for_twin("twin-eng-svc")
    assert runs
    assert EducationalRuleExecution.query.filter_by(run_id=runs[0].run_id).count() >= 8
    assert ReasoningExplanation.query.filter_by(run_id=runs[0].run_id).count() >= 1
    assert DecisionRecord.query.filter_by(run_id=runs[0].run_id).count() >= 1


def test_reasoning_history_immutable(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-imm",
        workspace_id="ws-imm",
        twin_id="twin-imm",
    )
    twin, _ = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"correct": False, "concept_title": "Bayes Theorem"},
    )
    svc = StudentReasoningService(retrieval=_make_retrieval_stub())
    twin = svc.reason(twin, triggered_by="first", persist=True)
    twin = svc.reason(twin, triggered_by="second", persist=True)

    runs = EducationalReasoningRun.query.filter_by(twin_id="twin-imm").all()
    assert len(runs) == 2
    run_ids = {r.run_id for r in runs}
    assert len(run_ids) == 2

    persistence = ReasoningPersistenceService()
    with pytest.raises(ValueError, match="already persisted"):
        # Re-persist first result-shaped run by cloning row attempt via service
        first = persistence.list_runs_for_twin("twin-imm")[0]
        from app.domain.educational_reasoning.reasoning_result import ReasoningResult
        from app.domain.student_digital_twin.confidence import (
            ConfidenceState,
            confidence_band_from_score,
        )
        from app.domain.student_digital_twin.learning_state import LearningState

        fake = ReasoningResult(
            run_id=first.run_id,
            twin_id=first.twin_id,
            triggered_by="dup",
            observation_ids=(),
            curriculum_evidence=CurriculumEvidenceBundle.empty(),
            executions=(),
            decisions=(),
            explanations=(),
            mastery=MasteryMap.empty(),
            confidence=ConfidenceState(
                score=0.0,
                band=confidence_band_from_score(0.0),
                evidence_count=0,
                reason="x",
            ),
            learning_state=LearningState.empty(),
            gaps=(),
            recommendations=(),
            summary="dup",
            created_at=datetime(2026, 7, 27, 12, 0, 0),
            engine_version=ENGINE_VERSION,
        )
        persistence.persist_result(fake)


def test_recommendation_rule_from_gaps():
    from app.domain.student_digital_twin.knowledge_gap import GapSeverity, KnowledgeGap

    gap = KnowledgeGap(
        gap_id="gap-1",
        twin_id="twin-eng",
        concept_id="concept-bayes",
        concept_title="Bayes Theorem",
        severity=GapSeverity.HIGH,
        confidence=0.8,
        likely_prerequisite_id="concept-conditional",
        likely_prerequisite_title="Conditional Probability",
        supporting_evidence=("ev-1",),
    )
    ctx = _context(()).with_updates(gaps=(gap,))
    ex = RecommendationRule().apply(ctx)
    assert ex.recommendations
    assert "Conditional Probability" in ex.recommendations[0].title
    assert ex.explanation.summary


def test_founder_reasoning_diagnostics(client, app, ctx):
    login_founder(client, app)

    rules = client.get("/founder/reasoning/rules")
    assert rules.status_code == 200
    body = rules.get_json()
    assert body["ok"] is True
    assert body["engine_version"] == ENGINE_VERSION
    assert any(r["code"] == "mastery_update" for r in body["rules"])

    create = client.post(
        "/founder/twin/",
        json={
            "student_id": "diag-eng",
            "workspace_id": "ws-diag-eng",
            "subject_code": "CS1",
        },
    )
    twin_id = create.get_json()["twin"]["twin_id"]
    twin = StudentDigitalTwinService().get(twin_id)
    assert twin is not None
    twin, _ = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"correct": False, "concept_title": "Bayes Theorem"},
    )
    StudentReasoningService(retrieval=_make_retrieval_stub()).reason(
        twin, triggered_by="prep", persist=True
    )

    history = client.get(f"/founder/reasoning/history?twin_id={twin_id}")
    assert history.status_code == 200
    runs = history.get_json()["runs"]
    assert runs
    run_id = runs[0]["run_id"]

    explanations = client.get(
        f"/founder/reasoning/explanations?twin_id={twin_id}&run_id={run_id}"
    )
    assert explanations.status_code == 200
    assert explanations.get_json()["explanations"]

    decisions = DecisionRecord.query.filter_by(run_id=run_id).all()
    assert decisions
    decision = client.get(
        f"/founder/reasoning/decision/{decisions[0].decision_id}"
    )
    assert decision.status_code == 200
    assert decision.get_json()["decision"]["rule_code"]

    # Run endpoint (uses live retrieval; may yield empty gaps without CIP index)
    run_resp = client.post(
        "/founder/reasoning/run",
        json={"twin_id": twin_id, "triggered_by": "founder_diag"},
    )
    assert run_resp.status_code == 200
    assert run_resp.get_json()["ok"] is True


def test_cip003_retrieval_profile_regression(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-cip3",
        workspace_id="ws-cip3",
        twin_id="twin-cip3",
    )
    twin, _ = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"correct": False, "concept_title": "Bayes Theorem"},
    )
    retrieval = _make_retrieval_stub()
    StudentReasoningService(retrieval=retrieval).reason(
        twin, triggered_by="cip3", persist=True
    )
    assert retrieval.retrieve.called
    query: RetrievalQuery = retrieval.retrieve.call_args.args[0]
    assert query.profile is RetrievalProfile.STUDENT_DIGITAL_TWIN
    assert query.workspace_id == "ws-cip3"


def test_educational_reasoning_service_pure_path(ctx):
    observations = (
        _obs(observation_id="p1", twin_id="twin-pure", correct=False),
        _obs(observation_id="p2", twin_id="twin-pure", correct=False),
    )
    result = EducationalReasoningService(
        retrieval=_make_retrieval_stub()
    ).reason_from_observations(
        twin_id="twin-pure",
        student_id="student-eng",
        workspace_id="ws-pure",
        subject_code="CS1",
        observations=observations,
        persist=True,
        computed_at=datetime(2026, 7, 27, 15, 0, 0),
    )
    assert result.gaps
    assert result.recommendations
    assert EducationalReasoningRun.query.filter_by(run_id=result.run_id).first()
