"""Additional branch coverage for EducationalOrchestrator."""

from __future__ import annotations

import pytest

from application.education.orchestration.dto.interaction_requests import (
    CheckpointRequest,
    InteractionKind,
    QuestionAnswerRequest,
    ReflectionRequest,
    SessionCompletionRequest,
    StudentInteractionRequest,
)
from application.education.orchestration.educational_orchestrator import (
    EducationalOrchestrator,
)
from application.errors import ApplicationError
from domain.education.educational_evidence.enums import LearningEnvironmentKind
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.application.education.orchestration.conftest import (
    AS_OF,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    FakeEvidenceProvider,
    FakeKnowledgeGraphProvider,
    FakeStudentStateProvider,
    SequenceUUIDGenerator,
    make_knowledge_graph,
    make_orchestrator,
    make_student_state,
)


@pytest.mark.parametrize(
    "request_obj",
    [
        StudentInteractionRequest(
            kind=InteractionKind.REFLECTION,
            reflection=ReflectionRequest(
                student_id=STUDENT_ID,
                reflection_text="reflection notes",
                occurred_at=AS_OF,
                learning_environment=LearningEnvironmentKind.REFLECTION_PROMPT.value,
            ),
        ),
        StudentInteractionRequest(
            kind=InteractionKind.CHECKPOINT,
            checkpoint=CheckpointRequest(
                student_id=STUDENT_ID,
                checkpoint_id="cp-1",
                occurred_at=AS_OF,
                learning_environment=LearningEnvironmentKind.CHECKPOINT_GATE.value,
            ),
        ),
        StudentInteractionRequest(
            kind=InteractionKind.SESSION_COMPLETION,
            session_completion=SessionCompletionRequest(
                student_id=STUDENT_ID,
                learning_episode_id="ep-1",
                occurred_at=AS_OF,
                learning_environment=LearningEnvironmentKind.STUDY_SESSION.value,
            ),
        ),
    ],
)
def test_process_student_interaction_dispatches_all_kinds(request_obj) -> None:
    orchestrator, *_ = make_orchestrator()
    result = orchestrator.process_student_interaction(request_obj)
    assert result.success is True


def test_process_student_interaction_valid_question_path() -> None:
    orchestrator, *_ = make_orchestrator()
    with pytest.raises(ValueError):
        StudentInteractionRequest(kind=InteractionKind.QUESTION_ANSWER)
    result = orchestrator.process_question_answer(
        QuestionAnswerRequest(
            student_id=STUDENT_ID,
            competency_id="c",
            is_correct=True,
            occurred_at=AS_OF,
            learning_environment=LearningEnvironmentKind.FREE_PRACTICE.value,
            subject_id=SUBJECT_ALGEBRA,
            evidence_id="ev-ok",
        )
    )
    assert result.success is True


def test_application_error_from_student_state() -> None:
    orchestrator, *_ = make_orchestrator(
        student_state_provider=FakeStudentStateProvider(
            error=ApplicationError("state coordination failed")
        )
    )
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "student_state_unavailable"


def test_refresh_without_publishers_still_records_publish_stages() -> None:
    state = make_student_state()
    orchestrator = EducationalOrchestrator(
        student_state_provider=FakeStudentStateProvider({STUDENT_ID: state}),
        evidence_provider=FakeEvidenceProvider({STUDENT_ID: []}),
        knowledge_graph_provider=FakeKnowledgeGraphProvider(
            {STUDENT_ID: make_knowledge_graph()}
        ),
        uuid_generator=SequenceUUIDGenerator(),
        assessment_publisher=None,
        recommendation_publisher=None,
    )
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is True
    assert "publish_assessment" in result.stages_completed
    assert "publish_recommendations" in result.stages_completed


def test_mastery_domain_failure_propagates() -> None:
    orchestrator, *_ = make_orchestrator()

    def boom(**_kwargs):
        raise EducationalInvariantViolation(
            "assessment broken",
            invariant="test.mastery",
        )

    orchestrator._estimate_mastery = boom  # type: ignore[method-assign]
    result = orchestrator.evaluate_student(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "mastery_estimation_failed"
    assert "estimate_mastery" not in result.stages_completed


def test_recommendation_domain_failure_propagates() -> None:
    orchestrator, *_ = make_orchestrator()

    def boom(**_kwargs):
        raise EducationalInvariantViolation(
            "recommendation broken",
            invariant="test.recommend",
        )

    orchestrator._recommend = boom  # type: ignore[method-assign]
    result = orchestrator.evaluate_student(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "recommendation_failed"
    assert "estimate_mastery" in result.stages_completed


def test_unexpected_mastery_exception_propagates() -> None:
    orchestrator, *_ = make_orchestrator()

    def boom(**_kwargs):
        raise RuntimeError("estimator crashed")

    orchestrator._estimate_mastery = boom  # type: ignore[method-assign]
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert "crashed" in (result.failure_message or "")


def test_unexpected_recommendation_exception_propagates() -> None:
    orchestrator, *_ = make_orchestrator()

    def boom(**_kwargs):
        raise RuntimeError("recommender crashed")

    orchestrator._recommend = boom  # type: ignore[method-assign]
    result = orchestrator.refresh_recommendations(STUDENT_ID, as_of=AS_OF)
    assert result.success is False
    assert result.failure_code == "recommendation_failed"
