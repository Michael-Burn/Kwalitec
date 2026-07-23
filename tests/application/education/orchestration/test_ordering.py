"""Correct stage ordering tests for Educational Orchestration."""

from __future__ import annotations

from application.education.orchestration.dto.interaction_requests import (
    QuestionAnswerRequest,
)
from application.education.orchestration.stages import (
    EVALUATION_PIPELINE,
    INTERACTION_PIPELINE,
    OrchestrationStage,
)
from domain.education.educational_evidence.enums import LearningEnvironmentKind
from tests.application.education.orchestration.conftest import (
    AS_OF,
    COMP_LINEAR,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    FakeEvidenceProvider,
    FakeKnowledgeGraphProvider,
    FakeStudentStateProvider,
    make_knowledge_graph,
    make_orchestrator,
    make_student_state,
)


def test_interaction_pipeline_order() -> None:
    call_order: list[str] = []

    class OrderedState(FakeStudentStateProvider):
        def get_student_state(self, student_id: str):
            call_order.append("state")
            return super().get_student_state(student_id)

    class OrderedGraph(FakeKnowledgeGraphProvider):
        def get_knowledge_graph(self, student_id: str):
            call_order.append("graph")
            return super().get_knowledge_graph(student_id)

    class OrderedEvidence(FakeEvidenceProvider):
        def record_evidence(self, evidence) -> None:
            call_order.append("record")
            super().record_evidence(evidence)

        def list_evidence(self, student_id: str):
            call_order.append("list")
            return super().list_evidence(student_id)

    state = make_student_state()
    graph = make_knowledge_graph()
    orchestrator, _, _, _, assessment_pub, rec_pub, _ = make_orchestrator(
        student_state_provider=OrderedState({STUDENT_ID: state}),
        knowledge_graph_provider=OrderedGraph({STUDENT_ID: graph}),
        evidence_provider=OrderedEvidence({STUDENT_ID: []}),
    )

    original_estimate = orchestrator._estimate_mastery
    original_recommend = orchestrator._recommend

    def tracking_estimate(**kwargs):
        call_order.append("mastery")
        return original_estimate(**kwargs)

    def tracking_recommend(**kwargs):
        call_order.append("recommend")
        return original_recommend(**kwargs)

    orchestrator._estimate_mastery = tracking_estimate  # type: ignore[method-assign]
    orchestrator._recommend = tracking_recommend  # type: ignore[method-assign]

    result = orchestrator.process_question_answer(
        QuestionAnswerRequest(
            student_id=STUDENT_ID,
            competency_id=COMP_LINEAR,
            is_correct=True,
            occurred_at=AS_OF,
            learning_environment=LearningEnvironmentKind.FREE_PRACTICE.value,
            subject_id=SUBJECT_ALGEBRA,
        )
    )
    assert result.success is True
    assert call_order == [
        "record",
        "state",
        "graph",
        "list",
        "mastery",
        "recommend",
    ]
    assert len(assessment_pub.published) == 1
    assert len(rec_pub.published) == 1

    expected_stages = tuple(stage.value for stage in INTERACTION_PIPELINE)
    assert result.stages_completed == expected_stages


def test_evaluation_pipeline_order_without_record() -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is True
    expected = tuple(stage.value for stage in EVALUATION_PIPELINE)
    assert result.stages_completed == expected
    assert OrchestrationStage.RECORD_EVIDENCE.value not in result.stages_completed


def test_failure_stops_before_later_stages() -> None:
    orchestrator, *_ = make_orchestrator(
        student_state_provider=FakeStudentStateProvider(
            error=Exception("state down")
        )
    )
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.stages_completed == ()
    assert result.failure_code == "student_state_unavailable"
    assert (
        OrchestrationStage.ESTIMATE_MASTERY.value
        not in result.stages_completed
    )
