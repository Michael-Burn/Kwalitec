"""TUTOR-001 Evidence-Backed Intelligent Tutor tests."""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import MagicMock

from app.application.adaptive_mission.adaptive_mission_service import (
    AdaptiveMissionService,
)
from app.application.assessment_pipeline.assessment_pipeline_service import (
    AssessmentPipelineService,
)
from app.application.intelligent_tutor.intelligent_tutor_service import (
    IntelligentTutorService,
)
from app.application.intelligent_tutor.ports.deterministic_tutor_generation import (
    DeterministicTutorGeneration,
)
from app.application.intelligent_tutor.ports.tutor_generation_port import (
    TutorGenerationRequest,
)
from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.assessment_pipeline.assessment_event import (
    AssessmentEvent,
    AssessmentEventType,
)
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.ranking import RankingBreakdown
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalResult,
)
from app.domain.intelligent_tutor.conversation_memory import (
    ConversationMemory,
    update_conversation_memory,
)
from app.domain.intelligent_tutor.response_builder import build_response_blueprint
from app.domain.intelligent_tutor.response_evidence import (
    EvidenceCategory,
    assemble_evidence,
)
from app.domain.intelligent_tutor.tutor_question import (
    TutorQuestion,
    TutorQuestionKind,
    classify_question,
)
from app.domain.learning_graph.graph_edge import GraphEdge
from app.domain.learning_graph.graph_node import GraphNode, PrerequisiteStatus
from app.domain.learning_graph.relationship import RelationshipType
from app.domain.student_digital_twin.observation import ObservationKind
from app.models.intelligent_tutor import (
    TutorExplanationRow,
    TutorMessageRow,
    TutorSessionRow,
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


def _make_retrieval_stub(
    *,
    concept_id: str = "concept-bayes",
    prerequisites: tuple[str, ...] = ("concept-conditional",),
) -> MagicMock:
    stub = MagicMock()
    evidence = (
        EvidenceItem(
            evidence_id="ev-tutor-1",
            role="definition",
            excerpt="Bayes theorem definition for tutor evidence",
            entity_id=concept_id,
        ),
    )
    ranked = RankedEvidence(
        entity_id=concept_id,
        kind="concept",
        title="Bayes Theorem",
        body="Definition body",
        document_id=1,
        version_label="2026",
        confidence=0.9,
        confidence_band="high",
        verified=True,
        provenance_id="prov-tutor-1",
        rank_score=0.88,
        ranking=_ranking(),
        evidence=evidence,
        prerequisites=prerequisites,
        related_concepts=(),
        supporting_formulae=(),
        worked_examples=(),
        practice_questions=(),
        learning_objectives=(),
    )
    stub.retrieve.return_value = RetrievalResult(
        query_text=concept_id,
        intent=QueryIntent.DEFINITION,
        profile=RetrievalProfile.TUTOR,
        results=(ranked,),
        concept_ids=(concept_id,),
        learning_objective_ids=(),
        definition_ids=(),
        formula_ids=(),
        example_ids=(),
        practice_question_ids=(),
        prerequisite_ids=prerequisites,
        related_concept_ids=(),
        retrieval_log_id="rl-tutor-1",
    )
    return stub


def _reasoned_twin(ctx, *, student_id: str = "s-tutor-1"):
    stub = _make_retrieval_stub()
    twin = StudentDigitalTwinService().create(
        student_id=student_id,
        workspace_id="ws-tutor",
        subject_code="CS1",
    )
    twin, _obs = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"correct": False, "concept_title": "Bayes Theorem"},
        persist=True,
    )
    updated = StudentReasoningService(retrieval=stub).reason(
        twin, triggered_by="tutor-test", persist=True
    )
    return updated, stub


def _attach_graph(twin):
    from app.application.learning_graph.persistence import (
        LearningGraphPersistenceService,
    )
    from app.extensions import db

    graph = LearningGraphService().get_for_twin(twin.twin_id)
    assert graph is not None
    nodes = (
        GraphNode(
            node_id="n-bayes",
            graph_id=graph.graph_id,
            concept_id="concept-bayes",
            concept_title="Bayes Theorem",
            mastery_score=0.3,
            prerequisite_status=PrerequisiteStatus.UNMET,
        ),
        GraphNode(
            node_id="n-cond",
            graph_id=graph.graph_id,
            concept_id="concept-conditional",
            concept_title="Conditional Probability",
            mastery_score=0.4,
            prerequisite_status=PrerequisiteStatus.NONE,
        ),
    )
    edges = (
        GraphEdge(
            edge_id="e-bayes-cond",
            graph_id=graph.graph_id,
            from_concept_id="concept-bayes",
            to_concept_id="concept-conditional",
            relationship_type=RelationshipType.PREREQUISITE,
            strength=0.9,
            confidence=0.9,
            provenance="tutor-test",
            supporting_evidence=("ev-tutor-1",),
        ),
    )
    updated = graph.with_structure(nodes=nodes, edges=edges)
    LearningGraphPersistenceService().replace_structure(updated)
    db.session.commit()
    return updated


