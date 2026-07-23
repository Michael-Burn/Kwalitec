"""Deterministic execution tests for Educational Orchestration."""

from __future__ import annotations

from application.education.orchestration.dto.interaction_requests import (
    QuestionAnswerRequest,
)
from domain.education.educational_evidence.enums import LearningEnvironmentKind
from tests.application.education.orchestration.conftest import (
    AS_OF,
    COMP_LINEAR,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    SequenceUUIDGenerator,
    make_orchestrator,
)


def test_identical_inputs_produce_identical_results() -> None:
    request = QuestionAnswerRequest(
        student_id=STUDENT_ID,
        competency_id=COMP_LINEAR,
        is_correct=True,
        occurred_at=AS_OF,
        learning_environment=LearningEnvironmentKind.FREE_PRACTICE.value,
        subject_id=SUBJECT_ALGEBRA,
        evidence_id="evidence-fixed-001",
    )

    first, *_ = make_orchestrator(uuid_generator=SequenceUUIDGenerator("run-a"))
    second, *_ = make_orchestrator(uuid_generator=SequenceUUIDGenerator("run-a"))

    result_a = first.process_question_answer(request)
    result_b = second.process_question_answer(request)

    assert result_a.success is True
    assert result_b.success is True
    assert result_a.stages_completed == result_b.stages_completed
    assert result_a.summary == result_b.summary
    assert result_a.decisions == result_b.decisions
    assert result_a.evidence_id == result_b.evidence_id
    assert result_a.snapshot == result_b.snapshot


def test_evaluate_student_is_deterministic() -> None:
    first, *_ = make_orchestrator(uuid_generator=SequenceUUIDGenerator("eval"))
    second, *_ = make_orchestrator(uuid_generator=SequenceUUIDGenerator("eval"))

    result_a = first.evaluate_student(STUDENT_ID, as_of=AS_OF)
    result_b = second.evaluate_student(STUDENT_ID, as_of=AS_OF)

    assert result_a.success and result_b.success
    assert result_a.summary == result_b.summary
    assert result_a.decisions == result_b.decisions
