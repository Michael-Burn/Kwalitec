"""Workflow orchestration and interaction processing tests."""

from __future__ import annotations

from application.education.orchestration.dto.interaction_requests import (
    CheckpointRequest,
    InteractionKind,
    QuestionAnswerRequest,
    ReflectionRequest,
    SessionCompletionRequest,
    StudentInteractionRequest,
)
from application.education.orchestration.stages import OrchestrationStage
from domain.education.educational_evidence.enums import LearningEnvironmentKind
from tests.application.education.orchestration.conftest import (
    AS_OF,
    COMP_LINEAR,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    make_orchestrator,
)


def test_process_question_answer_succeeds() -> None:
    orchestrator, _, evidence_port, _, assessment_pub, rec_pub, _ = (
        make_orchestrator()
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
    assert result.success is True
    assert result.student_id == STUDENT_ID
    assert result.evidence_id is not None
    assert result.summary is not None
    assert result.snapshot is not None
    assert result.summary.evidence_count >= 1
    assert len(evidence_port.recorded) == 1
    assert len(assessment_pub.published) == 1
    assert len(rec_pub.published) == 1
    assert OrchestrationStage.RECORD_EVIDENCE.value in result.stages_completed
    assert OrchestrationStage.ESTIMATE_MASTERY.value in result.stages_completed
    assert (
        OrchestrationStage.GENERATE_RECOMMENDATIONS.value
        in result.stages_completed
    )


def test_process_reflection_succeeds() -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.process_reflection(
        ReflectionRequest(
            student_id=STUDENT_ID,
            reflection_text="I need more practice on linear equations.",
            occurred_at=AS_OF,
            learning_environment=LearningEnvironmentKind.REFLECTION_PROMPT.value,
            subject_id=SUBJECT_ALGEBRA,
            competency_id=COMP_LINEAR,
        )
    )
    assert result.success is True
    assert result.summary is not None


def test_process_checkpoint_succeeds() -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.process_checkpoint(
        CheckpointRequest(
            student_id=STUDENT_ID,
            checkpoint_id="checkpoint-01",
            occurred_at=AS_OF,
            learning_environment=LearningEnvironmentKind.CHECKPOINT_GATE.value,
            subject_id=SUBJECT_ALGEBRA,
        )
    )
    assert result.success is True


def test_process_session_completion_succeeds() -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.process_session_completion(
        SessionCompletionRequest(
            student_id=STUDENT_ID,
            learning_episode_id="episode-01",
            occurred_at=AS_OF,
            learning_environment=LearningEnvironmentKind.STUDY_SESSION.value,
            subject_id=SUBJECT_ALGEBRA,
        )
    )
    assert result.success is True


def test_process_student_interaction_dispatches_question_answer() -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.process_student_interaction(
        StudentInteractionRequest(
            kind=InteractionKind.QUESTION_ANSWER,
            question_answer=QuestionAnswerRequest(
                student_id=STUDENT_ID,
                competency_id=COMP_LINEAR,
                is_correct=False,
                occurred_at=AS_OF,
                learning_environment=LearningEnvironmentKind.FREE_PRACTICE.value,
                subject_id=SUBJECT_ALGEBRA,
            ),
        )
    )
    assert result.success is True
    assert result.evidence_id is not None


def test_refresh_recommendations_skips_new_evidence() -> None:
    orchestrator, _, evidence_port, *_ = make_orchestrator()
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is True
    assert evidence_port.recorded == []
    assert OrchestrationStage.RECORD_EVIDENCE.value not in result.stages_completed
    assert OrchestrationStage.ESTIMATE_MASTERY.value in result.stages_completed


def test_evaluate_student_does_not_publish() -> None:
    orchestrator, _, _, _, assessment_pub, rec_pub, _ = make_orchestrator()
    result = orchestrator.evaluate_student(STUDENT_ID, as_of=AS_OF)
    assert result.success is True
    assert assessment_pub.published == []
    assert rec_pub.published == []
    assert (
        OrchestrationStage.PUBLISH_ASSESSMENT.value
        not in result.stages_completed
    )
    assert (
        OrchestrationStage.PUBLISH_RECOMMENDATIONS.value
        not in result.stages_completed
    )
    assert result.decisions == result.snapshot.decisions  # type: ignore[union-attr]


def test_evaluation_generates_decisions_and_summary() -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.evaluate_student(STUDENT_ID, as_of=AS_OF)
    assert result.success is True
    assert result.summary is not None
    assert result.summary.student_id == STUDENT_ID
    assert result.summary.assessment_id
    assert result.summary.recommendation_set_id
    assert result.summary.mastery_band
    assert result.snapshot is not None
    assert result.snapshot.decision_count() == len(result.decisions)