def test_classify_question_deterministic():
    assert classify_question("Why is today's mission focused on Bayes?") == (
        TutorQuestionKind.DAILY_MISSION
    )
    assert classify_question("Explain my knowledge gap") == (
        TutorQuestionKind.KNOWLEDGE_GAP
    )
    assert classify_question("What are the prerequisites?") == (
        TutorQuestionKind.PREREQUISITE
    )


def test_tutor_context_construction(ctx):
    twin, stub = _reasoned_twin(ctx)
    _attach_graph(twin)
    AdaptiveMissionService(retrieval=stub).generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    service = IntelligentTutorService(retrieval=stub)
    question = TutorQuestion(
        question_id="q1",
        twin_id=twin.twin_id,
        text="Why is today's mission the right focus?",
        kind=TutorQuestionKind.DAILY_MISSION,
    )
    context = service.build_context(twin, question, enrich_evidence=True)
    assert context.twin_id == twin.twin_id
    assert context.active_mission_id
    assert context.recommendation_summaries or context.knowledge_gap_summaries
    assert context.curriculum_excerpts
    assert context.learning_state_summary


def test_evidence_assembly(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-ev")
    service = IntelligentTutorService(retrieval=stub)
    question = TutorQuestion(
        question_id="q-ev",
        twin_id=twin.twin_id,
        text="Explain my knowledge gaps",
        kind=TutorQuestionKind.KNOWLEDGE_GAP,
        concept_id="concept-bayes",
    )
    context = service.build_context(twin, question, enrich_evidence=True)
    evidence = assemble_evidence(
        context, assembly_id="asm-1", question_kind=question.kind
    )
    assert evidence.items
    assert evidence.curriculum_count >= 1 or evidence.reasoning_count >= 1
    categories = {i.category for i in evidence.items}
    assert EvidenceCategory.REASONING in categories or (
        EvidenceCategory.CURRICULUM in categories
    )


def test_response_generation_deterministic(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-resp")
    service = IntelligentTutorService(retrieval=stub)
    response = service.ask(
        twin.twin_id,
        "Why is today's mission the right focus?",
        persist=True,
        enrich_evidence=True,
        asked_at=datetime(2026, 7, 27, 13, 0, 0),
    )
    assert response.body
    assert response.supporting_evidence_ids
    assert response.explanation.summary
    assert response.suggested_next_action
    assert response.generation_backend == "deterministic_placeholder"
    assert TutorSessionRow.query.filter_by(session_id=response.session_id).first()
    assert TutorMessageRow.query.filter_by(session_id=response.session_id).count() >= 2
    assert TutorExplanationRow.query.filter_by(
        explanation_id=response.explanation.explanation_id
    ).first()


def test_conversation_memory_updates(ctx):
    memory = ConversationMemory(
        memory_id="mem-1",
        session_id="sess-1",
        twin_id="twin-1",
    )
    updated = update_conversation_memory(
        memory,
        concept_ids=("concept-bayes", "concept-conditional"),
        active_mission_id="mission-1",
        learner_state_summary="Learner state: readiness=0.40",
        question_kind=TutorQuestionKind.DAILY_MISSION.value,
        response_id="tr-1",
        updated_at=datetime(2026, 7, 27, 14, 0, 0),
    )
    assert updated.turn_count == 1
    assert "concept-bayes" in updated.referenced_concept_ids
    assert updated.active_mission_id == "mission-1"
    again = update_conversation_memory(
        updated,
        concept_ids=("concept-bayes",),
        response_id="tr-2",
        updated_at=datetime(2026, 7, 27, 14, 5, 0),
    )
    assert again.turn_count == 2
    assert again.referenced_concept_ids.count("concept-bayes") == 1


def test_deterministic_placeholder_generation(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-gen")
    service = IntelligentTutorService(retrieval=stub)
    question = TutorQuestion(
        question_id="q-gen",
        twin_id=twin.twin_id,
        text="Explain my recovery plan",
        kind=TutorQuestionKind.RECOVERY_PLAN,
        concept_id="concept-bayes",
    )
    context = service.build_context(twin, question, enrich_evidence=True)
    evidence = assemble_evidence(
        context, assembly_id="asm-gen", question_kind=question.kind
    )
    blueprint = build_response_blueprint(
        context=context,
        evidence=evidence,
        question_kind=question.kind,
        explanation_id="exp-gen",
        response_seed="seed-gen",
    )
    gen = DeterministicTutorGeneration()
    result = gen.generate(
        TutorGenerationRequest(
            question=question, context=context, blueprint=blueprint
        )
    )
    assert result.backend == DeterministicTutorGeneration.BACKEND
    assert "Supporting evidence:" in result.body or blueprint.explanation.summary in (
        result.body
    )
    # Same inputs → same body
    again = gen.generate(
        TutorGenerationRequest(
            question=question, context=context, blueprint=blueprint
        )
    )
    assert again.body == result.body


def test_integration_with_student_digital_twin(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-twin")
    assert twin.recommendations or twin.knowledge_gaps
    response = IntelligentTutorService(retrieval=stub).ask(
        twin.twin_id,
        "What are my weak concepts?",
        kind=TutorQuestionKind.WEAK_CONCEPT,
        persist=False,
        enrich_evidence=False,
    )
    assert response.twin_id == twin.twin_id
    assert (
        response.explanation.summary
        or response.evidence_summaries
        or response.body
    )


def test_integration_with_educational_reasoning(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-reason")
    assert twin.reasoning_history
    context = IntelligentTutorService(retrieval=stub).build_context(
        twin,
        TutorQuestion(
            question_id="q-r",
            twin_id=twin.twin_id,
            text="Explain my mastery changes",
            kind=TutorQuestionKind.MASTERY_CHANGE,
        ),
        enrich_evidence=False,
    )
    assert context.reasoning_run_id == twin.reasoning_history[-1].reasoning_id


def test_integration_with_curriculum_retrieval(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-curr")
    service = IntelligentTutorService(retrieval=stub)
    context = service.build_context(
        twin,
        TutorQuestion(
            question_id="q-c",
            twin_id=twin.twin_id,
            text="Explain Bayes theorem study strategy",
            kind=TutorQuestionKind.STUDY_STRATEGY,
            concept_id="concept-bayes",
        ),
        enrich_evidence=True,
    )
    stub.retrieve.assert_called()
    assert context.curriculum_excerpts
    call_kwargs = stub.retrieve.call_args
    query = call_kwargs[0][0] if call_kwargs[0] else call_kwargs[1].get("query")
    if query is None:
        query = stub.retrieve.call_args.args[0]
    assert query.profile == RetrievalProfile.TUTOR


def test_regression_ame001_and_ap001(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-reg")
    mission = AdaptiveMissionService(retrieval=stub).generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    assert mission.status.value == "active"

    event = AssessmentEvent.create(
        event_id="aev-tutor-reg",
        event_type=AssessmentEventType.MISSION_COMPLETION,
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        activity_id=mission.mission_id,
        curriculum_entity_id=mission.objective.primary_concept_id,
        concept_ids=(mission.objective.primary_concept_id,),
        mission_id=mission.mission_id,
        source="tutor-regression",
        occurred_at=datetime(2026, 7, 27, 15, 0, 0),
    )
    result = AssessmentPipelineService(
        reasoning=StudentReasoningService(retrieval=stub)
    ).process(
        event,
        persist=True,
        reason=False,
        refresh_mission=False,
    )
    assert result.ok
    assert result.feedback is not None

    response = IntelligentTutorService(retrieval=stub).explain_mission(
        twin.twin_id,
        persist=True,
        enrich_evidence=True,
    )
    assert response.explanation.mission_id == mission.mission_id
    assert response.supporting_evidence_ids


def test_tutor_does_not_invent_reasoning(ctx):
    """Tutor consumes Twin decisions — does not replace Educational Reasoning."""
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-no-invent")
    before = len(twin.reasoning_history)
    IntelligentTutorService(retrieval=stub).ask(
        twin.twin_id,
        "Explain my confidence trends",
        kind=TutorQuestionKind.CONFIDENCE_TREND,
        persist=False,
        enrich_evidence=False,
    )
    reloaded = StudentDigitalTwinService().get(twin.twin_id)
    assert reloaded is not None
    assert len(reloaded.reasoning_history) == before


def test_founder_tutor_diagnostics(ctx, client, app):
    twin, stub = _reasoned_twin(ctx, student_id="s-tutor-founder")
    IntelligentTutorService(retrieval=stub).ask(
        twin.twin_id,
        "Why is today's mission the right focus?",
        persist=True,
        enrich_evidence=True,
    )
    login_founder(client, app)
    sessions = client.get(f"/founder/tutor/sessions?twin_id={twin.twin_id}")
    assert sessions.status_code == 200
    assert sessions.get_json()["ok"] is True

    context = client.get(
        f"/founder/tutor/context?twin_id={twin.twin_id}&text=Explain+gaps"
    )
    assert context.status_code == 200
    assert context.get_json()["ok"] is True

    evidence = client.get(
        f"/founder/tutor/evidence?twin_id={twin.twin_id}&text=Explain+gaps"
    )
    assert evidence.status_code == 200
    assert evidence.get_json()["ok"] is True

    explanations = client.get(f"/founder/tutor/explanations?twin_id={twin.twin_id}")
    assert explanations.status_code == 200
    assert explanations.get_json()["ok"] is True

    diagnostics = client.get(f"/founder/tutor/diagnostics?twin_id={twin.twin_id}")
    assert diagnostics.status_code == 200
    payload = diagnostics.get_json()
    assert payload["ok"] is True
    assert payload["engine_version"] == IntelligentTutorService.ENGINE_VERSION
