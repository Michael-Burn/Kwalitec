"""Failure propagation tests — deterministic application results."""

from __future__ import annotations

from application.education.orchestration.dto.interaction_requests import (
    QuestionAnswerRequest,
)
from application.errors import ApplicationError, NotFoundError
from domain.education.educational_evidence.enums import LearningEnvironmentKind
from tests.application.education.orchestration.conftest import (
    AS_OF,
    COMP_LINEAR,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    FakeAssessmentPublisher,
    FakeEvidenceProvider,
    FakeKnowledgeGraphProvider,
    FakeRecommendationPublisher,
    FakeStudentStateProvider,
    make_knowledge_graph,
    make_orchestrator,
    make_student_state,
)


def test_missing_student_state_returns_failure() -> None:
    orchestrator, *_ = make_orchestrator(
        student_state_provider=FakeStudentStateProvider({})
    )
    result = orchestrator.evaluate_student(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "student_state_unavailable"
    assert "not found" in (result.failure_message or "").lower()


def test_missing_knowledge_graph_returns_failure() -> None:
    orchestrator, *_ = make_orchestrator(
        knowledge_graph_provider=FakeKnowledgeGraphProvider({})
    )
    result = orchestrator.evaluate_student(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "knowledge_graph_unavailable"
    assert result.stages_completed == ("load_student_state",)


def test_evidence_list_failure_returns_failure() -> None:
    orchestrator, *_ = make_orchestrator(
        evidence_provider=FakeEvidenceProvider(
            list_error=ApplicationError("evidence store offline")
        )
    )
    result = orchestrator.evaluate_student(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "evidence_unavailable"
    assert "offline" in (result.failure_message or "")


def test_evidence_record_failure_returns_failure() -> None:
    orchestrator, *_ = make_orchestrator(
        evidence_provider=FakeEvidenceProvider(
            record_error=ApplicationError("cannot write evidence")
        )
    )
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
    assert result.success is False
    assert result.failure_code == "evidence_record_failed"
    assert result.stages_completed == ()


def test_assessment_publish_failure_returns_failure() -> None:
    orchestrator, *_ = make_orchestrator(
        assessment_publisher=FakeAssessmentPublisher(
            error=ApplicationError("publish assessment failed")
        )
    )
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "assessment_publish_failed"
    assert "generate_recommendations" in result.stages_completed
    assert "publish_assessment" not in result.stages_completed


def test_recommendation_publish_failure_returns_failure() -> None:
    orchestrator, *_ = make_orchestrator(
        recommendation_publisher=FakeRecommendationPublisher(
            error=ApplicationError("publish recommendations failed")
        )
    )
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "recommendation_publish_failed"
    assert "publish_assessment" in result.stages_completed


def test_empty_student_id_returns_invalid_request() -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.evaluate_student("  ", as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "invalid_request"


def test_not_found_error_does_not_raise() -> None:
    orchestrator, *_ = make_orchestrator(
        student_state_provider=FakeStudentStateProvider(
            error=NotFoundError("StudentEducationalState", STUDENT_ID)
        )
    )
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.failed_result is True
    assert result.summary is None
    assert result.snapshot is None


def test_domain_invariant_on_invalid_environment() -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.process_question_answer(
        QuestionAnswerRequest(
            student_id=STUDENT_ID,
            competency_id=COMP_LINEAR,
            is_correct=True,
            occurred_at=AS_OF,
            learning_environment="not-a-real-environment",
            subject_id=SUBJECT_ALGEBRA,
        )
    )
    assert result.success is False
    assert result.failure_code in {"domain_invariant", "evidence_record_failed"}


def test_graph_unavailable_preserves_prior_stage() -> None:
    state = make_student_state()
    orchestrator, *_ = make_orchestrator(
        student_state_provider=FakeStudentStateProvider({STUDENT_ID: state}),
        knowledge_graph_provider=FakeKnowledgeGraphProvider(
            error=NotFoundError("KnowledgeGraph", STUDENT_ID)
        ),
    )
    result = orchestrator.evaluate_student(STUDENT_ID, as_of=AS_OF)
    assert result.stages_completed == ("load_student_state",)
    # graph was never successfully loaded — mastery must not have run
    assert "estimate_mastery" not in result.stages_completed
    _ = make_knowledge_graph()  # keep import used for clarity in suite
